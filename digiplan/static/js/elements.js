export const statusquoDropdown = document.getElementById("situation_today");
export const futureDropdown = document.getElementById("result_views");
export const resultsTabs = document.getElementById("results-tabs");

// Show onboarding modal on start
document.addEventListener('DOMContentLoaded', (event) => {
    var myModal = new bootstrap.Modal(document.getElementById('onboardingModal'), {});
    myModal.show();
});

// Prevent continuous cycle of modal carousel
/* document.addEventListener("DOMContentLoaded", function() {
    var carouselEl = document.querySelector('#carouselExampleIndicators');
    var carousel = new bootstrap.Carousel(carouselEl, {
      wrap: false
    });

    var prevButton = document.querySelector('.carousel-control-prev');
    var nextButton = document.querySelector('.carousel-control-next');

    prevButton.addEventListener('click', function (event) {
      event.preventDefault();
      carousel.prev();
    });

    nextButton.addEventListener('click', function (event) {
      event.preventDefault();
      carousel.next();
    });

    carouselEl.addEventListener('slid.bs.carousel', function () {
      const carouselItems = carouselEl.querySelectorAll('.carousel-item');
      const currentIndex = Array.prototype.indexOf.call(carouselItems, carouselEl.querySelector('.carousel-item.active'));
      if (currentIndex === 0) {
        prevButton.classList.add('transparent');
      } else {
        prevButton.classList.remove('transparent');
      }

      if (currentIndex === carouselItems.length - 1) {
        nextButton.classList.add('transparent');
      } else {
        nextButton.classList.remove('transparent');
      }
    });
  }); */

// Update svg image above tabs in wind settings details
document.addEventListener('DOMContentLoaded', function() {
  const windTab = document.querySelector('#windTab');

  windTab.addEventListener('shown.bs.tab', function(event) {
    document.querySelectorAll('.js-wind-svg-container svg').forEach(svg => {
      svg.style.display = 'none';
    });

    // Get the newly activated tab's ID, e.g., "windPastTab"
    const activeTabId = event.target.id;

    // Correctly construct the SVG ID
    let baseId = activeTabId.replace('Tab', ''); // Results in e.g., "windPast"
    const svgToShowId = 'svg' + baseId.charAt(0).toUpperCase() + baseId.slice(1);

    // Show the corresponding SVG
    const svgToShow = document.getElementById(svgToShowId);
    if (svgToShow) {
      svgToShow.style.display = 'block';
    } else {
      console.error(`No SVG found with ID: ${svgToShowId}`);
    }
  });
});
  
  