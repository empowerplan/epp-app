"""Digiplan models."""


import pandas as pd
from django.contrib.gis.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from .managers import LabelMVTManager, RegionMVTManager, StaticMVTManager

# REGIONS


class Region(models.Model):
    """Base class for all regions - works as connector to other models."""

    class LayerType(models.TextChoices):
        """Region layer types."""

        COUNTRY = "country", _("Country")
        STATE = "state", _("State")
        DISTRICT = "district", _("District")
        MUNICIPALITY = "municipality", _("Municipality")

    layer_type = models.CharField(max_length=12, choices=LayerType.choices, null=False)

    class Meta:  # noqa: D106
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")


class Municipality(models.Model):
    """Model for region level municipality."""

    geom = models.MultiPolygonField(srid=4326)
    name = models.CharField(max_length=50, unique=True)
    area = models.FloatField()

    region = models.OneToOneField("Region", on_delete=models.DO_NOTHING, null=True)

    objects = models.Manager()
    vector_tiles = RegionMVTManager(columns=["id", "name", "bbox"])
    label_tiles = LabelMVTManager(geo_col="geom_label", columns=["id", "name"])

    data_file = "bkg_vg250_muns_region"
    layer = "vg250_gem"
    mapping = {"id": "id", "geom": "MULTIPOLYGON", "name": "name", "area": "area_km2"}

    class Meta:  # noqa: D106
        verbose_name = _("Municipality")
        verbose_name_plural = _("Municipalities")

    def __str__(self) -> str:
        """Return string representation of model."""
        return self.name

    @classmethod
    def area_whole_region(cls) -> float:
        """
        Return summed area of all municipalities.

        Returns
        -------
        float
            total area of all municipalities
        """
        return cls.objects.all().aggregate(Sum("area"))["area__sum"]


class Population(models.Model):
    """Population model."""

    year = models.IntegerField()
    value = models.IntegerField()
    entry_type = models.CharField(max_length=13)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)

    class Meta:  # noqa: D106
        verbose_name = _("Population")
        verbose_name_plural = _("Population")

    @classmethod
    def quantity_per_municipality_per_year(cls) -> pd.DataFrame:
        """
        Return population in 2022 per municipality and year.

        Returns
        -------
        pd.DataFrame
            Population per municipality (index) and year (column)
        """
        population_per_year = (
            pd.DataFrame.from_records(cls.objects.all().values("municipality__id", "year", "value"))  # noqa: PD010
            .set_index("municipality__id")
            .pivot(columns="year")
        )
        population_per_year.columns = population_per_year.columns.droplevel(0)
        return population_per_year


class RenewableModel(models.Model):
    """Base class for renewable cluster models."""

    geom = models.PointField(srid=4326)
    name = models.CharField(max_length=255, null=True)
    geometry_approximated = models.BooleanField()
    unit_count = models.BigIntegerField(null=True)
    capacity_net = models.FloatField(null=True)
    zip_code = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    commissioning_date = models.CharField(max_length=50, null=True)
    commissioning_date_planned = models.CharField(max_length=50, null=True)
    decommissioning_date = models.CharField(max_length=50, null=True)
    capacity_gross = models.FloatField(null=True)
    voltage_level = models.CharField(max_length=50, null=True)
    mastr_id = models.CharField(max_length=50, null=True)

    mun_id = models.ForeignKey(Municipality, on_delete=models.DO_NOTHING, null=True)

    objects = models.Manager()

    class Meta:  # noqa: D106
        abstract = True


