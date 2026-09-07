---
title: "Arquivo"
kicker: "Histórico"
description: "Histórico de novas obras, edições e mudanças no portal."
permalink: /arquivo/
---

<p class="realmat-page-lead">O arquivo preserva as versões publicadas e identifica qual edição está atualmente recomendada pelo catálogo.</p>

<section class="realmat-updates" aria-label="Histórico de publicações">
{% for book in site.data.books %}
  {% assign book_url = '/livros/' | append: book.id | append: '/' %}
  {% assign releases = book.releases | sort: "release_date" | reverse %}
  {% for release in releases %}
  <article>
    <header>
      <span class="date">{% if release.version == book.current_version %}Atual{% else %}Histórica{% endif %} · {{ release.version }}{% if release.release_date %} · {{ release.release_date }}{% endif %}</span>
      <h2>{{ book.title }} · {{ release.status }}</h2>
    </header>
    <p>A versão {{ release.version }} de <em>{{ book.title }}</em> está registrada no catálogo como uma referência imutável.</p>
    <a href="{{ book_url | relative_url }}">Ver a obra <span aria-hidden="true">↗</span></a>
    <a href="{{ release.release_url }}" target="_blank" rel="noopener noreferrer">Ver a release <span aria-hidden="true">↗</span></a>
    <a href="{{ release.pdf_url }}" target="_blank" rel="noopener noreferrer">Ver o PDF <span aria-hidden="true">↗</span></a>
  </article>
  {% endfor %}
{% endfor %}
</section>
