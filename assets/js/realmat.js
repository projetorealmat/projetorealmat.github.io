(function () {
  "use strict";

  var toggle = document.querySelector("[data-menu-toggle]");
  var panel = document.getElementById("realmat-menu-panel");
  var navigation = document.getElementById("site-nav");

  if (!toggle || !panel || !navigation) {
    return;
  }

  function closeMenu() {
    toggle.setAttribute("aria-expanded", "false");
    panel.classList.remove("is-open");
    document.body.classList.remove("realmat-menu-open");
  }

  toggle.addEventListener("click", function () {
    var isOpen = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!isOpen));
    panel.classList.toggle("is-open", !isOpen);
    document.body.classList.toggle("realmat-menu-open", !isOpen);
  });

  document.addEventListener("click", function (event) {
    if (document.body.classList.contains("realmat-menu-open") && !navigation.contains(event.target)) {
      closeMenu();
    }
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      closeMenu();
    }
  });

  window.addEventListener("resize", function () {
    if (window.innerWidth > 760) {
      closeMenu();
    }
  });
}());
