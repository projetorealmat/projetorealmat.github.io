(function () {
  "use strict";

  var root = document.documentElement;
  var toggle = document.querySelector("[data-menu-toggle]");
  var panel = document.getElementById("realmat-menu-panel");
  var navigation = document.getElementById("site-nav");
  var searchToggle = document.getElementById("realmat-search-toggle");
  var searchPanel = document.getElementById("search-content");

  root.classList.add("realmat-menu-js");

  function closeMenu(restoreFocus) {
    if (!toggle || !panel) {
      return;
    }

    var wasOpen = toggle.getAttribute("aria-expanded") === "true";
    var focusInMenu = panel.contains(document.activeElement);

    toggle.setAttribute("aria-expanded", "false");
    panel.classList.remove("is-open");

    if (restoreFocus && wasOpen && focusInMenu) {
      toggle.focus();
    }
  }

  function setSearchState(isOpen, restoreFocus) {
    if (!searchPanel || !searchToggle) {
      return;
    }

    searchPanel.classList.toggle("is-open", isOpen);
    searchPanel.setAttribute("aria-hidden", String(!isOpen));
    searchToggle.setAttribute("aria-expanded", String(isOpen));

    if (isOpen) {
      var input = searchPanel.querySelector("input[type=search]");
      if (input) {
        window.setTimeout(function () {
          input.focus();
        }, 0);
      }
    } else if (restoreFocus) {
      searchToggle.focus();
    }
  }

  if (toggle && panel) {
    toggle.addEventListener("click", function () {
      var isOpen = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!isOpen));
      panel.classList.toggle("is-open", !isOpen);
    });

    panel.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        closeMenu(false);
      });
    });

    document.addEventListener("click", function (event) {
      if (panel.classList.contains("is-open") && navigation && !navigation.contains(event.target)) {
        closeMenu(false);
      }
    });
  }

  if (searchToggle && searchPanel) {
    searchToggle.addEventListener("click", function () {
      var isOpen = searchPanel.classList.contains("is-open");
      setSearchState(!isOpen, false);
    });
  }

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      var searchWasOpen = searchPanel && searchPanel.classList.contains("is-open");
      setSearchState(false, searchWasOpen);
      closeMenu(true);
    }
  });

  window.addEventListener("resize", function () {
    if (window.innerWidth > 760) {
      closeMenu(false);
    }
  });

  var searchPage = document.querySelector("[data-search-results]");
  if (searchPage) {
    var pageInput = document.getElementById("realmat-search-page-input");
    var status = document.getElementById("realmat-search-status");
    var resultsContainer = document.getElementById("realmat-search-results");
    var index = Array.isArray(window.REALMAT_SEARCH_INDEX) ? window.REALMAT_SEARCH_INDEX : [];
    var query = new URLSearchParams(window.location.search).get("q") || "";

    if (pageInput) {
      pageInput.value = query;
    }

    function normalize(value) {
      return String(value || "").toLocaleLowerCase("pt-BR").normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    }

    function renderResults() {
      if (!status || !resultsContainer) {
        return;
      }

      resultsContainer.innerHTML = "";
      var normalizedQuery = normalize(query).trim();

      if (!normalizedQuery) {
        status.textContent = "Digite um termo para pesquisar no portal.";
        return;
      }

      var matches = index.filter(function (item) {
        return normalize(item.title + " " + item.text).indexOf(normalizedQuery) !== -1;
      }).slice(0, 20);

      status.textContent = matches.length === 1
        ? "1 resultado encontrado."
        : matches.length + " resultados encontrados.";

      matches.forEach(function (item) {
        var article = document.createElement("article");
        article.className = "realmat-search-result";

        var title = document.createElement("h2");
        var link = document.createElement("a");
        link.href = item.url;
        link.textContent = item.title;
        title.appendChild(link);

        var excerpt = document.createElement("p");
        var plainText = String(item.text || "").replace(/[\r\n]+/g, " ").trim();
        excerpt.textContent = plainText.length > 190 ? plainText.slice(0, 187) + "…" : plainText;

        article.appendChild(title);
        article.appendChild(excerpt);
        resultsContainer.appendChild(article);
      });
    }

    if (pageInput) {
      pageInput.addEventListener("input", function () {
        query = pageInput.value;
        var nextUrl = new URL(window.location.href);
        if (query) {
          nextUrl.searchParams.set("q", query);
        } else {
          nextUrl.searchParams.delete("q");
        }
        window.history.replaceState({}, "", nextUrl);
        renderResults();
      });
    }

    renderResults();
  }
}());
