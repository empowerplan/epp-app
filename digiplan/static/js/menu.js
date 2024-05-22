import { resultsTabs, futureDropdown } from "./elements.js";
import { terminateSimulation } from "./results.js";
import { hidePotentialLayers, showPotentialLayers } from "./sliders.js";

const menuNextBtn = document.getElementById("menu_next_btn");
const menuPreviousBtn = document.getElementById("menu_previous_btn");
const mapTab = document.getElementById("map-view-tab");
const chartTab = document.getElementById("chart-view-tab");
const regionChart = document.getElementById("region_chart_2045");
const panel = document.getElementById("js-panel-container");

const menuTabs = [
  {
    name: "challenges",
    event: eventTopics.MENU_CHALLENGES_SELECTED,
  },
  {
    name: "today",
    event: eventTopics.MENU_STATUS_QUO_SELECTED,
  },
  {
    name: "scenarios",
    event: eventTopics.MENU_SCENARIOS_SELECTED,
  },
  {
    name: "settings",
    event: eventTopics.MENU_SETTINGS_SELECTED,
  },
  {
    name: "results",
    event: eventTopics.MENU_RESULTS_SELECTED,
  },
];

menuNextBtn.addEventListener("click", function () {
  nextMenuTab();
  PubSub.publish(eventTopics.MENU_CHANGED);
});
menuPreviousBtn.addEventListener("click", function () {
  previousMenuTab();
  PubSub.publish(eventTopics.MENU_CHANGED);
});

mapTab.addEventListener("click", function () {
  PubSub.publish(eventTopics.MAP_VIEW_SELECTED);
});

chartTab.addEventListener("click", function () {
  PubSub.publish(eventTopics.CHART_VIEW_SELECTED);
});

PubSub.subscribe(eventTopics.MENU_CHALLENGES_SELECTED, showEmpowerplanContent);
PubSub.subscribe(eventTopics.MENU_CHANGED, togglePanel);
PubSub.subscribe(
  eventTopics.MENU_STATUS_QUO_SELECTED,
  setMapChartViewVisibility,
);
PubSub.subscribe(eventTopics.MENU_STATUS_QUO_SELECTED, hidePotentialLayers);
PubSub.subscribe(eventTopics.MENU_STATUS_QUO_SELECTED, hideEmpowerplanContent);
PubSub.subscribe(eventTopics.MENU_SETTINGS_SELECTED, setMapChartViewVisibility);
PubSub.subscribe(eventTopics.MENU_SETTINGS_SELECTED, deactivateChoropleth);
PubSub.subscribe(eventTopics.MENU_SETTINGS_SELECTED, terminateSimulation);
PubSub.subscribe(eventTopics.MENU_SETTINGS_SELECTED, hideEmpowerplanContent);
PubSub.subscribe(eventTopics.MENU_SETTINGS_SELECTED, showPotentialLayers);
PubSub.subscribe(eventTopics.MENU_RESULTS_SELECTED, setMapChartViewVisibility);
PubSub.subscribe(eventTopics.MENU_RESULTS_SELECTED, hidePotentialLayers);
PubSub.subscribe(eventTopics.MENU_RESULTS_SELECTED, hideEmpowerplanContent);
PubSub.subscribe(eventTopics.MENU_SCENARIOS_SELECTED, showEmpowerplanContent);
PubSub.subscribe(eventTopics.MAP_VIEW_SELECTED, setResultsView);
PubSub.subscribe(eventTopics.CHART_VIEW_SELECTED, setResultsView);

function updateWizardStyles(activeTabIndex) {
  const lines = document.querySelectorAll(".wizard__line");
  const steps = document.querySelectorAll(".wizard__list-item");
  lines.forEach((line) => line.classList.remove("active-line"));
  steps.forEach((step) =>
    step.querySelector(".wizard__list-number").classList.remove("completed"),
  );
  for (let i = 0; i < activeTabIndex - 1; i++) {
    if (lines[i]) {
      lines[i].classList.add("active-line");
    }
    steps[i].querySelector(".wizard__list-number").classList.add("completed");
  }
}

