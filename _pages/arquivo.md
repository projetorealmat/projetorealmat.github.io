---
title: "Edições anteriores"
kicker: "Histórico"
description: "Versões anteriores das obras do REALMat, reunidas para consulta e referência."
permalink: /arquivo/
---

<p class="realmat-page-lead">A edição atual está na página de cada livro. Aqui ficam as versões anteriores, preservadas para consulta e citação.</p>
<p class="realmat-note">Obras sem versões anteriores publicadas não aparecem nesta lista. As datas seguem o formato dia/mês/ano.</p>

<section class="realmat-updates" aria-label="Edições anteriores por obra">
{% for book in site.data.books %}
  {% assign previous_releases = book.releases | where_exp: "release", "release.version != book.current_version" %}
  {% if previous_releases.size > 0 %}
    {% assign book_url = '/livros/' | append: book.id | append: '/' %}
  <article id="{{ book.id }}">
    <header>
      <span class="date">Histórico de edições</span>
      <h2>{{ book.title }}</h2>
    </header>
    <p><a href="{{ book_url | relative_url }}">Acessar a página do livro e a edição atual</a></p>
    <ul class="realmat-release-list">
    {% for release in previous_releases %}
      {% assign stage = site.data.translation_stages | where: "id", release.translation_stage | first %}
      {% assign pdf = release.publications | where: "id", "pdf" | first %}
      <li>
        <span class="date">{{ release.version }} · {{ stage.label }}{% if release.release_date %} · <time datetime="{{ release.release_date }}">{{ release.release_date | date: "%d/%m/%Y" }}</time>{% endif %}</span>
        <a href="{{ release.release_url }}" target="_blank" rel="noopener noreferrer">Registro da edição no GitHub <span aria-hidden="true">↗</span></a>
        <a href="{{ pdf.url }}" target="_blank" rel="noopener noreferrer">Baixar PDF <span aria-hidden="true">↓</span></a>
      </li>
    {% endfor %}
    </ul>
  </article>
  {% endif %}
{% endfor %}
</section>
