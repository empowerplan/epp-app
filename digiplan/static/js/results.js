import { statusquoDropdown, futureDropdown } from "./elements.js";

const imageResults = document.getElementById("info_tooltip_results");

const simulationProgressDiv = document.getElementsByClassName(
  "panel-item__calc-alert",
)[0];
let simulationTimeout;
const SIMULATION_DELAYED = 60 * 1000; // Simulation is delayed if it takes longer than 1min
let timesSimulationChecked;
const SIMULATION_CHECK_TIME = 5000;
const SIMULATION_CHECK_LIMIT = (4 * 60 * 1000) / SIMULATION_CHECK_TIME; // Simulation is canceled after 4min

const SIMULATION_STARTED_DESCRIPTION =
  "Das Aufstellen und Optimieren des Energiesystems ist komplex.<br>Es braucht etwas Zeit, um Dir für Dein Szenario zuverlässige und genaue Ergebnisse zu liefern.";
const SIMULATION_DELAYED_DESCRIPTION =
  "Wir entschuldigen uns für die Verzögerung. Es scheint, dass die Optimierung länger dauert als erwartet. Bitte gedulde Dich noch einen Moment.<br>Derweil kannst Du Dir schon einige Vorergebnisse ansehen.";
const SIMULATION_INFEASIBLE_DESCRIPTION =
  "Das Modell konnte leider keine gültige Lösung finden. Das sollte eigentlich nicht passieren - eventuell lassen bestimmte Einstellungen der Komponenten keine Lösung zu?<br>Du kannst es gerne noch einmal mit anderen Einstellungen versuchen.";
const SIMULATION_ERROR_DESCRIPTION =
  "Wir entschuldigen uns für den Fehler. Es kann sein, dass unser Server gerade nicht verfügbar oder überlastet ist.<br>Bitte versuche es zu einem späteren Zeitpunkt noch einmal.";
const SIMULATION_FINISHED_DESCRIPTION =
  "Die Optimierung wurde erfolgreich abgeschlossen.<br>Du kannst Dir nun alle Ergebnisse anschauen.";

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
PubSub.subscribe(eventTopics.SIMULATION_STARTED, startSimulationProgress);
PubSub.subscribe(eventTopics.SIMULATION_STARTED, checkResultsPeriodically);
PubSub.subscribe(eventTopics.SIMULATION_FINISHED, enableFutureResults);
PubSub.subscribe(eventTopics.SIMULATION_FINISHED, showResultCharts);
PubSub.subscribe(eventTopics.SIMULATION_FINISHED, finishSimulationProgress);
PubSub.subscribe(eventTopics.SIMULATION_ERROR, errorAtSimulationProgress);
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

export function terminateSimulation(msg) {
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
  timesSimulationChecked = 0;
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
        if (timesSimulationChecked === SIMULATION_CHECK_LIMIT) {
          store.cold.task_id = null;
          map_store.cold.state.simulation_id = null;
          PubSub.publish(eventTopics.SIMULATION_ABORTED, terminateSimulation);
          const error_msg = { status: 500 };
          PubSub.publish(eventTopics.SIMULATION_ERROR, error_msg);
        } else {
          timesSimulationChecked += 1;
          setTimeout(checkResults, SIMULATION_CHECK_TIME);
        }
      } else {
        store.cold.task_id = null;
        map_store.cold.state.simulation_id = json.simulation_id;
        PubSub.publish(eventTopics.SIMULATION_FINISHED);
      }
    },
    error: function (error_msg) {
      store.cold.task_id = null;
      map_store.cold.state.simulation_id = null;
      PubSub.publish(eventTopics.SIMULATION_ERROR, error_msg);
    },
  });
}

function enableFutureResults(msg) {
  const options = futureDropdown.querySelectorAll("option");
  for (const option of options) {
    option.disabled = false;
  }
  return logMessage(msg);
}

function disableResultButtons(msg) {
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
        // Remove skeleton placeholder if it exists
        const skeleton = document
          .getElementById(charts[chart])
          .querySelector(".skeleton");
        if (skeleton !== null) {
          skeleton.remove();
        }
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

function startSimulationProgress(msg) {
  clearTimeout(simulationTimeout);
  setSimulationProgress(
    25,
    "Detailergebnisse werden berechnet",
    SIMULATION_STARTED_DESCRIPTION,
    "start",
  );
  simulationTimeout = setTimeout(function () {
    setSimulationProgress(
      25,
      "Die Simulation dauert länger als gewöhnlich",
      SIMULATION_DELAYED_DESCRIPTION,
      "delay",
    );
  }, SIMULATION_DELAYED);
  return logMessage(msg);
}

function errorAtSimulationProgress(msg, error_msg) {
  clearTimeout(simulationTimeout);
  if (error_msg.status === 400) {
    setSimulationProgress(
      100,
      "Die Simulation konnte keine Lösung finden.",
      SIMULATION_INFEASIBLE_DESCRIPTION,
      "error",
    );
  } else {
    setSimulationProgress(
      100,
      "Fehler bei der Berechnung",
      SIMULATION_ERROR_DESCRIPTION,
      "error",
    );
  }
  return logMessage(msg);
}

function finishSimulationProgress(msg) {
  setSimulationProgress(
    100,
    "Simulation ist fertig",
    SIMULATION_FINISHED_DESCRIPTION,
    "finish",
  );
  clearTimeout(simulationTimeout);
  simulationTimeout = setTimeout(function () {
    simulationProgressDiv.hidden = true;
  }, 2000);
  return logMessage(msg);
}

function setSimulationProgress(value, title, description, status) {
  const progressMessage = document.getElementsByClassName(
    "panel-item__calc-alert-message",
  )[0];
  const progressBar = document.getElementsByClassName("progress-bar")[0];
  const progressStatus = document.getElementsByClassName("progress")[0];
  const progressTooltip = document.querySelector(
    ".panel-item__calc-alert-explanation button",
  );
  simulationProgressDiv.hidden = false;
  progressBar.setAttribute("aria-valuenow", value);
  progressBar.style.width = `${value}%`;
  progressMessage.innerHTML = title;
  progressTooltip.setAttribute("title", description);
  new bootstrap.Tooltip(progressTooltip, { html: true });
  if (status === "error") {
    progressStatus.classList.add("progress--error");
  } else {
    progressStatus.classList.remove("progress--error");
  }
}
