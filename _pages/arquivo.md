---
title: "Arquivo"
kicker: "Histórico"
description: "Obras disponíveis e as edições atualmente recomendadas pelo catálogo."
permalink: /arquivo/
---

<p class="realmat-page-lead">O arquivo lista cada obra uma única vez, sempre com a última versão disponível. O histórico completo de versões fica na página individual de cada livro.</p>

<h2>Histórico editorial</h2>

<section class="realmat-updates" aria-label="Obras e versões atuais">
{% for book in site.data.books %}
  {% assign book_url = '/livros/' | append: book.id | append: '/' %}
  {% assign release = book.releases | where: "version", book.current_version | first %}
  {% assign stage = site.data.translation_stages | where: "id", release.translation_stage | first %}
  {% assign pdf = release.publications | where: "id", "pdf" | first %}
  <article>
    <header>
      <span class="date">Atual · {{ release.version }} · {{ stage.label }}{% if release.release_date %} · {{ release.release_date }}{% endif %}</span>
      <h2>{{ book.title }}</h2>
    </header>
    <p>A edição {{ release.version }} de <em>{{ book.title }}</em> é a última versão disponível no catálogo.</p>
    <a href="{{ book_url | relative_url }}">Ver a obra <span aria-hidden="true">↗</span></a>
    <a href="{{ release.entrypoint.url }}" target="_blank" rel="noopener noreferrer">Ler o livro <span aria-hidden="true">↗</span></a>
    <a href="{{ pdf.url }}" target="_blank" rel="noopener noreferrer">Baixar PDF <span aria-hidden="true">↓</span></a>
    <a href="{{ release.release_url }}" target="_blank" rel="noopener noreferrer">Ver a release <span aria-hidden="true">↗</span></a>
  </article>
{% endfor %}
</section>
