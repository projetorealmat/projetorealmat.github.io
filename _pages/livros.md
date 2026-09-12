---
title: "Livros"
kicker: "Biblioteca"
description: "Obras e traduções reunidas pelo REALMat para leitura e download."
permalink: /livros/
---

<p class="realmat-page-lead">Cada obra tem uma página própria no portal. A versão atual fica em destaque e as versões anteriores permanecem disponíveis para consulta e bifurcação.</p>

<section class="realmat-library" id="catalogo" aria-label="Catálogo de livros">
{% for book in site.data.books %}
  {% assign current = book.releases | where: "version", book.current_version | first %}
  {% assign stage = site.data.translation_stages | where: "id", current.translation_stage | first %}
  {% assign book_url = '/livros/' | append: book.id | append: '/' %}
  <article class="realmat-library__entry">
    <a href="{{ book_url | relative_url }}" class="image realmat-book-poster realmat-book-poster--small" aria-label="Ver {{ book.title }}">
      <span class="realmat-book-poster__inner">
        <span class="realmat-book-poster__number">{{ forloop.index }}</span>
        <span class="realmat-book-poster__name">{{ book.short_title }}</span>
        <span class="realmat-book-poster__subject">{{ book.subject }}</span>
        <span class="realmat-book-poster__formula" aria-hidden="true">p → q</span>
        <span class="realmat-book-poster__footer">edição {{ current.version }}</span>
      </span>
    </a>

    <div class="realmat-library__body">
      <header>
        <span class="date">{{ book.subject }} · {{ stage.label }}</span>
        <h2><a href="{{ book_url | relative_url }}">{{ book.title }}</a></h2>
      </header>
      <p>A edição {{ current.version }} corresponde a uma {{ stage.label | downcase }}. Consulte a página da obra para ler pelo formato principal, baixar o PDF oficial e ver o repositório da edição.</p>
      <p class="realmat-meta">PDF oficial · acesso aberto · {{ current.version }} · {{ stage.label }} · {{ book.releases.size }} versão(ões)</p>
      <ul class="actions">
        <li><a href="{{ book_url | relative_url }}" class="button primary">Ver a edição</a></li>
      </ul>
    </div>
  </article>
{% endfor %}
</section>

<p class="realmat-catalog-note"><span class="date">Publicação</span> Novas obras entram no catálogo quando uma edição é preparada e publicada em uma release imutável.</p>
