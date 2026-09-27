---
title: "Como contribuir"
kicker: "Participar"
description: "Orientações gerais e caminhos de colaboração para os projetos do REALMat."
permalink: /contribuir/
---

<p class="realmat-page-lead">Participe da revisão, adaptação e manutenção das obras do REALMat. O portal é o espaço de leitura. Esta página reúne o fluxo geral para editar, revisar e publicar as obras; cada página de livro encaminha para o repositório correspondente.</p>

{% for book in site.data.books %}
  {% assign current = book.releases | where: "version", book.current_version | first %}
  {% assign stage = site.data.translation_stages | where: "id", current.translation_stage | first %}
<section class="realmat-contribution" id="projeto-{{ book.id }}" aria-labelledby="contribute-{{ book.id }}-title">
  <div>
    <span class="date">Projeto de tradução · {{ current.version }} · {{ stage.label }}</span>
    <h2 id="contribute-{{ book.id }}-title">{{ book.title }}</h2>
  </div>
  <div class="realmat-contribution__links">
    <a href="https://github.com/{{ current.repository }}/issues" class="button primary" target="_blank" rel="noopener noreferrer">Discussões e correções <span aria-hidden="true">↗</span></a>
    <a href="https://github.com/{{ current.repository }}" class="button" target="_blank" rel="noopener noreferrer">Repositório da edição <span aria-hidden="true">↗</span></a>
  </div>
</section>
{% endfor %}

<hr />

{% assign first_book = site.data.books | first %}
{% assign first_book_url = '/livros/' | append: first_book.id | append: '/' %}
<section class="realmat-process" aria-labelledby="contribute-process-title">
  <header class="major">
    <span class="date">Fluxo de colaboração</span>
    <h2 id="contribute-process-title">Como participar</h2>
  </header>
  <ol>
    <li>Escolha uma obra e leia a edição disponível na <a href="{{ first_book_url | relative_url }}">página do livro</a>.</li>
    <li>Para relatar uma dúvida, correção ou sugestão, abra uma discussão (<em>issue</em>) no repositório correspondente.</li>
    <li>Para editar os arquivos-fonte, crie uma cópia do repositório (<em>fork</em>) se necessário e trabalhe em um ramo próprio (<em>branch</em>), sem alterar diretamente o ramo principal.</li>
    <li>Mantenha o formato dos arquivos-fonte e o processo de compilação definidos para a obra; atualize os metadados da edição quando necessário e execute as verificações locais disponíveis.</li>
    <li>Envie uma proposta de alteração (<em>pull request</em> ou PR) com a justificativa e aguarde as verificações automáticas e a revisão editorial.</li>
    <li>Depois da aprovação, a equipe do projeto decide se incorpora a alteração e publica uma nova edição.</li>
  </ol>
</section>

<section class="realmat-guidelines" aria-labelledby="guidelines-title">
  <header class="major">
    <span class="date">Boas práticas</span>
    <h2 id="guidelines-title">Colabore com clareza.</h2>
  </header>
  <ul>
    <li>explique o motivo de cada alteração;</li>
    <li>preserve a formatação e a notação matemática;</li>
    <li>indique a fonte quando sugerir uma mudança;</li>
    <li>faça alterações pequenas e fáceis de revisar;</li>
    <li>respeite a licença e os créditos de cada material.</li>
  </ul>
</section>
