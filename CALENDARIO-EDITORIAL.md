# Calendário Editorial — Bored of Toast

Planejamento de conteúdo por formato, com a estratégia de design para cada tipo novo.

Premissa: o conteúdo de maior alavancagem hoje não é receita. Receita exige foto real do prato, que depende de banco licenciado. Conteúdo de referência e comparação não tem essa dependência, é mais fácil de ranquear e performa melhor no Pinterest.

---

## Parte 1 — Estratégia de design para formatos novos

### O princípio

Nenhum formato novo inventa layout próprio. Todo conteúdo novo é montado a partir dos componentes que já existem no site. Isso preserva a identidade editorial e evita que o CSS cresça de forma desordenada.

### Componentes já existentes e reaproveitáveis

Levantados a partir das páginas publicadas:

| Componente | Onde existe hoje | Reuso proposto |
| --- | --- | --- |
| Numeração de seção (`01 /`, `02 /`) | Home | Abertura de qualquer página de referência |
| Passo numerado com `Look for` | Kitchen notes | Guias de técnica |
| Bloco `AVOID THIS` / `TRY THIS INSTEAD` | `keep-salad-crisp` | Conteúdo de erro comum e comparativos |
| Bloco `MAKE SUBSTITUTIONS` | `keep-salad-crisp` | Tabelas de substituição |
| `FROM NOTEBOOK TO TABLE` com links | Kitchen notes | Fechamento com links internos |
| Tabela de nutrição (`nut-row`) | Receitas | Base para qualquer tabela de dados |
| Bloco de fontes | Receitas | Todo conteúdo de referência |
| Selo `AI-generated` | Ilustrações de etapa | Gráficos editoriais |

Observação relevante: o padrão `nut-row` da tabela de nutrição já resolve linha de dados com rótulo e valor. Tabelas de referência devem partir dele, não de uma estrutura nova.

### O que exige componente novo

Apenas um: **tabela comparativa de múltiplas colunas**. A `nut-row` é de duas colunas; uma tabela de conversão forno para air fryer precisa de três ou mais.

Proposta de implementação:
- Novo arquivo `reference.css`, seguindo o padrão de `recipe.css` e `refinements.css`
- Nenhuma alteração em `style.css`, para não afetar páginas existentes
- Herdar as variáveis de cor, tipografia e espaçamento já definidas
- Responsivo por rolagem horizontal no mobile, não por reflow — tabela de conversão perde sentido se quebrar linha

### Refinamentos de design já identificados

Pontos levantados nas auditorias que valem atenção ao evoluir o layout:

1. Margens laterais vazias no desktop. A coluna de conteúdo é estreita e há faixa ampla de cada lado. É onde entra o sticky do right rail, a unidade de maior RPM em culinária.
2. Containers de anúncio precisam de altura reservada. Sem isso, CLS sobe e afeta tanto Core Web Vitals quanto elegibilidade em redes premium.
3. Bloco de receitas relacionadas ainda não existe. É a alavanca mais barata de páginas por sessão.
4. Incoerência de identidade pendente: o `CONTEXTO.md` descreve "digital watercolor, caderno desgastado", mas os assets publicados seguem direção fotográfica. Decidir antes de gerar imagem em volume.

---

## Parte 2 — Conteúdo de referência

Prioridade máxima. Não depende de foto de prato, vira pin direto, atrai links de entrada.

Estrutura de página, reaproveitando componentes:
- Abertura com numeração de seção
- Parágrafo de contexto (100 a 150 palavras)
- A tabela, em componente novo `reference-table`
- Bloco de ressalvas no padrão `AVOID THIS` / `TRY THIS INSTEAD`
- Fechamento `FROM NOTEBOOK TO TABLE` com links para receitas que usam aquilo
- Bloco de fontes

Peças planejadas:

1. Oven to air fryer conversion — já detalhada em `clusters/01-air-fryer.md`
2. Bean cooking chart — tempo de cozimento por leguminosa, seca e em lata
3. Can-to-cup conversions — rendimento de latas de 15 oz em xícaras e gramas
4. Herb substitution chart — fresco para seco, proporção 3:1 e os casos em que não se aplica
5. Pantry protein comparison — proteína por porção entre grão-de-bico, lentilha, edamame, tofu e feijão
6. How long does it keep — conservação por tipo de prato, com base em orientação da FDA

