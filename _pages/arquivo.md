---
title: "Arquivo"
kicker: "Histórico"
description: "Histórico de novas obras, edições e mudanças no portal."
permalink: /arquivo/
---

<p class="realmat-page-lead">O arquivo preserva as versões publicadas e identifica qual edição está atualmente recomendada pelo catálogo.</p>

<h2>Histórico editorial</h2>

<section class="realmat-updates" aria-label="Histórico de publicações">
{% for book in site.data.books %}
  {% assign book_url = '/livros/' | append: book.id | append: '/' %}
  {% assign releases = book.releases | sort: "release_date" | reverse %}
  {% for release in releases %}
    {% assign stage = site.data.translation_stages | where: "id", release.translation_stage | first %}
    {% assign pdf = release.publications | where: "id", "pdf" | first %}
  <article>
    <header>
      <span class="date">{% if release.version == book.current_version %}Atual{% else %}Histórica{% endif %} · {{ release.version }} · {{ stage.label }}{% if release.release_date %} · {{ release.release_date }}{% endif %}</span>
      <h2>{{ book.title }} · {{ stage.label }}</h2>
    </header>
    <p>A versão {{ release.version }} de <em>{{ book.title }}</em> está registrada no catálogo como uma referência imutável.</p>
    <a href="{{ book_url | relative_url }}">Ver a obra <span aria-hidden="true">↗</span></a>
    <a href="{{ release.entrypoint.url }}" target="_blank" rel="noopener noreferrer">Ler o livro <span aria-hidden="true">↗</span></a>
    <a href="{{ pdf.url }}" target="_blank" rel="noopener noreferrer">Baixar PDF <span aria-hidden="true">↓</span></a>
    <a href="{{ release.release_url }}" target="_blank" rel="noopener noreferrer">Ver a release <span aria-hidden="true">↗</span></a>
  </article>
  {% endfor %}
{% endfor %}
</section>
