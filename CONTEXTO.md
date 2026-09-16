# Contexto do Projeto: Bored of Toast

Este documento define as regras fundamentais e o escopo do projeto, consolidando as definições atuais.

## Identidade Visual e Layout
- O site possui um estilo orgânico: "digital watercolor", textura de caderno desgastado (tattered notebook) e paleta em tons de verde-oliva e terrosos.
- Logo e mascote originais devem ser preservados e exibidos corretamente na navegação.
- O site não utiliza frameworks como React, Vue ou Tailwind. Todo o estilo é feito em CSS puro e vanilla JS.

## Escopo Funcional e Conteúdo
- Todo o conteúdo público do site é escrito em **Inglês**.
- **Aba "Start Here" e "Shopping List" não existem mais na interface atual**.
- Os ingredientes nas receitas **não possuem checkboxes** interativos.
- A interatividade principal foca no ajuste de porções (pessoas) e substituições dinâmicas de ingredientes (*Swap options*). A matemática de rendimento (`data-swap-amount`) acompanha o número de pessoas automaticamente.
- O guia *"The Lunch Edit"* consta como um espaço em desenvolvimento, fora do escopo funcional das rodadas de correção atuais.

## Modelo Editorial
- O conteúdo é produzido por curadoria a partir de fontes públicas creditadas, com síntese editorial própria.
- Toda receita publicada precisa de pelo menos uma fonte externa com link direto e funcional no bloco de fontes.
- Nenhum nome de pessoa real pode ser citado sem link para a publicação onde a informação foi apresentada.
- Ilustrações de etapa são geradas por IA e identificadas como tais. A imagem principal do prato deve ser fotografia real ou licenciada.
- Dados nutricionais são estimativas calculadas a partir de bases de ingredientes, sempre acompanhadas de ressalva.
- O campo status em recipe_models.json controla a exibição de rótulos editoriais. Nenhum rótulo de status deve ser escrito diretamente no HTML.

## Regras de Dados Estruturados
- O JSON-LD é gerado exclusivamente a partir de recipe_models.json. Nenhum dado de receita deve ser duplicado em build.py.
- Ingredientes e passos no schema devem corresponder exatamente ao conteúdo visível, em texto puro, sem marcação HTML.
- aggregateRating só pode ser incluído quando houver avaliações reais coletadas. Nunca gerar valores.
- Campos sem dado confirmado devem ser omitidos do schema, não preenchidos com valor vazio ou provisório.

## Pendências de Validação
- **Validação Visual Pendente**: Em ambientes onde a checagem com um navegador real não é suportada por falta de interface gráfica (ex: execução por agentes automáticos via CLI), a prova definitiva de layout em dispositivos móveis e em resoluções variadas (375x812, 1440x900) dependerá de validação humana posterior, embora os testes em JSDOM garantam a estrutura HTML subjacente.
