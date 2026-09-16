# Pipeline de Produção — Bored of Toast

Processo para produzir receitas em volume sem perder qualidade. Complementa `CONTEXTO.md` e `GUIA-VISUAL.md`.

Premissa central: o gargalo não é a geração, é a revisão. A geração de uma receita leva minutos; o QC leva de 8 a 12. Se o volume pressionar, reduza volume — não reduza QC.

---

## Visão geral dos quatro estágios

| Estágio | Responsável | Tempo por receita |
| --- | --- | --- |
| 1. Coleta de fontes | Humano | 5–8 min |
| 2. Geração do rascunho | IA | 2–3 min |
| 3. QC automatizado | Build e testes | segundos |
| 4. QC humano | Humano | 8–12 min |

Total realista: 15 a 25 minutos por receita. Para 10 receitas por semana, reserve de 3 a 4 horas.

---

## Estágio 1 — Coleta de fontes

Antes de gerar qualquer coisa, reunir de 3 a 5 fontes reais da mesma receita.

O que registrar para cada fonte:
- Título exato da receita ou artigo
- Nome da publicação
- URL completa e funcional
- O que especificamente essa fonte informou (proporção, técnica, tempo, dica)

Publicações de referência em inglês, com boa reputação editorial:
- Serious Eats — forte em explicação técnica
- America's Test Kitchen — receitas testadas com metodologia
- EatingWell — bom em nutrição e porções
- Love and Lemons — forte em vegetariano
- King Arthur Baking — referência em panificação
- NYT Cooking — amplo, exige assinatura para algumas páginas

Regra de ouro: nenhum nome de pessoa real vai ao ar sem link direto para onde ela disse aquilo. Se não há link, apresentar como técnica geral, sem atribuição nominal.

### O ângulo que gera valor

Reescrever uma receita não adiciona nada — o original já está indexado. O que diferencia é a síntese comparativa.

Fraco: pegar uma receita, reescrever, creditar.

Forte: comparar 4 ou 5 versões, identificar onde divergem e explicar o trade-off. "Três das cinco receitas usam polvilho doce; duas misturam com azedo. A diferença está na elasticidade."

Esse formato é o que a IA faz bem e o que nenhum concorrente genérico tem.

---

## Estágio 2 — Geração do rascunho

Copiar `templates/receita-modelo.json`, renomear a chave para o slug e preencher via IA a partir das fontes coletadas.

A IA preenche: intro, why_it_works, steps com cue sensorial, ingredientes, swaps, FAQ, keywords.

A IA **não** preenche, por decisão de arquitetura:
- `date_published` e `date_modified`
- Valores de `nutrition`
- Campos de `sources`

Esses campos vêm com `[PREENCHER` no template e travam o build até serem substituídos por dado verificado. É a barreira técnica que impede conteúdo não verificado de ir ao ar.

### Ferramenta para nutrição

Usar calculadora real, não estimativa da IA. Opções gratuitas:
- Nutritionix (nutritionix.com) — busca por ingrediente com quantidade
- USDA FoodData Central (fdc.nal.usda.gov) — base oficial
- Cronometer — permite montar receita completa

Marcar sempre `is_estimate: true`. É a prática padrão do nicho e protege contra alegação de precisão.

---

## Estágio 3 — QC automatizado

Roda sem intervenção humana. Executar antes de qualquer commit:

```
python build.py
python tests/test_build.py
```

O que é verificado automaticamente:
- Nenhum `[PREENCHER` remanescente em qualquer campo
- Nenhum placeholder gravado em `dist/`
- Estrutura do `<ul>` de ingredientes íntegra
- JSON-LD sem strings vazias
- Nenhum literal de código Python no HTML
- Linha de metadados dos cards sem separadores órfãos
- `nutrition` omitido do schema quando não houver valores reais

Se o build falhar, ele imprime a árvore de campos pendentes. Corrigir e rodar novamente.

---

## Estágio 4 — QC humano

O que a máquina não pega. Reservar de 8 a 12 minutos e seguir a lista.

### Coerência técnica

- [ ] Temperaturas e tempos conferem com pelo menos duas fontes
- [ ] Proporções fazem sentido na prática (atenção a vinagrete: padrão é 3:1 óleo/ácido, salvo fonte em contrário)
- [ ] A soma dos ingredientes é coerente com o rendimento declarado
- [ ] `prep_time` + `cook_time` = `total_time`
- [ ] O escalonamento de porções produz números plausíveis em 1, 2, 4 e 6 pessoas

### Fontes e atribuição

- [ ] Toda URL de fonte abre e leva à página correta
- [ ] Nenhum nome de pessoa real sem link correspondente
- [ ] O texto não parafraseia nenhuma fonte de perto — é síntese própria
- [ ] O campo `note` de cada fonte descreve o que ela especificamente informou

