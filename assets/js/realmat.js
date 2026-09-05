(function () {
  "use strict";

  document.documentElement.classList.add("realmat-menu-js");

  var toggle = document.querySelector("[data-menu-toggle]");
  var panel = document.getElementById("realmat-menu-panel");
  var navigation = document.getElementById("site-nav");
  var searchToggle = document.getElementById("realmat-search-toggle");

  function setSearchState() {
    if (!searchToggle) {
      return;
    }
    var isExpanded = searchToggle.getAttribute("aria-expanded") === "true";
    searchToggle.setAttribute("aria-expanded", String(!isExpanded));
  }

  if (searchToggle) {
    searchToggle.addEventListener("click", setSearchState);
  }

  if (!toggle || !panel || !navigation) {
    return;
  }

  function closeMenu(restoreFocus) {
    toggle.setAttribute("aria-expanded", "false");
    panel.classList.remove("is-open");
    document.body.classList.remove("realmat-menu-open");
    if (restoreFocus) {
      toggle.focus();
    }
  }

  toggle.addEventListener("click", function () {
    var isOpen = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!isOpen));
    panel.classList.toggle("is-open", !isOpen);
    document.body.classList.toggle("realmat-menu-open", !isOpen);
  });

  document.addEventListener("click", function (event) {
    if (document.body.classList.contains("realmat-menu-open") && !navigation.contains(event.target)) {
      closeMenu(false);
    }
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      closeMenu(true);
    }
  });

  window.addEventListener("resize", function () {
    if (window.innerWidth > 760) {
      closeMenu(false);
    }
  });
}());
