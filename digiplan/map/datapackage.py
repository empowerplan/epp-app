"""Read functionality for digipipe datapackage."""

import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple, Union

import pandas as pd
from cache_memoize import cache_memoize
from django.conf import settings
from django.db.models import Sum
from django_oemof.settings import OEMOF_DIR

from config.settings.base import DIGIPIPE_DIR
from digiplan.map import config, models
from digiplan.map.utils import (
    interpolate_year_from_dataframe,
    interpolate_year_from_dict,
)


class Source(NamedTuple):
    """Stores information on data sources."""

    csv_file: str
    column: str


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


@cache_memoize(timeout=None)
def get_region_area() -> float:
    """Return total region area in ?."""
    return models.Municipality.objects.values("area").aggregate(Sum("area"))["area__sum"]


def get_employment() -> pd.DataFrame:
    """Return employment data."""
    employment_filename = settings.DIGIPIPE_DIR.path("scalars").path("employment.csv")
    return pd.read_csv(employment_filename, index_col=0)


def get_batteries() -> pd.DataFrame:
    """Return battery data."""
    battery_filename = settings.DIGIPIPE_DIR.path("scalars").path("bnetza_mastr_storage_stats_muns.csv")
    return pd.read_csv(battery_filename)


def get_power_demand(sector: str | None = None) -> dict[str, pd.DataFrame]:
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
        demand.append(demand_profile[sector] * interpolate_year_from_dataframe(demand_sector_per_mun, year).sum())
    return pd.concat(demand, axis=1).sum(axis=1)


def get_heat_demand(sector: str | None = None, distribution: str | None = None) -> dict[str, pd.DataFrame]:
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
    year: int | None = 2045,
    *,
    include_heatpumps: bool | None = False,
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
    sector: str | None = None,
    distribution: str | None = None,
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


def disaggregate_tsam_sequence(series: pd.Series, day_order: list[int]) -> pd.Series:
    """Disaggregate series for the whole year according to tsam_order."""
    # Split the demand sequence into days (24 timesteps per day)
    days = [series.iloc[i : i + 24] for i in range(0, len(series), 24)]

    # Rebuild the full year according to tsam_order
    full_year = []
    for day_idx in day_order:
        full_year.extend(days[day_idx].values)

    return pd.Series(full_year)


def get_heat_demand_profile(
    sector: str | None = None,
    distribution: str | None = None,
    scenario: str | None = None,
    *,
    disaggregate_tsam: bool = False,
) -> dict[str, dict[str, pd.DataFrame]]:
    """Return heat demand for given sector and distribution."""
    sectors = (sector,) if sector else ("hh", "cts", "ind")
    distributions = (distribution,) if distribution else ("central", "decentral")
    demand = defaultdict(dict)
    scenario = scenario or settings.OEMOF_ORIGINAL_SCENARIO
    if disaggregate_tsam:
        tsam_config = pd.read_csv(OEMOF_DIR / scenario / "data" / "tsam" / "tsa_parameters.csv", sep=";")
        day_order_raw = tsam_config.iloc[0]["order"]
        day_order = list(map(int, day_order_raw.strip("[]").split(",")))
    for sec in sectors:
        for dist in distributions:
            demand_filename = OEMOF_DIR / scenario / "data" / "sequences" / f"heat_{dist}-demand_{sec}_profile.csv"
            demand_sequence = pd.read_csv(demand_filename, sep=";")[f"ABW-heat_{dist}-demand_{sec}-profile"]
            if disaggregate_tsam:
                demand_sequence = disaggregate_tsam_sequence(demand_sequence, day_order)
            demand[sec][dist] = demand_sequence
    return demand


def get_electricity_demand_profile(
    sector: str | None = None,
    scenario: str | None = None,
) -> dict[str, pd.DataFrame]:
    """Return heat demand for given sector and distribution."""
    sectors = (sector,) if sector else ("hh", "cts", "ind")
    demand = defaultdict(dict)
    scenario = scenario or settings.OEMOF_ORIGINAL_SCENARIO
    for sec in sectors:
        demand_filename = OEMOF_DIR / scenario / "data" / "sequences" / f"electricity-demand_{sec}_profile.csv"
        demand[sec] = pd.read_csv(demand_filename, sep=";")[f"ABW-electricity-demand_{sec}-profile"]
    return demand


def get_thermal_efficiency(
    component: str,
    scenario: str | None = None,
    *,
    disaggregate_tsam: bool = False,
) -> Union[float, pd.Series]:
    """Return thermal efficiency from given component from oemof scenario."""
    scenario = scenario or settings.OEMOF_ORIGINAL_SCENARIO
    component_filename = OEMOF_DIR / scenario / "data" / "elements" / f"{component}.csv"
    component_df = pd.read_csv(component_filename, sep=";")
    if component_df["type"][0] in ("extraction", "backpressure"):
        return float(pd.read_csv(component_filename, sep=";")["thermal_efficiency"][0])

    if "efficiency" in component_df.columns and isinstance(component_df["efficiency"][0], float):
        return component_df["efficiency"][0]

    if "heatpump" in component:
        component = "efficiency"

    sequence_filename = OEMOF_DIR / scenario / "data" / "sequences" / f"{component}_profile.csv"
    efficiency_series = pd.read_csv(sequence_filename, sep=";").iloc[:, 1]
    if disaggregate_tsam:
        tsam_config = pd.read_csv(OEMOF_DIR / scenario / "data" / "tsam" / "tsa_parameters.csv", sep=";")
        day_order_raw = tsam_config.iloc[0]["order"]
        day_order = list(map(int, day_order_raw.strip("[]").split(",")))
        efficiency_series = disaggregate_tsam_sequence(efficiency_series, day_order)
    return efficiency_series


