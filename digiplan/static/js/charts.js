function createChart(div_id, options) {
  const chartElement = document.getElementById(div_id);
  let chart;
  if (echarts.getInstanceByDom(chartElement)) {
    chart = echarts.getInstanceByDom(chartElement);
    chart.clear();
  } else {
    chart = echarts.init(chartElement, null, {renderer: "svg"});
  }
  addUnitsToTooltip(options);
  chart.setOption(options);
  chart.resize();
}

function clearChart(div_id) {
  const chartElement = document.getElementById(div_id);
  if (echarts.getInstanceByDom(chartElement)) {
    const chart = echarts.getInstanceByDom(chartElement);
    chart.clear();
  }
}

function addUnitsToTooltip(options) {
  function unitFormatter(value, unit) {
    return value + ' ' + unit;
  }

  /* jshint ignore:start */
  for (const series of options.series) {
    if ("tooltip" in series && "unit" in series.tooltip) {
      series.tooltip.valueFormatter = function (value) {
        return unitFormatter(value, series.tooltip.unit);
      };
    }
  }
  /* jshint ignore:end */
}
