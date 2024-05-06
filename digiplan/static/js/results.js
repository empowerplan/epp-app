import { statusquoDropdown, futureDropdown } from "./elements.js";

const imageResults = document.getElementById("info_tooltip_results");
const resultSimNote = document.getElementById("result_simnote");

const SIMULATION_CHECK_TIME = 5000;
const PRE_RESULTS = [
  "energy_share_2045",
  "energy_2045",
  "energy_capita_2045",
  "energy_square_2045",
  "capacity_2045",
  "capacity_square_2045",
  "wind_turbines_2045",
  "wind_turbines_square_2045",
  "electricity_demand_2045",
  "electricity_demand_capita_2045",
  "heat_demand_2045",
  "heat_demand_capita_2045",
];

const resultCharts = {};

const SUMMARY_PRE_RESULTS = [
  "summary_electricity_wind_pv",
  "summary_electricity_area",
  "summary_wind_goal",
  "summary_wind_area",
  "summary_wind_demand_share",
  "summary_pv_goal",
  "summary_pv_area",
  "summary_pv_demand_share",
];

// Setup

// Disable settings form submit
$("#settings").submit(false);

statusquoDropdown.addEventListener("change", function () {
  if (statusquoDropdown.value === "") {
    deactivateChoropleth();
    PubSub.publish(eventTopics.CHOROPLETH_DEACTIVATED);
  } else {
    PubSub.publish(mapEvent.CHOROPLETH_SELECTED, statusquoDropdown.value);
  }
  imageResults.title =
    statusquoDropdown.options[statusquoDropdown.selectedIndex].title;
});
futureDropdown.addEventListener("change", function () {
  if (futureDropdown.value === "") {
    deactivateChoropleth();
    PubSub.publish(eventTopics.CHOROPLETH_DEACTIVATED);
  } else {
    PubSub.publish(mapEvent.CHOROPLETH_SELECTED, futureDropdown.value);
  }
  imageResults.title =
    futureDropdown.options[futureDropdown.selectedIndex].title;
});

// Subscriptions
PubSub.subscribe(eventTopics.MENU_RESULTS_SELECTED, showResultSkeletons);
PubSub.subscribe(eventTopics.MENU_RESULTS_SELECTED, storePreResults);
PubSub.subscribe(eventTopics.MENU_RESULTS_SELECTED, showPreResultCharts);
PubSub.subscribe(eventTopics.MENU_RESULTS_SELECTED, showSummaryPreResults);
PubSub.subscribe(eventTopics.MENU_RESULTS_SELECTED, disableResultButtons);
PubSub.subscribe(eventTopics.MENU_RESULTS_SELECTED, hideRegionChart);
PubSub.subscribe(eventTopics.MENU_RESULTS_SELECTED, simulate);
PubSub.subscribe(eventTopics.SIMULATION_STARTED, checkResultsPeriodically);
PubSub.subscribe(eventTopics.SIMULATION_FINISHED, enableFutureResults);
PubSub.subscribe(eventTopics.SIMULATION_FINISHED, showResultCharts);
PubSub.subscribe(mapEvent.CHOROPLETH_SELECTED, showRegionChart);
PubSub.subscribe(eventTopics.CHOROPLETH_DEACTIVATED, hideRegionChart);

// Subscriber Functions

function simulate(msg) {
  const settings = document.getElementById("settings");
  const formData = new FormData(settings); // jshint ignore:line
  if (store.cold.task_id != null) {
    $.ajax({
      url: "/oemof/terminate",
      type: "POST",
      data: { task_id: store.cold.task_id },
      success: function () {
        store.cold.task_id = null;
      },
    });
  }
  $.ajax({
    url: "/oemof/simulate",
    type: "POST",
    processData: false,
    contentType: false,
    data: formData,
    success: function (json) {
      store.cold.task_id = json.task_id;
      PubSub.publish(eventTopics.SIMULATION_STARTED);
    },
  });
  return logMessage(msg);
}

