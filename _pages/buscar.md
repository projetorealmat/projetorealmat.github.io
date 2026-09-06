---
title: "Buscar"
kicker: "Pesquisa"
description: "Encontre livros e páginas no portal REALMAT."
permalink: /buscar/
---

<div class="realmat-search" data-search-results>
  <form action="{{ '/buscar/' | relative_url }}" method="get" role="search">
    <label for="realmat-search-input">O que você procura?</label>
    <div class="realmat-search__controls">
      <input id="realmat-search-input" type="search" name="q" placeholder="Digite um título ou assunto" autocomplete="off">
      <button class="button primary" type="submit">Buscar</button>
    </div>
  </form>

  <p id="realmat-search-status" class="realmat-search__status" aria-live="polite"></p>
  <div id="realmat-search-results" class="realmat-search__results"></div>
</div>

<script>
window.REALMAT_SEARCH_INDEX = [
{% for item in site.pages %}
  {
    "title": {{ item.title | default: "" | jsonify }},
    "url": {{ item.url | relative_url | jsonify }},
    "text": {{ item.content | strip_html | strip_newlines | jsonify }}
  }{% unless forloop.last %},{% endunless %}
{% endfor %}
];
</script>