function nextMenuTab() {
  const currentTab = getCurrentMenuTab();
  currentTab.classList.toggle("active");
  const tabIndex = parseInt(currentTab.id.slice(6, 7));
  const currentStep = `step_${tabIndex}_${menuTabs[tabIndex - 1].name}`;
  document.getElementById(currentStep).classList.toggle("active");
  document.getElementById(currentStep).removeAttribute("aria-current", "step");
  const nextPanel = `panel_${tabIndex + 1}_${menuTabs[tabIndex].name}`;
  const nextStep = `step_${tabIndex + 1}_${menuTabs[tabIndex].name}`;
  document.getElementById(nextPanel).classList.toggle("active");
  document.getElementById(nextStep).classList.toggle("active");
  document.getElementById(nextStep).setAttribute("aria-current", "step");
  updateWizardStyles(tabIndex + 1);
  PubSub.publish(menuTabs[tabIndex].event);
  toggleMenuButtons(tabIndex);
}

function previousMenuTab() {
  const currentTab = getCurrentMenuTab();
  currentTab.classList.toggle("active");
  const tabIndex = parseInt(currentTab.id.slice(6, 7));
  const currentStep = `step_${tabIndex}_${menuTabs[tabIndex - 1].name}`;
  document.getElementById(currentStep).classList.toggle("active");
  document.getElementById(currentStep).removeAttribute("aria-current", "step");
  const nextPanel = `panel_${tabIndex - 1}_${menuTabs[tabIndex - 2].name}`;
  const nextStep = `step_${tabIndex - 1}_${menuTabs[tabIndex - 2].name}`;
  document.getElementById(nextPanel).classList.toggle("active");
  document.getElementById(nextStep).classList.toggle("active");
  document.getElementById(nextStep).setAttribute("aria-current", "step");
  updateWizardStyles(tabIndex - 1);
  PubSub.publish(menuTabs[tabIndex - 2].event);
  toggleMenuButtons(tabIndex - 2);
}

function toggleMenuButtons(tabIndex) {
  menuPreviousBtn.hidden = false;
  menuNextBtn.hidden = false;
  menuNextBtn.disabled = false;
  if (tabIndex === 0) {
    menuPreviousBtn.hidden = true;
  }
  if (tabIndex >= menuTabs.length - 1) {
    menuNextBtn.hidden = true;
  }
}

export function getCurrentMenuTab() {
  return document.querySelector(
    "#js-panel-container > .panel__content > .tab-content > .active",
  );
}

function setMapChartViewVisibility(msg) {
  const view_toggle = document.getElementsByClassName("view-toggle")[0];
  view_toggle.hidden = msg !== eventTopics.MENU_RESULTS_SELECTED;
  return logMessage(msg);
}

function setResultsView(msg) {
  if (msg === eventTopics.CHART_VIEW_SELECTED) {
    futureDropdown.parentElement.setAttribute(
      "style",
      "display: none !important",
    );
    regionChart.setAttribute("style", "display: none");
    resultsTabs.parentElement.setAttribute("style", "");
  } else {
    futureDropdown.parentElement.setAttribute("style", "");
    regionChart.setAttribute("style", "");
    resultsTabs.parentElement.setAttribute("style", "display: none !important");
  }
  return logMessage(msg);
}

function togglePanel(msg) {
  panel.hidden = getCurrentMenuTab().id === "panel_1_challenges";
  return logMessage(msg);
}

function showEmpowerplanContent(msg) {
  const contentID =
    msg === "MENU_CHALLENGES_SELECTED" ? "challenges" : "scenarios";
  const content = document.getElementById(contentID);
  content.hidden = false;
  content.style.alignItems = "center";
  content.style.padding = "3rem";
  document.getElementById("mainTabContent").hidden = true;
  return logMessage(msg);
}

function hideEmpowerplanContent(msg) {
  for (const contentID of ["challenges", "scenarios"]) {
    const content = document.getElementById(contentID);
    content.hidden = true;
    content.style.alignItems = null;
    content.style.padding = "0rem";
  }
  if (msg === "MENU_SETTINGS_SELECTED") {
    document.getElementById("map-view-tab").click();
  }
  document.getElementById("mainTabContent").hidden = false;
  map.resize();
  return logMessage(msg);
}
