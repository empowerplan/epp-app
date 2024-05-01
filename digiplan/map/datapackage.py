"""Read functionality for digipipe datapackage."""
import csv
import json
from collections import defaultdict, namedtuple
from pathlib import Path
from typing import Optional, Union

import pandas as pd
from cache_memoize import cache_memoize
from django.conf import settings
from django_oemof.settings import OEMOF_DIR

from config.settings.base import DIGIPIPE_DIR
from digiplan.map import config, models

Source = namedtuple("Source", ["csv_file", "column"])


def get_data_from_sources(sources: Union[Source, list[Source]]) -> pd.DataFrame:
    """Extract data from single or multiple sources and merge into dataframe."""
    source_files = defaultdict(list)
    if isinstance(sources, Source):
        source_files[sources.csv_file].append(sources.column)
    else:
        for source in sources:
            source_files[source.csv_file].append(source.column)

    dfs = []
    for source_file, columns in source_files.items():
        source_path = Path(DIGIPIPE_DIR, "scalars", source_file)
        dfs.append(pd.read_csv(source_path, usecols=columns))
    return pd.concat(dfs, axis=1)


def get_employment() -> pd.DataFrame:
    """Return employment data."""
    employment_filename = settings.DIGIPIPE_DIR.path("scalars").path("employment.csv")
    return pd.read_csv(employment_filename, index_col=0)


def get_batteries() -> pd.DataFrame:
    """Return battery data."""
    battery_filename = settings.DIGIPIPE_DIR.path("scalars").path("bnetza_mastr_storage_stats_muns.csv")
    return pd.read_csv(battery_filename)


def get_power_demand(sector: Optional[str] = None) -> dict[str, pd.DataFrame]:
    """Return power demand for given sector or all sectors."""
    sectors = (sector,) if sector else ("hh", "cts", "ind")
    demand = {}
    for sec in sectors:
        demand_filename = settings.DIGIPIPE_DIR.path("scalars").path(f"demand_{sec}_power_demand.csv")
        demand[sec] = pd.read_csv(demand_filename)
    return demand


def get_hourly_electricity_demand(year: int) -> pd.Series:
    """Return hourly electricity demand per sector."""
    demand_per_sector = get_power_demand()
    demand_profile = get_electricity_demand_profile()
    demand = []
    for sector, demand_sector_per_mun in demand_per_sector.items():
        demand.append(demand_profile[sector] * demand_sector_per_mun[str(year)].sum())
    return pd.concat(demand, axis=1).sum(axis=1)


def get_heat_demand(sector: Optional[str] = None, distribution: Optional[str] = None) -> dict[str, pd.DataFrame]:
    """Return heat demand for given sector or all sectors."""
    sectors = (sector,) if sector else ("hh", "cts", "ind")
    distribution_prefix = ("_cen" if distribution == "central" else "_dec") if distribution else ""
    demand = {}
    for sec in sectors:
        demand_filename = settings.DIGIPIPE_DIR.path("scalars").path(
            f"demand_{sec}_heat_demand{distribution_prefix}.csv",
        )
        demand[sec] = pd.read_csv(demand_filename)
    return demand


def get_heat_capacity_shares(
    distribution: str,
    year: Optional[int] = 2045,
    *,
    include_heatpumps: Optional[bool] = False,
) -> dict:
    """Return capacity shares of heating structure."""
    shares_filename = settings.DIGIPIPE_DIR.path("scalars").path(f"demand_heat_structure_esys_{distribution}.csv")
    with Path(shares_filename).open("r", encoding="utf-8") as shares_file:
        reader = csv.DictReader(shares_file)
        shares = {}
        summed_shares = 0.0
        for row in reader:
            if row["year"] != str(year):
                continue
            if row["carrier"] == "heat_pump" and not include_heatpumps:
                continue
            shares[row["carrier"]] = float(row["demand_rel"])
            summed_shares += float(row["demand_rel"])
    return {k: v / summed_shares for k, v in shares.items()}


