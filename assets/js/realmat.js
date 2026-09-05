(function () {
  "use strict";

  document.documentElement.classList.add("realmat-menu-js");

  var toggle = document.querySelector("[data-menu-toggle]");
  var panel = document.getElementById("realmat-menu-panel");
  var navigation = document.getElementById("site-nav");
  var searchToggle = document.getElementById("realmat-search-toggle");
  var searchPanel = document.getElementById("search-content");

  function syncSearchState() {
    if (!searchToggle) {
      return;
    }

    var isOpen = Boolean(searchPanel && (
      searchPanel.classList.contains("is--visible") ||
      searchPanel.classList.contains("is-open")
    ));
    searchToggle.setAttribute("aria-expanded", String(isOpen));
  }

  if (searchPanel) {
    syncSearchState();

    if (window.MutationObserver) {
      new MutationObserver(syncSearchState).observe(searchPanel, {
        attributes: true,
        attributeFilter: ["class"]
      });
    }

    if (searchToggle) {
      searchToggle.addEventListener("click", function () {
        window.setTimeout(syncSearchState, 0);
      });
    }
  }

  if (!toggle || !panel || !navigation) {
    return;
  }

  function closeMenu(restoreFocus) {
    var wasOpen = toggle.getAttribute("aria-expanded") === "true";
    var focusInMenu = panel.contains(document.activeElement);

    toggle.setAttribute("aria-expanded", "false");
    panel.classList.remove("is-open");
    document.body.classList.remove("realmat-menu-open");

    if (restoreFocus && wasOpen && focusInMenu) {
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
      syncSearchState();
    }
  });

  window.addEventListener("resize", function () {
    if (window.innerWidth > 760) {
      closeMenu(false);
    }
  });
}());
