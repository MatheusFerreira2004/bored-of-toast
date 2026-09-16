# Modelo flexível — duas receitas

## Fonte de conteúdo
`recipe_models.json` é a fonte dos ingredientes estruturados, substituições, tempos, fases, etapas e orientações das duas receitas editoriais. `build.py` conserva títulos, slugs, categorias e imagens principais. `pilot_recipe.py` renderiza qualquer entrada desse arquivo.

## Campos
- `base_people`, `max_people`, `meal_role`: rendimento e limites.
- `times`: lista de pares label/value. Preparo, cozimento, descanso e total podem ser incluídos conforme necessário; nunca são multiplicados pelo seletor.
- `batch_default`, `batch`: orientação normal e aviso acima de determinado número de pessoas.
- `ingredients`: quantidade e unidade, equivalente métrico e unidade métrica; group inicia um grupo, scale=whole arredonda itens inteiros. Sem qty significa quantidade a gosto. package descreve o tamanho fixo de cada embalagem.
- `swap`: quantidade, nome, efeito no prato, técnica, step_notes e step_overrides por ID de etapa. method_name preenche os tokens {{id}} usados nas instruções. Avaliar compatibilidade antes de cadastrar trocas combináveis.
- `steps`: lista livre; id estável, título, ação, phase opcional, duration opcional, cue/care opcionais, image/alt opcionais. Sem imagem não há espaço vazio.
- Campos de servir, variação, antecipação e conservação são específicos de cada receita.

## Duas receitas
Salada: três etapas, dois grupos, sem cozimento, duas ilustrações de técnica. Frigideira: cinco etapas em três fases, três grupos, preparo ~5 min e cozimento ~10 min; total ~15 min. Nenhum tempo está validado por teste culinário.

## Comportamento
`dist/recipe-engine.js` calcula quantidades e resolve os textos. `dist/pilot.js` aplica o resultado à página, incluindo desfazer. A interface atual não exibe lista de compras. As escolhas de pessoas/substituições persistem por receita na sessão atual.

## Continuar no Antigravity
Execute `py build.py`, depois `py serve.py`. Para validar a lógica, com Node disponível: `node tests/recipe-engine.cjs` e `node tests/recipe-dom.cjs`, a partir da raiz do projeto. Não é necessário instalar pacotes.

## Limites de verificação
Build, referências locais e testes de lógica aprovados. Revisão visual automatizada em navegador e impressão continuam pendentes. As duas receitas e suas substituições aguardam testes de cozinha. A receita de frigideira usa a imagem principal existente; não foram geradas ilustrações de etapas nesta atualização.