def get_summed_heat_demand_per_municipality(
    sector: Optional[str] = None,
    distribution: Optional[str] = None,
) -> dict[str, dict[str, pd.DataFrame]]:
    """Return heat demand for given sector and distribution."""
    sectors = (sector,) if sector else ("hh", "cts", "ind")
    distributions = (distribution,) if distribution else ("cen", "dec")
    demand = defaultdict(dict)
    for sec in sectors:
        for dist in distributions:
            demand_filename = settings.DIGIPIPE_DIR.path("scalars").path(
                f"demand_{sec}_heat_demand_{dist}.csv",
            )
            demand[sec][dist] = pd.read_csv(demand_filename)
    return demand


def get_heat_demand_profile(
    sector: Optional[str] = None,
    distribution: Optional[str] = None,
) -> dict[str, dict[str, pd.DataFrame]]:
    """Return heat demand for given sector and distribution."""
    sectors = (sector,) if sector else ("hh", "cts", "ind")
    distributions = (distribution,) if distribution else ("central", "decentral")
    demand = defaultdict(dict)
    for sec in sectors:
        for dist in distributions:
            demand_filename = (
                OEMOF_DIR / settings.OEMOF_SCENARIO / "data" / "sequences" / f"heat_{dist}-demand_{sec}_profile.csv"
            )
            demand[sec][dist] = pd.read_csv(demand_filename, sep=";")[f"ABW-heat_{dist}-demand_{sec}-profile"]
    return demand


def get_electricity_demand_profile(
    sector: Optional[str] = None,
) -> dict[str, pd.DataFrame]:
    """Return heat demand for given sector and distribution."""
    sectors = (sector,) if sector else ("hh", "cts", "ind")
    demand = defaultdict(dict)
    for sec in sectors:
        demand_filename = (
            OEMOF_DIR / settings.OEMOF_SCENARIO / "data" / "sequences" / f"electricity-demand_{sec}_profile.csv"
        )
        demand[sec] = pd.read_csv(demand_filename, sep=";")[f"ABW-electricity-demand_{sec}-profile"]
    return demand


def get_thermal_efficiency(component: str) -> float:
    """Return thermal efficiency from given component from oemof scenario."""
    component_filename = OEMOF_DIR / settings.OEMOF_SCENARIO / "data" / "elements" / f"{component}.csv"
    component_df = pd.read_csv(component_filename, sep=";")
    if component_df["type"][0] in ("extraction", "backpressure"):
        return float(pd.read_csv(component_filename, sep=";")["thermal_efficiency"][0])

    if "efficiency" in component_df.columns and isinstance(component_df["efficiency"][0], float):
        return component_df["efficiency"][0]

    if "heatpump" in component:
        component = "efficiency"
    sequence_filename = OEMOF_DIR / settings.OEMOF_SCENARIO / "data" / "sequences" / f"{component}_profile.csv"
    return pd.read_csv(sequence_filename, sep=";").iloc[:, 1]


@cache_memoize(timeout=None)
def get_potential_values() -> pd.DataFrame:
    """
    Calculate max_values for sliders.

    Returns
    -------
    dict
        dictionary with each slider / switch and respective max_value
    """
    areas = get_potential_areas()
    pv_density = {
        "pv_soil_quality_low": "pv_ground",
        "pv_soil_quality_medium": "pv_ground_vertical_bifacial",
        "pv_permanent_crops": "pv_ground_elevated",
        "pv_roof": "pv_roof",
    }
    power_density = json.load(Path.open(Path(settings.DIGIPIPE_DIR, "scalars/technology_data.json")))["power_density"]
    densities = [
        power_density["wind"] if technology.startswith("wind") else power_density[pv_density[technology]]
        for technology in areas
    ]
    hydro = get_data_from_sources(Source("bnetza_mastr_hydro_stats_muns.csv", "capacity_net"))
    potential_values = areas * densities
    potential_values["hydro"] = hydro
    return potential_values