class WindTurbine(RenewableModel):
    """Model holding wind turbines."""

    name_park = models.CharField(max_length=255, null=True)
    hub_height = models.FloatField(null=True)
    rotor_diameter = models.FloatField(null=True)
    site_type = models.CharField(max_length=255, null=True)
    manufacturer_name = models.CharField(max_length=255, null=True)
    type_name = models.CharField(max_length=255, null=True)
    constraint_deactivation_sound_emission = models.CharField(max_length=50, null=True)
    constraint_deactivation_sound_emission_night = models.CharField(max_length=50, null=True)
    constraint_deactivation_sound_emission_day = models.CharField(max_length=50, null=True)
    constraint_deactivation_shadowing = models.CharField(max_length=50, null=True)
    constraint_deactivation_animals = models.CharField(max_length=50, null=True)
    constraint_deactivation_ice = models.CharField(max_length=50, null=True)
    citizens_unit = models.CharField(max_length=50, null=True)

    data_file = "bnetza_mastr_wind_agg_region"
    layer = "bnetza_mastr_wind"
    mapping = {
        "geom": "POINT",
        "name": "name",
        "geometry_approximated": "geometry_approximated",
        "unit_count": "unit_count",
        "capacity_net": "capacity_net",
        "zip_code": "zip_code",
        "mun_id": {"id": "municipality_id"},
        "status": "status",
        "city": "city",
        "commissioning_date": "commissioning_date",
        "commissioning_date_planned": "commissioning_date_planned",
        "decommissioning_date": "decommissioning_date",
        "capacity_gross": "capacity_gross",
        "voltage_level": "voltage_level",
        "mastr_id": "mastr_id",
        "name_park": "name_park",
        "hub_height": "hub_height",
        "rotor_diameter": "rotor_diameter",
        "site_type": "site_type",
        "manufacturer_name": "manufacturer_name",
        "type_name": "type_name",
        "constraint_deactivation_sound_emission": "constraint_deactivation_sound_emission",
        "constraint_deactivation_sound_emission_night": "constraint_deactivation_sound_emission_night",
        "constraint_deactivation_sound_emission_day": "constraint_deactivation_sound_emission_day",
        "constraint_deactivation_shadowing": "constraint_deactivation_shadowing",
        "constraint_deactivation_animals": "constraint_deactivation_animals",
        "constraint_deactivation_ice": "constraint_deactivation_ice",
        "citizens_unit": "citizens_unit",
    }

    class Meta:  # noqa: D106
        verbose_name = _("Wind turbine")
        verbose_name_plural = _("Wind turbines")

    def __str__(self) -> str:
        """Return string representation of model."""
        return self.name

    @classmethod
    def quantity_per_municipality(cls) -> pd.DataFrame:
        """
        Calculate number of wind turbines per municipality.

        Returns
        -------
        dpd.DataFrame
            wind turbines per municipality
        """
        queryset = cls.objects.values("mun_id").annotate(units=Sum("unit_count")).values("mun_id", "units")
        wind_turbines = pd.DataFrame.from_records(queryset).set_index("mun_id")
        return wind_turbines["units"].reindex(Municipality.objects.all().values_list("id", flat=True), fill_value=0)


class PVroof(RenewableModel):
    """Model holding PV roof."""

    power_limitation = models.CharField(max_length=50, null=True)
    site_type = models.CharField(max_length=255, null=True)
    feedin_type = models.CharField(max_length=255, null=True)
    module_count = models.FloatField(null=True)
    usage_sector = models.CharField(max_length=50, null=True)
    orientation_primary = models.CharField(max_length=50, null=True)
    orientation_secondary = models.CharField(max_length=50, null=True)
    area_type = models.FloatField(null=True)
    area_occupied = models.FloatField(null=True)
    citizens_unit = models.CharField(max_length=50, null=True)
    landlord_to_tenant_electricity = models.CharField(max_length=50, null=True)

    data_file = "bnetza_mastr_pv_roof_agg_region"
    layer = "bnetza_mastr_pv_roof"

    mapping = {
        "geom": "POINT",
        "name": "name",
        "zip_code": "zip_code",
        "geometry_approximated": "geometry_approximated",
        "unit_count": "unit_count",
        "capacity_net": "capacity_net",
        "mun_id": {"id": "municipality_id"},
        "status": "status",
        "city": "city",
        "commissioning_date": "commissioning_date",
        "commissioning_date_planned": "commissioning_date_planned",
        "decommissioning_date": "decommissioning_date",
        "capacity_gross": "capacity_gross",
        "voltage_level": "voltage_level",
        "mastr_id": "mastr_id",
        "power_limitation": "power_limitation",
        "site_type": "site_type",
        "feedin_type": "feedin_type",
        "module_count": "module_count",
        "usage_sector": "usage_sector",
        "orientation_primary": "orientation_primary",
        "orientation_secondary": "orientation_secondary",
        "area_type": "area_type",
        "area_occupied": "area_occupied",
        "citizens_unit": "citizens_unit",
        "landlord_to_tenant_electricity": "landlord_to_tenant_electricity",
    }

    class Meta:  # noqa: D106
        verbose_name = _("Roof-mounted PV")
        verbose_name_plural = _("Roof-mounted PVs")

    def __str__(self) -> str:
        """Return string representation of model."""
        return self.name


