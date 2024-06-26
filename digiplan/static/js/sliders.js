// Variables
const SETTINGS_PARAMETERS = JSON.parse(
  document.getElementById("settings_parameters").textContent,
);
const panelContainer = document.getElementById("js-panel-container");
export const panelSliders = document.querySelectorAll(
  ".js-slider.js-slider-panel",
);
const powerPanelSliders = document.querySelectorAll(
  ".js-slider.js-slider-panel.js-power-mix",
);
const sliderMoreLabels = document.querySelectorAll(
  ".c-slider__label--more > .button",
);
export const detailSliders = document.querySelectorAll(
  ".js-slider.js-slider-detail-panel",
);
const powerMixInfoBanner = document.getElementById("js-power-mix");
const windTabs = document.querySelectorAll(
  "#windTab .sidepanel-tabs__nav-link",
);

const powerIcons = {
  s_h_1: `<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" height="16" width="16" viewBox="0 0 16 16"><path d="m5.22.89l-.18-.44-.45.16c-.13.05-3.13,1.17-4.11,3.39-.61,1.38.02,3,1.41,3.61.35.16.73.23,1.1.23.34,0,.67-.06.99-.19.68-.27,1.22-.78,1.51-1.45.98-2.22-.23-5.2-.28-5.32Zm-.63,4.92c-.39.88-1.42,1.28-2.3.9s-1.28-1.42-.9-2.3c.6-1.37,2.26-2.28,3.08-2.66.27.86.72,2.7.12,4.07Z"/><path d="m14.44,3.17l-.19-.44-.45.17c-.24.09-5.83,2.25-7.59,6.38-.51,1.19-.52,2.5-.04,3.69s1.4,2.13,2.59,2.64c.62.26,1.26.39,1.89.39,1.88,0,3.67-1.1,4.45-2.93,1.76-4.13-.55-9.66-.65-9.9Zm-.26,9.51c-.4.94-1.15,1.67-2.1,2.05-.95.38-1.99.37-2.93-.03s-1.67-1.15-2.05-2.1-.37-1.99.03-2.93c1.32-3.09,5.24-5.06,6.58-5.65.5,1.38,1.8,5.56.48,8.66Z"/></svg>`,
  s_pv_ff_1: `<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" height="16" width="16" viewBox="0 0 16 16"><path d="m12.07,15v-2.95h3.23L11.94.86h-7.88L.71,12.05h3.22v2.95H.35v1h15.29v-1h-3.58ZM8.51,1.88h2.67l.61,2.03h-3.28V1.88Zm0,3.05h3.59l.61,2.03h-4.2v-2.03Zm0,3.05h4.5l.92,3.05h-5.42v-3.05ZM4.82,1.88h2.67v2.03h-3.28l.61-2.03Zm-.92,3.05h3.59v2.03H3.29l.61-2.03Zm-1.83,6.1l.92-3.05h4.5v3.05H2.07Zm2.88,1.02h6.1v2.95h-6.1v-2.95Z"/></svg>`,
  s_pv_d_1: `<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" height="16" width="16" viewBox="0 0 16 16"><path d="m15.96,16l-3.91-2.36h.02v-2.92h3.23L11.94,0h-7.88L.71,10.71h3.22v2.92h.02L.04,16h15.92Zm-12.34-1l4.38-2.65,4.38,2.65H3.62ZM8.51.97h2.67l.61,1.95h-3.28V.97Zm0,2.92h3.59l.61,1.95h-4.2v-1.95Zm0,2.92h4.5l.92,2.92h-5.42v-2.92ZM4.82.97h2.67v1.95h-3.28l.61-1.95Zm-.92,2.92h3.59v1.95H3.29l.61-1.95Zm-1.83,5.85l.92-2.92h4.5v2.92H2.07Zm2.88.97h6.1v2.32l-3.05-1.85-3.05,1.85v-2.32Z"/></svg>`,
  s_w_1: `<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" height="16" width="16" viewBox="0 0 16 16"><path class="cls-1" d="m7.5,0v4.05c-.85.23-1.48,1.01-1.48,1.93,0,.16.02.31.05.46l-3.21,1.85.5.87,3.17-1.83c.25.28.58.48.96.58v7.09H1.49v1h6.01s1,0,1,0h0s6.01,0,6.01,0v-1h-6.01v-7.09c.39-.1.74-.33,1-.63l3.26,1.88.5-.87-3.32-1.91s0,0,0,0c.03-.13.04-.26.04-.4,0-.92-.63-1.71-1.48-1.93V0h-1,0Zm.5,4.98c.55,0,.98.44.98,1s-.44,1-.98,1-.98-.44-.98-1,.44-1,.98-1Z"/></svg>`,
};

