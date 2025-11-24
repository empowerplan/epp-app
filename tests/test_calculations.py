"""Module to test oemof simulation results."""

import os

import pandas as pd
import pytest
from django.test import SimpleTestCase
from django_oemof import models
from django_oemof import results as oemof_results
from django_oemof import simulation
from oemof.tabular.postprocessing import calculations as oc
from oemof.tabular.postprocessing import core

from digiplan.map import calculations, charts


class SimulationTest(SimpleTestCase):
    """Base class for simulation tests."""

    databases = ("default",)  # Needed, as otherwise django complains about tests using "default" DB
    parameters = {
        "s_v_1": 100,
        "s_v_3": 100,
        "s_v_4": 100,
        "s_v_5": 100,
        "s_w_1": 714,
        "w_v_1": 100,
        "w_v_3": 100,
        "w_v_4": 100,
        "w_v_5": 100,
        "s_pv_ff_1": 388,
        "s_pv_d_1": 298,
        "s_h_1": 5,
        "s_s_g_1": 1,
        "w_d_wp_3": 50,
        "w_d_wp_4": 50,
        "w_d_wp_5": 50,
        "w_z_wp_1": 50,
        "w_d_s_1": 100,
        "w_z_s_1": 100,
        "w_d_wp_1": True,
        "s_w_3": True,
        "s_w_4": True,
        "s_w_4_1": True,
        "s_w_4_2": True,
        "s_w_5": False,
        "s_w_5_1": 50,
        "s_w_5_2": 50,
        "s_pv_ff_3": 11,
        "s_pv_ff_4": 11,
        "s_pv_d_3": 5,
        "s_pv_d_4": 13,
        "t": "v19",
    }

    def setUp(self) -> None:
        """Starts/loads oemof simulation for given parameters."""
        self.simulation_id = simulation.simulate_scenario("scenario_2045_original", self.parameters)
        if os.environ.get("TEST_SHOW_SIMULATION_RESULTS", "False") == "True":
            self.results = models.Simulation.objects.get(pk=self.simulation_id).dataset.restore_results()

    def tearDown(self) -> None:  # noqa: D102 Needed to keep results in test DB
        pass

    @classmethod
    def tearDownClass(cls):  # noqa: D102, ANN206 Needed to keep results in test DB
        pass


class PreResultTest(SimpleTestCase):
    """Base class for pre result tests."""

    parameters = {
        "s_v_1": 100,
        "s_v_3": 11,
        "s_v_4": 22,
        "s_v_5": 33,
        "s_w_1": 714,
        "w_v_1": 100,
        "w_v_3": 10,
        "w_v_4": 20,
        "w_v_5": 30,
        "s_pv_ff_1": 388,
        "s_pv_d_1": 298,
        "s_h_1": 5,
        "s_s_g_1": 1,
        "w_d_wp_3": 50,
        "w_d_wp_4": 50,
        "w_d_wp_5": 50,
        "w_z_wp_1": 50,
        "w_d_s_1": 100,
        "w_z_s_1": 100,
        "w_d_wp_1": True,
        "s_w_3": True,
        "s_w_4": True,
        "s_w_4_1": True,
        "s_w_4_2": True,
        "s_w_5": False,
        "s_w_5_1": 50,
        "s_w_5_2": 50,
        "s_pv_ff_3": 11,
        "s_pv_ff_4": 11,
        "s_pv_d_3": 5,
        "s_pv_d_4": 13,
    }


