# Configuração do GitHub Project do REALMat

Esta configuração é feita uma única vez na organização `projetorealmat`.

## Criação

1. Abra **Projects** na organização e crie um projeto chamado `REALMat — produção editorial`.
2. Escolha a visualização inicial em quadro.
3. Adicione os repositórios `projetorealmat/forallx` e `projetorealmat/projetorealmat.github.io`.
4. Configure a entrada automática de issues e pull requests desses dois repositórios.

## Campos

- **Livro/repositório** — texto ou seleção;
- **Tipo** — tradução, terminologia, revisão linguística, revisão matemática, revisão editorial, LaTeX, portal, build e release;
- **Etapa** — triagem, em trabalho, em revisão, aprovado e publicado;
- **Capítulo/seção** — texto;
- **Responsável** e **revisor** — pessoas;
- **Release-alvo** — texto ou seleção;
- **Prioridade** — baixa, normal, alta e bloqueadora.

## Visualizações

- **Fluxo editorial:** quadro agrupado por etapa;
- **Acompanhamento por livro:** tabela agrupada por livro e capítulo;
- **Próxima release:** tabela filtrada pela release-alvo;
- **Fila de revisão:** quadro filtrado por etapa de revisão e revisor.

## Automação recomendada

- issue nova → `Triagem`;
- pull request aberta → `Em revisão`;
- issue fechada ou pull request merged → `Publicado`;
- item concluído → arquivar depois de alguns dias;
- mantenha decisões terminológicas e editoriais vinculadas à issue que as originou.

Os labels e milestones básicos são mantidos nos próprios repositórios por workflows versionados. O Project deve cuidar do fluxo entre os repositórios, não substituir as issues nem o histórico das releases.

## Permissões da sincronização automática

Para que o workflow `catalog-sync.yml` consiga publicar a branch e abrir o pull request, no repositório do portal ajuste **Settings → Actions → General**:

- em **Workflow permissions**, selecione **Read and write permissions**;
- habilite **Allow GitHub Actions to create and approve pull requests**, se essa opção estiver disponível.

No repositório `projetorealmat/forallx`, crie o secret `PORTAL_DISPATCH_TOKEN` com permissão de conteúdo no repositório do portal. Sem esse secret, releases continuam funcionando e a atualização do catálogo permanece manual.