const potentialPVLayers = [
  "potentialarea_pv_ground_soil_quality_low",
  "potentialarea_pv_ground_soil_quality_medium",
  "potentialarea_pv_ground_permanent_crops",
];
const potentialPVRoofLayers = ["potentialarea_pv_roof"];
const potentialWindLayers = [
  "potentialarea_wind_stp_2018_eg",
  "potentialarea_wind_stp_2024_vr",
  "potentialarea_wind_stp_2027",
];

const pvMapControl = document.getElementsByClassName("map__layers-pv")[0];

const sidepanelCloseButtons =
  document.getElementsByClassName("sidepanel__close");

// Setup

$(".js-slider.js-slider-panel.js-power-mix").ionRangeSlider({
  onFinish: function (data) {
    PubSub.publish(eventTopics.POWER_PANEL_SLIDER_CHANGE, data);
  },
});

$(".js-slider.js-slider-panel").ionRangeSlider({
  onFinish: function (data) {
    PubSub.publish(eventTopics.PANEL_SLIDER_CHANGE, data);
  },
});

$(".js-slider.js-slider-detail-panel").ionRangeSlider({
  onFinish: function (data) {
    PubSub.publish(eventTopics.DETAIL_PANEL_SLIDER_CHANGE, data);
  },
});

$(".js-slider").ionRangeSlider();

Array.from(sliderMoreLabels).forEach((moreLabel) => {
  moreLabel.addEventListener("click", () => {
    const sliderLabel = moreLabel.parentNode.parentNode.parentNode;
    PubSub.publish(eventTopics.MORE_LABEL_CLICK, sliderLabel);
  });
});

Array.from(windTabs).forEach((windTab) => {
  windTab.addEventListener("click", () => {
    calculate_max_wind();
    PubSub.publish(eventTopics.WIND_CONTROL_ACTIVATED);
  });
});

panelContainer.addEventListener("scroll", (e) => {
  document.documentElement.style.setProperty(
    "--scrollPosition",
    panelContainer.scrollTop + "px",
  );
});

Array.from(sidepanelCloseButtons).forEach((closeBtn) => {
  closeBtn.addEventListener("click", (event) => {
    closeSidepanel(event.target);
  });
});

// Subscriptions
PubSub.subscribe(eventTopics.STATES_INITIALIZED, updateSliderMarks);
//PubSub.subscribe(eventTopics.STATES_INITIALIZED, adaptSlidersScenario);
subscribeToEvents(
  [eventTopics.STATES_INITIALIZED, eventTopics.POWER_PANEL_SLIDER_CHANGE],
  createPercentagesOfPowerSources,
);
PubSub.subscribe(
  eventTopics.PANEL_SLIDER_CHANGE,
  showActivePanelSliderOnPanelSliderChange,
);
PubSub.subscribe(eventTopics.PANEL_SLIDER_CHANGE, hidePotentialLayers);
PubSub.subscribe(eventTopics.PANEL_SLIDER_CHANGE, adaptDetailSliders);
PubSub.subscribe(eventTopics.DETAIL_PANEL_SLIDER_CHANGE, adaptMainSliders);
PubSub.subscribe(eventTopics.DETAIL_PANEL_SLIDER_CHANGE, adaptDetailKeyResults);
PubSub.subscribe(
  eventTopics.MORE_LABEL_CLICK,
  showOrHideSidepanelsOnMoreLabelClick,
);
PubSub.subscribe(
  eventTopics.MORE_LABEL_CLICK,
  showOrHidePotentialLayersOnMoreLabelClick,
);
PubSub.subscribe(eventTopics.PV_CONTROL_ACTIVATED, showPVLayers);
PubSub.subscribe(eventTopics.PV_CONTROL_ACTIVATED, highlightPVMapControls);
PubSub.subscribe(eventTopics.PV_ROOF_CONTROL_ACTIVATED, showPVRoofLayers);
PubSub.subscribe(eventTopics.WIND_CONTROL_ACTIVATED, updateWindSelection);
PubSub.subscribe(eventTopics.WIND_CONTROL_ACTIVATED, showWindLayers);