class PVground(RenewableModel):
    """Model holding PV on ground."""

    power_limitation = models.CharField(max_length=50, null=True)
    site_type = models.CharField(max_length=255, null=True)
    feedin_type = models.CharField(max_length=255, null=True)
    module_count = models.FloatField(null=True)
    usage_sector = models.CharField(max_length=50, null=True)
    orientation_primary = models.CharField(max_length=50, null=True)
    orientation_secondary = models.CharField(max_length=50, null=True)
    area_type = models.FloatField(null=True)
    area_occupied = models.FloatField(null=True)
    citizens_unit = models.CharField(max_length=50, null=True)
    landlord_to_tenant_electricity = models.CharField(max_length=50, null=True)

    data_file = "bnetza_mastr_pv_ground_agg_region"
    layer = "bnetza_mastr_pv_ground"

    mapping = {
        "geom": "POINT",
        "name": "name",
        "zip_code": "zip_code",
        "geometry_approximated": "geometry_approximated",
        "unit_count": "unit_count",
        "capacity_net": "capacity_net",
        "mun_id": {"id": "municipality_id"},
        "status": "status",
        "city": "city",
        "commissioning_date": "commissioning_date",
        "commissioning_date_planned": "commissioning_date_planned",
        "decommissioning_date": "decommissioning_date",
        "capacity_gross": "capacity_gross",
        "voltage_level": "voltage_level",
        "mastr_id": "mastr_id",
        "power_limitation": "power_limitation",
        "site_type": "site_type",
        "feedin_type": "feedin_type",
        "module_count": "module_count",
        "usage_sector": "usage_sector",
        "orientation_primary": "orientation_primary",
        "orientation_secondary": "orientation_secondary",
        "area_type": "area_type",
        "area_occupied": "area_occupied",
        "citizens_unit": "citizens_unit",
        "landlord_to_tenant_electricity": "landlord_to_tenant_electricity",
    }

    class Meta:  # noqa: D106
        verbose_name = _("Ground-mounted PV")
        verbose_name_plural = _("Ground-mounted PV")


class Hydro(RenewableModel):
    """Hydro model."""

    water_origin = models.CharField(max_length=255, null=True)
    kwk_mastr_id = models.FloatField(null=True)
    plant_type = models.CharField(max_length=255, null=True)
    feedin_type = models.CharField(max_length=255, null=True)

    data_file = "bnetza_mastr_hydro_agg_region"
    layer = "bnetza_mastr_hydro"

    mapping = {
        "geom": "POINT",
        "name": "name",
        "zip_code": "zip_code",
        "geometry_approximated": "geometry_approximated",
        "unit_count": "unit_count",
        "capacity_net": "capacity_net",
        "mun_id": {"id": "municipality_id"},
        "status": "status",
        "city": "city",
        "commissioning_date": "commissioning_date",
        "commissioning_date_planned": "commissioning_date_planned",
        "decommissioning_date": "decommissioning_date",
        "capacity_gross": "capacity_gross",
        "voltage_level": "voltage_level",
        "mastr_id": "mastr_id",
        "water_origin": "water_origin",
        "kwk_mastr_id": "kwk_mastr_id",
        "plant_type": "plant_type",
        "feedin_type": "feedin_type",
    }

    class Meta:  # noqa: D106
        verbose_name = _("Hydro")
        verbose_name_plural = _("Hydro")


class Biomass(RenewableModel):
    """Biomass model."""

    fuel_type = models.CharField(max_length=50, null=True)
    kwk_mastr_id = models.CharField(max_length=50, null=True)
    th_capacity = models.FloatField(null=True)
    feedin_type = models.CharField(max_length=50, null=True)
    technology = models.CharField(max_length=255, null=True)
    fuel = models.CharField(max_length=255, null=True)
    biomass_only = models.CharField(max_length=50, null=True)
    flexibility_bonus = models.CharField(max_length=50, null=True)

    data_file = "bnetza_mastr_biomass_agg_region"
    layer = "bnetza_mastr_biomass"

    mapping = {
        "geom": "POINT",
        "name": "name",
        "zip_code": "zip_code",
        "geometry_approximated": "geometry_approximated",
        "unit_count": "unit_count",
        "capacity_net": "capacity_net",
        "mun_id": {"id": "municipality_id"},
        "status": "status",
        "city": "city",
        "commissioning_date": "commissioning_date",
        "commissioning_date_planned": "commissioning_date_planned",
        "decommissioning_date": "decommissioning_date",
        "capacity_gross": "capacity_gross",
        "voltage_level": "voltage_level",
        "mastr_id": "mastr_id",
        "fuel_type": "fuel_type",
        "kwk_mastr_id": "kwk_mastr_id",
        "th_capacity": "th_capacity",
        "feedin_type": "feedin_type",
        "technology": "technology",
        "fuel": "fuel",
        "biomass_only": "biomass_only",
        "flexibility_bonus": "flexibility_bonus",
    }

    class Meta:  # noqa: D106
        verbose_name = _("Biomass")
        verbose_name_plural = _("Biomass")