### Conteúdo

- [ ] `intro` entre 100 e 150 palavras, sem linguagem promocional
- [ ] `why_it_works` entre 200 e 300 palavras, com explicação técnica real
- [ ] Cada passo tem `cue` sensorial observável, não apenas tempo
- [ ] FAQ com 3 a 5 perguntas que alguém realmente faria
- [ ] Total de 900 a 1.400 palavras úteis na página
- [ ] Inglês natural, sem construção que soe traduzida

### Imagens

- [ ] Hero é foto real ou licenciada, e corresponde à receita descrita
- [ ] Licença do hero registrada em `assets/LICENCAS.md`
- [ ] Ilustrações de etapa seguem o DNA visual do `GUIA-VISUAL.md`
- [ ] Cada imagem de etapa mostra o que o texto descreve
- [ ] Nenhuma imagem com texto, mãos, rosto ou alimento cru
- [ ] `alt` descritivo em todas
- [ ] `is_ai_generated: true` nas etapas, ausente no hero

### Validação final

- [ ] Rich Results Test aprova o Recipe e o FAQPage
- [ ] PageSpeed: LCP abaixo de 2,5s e CLS abaixo de 0,1
- [ ] Links internos de `related_notes` e `related_recipes` funcionam

---

## Publicação em lotes temáticos

Não publicar receitas avulsas. Um lote = 8 receitas + 2 kitchen notes do mesmo tema.

Vantagens:
- Links internos surgem naturalmente
- Concentra autoridade tópica em um assunto
- Revisão mais eficiente, porque você permanece no mesmo contexto
- Gera material coerente para uma campanha de Pinterest

Sugestão de clusters, em ordem de potencial em inglês:
1. Air fryer — maior volume de busca e melhor conversão de produto digital
2. Receitas de 15 minutos
3. Meal prep e make-ahead
4. Alto teor de proteína vegetal
5. Café da manhã antecipado

---

## Distribuição

### Pinterest — canal principal

- 3 a 5 pins por página, cada um com ângulo diferente
- Formato 2:3, texto legível em thumbnail
- Gráficos editoriais (tabelas, matrizes, comparativos) tendem a performar melhor que foto de prato, porque entregam utilidade no próprio pin
- Distribuir ao longo de semanas, não publicar tudo de uma vez

### Facebook — secundário

- Carrosséis de dica entregam cerca de 80% do valor; a página expande com o porquê
- Menor páginas por sessão que o Pinterest, mas útil para alcance inicial

Segmentar métricas por fonte sempre. Pinterest e Facebook divergem muito em RPM e páginas por sessão, e a decisão de onde investir esforço sai daí.

---

## Métricas de acompanhamento

Por fonte de tráfego, semanalmente:

- RPM da sessão
- Páginas por sessão
- Tempo de engajamento
- Taxa de retorno de usuário
- Taxa de conversão da captura de e-mail

A alavanca mais barata de receita é páginas por sessão. Sair de 1,2 para 1,8 representa cerca de 50% mais receita sem nenhum tráfego novo — e depende quase só de links internos bem colocados.

---

## Escada de redes de anúncio

| Rede | Mínimo | RPM típico em food |
| --- | --- | --- |
| AdSense / Ezoic | sem mínimo | US$ 5–15 |
| Monumetric | 10 mil pageviews/mês | US$ 10–20 |
| Journey by Mediavine | 10 mil sessões/mês | US$ 15–25 |
| Mediavine | 50 mil sessões/mês | US$ 20–40 |
| Raptive | 100 mil pageviews/mês | US$ 25–45 |

Dois fatores de contexto:

- Tráfego de Pinterest e Facebook converte em RPM mais baixo que busca orgânica. Os números acima assumem mix com orgânico, então vale trabalhar SEO em paralelo desde o início.
- Sazonalidade é acentuada. Novembro e dezembro chegam ao dobro do RPM de janeiro. Ter tráfego maduro entrando em outubro faz diferença relevante no ano.

---

## Pré-requisitos para aplicar ao AdSense

- [ ] 25 a 40 páginas publicadas, organizadas em 3 ou 4 clusters
- [ ] Nenhum rótulo de status de desenvolvimento no ar
- [ ] Byline com pessoa real em todas as páginas
- [ ] About com autor identificado
- [ ] Contact com canal funcional
- [ ] Privacy Policy com cláusula CCPA/CPRA
- [ ] Terms of Use
- [ ] Ad e Affiliate Disclosure
- [ ] CMP certificado pelo Google (Funding Choices resolve gratuitamente)
- [ ] Canonical apontando para o domínio final
- [ ] Recipe schema validado em todas as receitas
- [ ] Bloco de fontes em todas as receitas
- [ ] LCP abaixo de 2,5s e CLS abaixo de 0,1