// Subscriber Functions
/**
 * Adapt detail sliders depending on related main sliders
 * @param {string} msg Publisher message
 * @param {object} data Data from changed ionrangeslider
 */
function adaptDetailSliders(msg, data) {
  if (data.input[0].id === "id_s_v_1") {
    $(`#id_s_v_3`).data("ionRangeSlider").update({ from: data.from });
    $(`#id_s_v_4`).data("ionRangeSlider").update({ from: data.from });
    $(`#id_s_v_5`).data("ionRangeSlider").update({ from: data.from });
  }
  if (data.input[0].id === "id_w_d_wp_1") {
    $(`#id_w_d_wp_3`).data("ionRangeSlider").update({ from: data.from });
    $(`#id_w_d_wp_4`).data("ionRangeSlider").update({ from: data.from });
    $(`#id_w_d_wp_5`).data("ionRangeSlider").update({ from: data.from });
  }
  if (data.input[0].id === "id_w_v_1") {
    $(`#id_w_v_3`).data("ionRangeSlider").update({ from: data.from });
    $(`#id_w_v_4`).data("ionRangeSlider").update({ from: data.from });
    $(`#id_w_v_5`).data("ionRangeSlider").update({ from: data.from });
  }
  return logMessage(msg);
}

/**
 * Adapt main slider depending on related detail sliders
 * @param {string} msg Publisher message
 * @param {object} data Data from changed ionrangeslider
 */
export function adaptMainSliders(msg, data) {
  const slider_id = data.input[0].id;
  if (slider_id === "id_s_w_6" || slider_id === "id_s_w_7") {
    calculate_max_wind();
  }
  if (slider_id === "id_s_pv_d_3") {
    calculate_max_pv_d();
  }
  if (
    slider_id === "id_s_pv_ff_3" ||
    slider_id === "id_s_pv_ff_4" ||
    slider_id === "id_s_pv_ff_5"
  ) {
    calculate_max_pv_ff();
  }
  if (
    slider_id === "id_s_v_3" ||
    slider_id === "id_s_v_4" ||
    slider_id === "id_s_v_5"
  ) {
    let factor_hh = $("#id_s_v_3").data("ionRangeSlider").result.from;
    let factor_ind = $("#id_s_v_5").data("ionRangeSlider").result.from;
    let factor_cts = $("#id_s_v_4").data("ionRangeSlider").result.from;
    let demand_hh = store.cold.slider_per_sector.s_v_1.hh;
    let demand_ind = store.cold.slider_per_sector.s_v_1.ind;
    let demand_cts = store.cold.slider_per_sector.s_v_1.cts;
    let new_val =
      (factor_hh * demand_hh +
        factor_ind * demand_ind +
        factor_cts * demand_cts) /
      (demand_hh + demand_ind + demand_cts);
    $(`#id_s_v_1`).data("ionRangeSlider").update({ from: new_val });
  }
  if (
    slider_id === "id_w_d_wp_3" ||
    slider_id === "id_w_d_wp_4" ||
    slider_id === "id_w_d_wp_5"
  ) {
    let factor_hh = $("#id_w_d_wp_3").data("ionRangeSlider").result.from;
    let factor_ind = $("#id_w_d_wp_4").data("ionRangeSlider").result.from;
    let factor_cts = $("#id_w_d_wp_5").data("ionRangeSlider").result.from;
    let demand_hh = store.cold.slider_per_sector.w_d_wp_1.hh;
    let demand_ind = store.cold.slider_per_sector.w_d_wp_1.ind;
    let demand_cts = store.cold.slider_per_sector.w_d_wp_1.cts;
    let new_val =
      (factor_hh * demand_hh +
        factor_ind * demand_ind +
        factor_cts * demand_cts) /
      (demand_hh + demand_ind + demand_cts);
    $(`#id_w_d_wp_1`).data("ionRangeSlider").update({ from: new_val });
  }
  if (
    slider_id === "id_w_v_3" ||
    slider_id === "id_w_v_4" ||
    slider_id === "id_w_v_5"
  ) {
    let factor_hh = $("#id_w_v_3").data("ionRangeSlider").result.from;
    let factor_ind = $("#id_w_v_4").data("ionRangeSlider").result.from;
    let factor_cts = $("#id_w_v_5").data("ionRangeSlider").result.from;
    let demand_hh = store.cold.slider_per_sector.w_d_wp_1.hh;
    let demand_ind = store.cold.slider_per_sector.w_d_wp_1.ind;
    let demand_cts = store.cold.slider_per_sector.w_d_wp_1.cts;
    let new_val =
      (factor_hh * demand_hh +
        factor_ind * demand_ind +
        factor_cts * demand_cts) /
      (demand_hh + demand_ind + demand_cts);
    $(`#id_w_v_1`).data("ionRangeSlider").update({ from: new_val });
  }
  return logMessage(msg);
}

