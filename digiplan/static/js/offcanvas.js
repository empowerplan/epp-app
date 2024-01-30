const mapView = document.getElementById("mapView");
const newOffcanvasDocumentation = new bootstrap.Offcanvas(document.getElementById('offcanvasDocumentation'));
// const newOffcanvasSources = new bootstrap.Offcanvas(document.getElementById('offcanvasSources'));
const newOffcanvasContact = new bootstrap.Offcanvas(document.getElementById('offcanvasContact'));
const offcanvasDocumentation = document.getElementById('offcanvasDocumentation');
// const offcanvassSources = document.getElementById('offcanvasSources');
const offcanvasContact = document.getElementById('offcanvasContact');

mapView.onclick = function() {
  newOffcanvasDocumentation.hide(offcanvasDocumentation);
  // newOffcanvasSources.hide(offcanvassSources);
  newOffcanvasContact.hide(offcanvasContact);
};


// Scenarios step
function selectScenarioCard(scenarioCardNumber) {
  const starSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#2348C3" class="bi bi-star-fill" viewBox="0 0 16 16">
  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
</svg>`
  const leftArrowSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="#2348C3" class="bi bi-arrow-left-circle-fill" viewBox="0 0 16 16">
  <path d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0m3.5 7.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z"/>
</svg>`;
  const rightArrowSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="#2348C3" class="bi bi-arrow-right-circle" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0M4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5z"/>
</svg>`;

  for (let i = 1; i <= 5; i++) {
    const card = document.getElementById('panelCard' + i);
    const selectedScenario = document.getElementById('selectedScenario' + i);
    const arrowIcon = card.querySelector('.arrow-icon');
    const scenarioStar = card.querySelector('.scenario-star');

    if (i === scenarioCardNumber) {
      // Selected scenario card
      selectedScenario.style.display = "block";
      scenarioStar.innerHTML = starSVG;
      card.classList.add('panel-card--selected');
      arrowIcon.innerHTML = leftArrowSVG;
    } else {
      // Unselected scenario cards
      selectedScenario.style.display = "none";
      scenarioStar.innerHTML = "";
      card.classList.remove('panel-card--selected');
      arrowIcon.innerHTML = rightArrowSVG;
    }
  }
}