class Combustion(RenewableModel):
    """Combustion model."""

    name_block = models.CharField(max_length=255, null=True)
    kwk_mastr_id = models.CharField(max_length=50, null=True)
    bnetza_id = models.CharField(max_length=50, null=True)
    usage_sector = models.CharField(max_length=50, null=True)
    th_capacity = models.FloatField(null=True)
    feedin_type = models.CharField(max_length=255, null=True)
    technology = models.CharField(max_length=255, null=True)
    fuel_other = models.CharField(max_length=255, null=True)
    fuels = models.CharField(max_length=255, null=True)

    data_file = "bnetza_mastr_combustion_agg_region"
    layer = "bnetza_mastr_combustion"

    mapping = {
        "geom": "POINT",
        "name": "name",
        "zip_code": "zip_code",
        "geometry_approximated": "geometry_approximated",
        "unit_count": "unit_count",
        "capacity_net": "capacity_net",
        "mun_id": {"id": "municipality_id"},
        "status": "status",
        "city": "city",
        "commissioning_date": "commissioning_date",
        "commissioning_date_planned": "commissioning_date_planned",
        "decommissioning_date": "decommissioning_date",
        "capacity_gross": "capacity_gross",
        "voltage_level": "voltage_level",
        "mastr_id": "mastr_id",
        "name_block": "block_name",
        "kwk_mastr_id": "kwk_mastr_id",
        "bnetza_id": "bnetza_id",
        "usage_sector": "usage_sector",
        "th_capacity": "th_capacity",
        "feedin_type": "feedin_type",
        "technology": "technology",
        "fuel_other": "fuel_other",
        "fuels": "fuels",
    }

    class Meta:  # noqa: D106
        verbose_name = _("Combustion")
        verbose_name_plural = _("Combustion")


class GSGK(RenewableModel):
    """GSGK model."""

    feedin_type = models.CharField(max_length=50, null=True)
    kwk_mastr_id = models.CharField(max_length=50, null=True)
    th_capacity = models.FloatField(null=True)
    unit_type = models.CharField(max_length=255, null=True)
    technology = models.CharField(max_length=255, null=True)

    data_file = "bnetza_mastr_gsgk_agg_region"
    layer = "bnetza_mastr_gsgk"

    mapping = {
        "geom": "POINT",
        "name": "name",
        "zip_code": "zip_code",
        "geometry_approximated": "geometry_approximated",
        "unit_count": "unit_count",
        "capacity_net": "capacity_net",
        "mun_id": {"id": "municipality_id"},
        "status": "status",
        "city": "city",
        "commissioning_date": "commissioning_date",
        "commissioning_date_planned": "commissioning_date_planned",
        "decommissioning_date": "decommissioning_date",
        "capacity_gross": "capacity_gross",
        "voltage_level": "voltage_level",
        "mastr_id": "mastr_id",
        "feedin_type": "feedin_type",
        "kwk_mastr_id": "kwk_mastr_id",
        "th_capacity": "th_capacity",
        "unit_type": "type",
        "technology": "technology",
    }

    class Meta:  # noqa: D106
        verbose_name = _("GSGK")
        verbose_name_plural = _("GSGK")


class Storage(RenewableModel):
    """Storage model."""

    data_file = "bnetza_mastr_storage_agg_region"
    layer = "bnetza_mastr_storage"

    mapping = {
        "geom": "POINT",
        "name": "name",
        "zip_code": "zip_code",
        "geometry_approximated": "geometry_approximated",
        "unit_count": "unit_count",
        "capacity_net": "capacity_net",
        "mun_id": {"id": "municipality_id"},
        "status": "status",
        "city": "city",
        "commissioning_date": "commissioning_date",
        "commissioning_date_planned": "commissioning_date_planned",
        "decommissioning_date": "decommissioning_date",
        "capacity_gross": "capacity_gross",
        "voltage_level": "voltage_level",
    }

    class Meta:  # noqa: D106
        verbose_name = _("Battery storage")
        verbose_name_plural = _("Battery storages")


class StaticRegionModel(models.Model):
    """Base class for static region models."""

    geom = models.MultiPolygonField(srid=4326)

    objects = models.Manager()
    vector_tiles = StaticMVTManager(columns=[])

    mapping = {"geom": "MULTIPOLYGON"}

    class Meta:  # noqa: D106
        abstract = True


