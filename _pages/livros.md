---
title: "Livros"
kicker: "Biblioteca"
description: "Obras e traduções reunidas pelo REALMat para leitura e download."
permalink: /livros/
---

{% assign book = site.data.books | first %}

<p class="realmat-page-lead">Cada obra tem uma página própria no portal. Nela você encontra a edição disponível, informações sobre o trabalho e o PDF para leitura no navegador ou download.</p>

<section class="realmat-library" id="catalogo" aria-label="Catálogo de livros">
  <article class="realmat-library__entry">
    <a href="{{ '/livros/forallx/' | relative_url }}" class="image realmat-book-poster realmat-book-poster--small" aria-label="Ver forallx: Lógica">
      <span class="realmat-book-poster__inner">
        <span class="realmat-book-poster__number">01</span>
        <span class="realmat-book-poster__name">forallx</span>
        <span class="realmat-book-poster__subject">lógica formal</span>
        <span class="realmat-book-poster__formula" aria-hidden="true">p → q</span>
        <span class="realmat-book-poster__footer">tradução brasileira</span>
      </span>
    </a>

    <div class="realmat-library__body">
      <header>
        <span class="date">{{ book.subject }} · {{ book.status }}</span>
        <h2><a href="{{ '/livros/forallx/' | relative_url }}">forallx: Lógica</a></h2>
      </header>
      <p>Uma introdução à lógica formal, traduzida e adaptada para o português brasileiro. A edição {{ book.version }} está {{ book.status }}.</p>
      <p class="realmat-meta">Disponível em PDF · acesso aberto · {{ book.version }}</p>
      <ul class="actions">
        <li><a href="{{ '/livros/forallx/' | relative_url }}" class="button primary">Ver a edição</a></li>
        <li><a href="{{ book.pdf_path | relative_url }}" target="_blank" rel="noopener noreferrer">Ler o PDF <span aria-hidden="true">↗</span></a></li>
        <li><a href="{{ book.release_url }}" target="_blank" rel="noopener noreferrer">Ver release e fontes <span aria-hidden="true">↗</span></a></li>
      </ul>
    </div>
  </article>
</section>

<p class="realmat-catalog-note"><span class="date">Próximas obras</span> Novas traduções entrarão no catálogo quando houver uma edição preparada para leitura.</p>