function storePreResults(msg) {
  const settings = document.getElementById("settings");
  const formData = new FormData(settings); // jshint ignore:line
  const userSettings = Object.fromEntries(formData.entries());
  Object.assign(map_store.cold.state, userSettings);
  return logMessage(msg);
}

function checkResultsPeriodically(msg) {
  setTimeout(checkResults, SIMULATION_CHECK_TIME);
  return logMessage(msg);
}

function checkResults() {
  $.ajax({
    url: "/oemof/simulate",
    type: "GET",
    data: { task_id: store.cold.task_id },
    success: function (json) {
      if (json.simulation_id == null) {
        setTimeout(checkResults, SIMULATION_CHECK_TIME);
      } else {
        store.cold.task_id = null;
        map_store.cold.state.simulation_id = json.simulation_id;
        PubSub.publish(eventTopics.SIMULATION_FINISHED);
      }
    },
    error: function () {
      store.cold.task_id = null;
      map_store.cold.state.simulation_id = null;
      PubSub.publish(eventTopics.SIMULATION_FINISHED);
    },
  });
}

function enableFutureResults(msg) {
  resultSimNote.innerText = "";
  const options = futureDropdown.querySelectorAll("option");
  for (const option of options) {
    option.disabled = false;
  }
  return logMessage(msg);
}

function disableResultButtons(msg) {
  resultSimNote.innerText = "Berechnung läuft ...";
  futureDropdown.selectedIndex = 0;
  const options = futureDropdown.querySelectorAll("option");
  for (const option of options) {
    if (!PRE_RESULTS.includes(option.value)) {
      option.disabled = true;
    }
  }
  return logMessage(msg);
}

function showRegionChart(msg, lookup) {
  const region_lookup = `${lookup}_region`;
  let charts = {};
  if (region_lookup.includes("2045")) {
    charts[region_lookup] = "region_chart_2045";
  } else {
    charts[region_lookup] = "region_chart_statusquo";
  }
  showCharts(charts);
  return logMessage(msg);
}

function hideRegionChart(msg) {
  clearChart("region_chart_statusquo");
  clearChart("region_chart_2045");
  return logMessage(msg);
}

function showPreResultCharts(msg) {
  showCharts(preResultCharts);
  return logMessage(msg);
}

function showResultCharts(msg) {
  showCharts(resultCharts);
  return logMessage(msg);
}

function showSummaryPreResults(msg) {
  showSummaryResults(SUMMARY_PRE_RESULTS);
  return logMessage(msg);
}

function showCharts(charts = {}) {
  $.ajax({
    url: "/charts",
    type: "GET",
    data: {
      charts: Object.keys(charts),
      map_state: JSON.stringify(map_store.cold.state),
    },
    success: function (chart_options) {
      for (const chart in charts) {
        createChart(charts[chart], chart_options[chart]);
      }
    },
  });
}

function showSummaryResults(summaries = []) {
  $.ajax({
    url: "/summary_results",
    type: "GET",
    data: {
      summaries: summaries,
      map_state: JSON.stringify(map_store.cold.state),
    },
    success: function (summaryResults) {
      for (const [div_id, summary] of Object.entries(summaryResults)) {
        const summaryDiv = document.getElementById(div_id);
        summaryDiv.innerHTML = summary;
      }
    },
  });
}

function showResultSkeletons(msg) {
  const skeleton_template = document.getElementById("result_skeleton");
  for (const chart_div_id of Object.values(preResultCharts)) {
    const chart_div = document.getElementById(chart_div_id);
    const chart = echarts.getInstanceByDom(chart_div);
    if (chart !== undefined) {
      chart.dispose();
    }
    const skeleton = skeleton_template.content.cloneNode(true);
    chart_div.appendChild(skeleton);
  }
  return logMessage(msg);
}