@cache_memoize(timeout=None)
def get_potential_capacities() -> pd.DataFrame:
    """
    Calculate maximum potential capacities in MW.

    Returns
    -------
    pd.DataFrame
        holding potential capacities for all technologies in MW

    """
    areas = get_potential_areas()
    # TODO (Hendrik Huyskens): Could be refactored using datapackage.get_power_density
    # https://github.com/empowerplan/epp-app/issues/118
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
def get_potential_areas(technology: str | None = None) -> pd.DataFrame:
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


def get_potential_areas_region(region_id: int, technology: str | None = None) -> pd.Series:
    """
    Return potential areas for a specific region (municipality).

    Parameters
    ----------
    region_id: int
        Municipality ID to filter for
    technology: str | None
        If given, returns a Series with a single value for the requested technology.
        If None, returns a Series with a single row containing all technologies.

    Returns
    -------
    pd.Series
        Potential areas for the given municipality (in sqkm). Index are technologies if technology is None.

    """
    areas = get_potential_areas(technology)
    # areas can be a Series (for a single technology) or a DataFrame (for all)
    if isinstance(areas, pd.Series):
        # Index is municipality id
        if region_id in areas.index:
            return pd.Series({technology: areas.loc[region_id]})
        return pd.Series({technology: 0.0})

    # DataFrame case: filter row by region_id and return as Series
    if region_id in areas.index:
        return areas.loc[region_id]
    # Municipality may be missing (e.g., filtered datasets); return zeros with same columns
    return pd.Series(dict.fromkeys(areas.columns, 0.0))


@cache_memoize(timeout=None)
def get_full_load_hours(year: int) -> pd.Series:
    """Return full load hours for given year."""
    full_load_hours = pd.Series(
        data=[
            interpolate_year_from_dict(technology_data, year)
            for technology_data in config.TECHNOLOGY_DATA["full_load_hours"].values()
        ],
        index=config.TECHNOLOGY_DATA["full_load_hours"].keys(),
    )
    return full_load_hours


@cache_memoize(timeout=None)
def get_capacities_from_datapackage() -> pd.DataFrame:
    """Return renewable capacities for given year from datapackage."""
    # Override MaStR data manually
    filenames_rpg_data = {
        "wind": "rpg_ols_wind_stats_muns_operating.csv",
        "pv_ground": "rpg_ols_pv_ground_stats_muns_operating.csv",
    }
    capacities = pd.concat(
        [
            pd.read_csv(
                settings.DIGIPIPE_DIR.path("scalars").path(
                    (
                        f"bnetza_mastr_{tech}_stats_muns.csv"
                        if tech not in ["wind", "pv_ground"]
                        else filenames_rpg_data.get(tech)
                    ),
                ),
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
    energy_settings = json.load(Path.open(Path(settings.DIGIPIPE_DIR, "settings/energy_settings_panel.json")))
    technologies = {"wind": "s_w_1", "pv_ground": "s_pv_ff_1", "pv_roof": "s_pv_d_1", "ror": "s_h_1"}

    data = {"bioenergy": interpolate_year_from_dict({2022: 98.476, 2040: 0}, year)}
    for technology, key in technologies.items():
        data[technology] = interpolate_year_from_dict(
            {2022: energy_settings[key].get("status_quo", 0.0), 2045: energy_settings[key].get("future_scenario_2040")},
            year,
        )
    slider_settings = pd.Series(data)
    return slider_settings


@cache_memoize(timeout=None)
def get_power_density() -> dict:
    """Return power density for technology."""
    technologies = {
        "pv_soil_quality_low": "pv_ground",
        "pv_soil_quality_medium": "pv_ground_vertical_bifacial",
        "pv_permanent_crops": "pv_ground_elevated",
        "pv_roof": "pv_roof",
        "wind": "wind",
        "hydro": "st",
    }
    power_density = json.load(Path.open(Path(settings.DIGIPIPE_DIR, "scalars/technology_data.json")))["power_density"]
    densities = {
        technology: power_density["wind"] if technology.startswith("wind") else power_density[technologies[technology]]
        for technology in technologies
    }
    return densities


def get_profile(technology: str, scenario: str | None = None) -> pd.Series:
    """Return profile for given technology from oemof datapackage."""
    scenario = scenario or settings.OEMOF_ORIGINAL_SCENARIO
    profile_filename = OEMOF_DIR / scenario / "data" / "sequences" / f"{technology}_profile.csv"
    profile = pd.read_csv(profile_filename, sep=";", index_col=0)
    return profile.iloc[:, 0]
