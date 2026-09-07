---
title: "Tópicos"
kicker: "Explorar"
description: "Explore os assuntos presentes nas obras e traduções do REALMat."
permalink: /topicos/
---

<p class="realmat-page-lead">Os tópicos ajudam a encontrar uma obra pelo assunto. O catálogo é agrupado automaticamente a partir dos metadados de cada livro.</p>

<section class="realmat-topics" aria-label="Tópicos do catálogo">
{% assign topic_groups = site.data.books | group_by: "subject" %}
{% for group in topic_groups %}
  <article class="realmat-topic">
    <span class="date">{{ group.items.size }} obra(s)</span>
    <h2>{{ group.name }}</h2>
    {% for book in group.items %}
      {% assign book_url = '/livros/' | append: book.id | append: '/' %}
      <p><a href="{{ book_url | relative_url }}">{{ book.title }}</a></p>
    {% endfor %}
  </article>
{% endfor %}
</section>
