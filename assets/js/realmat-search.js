(function () {
  "use strict";

  var root = document.querySelector("[data-search-results]");
  if (!root) return;

  var input = root.querySelector("#realmat-search-input");
  var status = root.querySelector("#realmat-search-status");
  var results = root.querySelector("#realmat-search-results");
  var index = Array.isArray(window.REALMAT_SEARCH_INDEX)
    ? window.REALMAT_SEARCH_INDEX
    : [];

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, function (character) {
      return {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
      }[character];
    });
  }

  function normalize(value) {
    return String(value || "")
      .toLocaleLowerCase("pt-BR")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  function tokenize(value) {
    return normalize(value).trim().split(/\s+/).filter(Boolean);
  }

  function render(query) {
    var tokens = tokenize(query);
    var matches = index.filter(function (item) {
      var haystack = normalize((item.title || "") + " " + (item.text || ""));
      return !tokens.length || tokens.every(function (token) {
        return haystack.indexOf(token) !== -1;
      });
    }).slice(0, 20);

    status.textContent = tokens.length
      ? matches.length + " resultado(s) encontrado(s)."
      : "Mostrando páginas do portal.";

    if (!matches.length && tokens.length) {
      results.innerHTML = '<p class="realmat-search__empty">Nenhum resultado encontrado. Tente outro termo.</p>';
      return;
    }

    results.innerHTML = matches.map(function (item) {
      var excerpt = String(item.text || "").replace(/\s+/g, " ").trim();
      if (excerpt.length > 180) excerpt = excerpt.slice(0, 177) + "...";
      return '<article class="realmat-search__result">' +
        '<h3><a href="' + escapeHtml(item.url) + '">' +
        escapeHtml(item.title || "Página") + "</a></h3>" +
        "<p>" + escapeHtml(excerpt) + "</p>" +
        "</article>";
    }).join("");
  }

  var params = new URLSearchParams(window.location.search);
  var initialQuery = params.get("q") || "";
  input.value = initialQuery;
  input.addEventListener("input", function () {
    render(input.value);
  });
  render(initialQuery);
}());
