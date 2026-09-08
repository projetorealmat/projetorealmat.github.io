# Fluxo editorial e de publicação do REALMat

O portal organiza a descoberta e a leitura das obras. O conteúdo de cada livro é revisado no seu próprio repositório; o catálogo do portal registra releases imutáveis e qual delas deve ser apresentada como atual.

## Organização no GitHub Project

Quando o Project do REALMat estiver criado, issues e pull requests dos dois repositórios devem ser adicionados automaticamente. Os campos recomendados são:

- **Livro/repositório**;
- **Tipo:** tradução, terminologia, revisão linguística, revisão matemática, revisão editorial, LaTeX, portal, build ou release;
- **Etapa:** triagem, em trabalho, em revisão, aprovado ou publicado;
- **Release-alvo**;
- **Responsável**, **revisor**, **capítulo/seção** e **prioridade**.

Use a visão de quadro para o fluxo, a tabela para acompanhar capítulos e a visão agrupada por release para planejar publicações.

## Catálogo versionado

O arquivo `_data/books.json` é a fonte versionada da edição exibida no portal. Cada item representa um livro e contém:

- `current_version`: release recomendada para leitura no momento;
- `releases`: histórico completo das versões publicadas no repositório do livro.

Cada release deve apontar para uma tag semver ou para um SHA completo, nunca para `main`, `master` ou `HEAD`, e deve conter o SHA-256 do PDF publicado. Releases antigas não devem ser removidas quando uma versão nova é publicada: o catálogo mantém os links para permitir citação, comparação e bifurcação.

As páginas em `generated/books/` são geradas a partir do catálogo durante o build. Não edite essas páginas diretamente; altere `_data/books.json` e regenere o site. A página de cada livro apresenta a release atual e o histórico correspondente; **Arquivo**, **Tópicos**, a busca e o rodapé também são derivados do mesmo catálogo.

## Atualização do catálogo

O workflow do portal baixa o asset oficial da release e verifica esse digest antes de construir o site. Assim, o PDF exibido no portal é o mesmo arquivo que pode ser citado e bifurcado no repositório do livro.

Uma release dispara uma proposta automática de atualização do catálogo. O wrapper local chama o workflow reutilizável mantido em [`projetorealmat/.github`](https://github.com/projetorealmat/.github), que faz upsert da nova versão, preserva as versões anteriores e abre um pull request com a identidade da GitHub App organizacional `REALMat Automation`. O auto-merge é solicitado nessa PR, mas só pode ocorrer depois dos checks obrigatórios do portal; não há PAT nem secret de dispatch específico por livro.

## Labels e milestones

Labels recomendadas: `catálogo`, `portal`, `navegação`, `busca`, `acessibilidade`, `release`, `build` e `bloqueado`. Milestones devem corresponder às versões que o portal precisa publicar, como `v0.2.0` e `v1.0.0`.

A configuração detalhada do quadro está em [PROJECT_SETUP.md](PROJECT_SETUP.md).
