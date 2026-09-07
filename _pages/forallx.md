---
layout: single
title: "forallx: Lógica"
kicker: "Livro em destaque"
description: "Uma tradução e adaptação brasileira de forall x: An Introduction to Formal Logic, em revisão editorial."
permalink: /livros/forallx/
---

{% assign book = site.data.books | where: "id", "forallx" | first %}

<section class="realmat-book-detail" aria-labelledby="forallx-reading-title">
  <div class="realmat-book-detail__cover realmat-book-poster realmat-book-poster--large" role="img" aria-label="Capa tipográfica de forallx: Lógica">
    <span class="realmat-book-poster__inner">
      <span class="realmat-book-poster__number">01</span>
      <span class="realmat-book-poster__name">forallx</span>
      <span class="realmat-book-poster__subject">lógica formal</span>
      <span class="realmat-book-poster__formula" aria-hidden="true">p → q</span>
      <span class="realmat-book-poster__footer">tradução brasileira</span>
    </span>
  </div>

  <div class="realmat-book-detail__copy">
    <header class="major">
      <span class="date">Leitura da edição {{ book.version }} · {{ book.status }}</span>
      <h2 id="forallx-reading-title">Leia no navegador ou baixe o PDF.</h2>
    </header>
    <p>A edição {{ book.version }} está {{ book.status }}. O portal publica o PDF oficial da release declarada no catálogo; o botão de leitura abre esse arquivo no visualizador nativo do navegador e o segundo botão salva uma cópia para consulta offline.</p>
    <ul class="actions">
      <li><a href="{{ book.pdf_path | relative_url }}" class="button primary" target="_blank" rel="noopener noreferrer">Ler no navegador <span aria-hidden="true">↗</span></a></li>
      <li><a href="{{ book.pdf_path | relative_url }}" class="button" download="forallx.pdf">Baixar PDF <span aria-hidden="true">↓</span></a></li>
      <li><a href="{{ book.release_url }}" class="button" target="_blank" rel="noopener noreferrer">Release e fontes <span aria-hidden="true">↗</span></a></li>
    </ul>
    <p class="realmat-note">O arquivo abre em uma nova aba e pode ser baixado pelo próprio navegador.</p>
  </div>
</section>

<hr />

<section class="realmat-facts" aria-label="Informações da edição">
  <div>
    <span class="realmat-facts__number">01</span>
    <h3>Estado</h3>
    <p>Tradução e adaptação brasileira {{ book.status }}, versão {{ book.version }}.</p>
  </div>
  <div>
    <span class="realmat-facts__number">02</span>
    <h3>Origem</h3>
    <p>Baseado em <em>forall x: An Introduction to Formal Logic</em>, de P. D. Magnus.</p>
  </div>
  <div>
    <span class="realmat-facts__number">03</span>
    <h3>Formato</h3>
    <p>PDF de acesso aberto para leitura no navegador e estudo offline.</p>
  </div>
</section>

<section class="realmat-callout" aria-labelledby="forallx-contribute-title">
  <div>
    <span class="date">Participação</span>
    <h2 id="forallx-contribute-title">Encontrou uma correção ou quer colaborar?</h2>
  </div>
  <div>
    <p>As discussões, orientações e fontes do projeto estão na área de contribuição.</p>
    <a href="{{ '/contribuir/' | relative_url }}" class="button">Como contribuir <span aria-hidden="true">↗</span></a>
  </div>
</section>
