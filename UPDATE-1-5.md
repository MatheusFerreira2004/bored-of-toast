# Atualização 1–5

1. Paleta centralizada em style.css; regras do modelo editorial reunidas em recipe.css. Correção de texto escuro explícita nas receitas. Existem estilos históricos de componentes antigos que ainda podem ser removidos em uma revisão posterior.
2. Oito receitas usam um renderer e motor de pessoas compartilhados. recipe_adapter.py mantém os dados das seis receitas em build.py. Medidas métricas acompanham quantidades; tamanhos de embalagem continuam fixos. As dicas de substituição dessas seis receitas são texto, sem botões que simulem substituição automática. Preparos e conteúdo continuam em desenvolvimento.
3. Home com três receitas e link View all 8 recipes. Kitchen Notes fica acessível mais cedo. Catálogo continua com oito cards.
4. Filtros medem o cabeçalho com ResizeObserver e após carregamento das fontes. Sem JavaScript ficam no fluxo. Cards hidden não ficam visíveis por causa de display:grid/flex.
5. Oito imagens culinárias convertidas para WebP em 480, 800 e 1200 px, servidas por srcset/sizes. Os cinco PNG novos somavam 12.354.433 bytes; suas versões de 800 px somam 200.328 bytes (98,4% menos bytes). Comparação de arquivos, não de tempo de carregamento medido. Originais preservados fora de dist.

## Verificação

- build.py: 17 rotas geradas.
- recipe-engine.cjs, recipe-dom.cjs e all-recipes.cjs: passaram.
- Inspeção estática: oito modelos únicos, três cards na home, imagens e candidatos srcset presentes, nenhum checkbox legado nas receitas.
- Navegador: tentativa de http://localhost:8000/recipes/ retornou net::ERR_BLOCKED_BY_CLIENT. Não houve validação visual real ou teste de sobreposição mobile.
- O conteúdo culinário foi preservado; as receitas ainda precisam de testes de cozinha e revisão editorial antes da publicação.

## Arquivos principais

build.py, pilot_recipe.py, recipe_adapter.py, optimize_images.py, dist/style.css, dist/refinements.css, dist/recipe.css, dist/site.js, dist/recipe-engine.js, tests/all-recipes.cjs e páginas geradas.

Para abrir: python serve.py. Para gerar: python build.py. ImageMagick só é necessário para regenerar imagens com python optimize_images.py, não para abrir/compilar o site.
