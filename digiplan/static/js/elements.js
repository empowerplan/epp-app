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
    document.querySelectorAll('.js-wind-svg-container svg [id^="circle"]').forEach(circle => {
      circle.style.display = 'none';
    });

    // Get the newly activated tab's ID
    const activeTabId = event.target.id;
    let baseIdSuffix = activeTabId.replace('wind', '').replace('Tab', '');
    const circleToShowId = 'circle' + baseIdSuffix.charAt(0).toUpperCase() + baseIdSuffix.slice(1);

    // Show the corresponding circle within the SVG
    const circleToShow = document.getElementById(circleToShowId);
    if (circleToShow) {
      circleToShow.style.display = 'block';
    } else {
      console.error(`No circle found with ID: ${circleToShowId}`);
    }

    // Make sure the common SVG container is always displayed
    const svgContainer = document.querySelector('.js-wind-svg-container svg');
    if (svgContainer) {
      svgContainer.style.display = 'block';
    }
  });

  // Adding down arrow as scroll indicator
  const arrow = document.querySelector('.arrow-container');
  const resultTab = document.querySelector('#results-pv-tab.nav-link');
  const mainTabContent = document.querySelector('#mainTabContent');
  let arrowDisplayed = false;

  if (resultTab && mainTabContent) {
    const observer = new MutationObserver(function(mutations) {
      mutations.forEach(mutation => {
        if (mutation.attributeName === 'class' && !arrowDisplayed) {
          if (resultTab.classList.contains('active')) {
            setTimeout(() => {
              arrow.classList.add('show');
              arrowDisplayed = true;
            }, 1000);
          }
        }
      });
    });

    observer.observe(resultTab, {
      attributes: true
    });

    mainTabContent.addEventListener('scroll', function() {
      let threshold = mainTabContent.scrollHeight - mainTabContent.clientHeight - 300;
      if (mainTabContent.scrollTop >= threshold && arrowDisplayed) {
        arrow.classList.remove('show');
      }
    });
  } else {
    console.error('The required elements were not found in the DOM.');
  }
});