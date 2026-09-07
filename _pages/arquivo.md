---
title: "Arquivo"
kicker: "Histórico"
description: "Histórico de novas obras, edições e mudanças no portal."
permalink: /arquivo/
---

{% assign book = site.data.books | first %}

<p class="realmat-page-lead">Registro das principais etapas de publicação do portal.</p>

<section class="realmat-updates" aria-label="Histórico de publicações">
  <article>
    <header>
      <span class="date">5 de setembro de 2026 · Livro · {{ book.version }}</span>
      <h2>forallx disponível para leitura</h2>
    </header>
    <p>O portal oferece a edição {{ book.version }} de <em>forallx: Lógica</em> para leitura e download. O estado editorial atual é: {{ book.status }}.</p>
    <a href="{{ '/livros/forallx/' | relative_url }}">Ver a edição <span aria-hidden="true">↗</span></a>
    <a href="{{ book.release_url }}" target="_blank" rel="noopener noreferrer">Ver a release <span aria-hidden="true">↗</span></a>
  </article>

  <article>
    <header>
      <span class="date">5 de setembro de 2026 · Portal</span>
      <h2>Estrutura inicial do REALMat</h2>
    </header>
    <p>O portal foi organizado para separar a leitura pública dos livros do espaço de colaboração e desenvolvimento.</p>
  </article>
</section>
