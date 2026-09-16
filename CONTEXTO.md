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
- Todas as receitas são tratadas como **"Development editions"**; não fazemos alegações de que passaram por testes intensivos de cozinha (kitchen testing).
- O guia *"The Lunch Edit"* consta como um espaço em desenvolvimento, fora do escopo funcional das rodadas de correção atuais.

## Pendências de Validação
- **Validação Visual Pendente**: Em ambientes onde a checagem com um navegador real não é suportada por falta de interface gráfica (ex: execução por agentes automáticos via CLI), a prova definitiva de layout em dispositivos móveis e em resoluções variadas (375x812, 1440x900) dependerá de validação humana posterior, embora os testes em JSDOM garantam a estrutura HTML subjacente.