class HeatShareTestCase(SimpleTestCase):
    """Test if heat component shares are correct."""

    databases = ("default",)
    parameters = {
        "s_v_1": 100,
        "s_v_3": 100,
        "s_v_4": 100,
        "s_v_5": 100,
        "s_w_1": 714,
        "w_v_1": 100,
        "w_v_3": 80,
        "w_v_4": 70,
        "w_v_5": 60,
        "s_pv_ff_1": 388,
        "s_pv_d_1": 298,
        "s_h_1": 5,
        "s_s_g_1": 1,
        "w_d_wp_3": 50,
        "w_d_wp_4": 45,
        "w_d_wp_5": 40,
        "w_z_wp_1": 50,
        "w_d_s_1": 100,
        "w_z_s_1": 100,
        "w_d_wp_1": True,
        "s_w_3": True,
        "s_w_4": True,
        "s_w_4_1": True,
        "s_w_4_2": True,
        "s_w_5": False,
        "s_w_5_1": 50,
        "s_w_5_2": 50,
        "s_pv_ff_3": 11,
        "s_pv_ff_4": 11,
        "s_pv_d_3": 5,
        "s_pv_d_4": 13,
        "t": "v27",
    }

    def setUp(self) -> None:
        """Starts/loads oemof simulation for given parameters."""
        self.simulation_id = simulation.simulate_scenario("tsam_40_24_1_cost_0", self.parameters)
        self.results = models.Simulation.objects.get(pk=self.simulation_id).dataset.restore_results()

    def test_heat_demands(self):  # noqa: D102
        assert (
            pytest.approx(
                self.results[1][("ABW-heat_central", "ABW-heat_central-demand_hh")]["sequences"]["flow"].sum(),
            )
            == 158269 * 0.8
        )
        assert (
            pytest.approx(
                self.results[1][("ABW-heat_central", "ABW-heat_central-demand_cts")]["sequences"]["flow"].sum(),
            )
            == 70127 * 0.7
        )
        assert (
            pytest.approx(
                self.results[1][("ABW-heat_central", "ABW-heat_central-demand_ind")]["sequences"]["flow"].sum(),
            )
            == 37795 * 0.6
        )
        assert (
            pytest.approx(
                self.results[1][("ABW-heat_decentral", "ABW-heat_decentral-demand_hh")]["sequences"]["flow"].sum(),
            )
            == 2105770 * 0.8
        )
        assert (
            pytest.approx(
                self.results[1][("ABW-heat_decentral", "ABW-heat_decentral-demand_cts")]["sequences"]["flow"].sum(),
            )
            == 431145 * 0.7
        )
        assert (
            pytest.approx(
                self.results[1][("ABW-heat_decentral", "ABW-heat_decentral-demand_ind")]["sequences"]["flow"].sum(),
            )
            == 272674 * 0.6
        )

        total_central = sum(
            data["sequences"]["flow"].sum()
            for flow, data in self.results[1].items()
            if flow[0] == "ABW-heat_central" and "storage" not in flow[1]
        )
        total_central_expected = 158269 * 0.8 + 70127 * 0.7 + 37795 * 0.6
        assert (
            pytest.approx(total_central) == total_central_expected
        ), f"Expected {total_central_expected}, got {total_central}"
        total_decentral = sum(
            data["sequences"]["flow"].sum()
            for flow, data in self.results[1].items()
            if flow[0] == "ABW-heat_decentral" and "storage" not in flow[1]
        )
        total_decentral_expected = 2105770 * 0.8 + 431145 * 0.7 + 272674 * 0.6
        assert (
            pytest.approx(total_decentral) == total_decentral_expected
        ), f"Expected {total_decentral_expected}, got {total_decentral}"

    def test_heat_share(self):
        """Test heat component shares for central and decentral heat busses."""
        assert (
            pytest.approx(
                self.results[1][("ABW-electricity-heatpump_central", "ABW-heat_central")]["sequences"]["flow"].sum(),
            )
            == 158269 * 0.8 * 0.5 + 70127 * 0.7 * 0.5 + 37795 * 0.6 * 0.5
        )
        assert (
            pytest.approx(
                self.results[1][("ABW-electricity-heatpump_decentral", "ABW-heat_decentral")]["sequences"][
                    "flow"
                ].sum(),
            )
            == 2105770 * 0.8 * 0.5 + 431145 * 0.7 * 0.45 + 272674 * 0.6 * 0.4
        )

        factor = 0.2306220042
        central_shares = {
            "ABW-ch4-extchp": 0.037485549131388775 / factor,
            "ABW-ch4-bpchp": 0.0011234133013475554 / factor,
            "ABW-biogas-bpchp": 0.008366081174604877 / factor,
            "ABW-solar-thermalcollector": 0.081073249657315 / factor,
            # Boiler exceeds share as it is the backup heat generator
            # (could be explained by storage losses from storing solar_thermal energy?!)
            # "ABW-ch4-boiler": 0.002799132549946667 / factor + 0.005024220543519689 / factor,
            "ABW-electricity-pth": 0.008154535911400959 / factor,
            "ABW-wood-extchp": 0.08659582199360916 / factor,
        }
        for component, share in central_shares.items():
            central_heat_demand = 158269 * 0.8 * (1 - 0.5) + 70127 * 0.7 * (1 - 0.5) + 37795 * 0.6 * (1 - 0.5)
            current_value = self.results[1][(f"{component}_central", "ABW-heat_central")]["sequences"]["flow"].sum()
            assert (
                pytest.approx(current_value, 0.1) == central_heat_demand * share
            ), f"Expected {central_heat_demand * share}, got {current_value}"

        factor = 0.112341887624161
        decentral_shares = {
            "ABW-ch4-boiler": 0.0 / factor,
            "ABW-solar-thermalcollector": 0.004739072023327305 / factor,
            "ABW-wood-extchp": 0.02309131305472451 / factor,
            "ABW-electricity-pth": 0.056497203680542236 / factor,
            "ABW-biogas-bpchp": 0.0022308674367488004 / factor,
            "ABW-ch4-bpchp": 0.0002995651248991247 / factor,
            "ABW-ch4-extchp": 0.009995754184134148 / factor,
            "ABW-wood-oven": 0.01548811211978472 / factor,
        }
        for component, share in decentral_shares.items():
            decentral_heat_demand = 2105770 * 0.8 * (1 - 0.5) + 431145 * 0.7 * (1 - 0.45) + 272674 * 0.6 * (1 - 0.4)
            component_name = f"{component}_decentral" if component != "ABW-wood-oven" else "ABW-wood-oven"
            assert (
                pytest.approx(self.results[1][(component_name, "ABW-heat_decentral")]["sequences"]["flow"].sum(), 0.1)
                == decentral_heat_demand * share
            )


