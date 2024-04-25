// Goals & scenarios, initioalize charts

// Results view, initiliaze charts
// const detailed_overview_chart = echarts.init(document.getElementById("detailed_overview_chart"));
const wind_capacity_chart = echarts.init(document.getElementById("wind_capacity_chart"));
const wind_areas_chart = echarts.init(document.getElementById("wind_areas_chart"));

const electricity_overview_chart = echarts.init(document.getElementById("electricity_overview_chart"));
const electricity_autarky_chart = echarts.init(document.getElementById("electricity_autarky_chart"));
// const mobility_overview_chart = echarts.init(document.getElementById("mobility_overview_chart"));
// const mobility_THG_chart = echarts.init(document.getElementById("mobility_THG_chart"));
const heat_decentralized_chart = echarts.init(document.getElementById("heat_decentralized_chart"));
const heat_centralized_chart = echarts.init(document.getElementById("heat_centralized_chart"));

// Onboarding Charts
const onboarding_wind_div = document.getElementById("onboarding_wind_chart");
const onboarding_wind_chart = echarts.init(onboarding_wind_div);
const onboarding_pv_ground_div = document.getElementById("onboarding_pv_ground_chart");
const onboarding_pv_ground_chart = echarts.init(onboarding_pv_ground_div);
const onboarding_pv_roof_div = document.getElementById("onboarding_pv_roof_chart");
const onboarding_pv_roof_chart = echarts.init(onboarding_pv_roof_div);

PubSub.subscribe(eventTopics.MENU_CHANGED, resizeCharts);

// Styling variables
const chart_tooltip = {
  trigger: 'axis',
  axisPointer: {
  type: 'shadow'
  }
};
const chart_bar_width_sm = 16;
const chart_grid_goal = {
  top: '10%',
  left: '15%',
  right: '15%',
  bottom: '18%',
  height: '120',
  containLabel: true
};
const chart_grid_results = {
  top: '10%',
  left: '3%',
  right: '25%',
  bottom: '18%',
  containLabel: true
};
const chart_text_style = {
  fontFamily: "Roboto",
  fontSize: 10,
  //fontWeight: 300,
  //color: '#002C50'
};
const chart_legend = {
  show: true,
  bottom: '0',
  itemWidth: 10,
  itemHeight: 10
};

// CHARTS -> defined in /map/charts/

// get options for result view charts
// const detailed_overview_option = JSON.parse(document.getElementById("detailed_overview").textContent);
const wind_capacity_option = JSON.parse(document.getElementById("wind_capacity").textContent);
const wind_areas_option = JSON.parse(document.getElementById("wind_areas").textContent);

const electricity_overview_option = JSON.parse(document.getElementById("electricity_overview").textContent);
const electricity_autarky_option = JSON.parse(document.getElementById("electricity_autarky").textContent);
// const mobility_overview_option = JSON.parse(document.getElementById("mobility_overview").textContent);
// const mobility_ghg_option = JSON.parse(document.getElementById("mobility_ghg").textContent);
const heat_decentralized_option = JSON.parse(document.getElementById("heat_decentralized").textContent);
const heat_centralized_option = JSON.parse(document.getElementById("heat_centralized").textContent);

// get options for onboarding charts
const onboarding_wind_option = JSON.parse(document.getElementById("onboarding_wind").textContent);
const onboarding_pv_ground_option = JSON.parse(document.getElementById("onboarding_pv_ground").textContent);
const onboarding_pv_roof_option = JSON.parse(document.getElementById("onboarding_pv_roof").textContent);

function resizeCharts() {
  setTimeout(function () {
    // detailed_overview_chart.resize();
    wind_capacity_chart.resize();
    wind_areas_chart.resize();
    electricity_overview_chart.resize();
    electricity_autarky_chart.resize();
    // mobility_overview_chart.resize();
    // mobility_THG_chart.resize();
    heat_decentralized_chart.resize();
    heat_centralized_chart.resize();
    onboarding_wind_chart.resize();
    onboarding_pv_ground_chart.resize();
    onboarding_pv_roof_chart.resize();
  }, 200);
}

// Results, setOptions
// detailed_overview_chart.setOption(detailed_overview_option);
wind_capacity_chart.setOption(wind_capacity_option);
wind_areas_chart.setOption(wind_areas_option);
electricity_overview_chart.setOption(electricity_overview_option);
electricity_autarky_chart.setOption(electricity_autarky_option);
// mobility_overview_chart.setOption(mobility_overview_option);
// mobility_THG_chart.setOption(mobility_ghg_option);
heat_decentralized_chart.setOption(heat_decentralized_option);
heat_centralized_chart.setOption(heat_centralized_option);

// onboarding Charts
onboarding_wind_chart.setOption(onboarding_wind_option);
onboarding_pv_ground_chart.setOption(onboarding_pv_ground_option);
onboarding_pv_roof_chart.setOption(onboarding_pv_roof_option);

resizeCharts();

window.addEventListener("resize", resizeCharts);
document.addEventListener("show.bs.tab", resizeCharts);


function createChart(div_id, options) {
  const chartElement = document.getElementById(div_id);
  let chart;
  if (echarts.getInstanceByDom(chartElement)) {
    chart =  echarts.getInstanceByDom(chartElement);
    chart.clear();
  } else {
    chart = echarts.init(chartElement, null, {renderer: 'svg'});
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
