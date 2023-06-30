
import {statusquoDropdown} from "./elements.js";

const imageResults = document.getElementById("info_tooltip_results");
const simulation_spinner = document.getElementById("simulation_spinner");

const SIMULATION_CHECK_TIME = 5000;

// Setup

// Disable settings form submit
$('#settings').submit(false);

statusquoDropdown.addEventListener("change", function() {
    PubSub.publish(mapEvent.CHOROPLETH_SELECTED, statusquoDropdown.value);
    imageResults.title = statusquoDropdown.options[statusquoDropdown.selectedIndex].title;
});


// Subscriptions
PubSub.subscribe(eventTopics.MENU_RESULTS_SELECTED, simulate);
PubSub.subscribe(eventTopics.MENU_RESULTS_SELECTED, showSimulationSpinner);
PubSub.subscribe(eventTopics.SIMULATION_STARTED, checkResultsPeriodically);
PubSub.subscribe(eventTopics.SIMULATION_FINISHED, showResults);
PubSub.subscribe(eventTopics.SIMULATION_FINISHED, hideSimulationSpinner);
PubSub.subscribe(eventTopics.SIMULATION_FINISHED, checkResultCharts);
// for testing:
PubSub.subscribe(eventTopics.CHART_VIEW_SELECTED, checkResultCharts);


// Subscriber Functions

function simulate(msg) {
    const settings = document.getElementById("settings");
    const formData = new FormData(settings); // jshint ignore:line
    if (store.cold.task_id != null) {
        $.ajax({
            url : "/oemof/terminate",
            type : "POST",
            data : {task_id: store.cold.task_id},
        });
    }
    $.ajax({
        url : "/oemof/simulate",
        type : "POST",
        processData: false,
        contentType: false,
        data : formData,
        success : function(json) {
            store.cold.task_id = json.task_id;
            PubSub.publish(eventTopics.SIMULATION_STARTED);
        },
    });
    return logMessage(msg);
}

function checkResultsPeriodically(msg) {
    setTimeout(checkResults, SIMULATION_CHECK_TIME);
    return logMessage(msg);
}

function checkResults() {
    $.ajax({
        url: "/oemof/simulate",
        type : "GET",
        data : {task_id: store.cold.task_id},
        success: function(json) {
            if (json.simulation_id == null) {
                setTimeout(checkResults, SIMULATION_CHECK_TIME);
            } else {
                store.cold.task_id = null;
                map_store.cold.state.simulation_id = json.simulation_id;
                PubSub.publish(eventTopics.SIMULATION_FINISHED);
            }
        }
    });
}

function showResults(msg, simulation_id) {
    $.ajax({
        url : "/visualization",
        type : "GET",
        data : {
            simulation_ids: simulation_id,
            visualization: "total_system_costs",
        },
        success : function(json) {
            console.log(json);
        },
    });
    return logMessage(msg);
}

function showSimulationSpinner(msg) {
    simulation_spinner.hidden = false;
    return logMessage(msg);
}

function hideSimulationSpinner(msg) {
    simulation_spinner.hidden = true;
    return logMessage(msg);
}

function checkResultCharts(msg) {
    $.ajax({
        url : "/charts",
        type : "GET",
        data : {
            //needs correct simulation_id
            simulation_id: 3,
        },
        success : function(json) {
            detailed_overview_chart.setOption(json.detailed_overview_chart); // jshint ignore:line
        },
    });
    return logMessage(msg);
}
