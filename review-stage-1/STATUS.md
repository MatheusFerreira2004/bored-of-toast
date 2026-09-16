# Etapa 1 — correções de cor (validação visual pendente)

Arquivos de implementação alterados: dist/style.css e dist/refinements.css.

- Paleta base alinhada à paleta aprovada. Azuis antigos de textos, fundos, bordas e sombras migrados para variáveis semânticas.
- recipe-box e superfícies brancas de tela usam papel quente. Impressão continua branca.
- Pill ativa recebe texto claro explicitamente para superar a regra global nav a com !important.
- Ingredientes marcados mantêm texto secundário legível sem redução adicional de opacidade.
- Logo, imagens, textos, JS, layout e tipografia preservados. Manrope permanece para decisão na Etapa 2.

Verificação: build.py passou (17 rotas); tests/recipe-engine.cjs e tests/recipe-dom.cjs passaram. Comparação estática confirmou manutenção de fontes, dimensões, espaçamentos, grids, proporções e scroll-margin-top. Nenhum dos oito hexadecimais azuis indicados pelo usuário permanece nos CSS.

Limitação: tentativa de abrir http://localhost:8000/recipes/ no navegador retornou net::ERR_BLOCKED_BY_CLIENT. Não houve renderização real nem capturas antes/depois. Não se afirma ausência de outros problemas de contraste, overflow ou sobreposição. A auditoria visual de todas as rotas ainda está pendente.

Próxima ação: comparar visualmente Home, /recipes/, receitas editoriais e tradicionais, Kitchen Notes e páginas institucionais/produto em navegador. Não iniciar Etapa 2 sem confirmação do usuário.

O diff completo está em colors.diff. Os CSS anteriores estão em before/ para comparação ou reversão.