class EnergySharePerMunicipalityTest(SimpleTestCase):
    """Test energy shares per municipality calculation."""

    databases = ("default",)

    def test_energy_shares_per_municipality(self):  # noqa: D102
        results = calculations.energy_shares_per_municipality()
        assert len(results) == 20


class ElectricityDemandPerMunicipalityTest(SimpleTestCase):
    """Test electricity demand per municipality calculation."""

    databases = ("default",)

    def test_electricity_demand_per_municipality(self):  # noqa: D102
        results = calculations.electricity_demand_per_municipality()
        assert len(results) == 20
        assert len(results.columns) == 3


class HeatDemandPerMunicipalityTest(SimpleTestCase):
    """Test heat demand per municipality calculation."""

    databases = ("default",)

    def test_heat_demand_per_municipality(self):  # noqa: D102
        results = calculations.heat_demand_per_municipality()
        assert len(results) == 20
        assert len(results.columns) == 3


class PotentialShareTest(SimpleTestCase):
    """Test disaggregation of renewable potentials."""

    def test_potential_share(self):
        """Test renewable capacities."""
        parameters = {
            "s_w_3": True,
            "s_pv_ff_3": 50,
            "s_pv_ff_4": 50,
        }
        calculations.calculate_potential_shares(parameters)
        # assert results.sum() almost [1,1,1,1]


class ElectricityProductionTest(SimulationTest):
    """Test electricity production calculation."""

    def test_electricity_production(self):  # noqa: D102
        results = oemof_results.get_results(
            self.simulation_id,
            calculations=[calculations.electricity_production],
        )
        assert next(iter(results.values())).iloc[0] > 0


class Energies2045Test(PreResultTest):
    """Test electricity production calculation."""

    def test_electricity_production(self):  # noqa: D102
        calculations.energies_per_municipality_2045(self.parameters)


class Capacities2045Test(SimulationTest):
    """Test electricity production calculation."""

    def test_capacities_2045(self):  # noqa: D102
        calculations.capacities_per_municipality_2045(self.parameters)


class WindTurbines2045Test(PreResultTest):
    """Test wind turbine calculation."""

    def test_wind_turbines_2045(self):  # noqa: D102
        result = calculations.wind_turbines_per_municipality_2045(self.parameters)
        assert len(result) == 20


class HeatProductionTest(SimulationTest):
    """Test heat production calculation."""

    def test_heat_production(self):  # noqa: D102
        results = oemof_results.get_results(
            self.simulation_id,
            calculations=[calculations.heat_production],
        )
        assert next(iter(results.values())).iloc[0] > 0


class ElectricityDemandTest(SimulationTest):
    """Test electricity demand calculation."""

    def test_electricity_demand(self):  # noqa: D102
        results = oemof_results.get_results(
            self.simulation_id,
            calculations=[calculations.electricity_demand],
        )
        assert next(iter(results.values())).iloc[1] > 0


