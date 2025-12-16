function createChart(div_id, options) {
  const chartElement = document.getElementById(div_id);
  let chart;
  if (echarts.getInstanceByDom(chartElement)) {
    chart = echarts.getInstanceByDom(chartElement);
    chart.clear();
  } else {
    chart = echarts.init(chartElement, null, {renderer: "svg"});
  }
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