---

## Parte 3 — Kitchen Notes

Doze já publicadas. É o melhor recurso do site: evergreen, sem dependência de foto de prato, e sustenta links internos.

Estrutura já existe e funciona. Reaproveitar integralmente.

Peças planejadas:

1. Why your beans are bland — temperar a água de cozimento, não apenas o prato final
2. The two-minute rule for garlic — quando entra e por que queima
3. How to dry greens without a spinner
4. Salt: when to add it and why timing matters
5. Why acid at the end changes everything
6. Why food doesn't crisp in the air fryer — já no cluster 01

---

## Parte 4 — One Ingredient, Different Ways

A categoria já existe no site e está subutilizada. É o formato que constrói autoridade tópica mais rápido.

Vantagem de produção: a página pilar não exige imagem nova. Usa os heros das receitas que já linka.

Estrutura: abertura com numeração de seção, parágrafo de contexto, grade de cards de receita (componente já existente na home e na listagem), fechamento com links.

Peças planejadas:

1. Chickpeas, 5 ways — pilar ligando salada, hummus, assado, air fryer e uma quinta preparação
2. One can of white beans, 4 dinners
3. A bag of lentils, 5 meals

---

## Parte 5 — Comparativos

Formato que aproveita diretamente o modelo de curadoria de múltiplas fontes. Gera conteúdo que não existia antes da síntese.

Estrutura: abertura, contexto, tabela comparativa, bloco de veredito no padrão `TRY THIS INSTEAD`, fontes.

Peças planejadas:

1. Oven vs air fryer: crispy chickpeas compared
2. Canned vs dried beans: cost, time and texture
3. Five versions of overnight oats, and which one holds up
4. Feta vs goat cheese vs avocado in a grain bowl

---

## Parte 6 — Conteúdo que alimenta o produto digital

"The Lunch Edit" já existe como espaço no site. Estes conteúdos criam demanda e coletam sinal sobre o que a audiência quer comprar.

Cada peça com captura de e-mail oferecendo a versão em PDF.

Peças planejadas:

1. Five lunches from one grocery run
2. Sunday prep, weekday lunches — três tarefas no domingo, cinco almoços
3. The six-ingredient pantry that covers ten meals

Decisão sobre o produto pago deve sair dos dados: as páginas com mais tráfego, tempo de leitura e salvamento no Pinterest indicam o tema. Com 300 a 500 assinantes, perguntar diretamente à lista vale mais que qualquer estimativa.

---

## Parte 7 — Calendário sazonal

RPM em novembro e dezembro chega ao dobro de janeiro. Conteúdo sazonal precisa de 6 a 8 semanas de antecedência para amadurecer em busca e Pinterest.

| Publicar em | Tema |
| --- | --- |
| Setembro e outubro | Make-ahead breakfasts, lunchbox, comfort food |
| Outubro e novembro | Acompanhamentos de Thanksgiving em versão plant-forward, uso de sobras |
| Dezembro | Refeições simples entre feriados |
| Janeiro | High-protein, meal prep, pantry reset |

---

## Sequência recomendada

1. Cluster 01 (air fryer), com a tabela de conversão adiantada — é o maior gerador de salvamento do lote
2. Cluster de referência puro: quatro a cinco tabelas. Lote mais rápido de produzir e maior retorno por esforço
3. Cluster de comparativos, aproveitando as receitas já publicadas
4. A partir daí, sazonal conforme o calendário

Ao fim dos dois primeiros clusters o site chega à faixa de 30 páginas, que é o alvo para aplicar ao AdSense.

---

## Matriz de dependência de imagem

Referência para planejar produção. Peças sem dependência de foto real são as de execução mais rápida.

| Formato | Foto real | Gráfico por IA | Ilustração de etapa |
| --- | --- | --- | --- |
| Receita | Obrigatória no hero | Opcional | Sim |
| Tabela de referência | Não | Obrigatório | Não |
| Kitchen note | Não | Opcional | Sim |
| One ingredient | Reusa existentes | Opcional | Não |
| Comparativo | Reusa existentes | Obrigatório | Não |

Conclusão prática: de cada dez peças publicadas, apenas as receitas exigem licenciamento de foto nova. Os outros formatos avançam sem esse gargalo.
