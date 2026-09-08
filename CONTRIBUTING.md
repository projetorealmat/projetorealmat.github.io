# Como contribuir

O portal REALMat apresenta livros e traduções publicados pelo projeto. O conteúdo editorial de cada obra permanece no repositório próprio do livro; este repositório organiza o catálogo, a navegação e a publicação do site.

## Tipos de contribuição

- correções de navegação, acessibilidade, busca ou layout;
- correções do catálogo e dos metadados de uma edição;
- documentação e melhoria dos testes;
- identificação de links quebrados ou problemas no GitHub Pages.

Correções de tradução, matemática ou LaTeX devem ser propostas no repositório do livro correspondente, como [projetorealmat/forallx](https://github.com/projetorealmat/forallx).

## Fluxo

1. Abra uma issue ou escolha uma tarefa existente.
2. Crie uma branch a partir de `main`.
3. Faça uma alteração pequena e relacionada ao objetivo.
4. Execute os testes locais disponíveis:
   ```sh
   python3 scripts/test_massively_theme.py
   node --check assets/js/realmat-search.js
   ```
5. Abra um pull request para `main` e preencha o checklist.
6. Aguarde o workflow do GitHub Pages e o teste do site gerado.

## Catálogo e publicação

O arquivo [_data/books.json](_data/books.json) é a fonte da versão publicada de cada livro. A referência deve ser uma tag semver ou commit imutável; não use `main`, `master` ou `HEAD`. Cada item também registra o SHA-256 do PDF da release.

O workflow baixa o asset oficial da release e verifica o digest antes de construir o site. Os PDFs em `assets/books/` são artefatos gerados pelo workflow e não devem ser editados manualmente. Para alterar o livro, faça a mudança no repositório da obra, publique uma nova release e depois atualize o catálogo por pull request.

## Licenças

O tema Massively mantém sua licença própria, indicada em [MASSIVELY_LICENSE.txt](MASSIVELY_LICENSE.txt). Cada livro conserva a licença declarada em seu próprio repositório.

## Organização no GitHub Project

Associe issues e pull requests ao Project do REALMat quando ele estiver criado. Para o portal, use labels como `catálogo`, `portal`, `navegação`, `busca`, `acessibilidade`, `release`, `build` e `bloqueado`. Milestones devem representar versões que precisam ser publicadas, como `v0.2.0` e `v1.0.0`.

Alterações ainda incompletas devem ser draft PRs. Ao solicitar revisão, vincule a issue e indique se o catálogo, a release, a busca ou a navegação foram afetados. Consulte [EDITORIAL_WORKFLOW.md](EDITORIAL_WORKFLOW.md) para o fluxo completo.
