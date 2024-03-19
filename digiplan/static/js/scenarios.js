import { getCurrentMenuTab } from "./menu.js";

let currentScenario = null;
//const scenarioPanels = ["panelCard1", "panelCard2", "panelCard3", "panelCard4"];
const scenarioPanels = ["panelCard1", "panelCard2", "panelCard3"];

for (const scenarioPanel of scenarioPanels) {
  document
    .getElementById(scenarioPanel)
    .addEventListener("click", scenarioCardClicked);
}

Array.from(document.getElementsByClassName("scenarios__btn")).forEach(
  function (e) {
    e.addEventListener("click", function () {
      PubSub.publish(eventTopics.SCENARIO_SELECTED);
    });
  },
);

PubSub.subscribe(eventTopics.MENU_CHANGED, checkIfScenarioIsSelected);
PubSub.subscribe(eventTopics.SCENARIO_SELECTED, selectScenario);
PubSub.subscribe(eventTopics.SCENARIO_SELECTED, checkIfScenarioIsSelected);

function checkIfScenarioIsSelected(msg) {
  const currentTab = getCurrentMenuTab();
  const tabIndex = parseInt(currentTab.id.slice(6, 7));
  // if (tabIndex === 3) {
  //   document.getElementById("menu_next_btn").hidden = currentScenario === null;
  // }
  return logMessage(msg);
}

function selectScenario(msg) {
  // Get currently selected scenario
  const selectedPanel = document.getElementsByClassName(
    "panel-card--selected",
  )[0].id;
  // Set current scenario and enable next button
  currentScenario = parseInt(selectedPanel.slice(-1));

  // Style all scenario buttons according to current selection
  Array.from(document.getElementsByClassName("scenarios")).forEach(
    function (e) {
      // Get scenario id
      const scenario = parseInt(e.id.slice(-1));
      const scenario_btn = e.getElementsByClassName("scenarios__btn")[0];
      if (scenario_btn === undefined) {
        return;
      }
      if (currentScenario === scenario) {
        // Show underlying scenario button as selected
        scenario_btn.classList.remove("scenarios__btn--active");
        scenario_btn.classList.remove("scenarios__btn--active-outline");
        scenario_btn.classList.add("scenarios__btn--selected");
      } else {
        // Show underlying scenario button as active-outline
        scenario_btn.classList.remove("scenarios__btn--active");
        scenario_btn.classList.remove("scenarios__btn--selected");
        scenario_btn.classList.add("scenarios__btn--active-outline");
      }
    },
  );
  return logMessage(msg);
}

function scenarioCardClicked(event) {
  const scenarioCardNumber = parseInt(event.currentTarget.id.slice(-1));
  selectScenarioCard(scenarioCardNumber);
}

function selectScenarioCard(scenarioCardNumber) {
  currentScenario = scenarioCardNumber;

  const starSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#2348C3" class="bi bi-star-fill" viewBox="0 0 16 16">
  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
</svg>`;
  const leftArrowSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="#2348C3" class="bi bi-arrow-left-circle" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-4.5-.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z"/>
</svg>`;
  const rightArrowSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="#2348C3" class="bi bi-arrow-right-circle-fill" viewBox="0 0 16 16">
  <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5z"/>
</svg>`;

  for (let i = 1; i <= 4; i++) {
    const card = document.getElementById("panelCard" + i);
    const selectedScenario = document.getElementById("selectedScenario" + i);
    const arrowIcon = card.querySelector(".arrow-icon");
    const scenarioStar = card.querySelector(".scenario-star");

    if (i === scenarioCardNumber) {
      // Selected scenario card
      selectedScenario.style.display = "block";
      scenarioStar.innerHTML = starSVG;
      card.classList.add("panel-card--selected");
      arrowIcon.innerHTML = leftArrowSVG;
    } else {
      // Unselected scenario cards
      selectedScenario.style.display = "none";
      scenarioStar.innerHTML = "";
      card.classList.remove("panel-card--selected");
      arrowIcon.innerHTML = rightArrowSVG;
    }
  }
}