@cache_memoize(timeout=None)
def get_potential_areas(technology: Optional[str] = None) -> pd.DataFrame:
    """
    Return potential areas.

    Parameters
    ----------
    technology: str
        If given, potential area only for this technology is returned

    Returns
    -------
    dict
        Potential areas of all technologies or specified one (in sqkm)
    """
    sources = {
        "wind_2018": Source("potentialarea_wind_area_stats_muns.csv", "stp_2018_eg"),
        "wind_2024": Source("potentialarea_wind_area_stats_muns.csv", "stp_2024_vr"),
        "pv_soil_quality_low": Source("potentialarea_pv_ground_area_stats_muns.csv", "soil_quality_low_region"),
        "pv_soil_quality_medium": Source("potentialarea_pv_ground_area_stats_muns.csv", "soil_quality_medium_region"),
        "pv_permanent_crops": Source("potentialarea_pv_ground_area_stats_muns.csv", "permanent_crops_region"),
        "pv_roof": Source("potentialarea_pv_roof_area_stats_muns.csv", "roof_area_pv_potential_sqkm"),
    }

    column_mapping = {source.column: new_column for new_column, source in sources.items()}
    column_mapping["wind_2027"] = "wind_2027"

    # Add wind for 2027 directly from model data, as it is not included in datapackage
    wind_2027 = pd.DataFrame(models.Municipality.objects.all().values("id", "area")).set_index("id")
    wind_2027.columns = ["wind_2027"]
    if technology is not None:
        if technology == "wind_2027":
            return wind_2027
        sources = {technology: sources[technology]}

    areas = get_data_from_sources(sources.values())
    areas = pd.concat([areas, wind_2027], axis=1)
    areas.columns = [column_mapping[column] for column in areas.columns]
    if technology is not None:
        return areas[technology]
    return areas


@cache_memoize(timeout=None)
def get_full_load_hours(year: int) -> pd.Series:
    """Return full load hours for given year."""
    full_load_hours = pd.Series(
        data=[technology_data[str(year)] for technology_data in config.TECHNOLOGY_DATA["full_load_hours"].values()],
        index=config.TECHNOLOGY_DATA["full_load_hours"].keys(),
    )
    return full_load_hours


@cache_memoize(timeout=None)
def get_capacities_from_datapackage() -> pd.DataFrame:
    """Return renewable capacities for given year from datapackage."""
    capacities = pd.concat(
        [
            pd.read_csv(
                settings.DIGIPIPE_DIR.path("scalars").path(f"bnetza_mastr_{tech}_stats_muns.csv"),
                index_col="municipality_id",
                usecols=["municipality_id", "capacity_net"],
            ).rename(columns={"capacity_net": tech})
            for tech in ["wind", "pv_roof", "pv_ground", "hydro", "biomass"]
        ],
        axis=1,
    )
    capacities.index.name = "mun_id"
    return capacities


def get_capacities_from_sliders(year: int) -> pd.Series:
    """Return renewable capacities for given year from slider settings (totals for each technology)."""
    if year == 2022:  # noqa: PLR2004
        lookup = "status_quo"
        bioenergy_power = 55.7  # Workaround for bioenergy as there's no slider
    elif year == 2045:  # noqa: PLR2004
        lookup = "future_scenario_2040"
        bioenergy_power = 0
    else:
        msg = "Unknown year"
        raise ValueError(msg)
    energy_settings = json.load(Path.open(Path(settings.DIGIPIPE_DIR, "settings/energy_settings_panel.json")))
    technologies = {"wind": "s_w_1", "pv_ground": "s_pv_ff_1", "pv_roof": "s_pv_d_1", "ror": "s_h_1"}
    slider_settings = pd.Series(
        data={
            **{technology: energy_settings[key].get(lookup, 0.0) for technology, key in technologies.items()},
            "bioenergy": bioenergy_power,
        },
    )
    return slider_settings


@cache_memoize(timeout=None)
def get_power_density(technology: Optional[str] = None) -> dict:
    """Return power density for technology."""
    if technology:
        return config.TECHNOLOGY_DATA["power_density"][technology]
    return config.TECHNOLOGY_DATA["power_density"]


def get_profile(technology: str) -> pd.Series:
    """Return profile for given technology from oemof datapackage."""
    profile_filename = OEMOF_DIR / settings.OEMOF_SCENARIO / "data" / "sequences" / f"{technology}_profile.csv"
    profile = pd.read_csv(profile_filename, sep=";", index_col=0)
    return profile.iloc[:, 0]