function closeSidepanel(panelCloseBtn) {
  panelCloseBtn.parentNode.parentNode.previousElementSibling.classList.remove(
    "active",
    "active-sidepanel",
  );
  hidePotentialLayers();
}

function showOrHidePotentialLayersOnMoreLabelClick(msg, moreLabel) {
  const classes = ["active", "active-sidepanel"];
  const show = moreLabel.classList.contains(classes[0]);
  hidePotentialLayers();
  if (show) {
    const sliderLabel = moreLabel.getElementsByTagName("input")[0];
    if (sliderLabel.id === "id_s_pv_ff_1") {
      PubSub.publish(eventTopics.PV_CONTROL_ACTIVATED);
    }
    if (sliderLabel.id === "id_s_pv_d_1") {
      PubSub.publish(eventTopics.PV_ROOF_CONTROL_ACTIVATED);
    }
    if (sliderLabel.id === "id_s_w_1") {
      PubSub.publish(eventTopics.WIND_CONTROL_ACTIVATED);
    }
  }
  return logMessage(msg);
}

function showOrHideSidepanelsOnMoreLabelClick(msg, moreLabel) {
  const classes = ["active", "active-sidepanel"];
  const hide =
    moreLabel.classList.contains(classes[0]) &&
    moreLabel.classList.contains(classes[1]);
  if (hide) {
    moreLabel.classList.remove(...classes);
  } else {
    Array.from(panelSliders).forEach((item) =>
      item.parentNode.classList.remove(...classes),
    );
    moreLabel.classList.add(...classes);
  }
  return logMessage(msg);
}

function showActivePanelSliderOnPanelSliderChange(msg, data) {
  const changedSlider = data.input[0];
  const changedSliderLabel = changedSlider.parentNode;

  const sliderForm = changedSliderLabel.parentNode.parentNode.parentNode;
  // Check if any sidepanel is open, by checking if any slider has an active element
  if (sliderForm.getElementsByClassName("c-slider active").length === 0) {
    return logMessage(msg);
  }
  const isActivePanel = changedSliderLabel.classList.contains("active");

  if (!isActivePanel) {
    Array.from(panelSliders).forEach((item) => {
      const itemPanel = item.parentNode;
      if (itemPanel !== changedSliderLabel) {
        itemPanel.classList.remove("active", "active-sidepanel");
      }
    });

    changedSliderLabel.classList.add("active", "active-sidepanel");
  }
  return logMessage(msg);
}

function createPercentagesOfPowerSources(msg) {
  let ids = [];
  let values = [];
  Array.from(powerPanelSliders).forEach(function (item) {
    ids.push(item.id);
    values.push($("#" + item.id).data().from);
  });
  const total = getTotalOfValues(values);
  const weights = getWeightsInPercent(values, total);
  const colors = getColorsByIds(ids);
  const icons = getIconsByIds(ids);
  updatePowerMix(weights, colors, icons);
  return logMessage(msg);
}

/* when the other forms get Status Quo marks, there needs to be an iteration over the forms! (line 117)*/
export function updateSliderMarks(msg) {
  for (let [slider_name, slider_marks] of Object.entries(
    store.cold.slider_marks,
  )) {
    let slider = $(`#id_${slider_name}`).data("ionRangeSlider");
    slider.update({
      // jshint ignore:start
      onUpdate: function (data) {
        addMarks(data, slider_marks);
      },
      // jshint ignore:end
    });
  }
  return logMessage(msg);
}

function showPVLayers(msg) {
  hidePotentialLayers();
  for (let layer of potentialPVLayers) {
    if (store.cold.distill) {
      layer = `${layer}_distilled`;
    }
    turn_on_layer(layer);
  }
  return logMessage(msg);
}

function showPVRoofLayers(msg) {
  hidePotentialLayers();
  for (let layer of potentialPVRoofLayers) {
    if (store.cold.distill) {
      layer = `${layer}_distilled`;
    }
    turn_on_layer(layer);
  }
  return logMessage(msg);
}

