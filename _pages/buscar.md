---
title: "Buscar"
kicker: "Pesquisa"
description: "Encontre livros e páginas no portal REALMAT."
permalink: /buscar/
---

<div class="realmat-search-page" data-search-results>
  <form class="realmat-search-page__form" action="{{ '/buscar/' | relative_url }}" method="get" role="search">
    <label for="realmat-search-page-input">O que você procura?</label>
    <div class="realmat-search-form__controls">
      <input id="realmat-search-page-input" type="search" name="q" placeholder="Digite um título ou assunto" autocomplete="off">
      <button class="realmat-button realmat-button--primary" type="submit">Buscar</button>
    </div>
  </form>

  <p id="realmat-search-status" class="realmat-search-status" aria-live="polite"></p>
  <div id="realmat-search-results" class="realmat-search-results"></div>
</div>

<script>
window.REALMAT_SEARCH_INDEX = [
{% for item in site.pages %}
{% if item.title %}
  {
    "title": {{ item.title | jsonify }},
    "url": {{ item.url | relative_url | jsonify }},
    "text": {{ item.content | strip_html | strip_newlines | jsonify }}
  }{% unless forloop.last %},{% endunless %}
{% endif %}
{% endfor %}
];
</script>