class AirTraffic(StaticRegionModel):  # noqa: D101
    data_file = "air_traffic_control_system_region"
    layer = "air_traffic_control_system"


class BiosphereReserve(StaticRegionModel):  # noqa: D101
    data_file = "biosphere_reserve_region"
    layer = "biosphere_reserve"


class DrinkingWaterArea(StaticRegionModel):  # noqa: D101
    data_file = "drinking_water_protection_area_region"
    layer = "drinking_water_protection_area"


class FaunaFloraHabitat(StaticRegionModel):  # noqa: D101
    data_file = "fauna_flora_habitat_region"
    layer = "fauna_flora_habitat"


class Floodplain(StaticRegionModel):  # noqa: D101
    data_file = "floodplain_region"
    layer = "floodplain"


class Forest(StaticRegionModel):  # noqa: D101
    data_file = "forest_region"
    layer = "forest"


class Grid(StaticRegionModel):  # noqa: D101
    data_file = "grid_region"
    layer = "grid"


class Industry(StaticRegionModel):  # noqa: D101
    data_file = "industry_region"
    layer = "industry"


class LandscapeProtectionArea(StaticRegionModel):  # noqa: D101
    data_file = "landscape_protection_area_region"
    layer = "landscape_protection_area"


class LessFavouredAreasAgricultural(StaticRegionModel):  # noqa: D101
    data_file = "less_favoured_areas_agricultural_region"
    layer = "less_favoured_areas_agricultural"


class Military(StaticRegionModel):  # noqa: D101
    data_file = "military_region"
    layer = "military"


class NatureConservationArea(StaticRegionModel):  # noqa: D101
    data_file = "nature_conservation_area_region"
    layer = "nature_conservation_area"


class Railway(StaticRegionModel):  # noqa: D101
    data_file = "railway_region"
    layer = "railway"


class Road(StaticRegionModel):  # noqa: D101
    data_file = "road_region"
    layer = "road"


class SoilQualityHigh(StaticRegionModel):  # noqa: D101
    data_file = "soil_quality_high_region"
    layer = "soil_quality_high"


class SoilQualityLow(StaticRegionModel):  # noqa: D101
    data_file = "soil_quality_low_region"
    layer = "soil_quality_low"


class SpecialProtectionArea(StaticRegionModel):  # noqa: D101
    data_file = "special_protection_area_region"
    layer = "special_protection_area"


class Water(StaticRegionModel):  # noqa: D101
    data_file = "water_region"
    layer = "water"


class PVGroundCriteriaSettlements(StaticRegionModel):  # noqa: D101
    data_file = "pv_ground_criteria_settlements"
    layer = "Wohnbauflaechen"


class PVGroundCriteriaSettlements200m(StaticRegionModel):  # noqa: D101
    data_file = "pv_ground_criteria_settlements_200m"
    layer = "Wohnpuffer_200m"


class PVGroundCriteriaAviation(StaticRegionModel):  # noqa: D101
    data_file = "pv_ground_criteria_aviation"
    layer = "Landebahnflaechen"


class PotentialareaPVGroundSoilQualityLow(StaticRegionModel):  # noqa: D101
    data_file = "potentialarea_pv_ground_soil_quality_low_region"
    layer = "potentialarea_pv_ground_soil_quality_low_region"


class PotentialareaPVGroundSoilQualityMedium(StaticRegionModel):  # noqa: D101
    data_file = "potentialarea_pv_ground_soil_quality_medium_region"
    layer = "potentialarea_pv_ground_soil_quality_medium_region"


class PotentialareaPVGroundPermanentCrops(StaticRegionModel):  # noqa: D101
    data_file = "potentialarea_pv_ground_permanent_crops_region"
    layer = "potentialarea_pv_ground_permanent_crops_region"


class PotentialareaPVRoof(StaticRegionModel):  # noqa: D101
    data_file = "potentialarea_pv_roof_region"
    layer = "potentialarea_pv_roof_region"


class PotentialAreaWindSTP2018EG(StaticRegionModel):  # noqa: D101
    data_file = "potentialarea_wind_stp_2018_eg"
    layer = "potentialarea_wind_stp_2018_eg"


class PotentialAreaWindSTP2024VR(StaticRegionModel):  # noqa: D101
    data_file = "potentialarea_wind_stp_2024_vr"
    layer = "potentialarea_wind_stp_2024_vr"