function calculate_max_wind() {
  const currentWindTab = document
    .getElementById("windTab")
    .getElementsByClassName("active")[0].id;
  let newWindMax;
  if (currentWindTab === "windPastTab") {
    newWindMax = Math.round(store.cold.potentials.wind_2018);
  } else if (currentWindTab === "windPresentTab") {
    const slider_value =
      $("#id_s_w_6").data("ionRangeSlider").result.from /
      $("#id_s_w_6").data("ionRangeSlider").result.max;
    newWindMax = Math.round(store.cold.potentials.wind_2024) * slider_value;
  } else if (currentWindTab === "windFutureTab") {
    const slider_value =
      $("#id_s_w_7").data("ionRangeSlider").result.from / 100;
    newWindMax = Math.round(store.cold.potentials.wind_2027) * slider_value;
  }
  $(`#id_s_w_1`)
    .data("ionRangeSlider")
    .update({ max: Math.round(newWindMax) });
}

function calculate_max_pv_ff() {
  const slider_soil_quality_low =
    $("#id_s_pv_ff_3").data("ionRangeSlider").result.from / 100;
  const slider_soil_quality_medium =
    $("#id_s_pv_ff_4").data("ionRangeSlider").result.from / 100;
  const slider_permanent_crops =
    $("#id_s_pv_ff_5").data("ionRangeSlider").result.from / 100;
  const newPVMax =
    slider_soil_quality_low *
      Math.round(store.cold.potentials.pv_soil_quality_low) +
    slider_soil_quality_medium *
      Math.round(store.cold.potentials.pv_soil_quality_medium) +
    slider_permanent_crops *
      Math.round(store.cold.potentials.pv_permanent_crops);
  $(`#id_s_pv_ff_1`)
    .data("ionRangeSlider")
    .update({ max: Math.round(newPVMax) });
}

function calculate_max_pv_d() {
  const slider_value =
    $("#id_s_pv_d_3").data("ionRangeSlider").result.from / 100;
  const newPVMax = Math.round(slider_value * store.cold.potentials.pv_roof);
  $(`#id_s_pv_d_1`).data("ionRangeSlider").update({ max: newPVMax });
}

function showWindLayers(msg) {
  hidePotentialLayers();
  const currentWindTab = document
    .getElementById("windTab")
    .getElementsByClassName("active")[0].id;
  let layers = [];
  if (currentWindTab === "windPastTab") {
    layers.push("potentialarea_wind_stp_2018_eg");
  } else if (currentWindTab === "windPresentTab") {
    layers.push("potentialarea_wind_stp_2024_vr");
  } else if (currentWindTab === "windFutureTab") {
    layers.push("potentialarea_wind_stp_2024_vr");
    layers.push("potentialarea_wind_stp_2027");
  } else {
    throw Error(`Unknown wind tab '${currentWindTab}' found.`);
  }
  for (let layer of layers) {
    if (store.cold.distill) {
      layer = `${layer}_distilled`;
    }
    turn_on_layer(layer);
  }
  return logMessage(msg);
}

function updateWindSelection(msg) {
  const windInput = document.getElementById("id_wind_year");
  const currentWindTab = document
    .getElementById("windTab")
    .getElementsByClassName("active")[0].id;
  if (currentWindTab === "windPastTab") {
    windInput.value = "wind_2018";
  } else if (currentWindTab === "windPresentTab") {
    windInput.value = "wind_2024";
  } else if (currentWindTab === "windFutureTab") {
    windInput.value = "wind_2027";
  } else {
    throw Error(`Unknown wind tab '${currentWindTab}' found.`);
  }
  return logMessage(msg);
}

export function showPotentialLayers(msg) {
  const activeSidepanels = document.getElementsByClassName("active-sidepanel");
  if (activeSidepanels.length > 0) {
    const activeSlider =
      document.getElementsByClassName("active-sidepanel")[0].classList[1];
    if (activeSlider === "s_w_1") {
      showWindLayers(msg);
    }
    if (activeSlider === "s_pv_ff_1") {
      showPVLayers(msg);
    }
    if (activeSlider === "s_pv_d_1") {
      showPVRoofLayers(msg);
    }
  }
  return logMessage(msg);
}

export function hidePotentialLayers(msg) {
  for (let layer of potentialPVLayers
    .concat(potentialPVRoofLayers)
    .concat(potentialWindLayers)) {
    if (store.cold.distill) {
      layer = `${layer}_distilled`;
    }
    turn_off_layer(layer);
  }
  return logMessage(msg);
}