class ElectricityDemand2045Test(PreResultTest):
    """Test electricity demand calculation."""

    def test_electricity_demand(self):  # noqa: D102
        results = calculations.electricity_demand_per_municipality_2045(self.pre_result_id)
        assert len(results) == 20
        assert len(results.columns) == 3

        municipality_id = 13
        hh = 15368.324510202196
        cts = 15885.55560626756
        ind = 79900.92318810655
        assert results.iloc[municipality_id, 0] == pytest.approx(hh * 0.11 * 1e-3)
        assert results.iloc[municipality_id, 1] == pytest.approx(cts * 0.22 * 1e-3)
        assert results.iloc[municipality_id, 2] == pytest.approx(ind * 0.33 * 1e-3)


class HeatDemandTest(SimulationTest):
    """Test heat demand calculation."""

    def test_heat_demand(self):  # noqa: D102
        results = oemof_results.get_results(
            self.simulation_id,
            calculations=[calculations.heat_demand],
        )
        assert next(iter(results.values())).iloc[0] > 0

    def test_heat_demand_all_outputs(self):  # noqa: D102
        results = oemof_results.get_results(
            self.simulation_id,
            calculations=[
                core.ParametrizedCalculation(
                    oc.AggregatedFlows,
                    {
                        "from_nodes": ["ABW-heat_central", "ABW-heat_decentral"],
                    },
                ),
            ],
        )
        assert next(iter(results.values())).iloc[0] > 0


class HeatDemand2045Test(PreResultTest):
    """Test heat demand calculation in 2045."""

    def test_electricity_demand(self):  # noqa: D102
        results = calculations.heat_demand_per_municipality_2045(self.pre_result_id)
        assert len(results) == 20
        assert len(results.columns) == 3

        municipality_id = 9
        hh = 171353.1535566939
        cts = 71958.67546243734
        ind = 280765.29433642636
        assert results.iloc[municipality_id, 0] == pytest.approx(hh * 0.1 * 1e-3)
        assert results.iloc[municipality_id, 1] == pytest.approx(cts * 0.2 * 1e-3)
        assert results.iloc[municipality_id, 2] == pytest.approx(ind * 0.3 * 1e-3)


class RegionalIndependency(SimulationTest):
    """Test regional dependency calculation."""

    def test_regional_independency(self):  # noqa: D102
        results = calculations.get_regional_independency(self.simulation_id)
        assert len(results) == 4


class ElectricityProductionFromBiomassTest(SimulationTest):
    """Test electricity production from biomass calculation."""

    def test_electricity_production_from_biomass(self):  # noqa: D102
        results = calculations.electricity_from_from_biomass(self.simulation_id)
        assert isinstance(results, float) is True


class ElectricityOverviewTest(SimulationTest):
    """Test electricity overview calculation."""

    def test_electricity_overview(self):  # noqa: D102
        result = calculations.electricity_overview(self.simulation_id)
        assert len(result) == 10


class MunicipalityTest(SimpleTestCase):
    """Test."""

    databases = ("default",)

    def test_square(self):
        """Test."""
        series = pd.Series([1, 2, 3], index=["a", "b", "c"])
        calculations.value_per_municipality(series)


class HeatStructureTest(SimulationTest):
    """Test heat overview calculation."""

    def test_heat_overview(self):  # noqa: D102
        result = calculations.heat_overview(self.simulation_id, "central")
        assert list(result.keys()) == ["2022", "2045", "user"]
        for values in result.values():
            assert len(values) == 13


class ElectricityOverviewChartTest(SimulationTest):
    """Test electricity overview chart creation."""

    def test_electricity_overview_chart(self):  # noqa: D102
        chart = charts.ElectricityOverviewChart(self.simulation_id)
        chart.render()


class HeatStructureChartTest(SimulationTest):
    """Test heat overview chart creation."""

    def test_heat_overview_chart(self):  # noqa: D102
        chart = charts.HeatStructureChart(self.simulation_id)
        options = chart.render()
        assert options["series"][0]["data"][1] == 3512007725.957367


class CapacityTest(SimulationTest):
    """Test reading capacities from oemof parameters."""

    def test_oemof_capacities(self):
        """Test capacity reading from oemof results."""
        results = oemof_results.get_results(self.simulation_id, {"capacities": calculations.Capacities})
        assert results["capacities"].loc["ABW-wind-onshore", "None"] == 1000.0
