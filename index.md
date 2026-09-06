---
layout: home
title: "REALMAT"
description: "Recursos Educacionais Abertos de Matemática para ensino, estudo e tradução."
permalink: /
---

<div class="realmat-home__shell">
  <section class="realmat-editorial-intro" aria-labelledby="realmat-home-title">
    <div>
      <p class="realmat-kicker">Biblioteca aberta</p>
      <h1 id="realmat-home-title">Matemática em português para ler e ensinar.</h1>
    </div>
    <div class="realmat-editorial-intro__aside">
      <p>O REALMAT reúne livros e traduções para quem estuda, ensina e quer ampliar o acesso ao conhecimento matemático.</p>
      <a class="realmat-button realmat-button--primary" href="{{ '/livros/' | relative_url }}">Ver os livros</a>
    </div>
  </section>

  <section id="destaque" class="realmat-featured" aria-labelledby="realmat-featured-title">
    <div class="realmat-section-bar">
      <span class="realmat-kicker">Em destaque</span>
      <span class="realmat-section-bar__note">01 · livro traduzido</span>
    </div>

    <div class="realmat-featured__grid">
      <a class="realmat-cover realmat-cover--forallx" href="{{ '/livros/forallx/' | relative_url }}" aria-label="Ver forallx: Lógica">
        <span class="realmat-cover__number">01</span>
        <span class="realmat-cover__name">forallx</span>
        <span class="realmat-cover__subject">lógica formal</span>
        <span class="realmat-cover__formula" aria-hidden="true">p → q</span>
        <span class="realmat-cover__footer">tradução brasileira</span>
      </a>

      <div class="realmat-featured__copy">
        <p class="realmat-kicker">Livro em revisão editorial</p>
        <h2 id="realmat-featured-title">forallx: Lógica</h2>
        <p>Uma introdução à lógica formal, traduzida e adaptada para o português brasileiro. A edição atual pode ser consultada no portal e baixada para estudo offline.</p>
        <p class="realmat-meta">Livro · tradução · acesso aberto</p>
        <div class="realmat-actions">
          <a class="realmat-button realmat-button--primary" href="{{ '/livros/forallx/' | relative_url }}">Ver a edição</a>
          <a class="realmat-text-link" href="{{ '/assets/books/forallx.pdf' | relative_url }}" target="_blank" rel="noopener noreferrer">Ler o PDF <span aria-hidden="true">↗</span></a>
        </div>
      </div>
    </div>
  </section>

  <section class="realmat-home-guidance" aria-label="Caminhos do portal">
    <article>
      <p class="realmat-kicker">Para estudar</p>
      <h2>Leia no portal, baixe quando precisar.</h2>
      <p>O catálogo leva às páginas de cada obra, com informações sobre a edição e acesso direto ao PDF.</p>
      <a class="realmat-text-link" href="{{ '/livros/' | relative_url }}">Abrir a biblioteca <span aria-hidden="true">↗</span></a>
    </article>
    <article>
      <p class="realmat-kicker">Para participar</p>
      <h2>Contribua no espaço de cada projeto.</h2>
      <p>As orientações gerais e os links para discussões e arquivos-fonte ficam reunidos em uma única página.</p>
      <a class="realmat-text-link" href="{{ '/contribuir/' | relative_url }}">Como contribuir <span aria-hidden="true">↗</span></a>
    </article>
  </section>
</div>
