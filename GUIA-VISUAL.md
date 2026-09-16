# Guia Visual — Bored of Toast

Documento de referência para produção de imagens em volume. Complementa o `CONTEXTO.md`.

Objetivo: garantir que 30+ páginas pareçam um veículo editorial único, e não conteúdo avulso. Consistência visual é o que sustenta reconhecimento de marca no Pinterest e credibilidade para rede de anúncios.

---

## 1. Estratégia por slot de imagem

Regra central: IA para apoio didático, fotografia real para prova de resultado.

| Slot | Origem | Justificativa |
| --- | --- | --- |
| Hero (prato finalizado) | Foto real ou licenciada | É a prova do resultado. Público de culinária identifica prato sintético e o retorno de usuário cai. |
| Ilustrações de etapa | IA | Apoio didático. Ninguém espera fotografia documental em "whisk the dressing". |
| Gráficos editoriais | IA | Tabelas de conversão, matrizes de decisão, comparativos. Formato onde IA é legítima e performa bem no Pinterest. |
| Embed da fonte original | Instagram / TikTok / YouTube | Traz imagem real com atribuição embutida e reforça a curadoria. |

Nunca gerar por IA: prato finalizado no hero, rosto de pessoa, mãos executando ação.

### Fontes aceitas para o hero

- Pexels e Unsplash (licença comercial, verificar caso a caso)
- Envato ou Depositphotos (assinatura)
- Licenciamento direto com criador, em troca de crédito e backlink

Registrar toda imagem em `assets/LICENCAS.md` com: arquivo, URL de origem, licença, data. Se houver contestação, a resposta sai em minutos.

---

## 2. DNA visual

Derivado dos assets já existentes no site. Manter rigorosamente.

Superfície e props
- Fundo: linho bege claro ou madeira clara, textura suave
- Louça: cerâmica off-white, bordas irregulares, acabamento fosco
- Utensílios: metal escovado, madeira natural, pano de linho dobrado
- Sem plástico, sem inox espelhado, sem louça estampada

Luz
- Luz natural difusa, entrando pela esquerda
- Sombras suaves, sem contraste duro
- Temperatura levemente quente

Paleta
- Base: bege quente, creme, off-white
- Acentos: verde-oliva, terracota suave
- Sem cores saturadas ou neon

Composição
- Ângulo de 45 graus na maioria das etapas; top-down apenas para mise en place
- Espaço negativo generoso
- Um único ponto focal por imagem
- Enquadramento limpo, sem elementos competindo

---

## 3. Prompt base — ilustrações de etapa

Usar em inglês. Substituir apenas o bloco `[ACTION]`.

```
Editorial food illustration, soft digital watercolor style with gentle
paper texture. [ACTION]. Viewed from a 45-degree angle. Off-white matte
ceramic vessel resting on a warm beige linen surface. Soft natural
diffused daylight from the left, gentle shadows. Muted earthy palette:
warm beige, cream, olive green, subtle terracotta accents. Clean
uncluttered composition with generous negative space, single focal
point. No hands, no people, no text, no logos, no watermarks.
4:3 aspect ratio.
```

Exemplos de `[ACTION]`

- `Olive oil and lemon juice being whisked in a shallow ceramic bowl, whisk resting inside, mixture slightly cloudy`
- `Chickpeas draining in a metal sieve over a ceramic bowl, a folded linen cloth beside it`
- `Chickpeas, diced cucumber and halved cherry tomatoes tossed together in a wide ceramic bowl, lightly coated`
- `Crumbled feta being folded into a chickpea and cucumber salad, distinct white crumbles visible`

Descrever sempre o sinal sensorial que o texto da etapa menciona. Se o passo diz "the mixture looks slightly cloudy", a imagem precisa mostrar isso. Coerência entre texto e imagem é o que diferencia apoio didático de decoração.

---

## 4. Regras negativas

Incluir no campo de negative prompt, quando a ferramenta suportar:

