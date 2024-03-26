PubSub.subscribe(mapEvent.MAP_LAYER_SWITCH_CLICK, toggleCoupledPanelControl);

$("#js-map-layers-btn").on("click", function () {
  $("#js-map-layers-box").show();
});

$("#js-map-layers-box-close").on("click", function () {
  $("#js-map-layers-box").hide();
});

function toggleCoupledPanelControl(msg, layerSwitch) {
  for (const control of document.querySelectorAll(`#${layerSwitch.id}`)) {
    control.checked = layerSwitch.checked;
  }
  return logMessage(msg);
}
