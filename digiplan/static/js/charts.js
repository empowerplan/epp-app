/* jshint ignore:start */
const preResultCharts = {
  wind_capacity: "wind_capacity_chart",
  wind_areas: "wind_areas_chart",
  pv_ground_capacity: "pv_ground_capacity_chart",
  pv_ground_areas: "pv_ground_areas_chart",
  pv_roof_capacity: "pv_roof_capacity_chart",
  pv_roof_areas: "pv_roof_areas_chart",
};
/* jshint ignore:end */

// Onboarding Charts
const onboarding_wind_div = document.getElementById("onboarding_wind_chart");
const onboarding_wind_chart = echarts.init(onboarding_wind_div);
const onboarding_wind_option = JSON.parse(
  document.getElementById("onboarding_wind").textContent,
);
onboarding_wind_chart.setOption(onboarding_wind_option);

const onboarding_pv_ground_div = document.getElementById(
  "onboarding_pv_ground_chart",
);
const onboarding_pv_ground_chart = echarts.init(onboarding_pv_ground_div);
const onboarding_pv_ground_option = JSON.parse(
  document.getElementById("onboarding_pv_ground").textContent,
);
onboarding_pv_ground_chart.setOption(onboarding_pv_ground_option);

const onboarding_pv_roof_div = document.getElementById(
  "onboarding_pv_roof_chart",
);
const onboarding_pv_roof_chart = echarts.init(onboarding_pv_roof_div);
const onboarding_pv_roof_option = JSON.parse(
  document.getElementById("onboarding_pv_roof").textContent,
);
onboarding_pv_roof_chart.setOption(onboarding_pv_roof_option);

PubSub.subscribe(eventTopics.MENU_CHANGED, resizeCharts);

function resizeCharts() {
  setTimeout(function () {
    for (const preResultChart of Object.values(preResultCharts)) {
      const chartDiv = document.getElementById(preResultChart);
      const chart = echarts.getInstanceByDom(chartDiv);
      if (chart !== undefined) {
        chart.resize();
      }
    }
    onboarding_wind_chart.resize();
    onboarding_pv_ground_chart.resize();
    onboarding_pv_roof_chart.resize();
  }, 200);
}

resizeCharts();

window.addEventListener("resize", resizeCharts);
document.addEventListener("show.bs.tab", resizeCharts);

function createChart(div_id, options) {
  const chartElement = document.getElementById(div_id);
  let chart;
  if (echarts.getInstanceByDom(chartElement)) {
    chart = echarts.getInstanceByDom(chartElement);
    chart.clear();
  } else {
    chart = echarts.init(chartElement, null, { renderer: "svg" });
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
