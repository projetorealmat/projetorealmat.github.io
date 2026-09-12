---
layout: home
title: "REALMat"
description: "Recursos Educacionais Abertos na Licenciatura em Matemática"
permalink: /
---

{% assign featured_book = site.data.books | first %}
{% assign featured_release = featured_book.releases | where: "version", featured_book.current_version | first %}
{% assign featured_stage = site.data.translation_stages | where: "id", featured_release.translation_stage | first %}
{% assign featured_url = '/livros/' | append: featured_book.id | append: '/' %}

<article class="post featured realmat-home" aria-labelledby="realmat-featured-title">
  <header class="major">
    <span class="date">Biblioteca aberta · {{ featured_release.version }} · {{ featured_stage.label }}</span>
    <h2 id="realmat-featured-title"><a href="{{ featured_url | relative_url }}">{{ featured_book.title }}<br />para ler e ensinar</a></h2>
    <p>Livros e traduções de matemática em acesso aberto, com edições preparadas para leitura e colaboração. A obra em destaque é {{ featured_book.title }}.</p>
  </header>

  <figure class="realmat-logo-hero">
    <img src="{{ '/assets/images/realmat-logo.jpg' | relative_url }}" alt="Logomarca REALMat com um livro aberto e elementos matemáticos" loading="lazy">
  </figure>

  <a href="{{ featured_url | relative_url }}" class="image main realmat-book-poster" aria-label="Conheça {{ featured_book.title }}">
    <span class="realmat-book-poster__inner">
      <span class="realmat-book-poster__number">01</span>
      <span class="realmat-book-poster__name">{{ featured_book.short_title }}</span>
      <span class="realmat-book-poster__subject">{{ featured_book.subject }}</span>
      <span class="realmat-book-poster__formula" aria-hidden="true">p → q</span>
      <span class="realmat-book-poster__footer">edição {{ featured_release.version }}</span>
    </span>
  </a>

  <ul class="actions special">
    <li><a href="{{ '/livros/' | relative_url }}" class="button primary large">Ver os livros</a></li>
    <li><a href="{{ featured_url | relative_url }}" class="button" >Abrir a edição <span aria-hidden="true">↗</span></a></li>
  </ul>
</article>

<section class="posts realmat-home-posts" aria-label="Caminhos do portal">
  <article>
    <header>
      <span class="date">Para estudar</span>
      <h2><a href="{{ '/livros/' | relative_url }}">Livros<br />e traduções</a></h2>
    </header>
    <div class="realmat-card-mark" aria-hidden="true">01</div>
    <p>Encontre cada obra no portal, leia a edição disponível no navegador ou baixe o PDF para estudar offline.</p>
    <ul class="actions special"><li><a href="{{ '/livros/' | relative_url }}" class="button">Abrir a biblioteca</a></li></ul>
  </article>

  <article>
    <header>
      <span class="date">Para participar</span>
      <h2><a href="{{ '/contribuir/' | relative_url }}">Contribua<br />com um projeto</a></h2>
    </header>
    <div class="realmat-card-mark" aria-hidden="true">02</div>
    <p>Veja as orientações gerais e siga para as discussões e arquivos-fonte do livro que deseja ajudar a construir.</p>
    <ul class="actions special"><li><a href="{{ '/contribuir/' | relative_url }}" class="button">Como contribuir</a></li></ul>
  </article>

  <article>
    <header>
      <span class="date">O projeto</span>
      <h2><a href="{{ '/sobre/' | relative_url }}">Acesso aberto<br />à matemática</a></h2>
    </header>
    <div class="realmat-card-mark" aria-hidden="true">03</div>
    <p>Conheça os princípios do REALMat e a forma como cada tradução é organizada, revisada e publicada.</p>
    <ul class="actions special"><li><a href="{{ '/sobre/' | relative_url }}" class="button">Conhecer o REALMat</a></li></ul>
  </article>

  <article>
    <header>
      <span class="date">Navegação</span>
      <h2><a href="{{ '/buscar/' | relative_url }}">Encontre uma<br />página</a></h2>
    </header>
    <div class="realmat-card-mark" aria-hidden="true">04</div>
    <p>Pesquise livros, páginas e assuntos no conteúdo público do portal.</p>
    <ul class="actions special"><li><a href="{{ '/buscar/' | relative_url }}" class="button">Buscar no portal</a></li></ul>
  </article>
</section>
