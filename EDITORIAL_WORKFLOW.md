# Fluxo editorial e de publicação do REALMat

O portal organiza a descoberta e a leitura das obras. O conteúdo de cada livro é revisado no seu próprio repositório; o catálogo do portal registra qual release imutável deve ser publicada.

## Organização no GitHub Project

Quando o Project do REALMat estiver criado, issues e pull requests dos dois repositórios devem ser adicionados automaticamente. Os campos recomendados são:

- **Livro/repositório**;
- **Tipo:** tradução, terminologia, revisão linguística, revisão matemática, revisão editorial, LaTeX, portal, build ou release;
- **Etapa:** triagem, em trabalho, em revisão, aprovado ou publicado;
- **Release-alvo**;
- **Responsável**, **revisor**, **capítulo/seção** e **prioridade**.

Use a visão de quadro para o fluxo, a tabela para acompanhar capítulos e a visão agrupada por release para planejar publicações.

## Atualização do catálogo

O arquivo `_data/books.json` é a fonte versionada da edição exibida no portal. Cada item deve apontar para uma tag semver ou para um SHA completo, nunca para `main`, `master` ou `HEAD`, e deve conter o SHA-256 do PDF publicado na release.

O workflow do portal baixa o asset oficial da release e verifica esse digest antes de construir o site. Assim, o PDF exibido no portal é o mesmo arquivo que pode ser citado e bifurcado no repositório do livro.

Uma release pode disparar uma proposta automática de atualização do catálogo. Essa automação abre um pull request; a publicação continua dependendo da revisão humana e do merge desse PR.

## Labels e milestones

Labels recomendadas: `catálogo`, `portal`, `navegação`, `busca`, `acessibilidade`, `release`, `build` e `bloqueado`. Milestones devem corresponder às versões que o portal precisa publicar, como `v0.2.0` e `v1.0.0`.