function highlightPVMapControls(msg) {
  pvMapControl.scrollIntoView();
  pvMapControl.classList.add("blinking");
  setTimeout(function () {
    pvMapControl.classList.remove("blinking");
  }, 2000);
  return logMessage(msg);
}

function adaptDetailKeyResults(msg, data) {
  const slider_id = data.input[0].id;
  let wind_year;
  let target;
  let url_data = {};

  if (slider_id === "id_s_w_6") {
    wind_year = "wind_2024";
    url_data.id_s_w_6 = data.from;
    target = "wind_key_results_2024";
  } else if (slider_id === "id_s_w_7") {
    wind_year = "wind_2027";
    url_data.id_s_w_7 = data.from;
    target = "wind_key_results_2027";
  } else if (
    ["id_s_pv_ff_3", "id_s_pv_ff_4", "id_s_pv_ff_5"].includes(slider_id)
  ) {
    url_data.id_s_pv_ff_3 =
      $("#id_s_pv_ff_3").data("ionRangeSlider").result.from;
    url_data.id_s_pv_ff_4 =
      $("#id_s_pv_ff_4").data("ionRangeSlider").result.from;
    url_data.id_s_pv_ff_5 =
      $("#id_s_pv_ff_5").data("ionRangeSlider").result.from;
    target = "pv_ground_key_results";
  } else if (slider_id === "id_s_pv_d_3") {
    url_data.id_s_pv_d_3 = data.from;
    target = "pv_roof_key_results";
  } else {
    return logMessage(msg);
  }

  const query = new URLSearchParams(url_data).toString();
  let url = `/detail_key_results?${query}`;
  if (wind_year !== undefined) {
    url += "&wind_year=" + wind_year;
  }
  fetch(url)
    .then((response) => {
      // Check if the response is successful
      if (!response.ok) {
        throw new Error(
          `Error requesting detail key results for slider ${slider_id}`,
        );
      }
      // Return the response as HTML
      return response.text();
    })
    .then((html) => {
      // Insert the HTML into the DOM
      document.getElementById(target).innerHTML = html;
    })
    .catch((error) => {
      console.error(
        `Error requesting detail key results for slider ${slider_id}:`,
        error,
      );
    });
  return logMessage(msg);
}

// Helper Functions

function getColorsByIds(ids) {
  let colors = [];
  for (let id of ids) {
    const cleanedId = id.replace(/^id_/, "");
    colors.push(SETTINGS_PARAMETERS[cleanedId].color);
  }
  return colors;
}

function getIconsByIds(ids) {
  let icons = [];
  for (let id of ids) {
    const cleanedId = id.replace(/^id_/, "");
    icons.push(powerIcons[cleanedId]);
  }
  return icons;
}

function updatePowerMix(weights, colors, icons) {
  const msg = "Unequal amount of weights and colors";
  if (weights.length !== colors.length) throw new Error(msg);
  let html = `<div class="power-mix__chart"><div class="power-mix__icons">`;
  for (const index of weights.keys()) {
    html += `<div style="width: ${weights[index]}%;">${icons[index]}</div>`;
  }
  html += `</div><div class="power-mix__colors">`;
  for (const index of weights.keys()) {
    html += `<div style="width: ${weights[index]}%; background-color: ${colors[index]}; text-align: center; height: 1rem;"></div>`;
  }
  html += `</div></div>`;
  powerMixInfoBanner.innerHTML = html;
}

function getWeightsInPercent(values, total) {
  let weights = [];
  for (const value of values) {
    weights.push((parseInt(value) / parseInt(total)) * 100);
  }
  return weights;
}

function getTotalOfValues(values) {
  let total = 0;
  for (const value of values) {
    total += value;
  }
  return total;
}

function convertToPercent(num, min, max) {
  return ((num - min) / (max - min)) * 100;
}

function addMarks(data, marks) {
  let html = "";

  for (let i = 0; i < marks.length; i++) {
    let percent = convertToPercent(marks[i][1], data.min, data.max);
    // Fix percentage due to offset
    percent = percent - 2.5 - (3.5 * percent) / 100;
    html += `<span class="showcase__mark" style="left: ${percent}%">`;
    html += marks[i][0];
    html += "</span>";
  }

  data.slider.append(html);
}

$(document).ready(function () {
  $(`#id_s_h_1`).data("ionRangeSlider").update({ block: true });
  calculate_max_pv_ff();
  calculate_max_pv_d();
});
