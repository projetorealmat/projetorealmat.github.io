---
title: "Livros"
kicker: "Biblioteca"
description: "Obras e traduções reunidas pelo REALMat para leitura e download."
permalink: /livros/
---

<p class="realmat-page-lead">Cada obra tem uma página própria com a edição atual, os formatos disponíveis e a situação da tradução. As versões anteriores ficam no <a href="{{ '/arquivo/' | relative_url }}">arquivo de edições</a>.</p>

<section class="realmat-library" id="catalogo" aria-label="Catálogo de livros">
{% for book in site.data.books %}
  {% assign current = book.releases | where: "version", book.current_version | first %}
  {% assign stage = site.data.translation_stages | where: "id", current.translation_stage | first %}
  {% assign book_url = '/livros/' | append: book.id | append: '/' %}
  <article class="realmat-library__entry">
    <a href="{{ book_url | relative_url }}" class="image realmat-book-poster realmat-book-poster--small" aria-label="Ver {{ book.title }}">
      {% include book-poster-content.html book=book index=forloop.index %}
    </a>

    <div class="realmat-library__body">
      <header>
        <span class="date">{{ book.subject }} · {{ stage.label }}</span>
        <h2><a href="{{ book_url | relative_url }}">{{ book.title }}</a></h2>
      </header>
      <p>A edição {{ current.version }} corresponde a uma {{ stage.label | downcase }}. Consulte a página da obra para ler pelo formato principal, baixar o PDF oficial e ver o repositório da edição.</p>
      <p class="realmat-meta">PDF oficial · acesso aberto · {{ current.version }} · {{ stage.label }}</p>
      <ul class="actions">
        <li><a href="{{ book_url | relative_url }}" class="button primary">Ver a edição</a></li>
      </ul>
    </div>
  </article>
{% endfor %}
</section>

<p class="realmat-catalog-note"><span class="date">Publicação</span> Novas obras entram no catálogo quando uma edição é preparada e publicada em uma versão numerada e preservada.</p>