```
hands, fingers, people, faces, text, letters, numbers, labels,
watermarks, logos, raw or undercooked food, pink meat, oversaturated
colors, neon, plastic containers, mirror-finish stainless steel,
patterned dishware, harsh direct flash, deep black shadows, cluttered
background, multiple focal points, blurry, distorted utensils
```

Justificativa dos itens mais importantes:

- Mãos e rostos: é onde IA falha de forma mais perceptível
- Texto e números: gera artefatos ilegíveis, problema recorrente em geração de imagem
- Comida crua ou rosada: toca em segurança alimentar e destrói credibilidade instantaneamente

---

## 5. Especificações de export

Ilustrações de etapa
- 800 × 600 px, WebP, qualidade 82
- Nome: `{recipe-slug}-{step-id}.webp`
- Exemplo: `lemon-chickpea-salad-combine.webp`

Hero
- Três tamanhos: 1200 × 900, 800 × 600, 480 × 360
- WebP, qualidade 85
- Nome: `{ingrediente-principal}-{largura}.webp`
- Exemplo: `chickpea-1200.webp`

Pinterest
- 1000 × 1500 px (2:3), WebP ou JPEG
- Nome: `pin-{recipe-slug}-{variante}.webp`

Sempre declarar `width` e `height` no HTML. Dimensão explícita evita CLS, que impacta Core Web Vitals e elegibilidade em redes premium.

---

## 6. Variantes para Pinterest

Três a cinco pins por página, cada um com ângulo distinto. O pin que entrega utilidade no próprio card performa melhor que foto de prato isolada.

1. Resultado — hero em 2:3 com título tipográfico
2. Uma dica — a técnica central da receita, formato de frase
3. Substituição — "out of feta? use avocado", com o trade-off
4. Gráfico editorial — tabela de conversão ou matriz de decisão
5. Passo a passo — grade de 3 ou 4 etapas numeradas

Texto legível em thumbnail: mínimo 48 px de altura de fonte no arquivo de 1000 × 1500. Testar reduzindo a imagem a 20% e verificando legibilidade.

Distribuir ao longo de semanas, não publicar todos de uma vez.

---

## 7. Rotulagem obrigatória

Ilustrações de etapa levam `is_ai_generated: true` em `recipe_models.json`, o que renderiza o selo "AI-generated" automaticamente.

O hero, sendo foto real ou licenciada, **não** recebe esse campo.

Disclosure discreto, uma vez por página, no rodapé da seção de método. Não repetir em toda imagem — polui e sinaliza conteúdo não verificado.

Todo arquivo precisa de `alt` descritivo, escrito para quem não vê a imagem. Descrever o que está acontecendo, não apenas nomear ingredientes.

---

## 8. Checklist de QC por imagem

Antes de subir qualquer asset:

- [ ] Nenhum texto, letra ou número visível na imagem
- [ ] Nenhuma mão, dedo ou rosto
- [ ] Paleta coerente com as demais imagens da página
- [ ] Louça e superfície dentro do DNA visual
- [ ] A imagem corresponde ao que o texto da etapa descreve
- [ ] Nenhum alimento com aparência crua ou mal cozida
- [ ] Dimensões e formato conforme especificação
- [ ] Nome de arquivo no padrão
- [ ] `alt` escrito e descritivo
- [ ] Hero: licença registrada em `assets/LICENCAS.md`

---

## 9. Pendência a resolver

O `CONTEXTO.md` descreve a identidade como "digital watercolor, textura de caderno desgastado, paleta em tons de verde-oliva e terrosos". Os assets existentes seguem uma direção mais fotográfica: cerâmica off-white, linho bege, luz natural difusa.

As duas descrições convivem parcialmente, mas convém alinhar antes de escalar para 30 páginas. Decisão pendente de Matheus:

- Manter a direção fotográfica atual e ajustar o `CONTEXTO.md`, ou
- Reforçar o traço aquarelado nas próximas gerações e retrabalhar os assets existentes

Este guia assume a primeira opção, por ser o que está efetivamente publicado.
