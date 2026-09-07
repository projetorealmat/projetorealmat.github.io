---
title: "Buscar"
kicker: "Pesquisa"
description: "Encontre livros e páginas no portal REALMat."
permalink: /buscar/
---

<div class="realmat-search" data-search-results>
  <form action="{{ '/buscar/' | relative_url }}" method="get" role="search">
    <label for="realmat-search-input">O que você procura?</label>
    <div class="realmat-search__controls">
      <input id="realmat-search-input" type="search" name="q" placeholder="Digite um título ou assunto" autocomplete="off" aria-describedby="realmat-search-help">
      <button class="button primary" type="submit">Buscar</button>
    </div>
    <p id="realmat-search-help" class="realmat-search__help">A busca considera títulos, assuntos e textos das páginas do portal.</p>
  </form>

  <p id="realmat-search-status" class="realmat-search__status" aria-live="polite"></p>
  <div id="realmat-search-results" class="realmat-search__results"></div>
  <noscript><p class="realmat-search__noscript">Ative JavaScript para pesquisar no conteúdo do portal.</p></noscript>
</div>

<script>
window.REALMAT_SEARCH_INDEX = [
{% assign search_index_count = 0 %}
{% for item in site.pages %}
  {% assign include_item = true %}
  {% if item.url contains '/livros/' %}{% assign include_item = false %}{% endif %}
  {% if item.url == '/livros/' %}{% assign include_item = true %}{% endif %}
  {% unless item.url == '/buscar/' or item.url == '/404.html' or item.url == '/atualizacoes/' %}
    {% if include_item %}
      {% if search_index_count > 0 %},{% endif %}
      {
        "title": {{ item.title | default: "" | jsonify }},
        "url": {{ item.url | relative_url | jsonify }},
        "text": {{ item.content | strip_html | strip_newlines | jsonify }}
      }
      {% assign search_index_count = search_index_count | plus: 1 %}
    {% endif %}
  {% endunless %}
{% endfor %}
{% for book in site.data.books %}
  {% assign book_url = '/livros/' | append: book.id | append: '/' %}
  {% if search_index_count > 0 %},{% endif %}
  {
    "title": {{ book.title | jsonify }},
    "url": {{ book_url | relative_url | jsonify }},
    "text": {{ book.title | append: " " | append: book.subject | append: " " | append: book.current_version | jsonify }}
  }
  {% assign search_index_count = search_index_count | plus: 1 %}
{% endfor %}
];
</script>
