/* Bored of Toast recipe library.
   To add a recipe, copy one object and edit it. Quantities (q) are numbers so the servings scaler can adjust them. */
const RECIPES = [
  {
    id: 'chicken-avocado-salad',
    title: 'Grilled Chicken Avocado Salad',
    subtitle: 'Smoky, juicy chicken over peppery greens with creamy avocado and a bright honey-lemon dressing.',
    category: 'Salads', tags: ['quick', 'healthy'],
    img: 'images/hero-bowl.jpg', prep: 10, cook: 15, serves: 2, level: 'Easy',
    desc: 'Juicy chicken, creamy avocado and peppery greens.',
    intro: [
      'This is the salad we make when we want something fresh but still want to feel full an hour later. The chicken gets a quick smoky rub and a hard sear, so it stays juicy inside with a golden crust outside.',
      'Everything else comes together while the chicken rests: a handful of greens, sweet cherry tomatoes, ripe avocado and a three-ingredient dressing you will want to put on everything.'
    ],
    why: [
      ['Ready in 25 minutes', 'Faster than delivery and far more satisfying.'],
      ['High in protein', 'About 40 g per serving to keep you full.'],
      ['Meal-prep friendly', 'Cook the chicken ahead and assemble in minutes.']
    ],
    ingredients: [
      { group: 'For the chicken', items: [
        { q: 2, u: '', n: 'boneless, skinless chicken breasts', note: 'about 1 lb / 450 g' },
        { q: 1, u: 'tsp', n: 'smoked paprika' },
        { q: 1, u: 'tsp', n: 'garlic powder' },
        { q: 0.5, u: 'tsp', n: 'kosher salt' },
        { q: 1, u: 'tbsp', n: 'olive oil' }
      ]},
      { group: 'For the dressing', items: [
        { q: 3, u: 'tbsp', n: 'extra-virgin olive oil' },
        { q: 1, u: 'tbsp', n: 'fresh lemon juice' },
        { q: 1, u: 'tsp', n: 'honey' },
        { q: null, u: '', n: 'salt and black pepper', note: 'to taste' }
      ]},
      { group: 'For the salad', items: [
        { q: 4, u: 'cups', n: 'arugula and mixed greens' },
        { q: 1, u: 'cup', n: 'cherry tomatoes', note: 'halved' },
        { q: 1, u: '', n: 'ripe avocado', note: 'sliced' },
        { q: 1, u: 'tbsp', n: 'sesame seeds', note: 'toasted' }
      ]}
    ],
    steps: [
      { t: 'Season the chicken', d: 'Pat the chicken dry with paper towels. If one end is much thicker, pound it to an even ¾-inch thickness. Rub with olive oil, then season all over with smoked paprika, garlic powder and salt.', tip: 'Even thickness means the chicken cooks evenly, with no dry edges and raw centers.' },
      { t: 'Sear until golden', d: 'Heat a grill pan or skillet over medium-high heat. Cook the chicken for 5–6 minutes per side, without moving it, until deeply golden and the thickest part reaches 165°F (74°C).' },
      { t: 'Let it rest', d: 'Move the chicken to a cutting board and rest for 5 minutes before slicing against the grain. This keeps the juices inside the meat instead of on the board.' },
      { t: 'Shake the dressing', d: 'Add the olive oil, lemon juice, honey, a pinch of salt and pepper to a small jar. Close and shake until creamy and emulsified.' },
      { t: 'Assemble and serve', d: 'Toss the greens and tomatoes with half of the dressing and divide between two bowls. Top with sliced chicken and avocado, drizzle with the remaining dressing and finish with sesame seeds.' }
    ],
    tips: [
      'Slice the avocado at the very last minute and squeeze a little lemon over it so it stays bright green.',
      'No grill pan? A cast-iron skillet gives you an even better crust.',
      'Warm chicken over cold greens is part of the magic. Assemble just before eating.'
    ],
    storage: 'Store the chicken, greens and dressing separately in the fridge for up to 3 days. Slice the avocado fresh each time.',
    variations: [
      ['Make it vegetarian', 'Swap the chicken for crispy roasted chickpeas or grilled halloumi.'],
      ['Add some crunch', 'Toss in toasted almonds, pumpkin seeds or crushed tortilla chips.'],
      ['Turn it into a wrap', 'Roll everything into a large tortilla for a lunch you can take anywhere.']
    ],
    nutrition: { calories: 520, protein: 42, carbs: 14, fat: 34, fiber: 8 },
    faq: [
      ['Can I use chicken thighs?', 'Yes. Boneless thighs are even juicier. Cook them for 6–7 minutes per side.'],
      ['Can I make the dressing ahead?', 'Absolutely. It keeps in the fridge for up to a week. Shake again before using.']
    ]
  },
  {
    id: 'creamy-garlic-pasta',
    title: 'Creamy Garlic Pasta',
    subtitle: 'Silky Parmesan cream sauce, two kinds of garlic and just one pan. Comfort food in 20 minutes.',
    category: 'Main Dishes', tags: ['quick'],
    img: 'images/creamy-garlic-pasta.jpg', prep: 5, cook: 15, serves: 4, level: 'Easy',
    desc: 'Rich, comforting and ready in 20 minutes.',
    intro: [
      'Some nights you need a big bowl of pasta, and you need it fast. This one is built on pantry staples and gets its depth from using garlic two ways: minced for bold flavor and thinly sliced for sweet, golden bites.',
      'The secret to a sauce that is glossy instead of greasy is starchy pasta water. It helps the cream and cheese cling to every strand.'
    ],
    why: [
      ['20 minutes, start to finish', 'The sauce cooks while the pasta boils.'],
      ['Pantry ingredients', 'Pasta, garlic, butter, cream and cheese.'],
      ['Crowd-pleaser', 'Kids and adults both go back for seconds.']
    ],
    ingredients: [
      { group: 'For the pasta', items: [
        { q: 12, u: 'oz', n: 'fettuccine', note: '340 g, or any long pasta' },
        { q: 1, u: 'tbsp', n: 'kosher salt', note: 'for the pasta water' }
      ]},
      { group: 'For the sauce', items: [
        { q: 2, u: 'tbsp', n: 'unsalted butter' },
        { q: 6, u: '', n: 'garlic cloves', note: '3 minced, 3 thinly sliced' },
        { q: 1, u: 'cup', n: 'heavy cream' },
        { q: 0.75, u: 'cup', n: 'Parmesan', note: 'finely grated, plus more to serve' },
        { q: 0.5, u: 'cup', n: 'reserved pasta water' },
        { q: null, u: '', n: 'black pepper and fresh parsley', note: 'to finish' }
      ]}
    ],
    steps: [
      { t: 'Boil the pasta', d: 'Bring a large pot of water to a boil and add the salt. Cook the fettuccine 1 minute less than the package says. Before draining, scoop out 1 cup of the cooking water.', tip: 'The water should taste like the sea. This is your only chance to season the pasta itself.' },
      { t: 'Toast the garlic', d: 'While the pasta cooks, melt the butter in a large skillet over medium-low heat. Add the sliced and minced garlic and cook for 2–3 minutes, stirring, until fragrant and just turning golden.' },
      { t: 'Build the sauce', d: 'Pour in the cream and bring to a gentle simmer. Let it bubble softly for 3 minutes to thicken slightly.' },
      { t: 'Melt in the cheese', d: 'Turn the heat to low and stir in the Parmesan a handful at a time until smooth. Keeping the heat low stops the cheese from turning grainy.' },
      { t: 'Toss and loosen', d: 'Add the pasta to the skillet with ½ cup of pasta water. Toss with tongs for 1–2 minutes until the sauce is glossy and coats every strand. Add more water if it looks thick.' },
      { t: 'Finish and serve', d: 'Season generously with black pepper, taste for salt and top with parsley and extra Parmesan. Serve right away.' }
    ],
    tips: [
      'Grate your own Parmesan. Pre-shredded cheese has anti-caking agents that keep it from melting smoothly.',
      'Do not let the garlic brown too much. It turns bitter in seconds.',
      'The sauce thickens as it sits, so keep some pasta water nearby.'
    ],
    storage: 'Keep leftovers in an airtight container in the fridge for up to 2 days. Reheat gently in a pan with a splash of milk or water, stirring until creamy again.',
    variations: [
      ['Add protein', 'Top with grilled chicken, sautéed shrimp or crispy pancetta.'],
      ['Add greens', 'Stir in two handfuls of baby spinach right at the end.'],
      ['Lemon twist', 'Add the zest of one lemon for a brighter, lighter sauce.']
    ],
    nutrition: { calories: 640, protein: 20, carbs: 66, fat: 33, fiber: 3 },
    faq: [
      ['Can I use milk instead of cream?', 'Whole milk works, but the sauce will be thinner. Stir 1 tsp of cornstarch into the cold milk first to help it thicken.'],
      ['Which pasta works best?', 'Long, flat shapes like fettuccine or linguine hold creamy sauces best, but penne works too.']
    ]
  },
  {
    id: 'sheet-pan-salmon',
    title: 'Honey Dijon Sheet Pan Salmon',
    subtitle: 'Tender, flaky salmon under a sticky honey-mustard glaze, roasted with lemon and fresh herbs.',
    category: 'Main Dishes', tags: ['healthy', 'quick'],
    img: 'images/sheet-pan-salmon.jpg', prep: 10, cook: 15, serves: 4, level: 'Easy',
    desc: 'Fresh, healthy and full of flavor.',
    intro: [
      'If cooking fish at home feels intimidating, start here. Roasting on a sheet pan is the most forgiving method there is: no flipping, no sticking and no fishy smell filling the kitchen.',
      'A quick glaze of honey, Dijon and garlic caramelizes in the oven, while lemon slices and herbs steam on top and keep the salmon incredibly moist.'
    ],
    why: [
      ['Weeknight-easy', '10 minutes of prep, then the oven does the work.'],
      ['Good for you', 'Packed with omega-3s and lean protein.'],
      ['One pan to wash', 'Line it with parchment and cleanup is done.']
    ],
    ingredients: [
      { group: 'For the salmon', items: [
        { q: 4, u: '', n: 'salmon fillets', note: 'about 6 oz / 170 g each, skin on or off' },
        { q: 1, u: '', n: 'lemon', note: 'thinly sliced' },
        { q: null, u: '', n: 'fresh thyme and dill sprigs' },
        { q: null, u: '', n: 'salt and black pepper' }
      ]},
      { group: 'For the glaze', items: [
        { q: 2, u: 'tbsp', n: 'olive oil' },
        { q: 2, u: 'tbsp', n: 'honey' },
        { q: 1, u: 'tbsp', n: 'Dijon mustard' },
        { q: 2, u: '', n: 'garlic cloves', note: 'minced' }
      ]}
    ],
    steps: [
      { t: 'Heat the oven', d: 'Preheat the oven to 400°F (200°C) and line a sheet pan with parchment paper.' },
      { t: 'Season the fillets', d: 'Pat the salmon dry and place it on the pan with a little space between each piece. Season with salt and pepper.', tip: 'Take the salmon out of the fridge 15 minutes before cooking so it roasts more evenly.' },
      { t: 'Glaze', d: 'Whisk the olive oil, honey, Dijon and garlic in a small bowl. Brush it generously over the top and sides of each fillet.' },
      { t: 'Top and roast', d: 'Lay lemon slices and herb sprigs over the salmon. Roast for 12–15 minutes, until the thickest part flakes easily and reaches 125–130°F (52–54°C) for medium.' },
      { t: 'Rest and serve', d: 'Let it sit for 2 minutes, then spoon any glaze from the pan over the top. Serve with rice, roasted vegetables or a green salad.' }
    ],
    tips: [
      'For a caramelized top, switch to broil for the last 1–2 minutes and watch closely.',
      'Thinner fillets cook faster. Start checking at 10 minutes.',
      'Add asparagus or green beans to the same pan for a complete meal.'
    ],
    storage: 'Refrigerate leftovers for up to 2 days. Enjoy cold over salad or reheat at 275°F (135°C) for 10 minutes so the fish does not dry out.',
    variations: [
      ['Spicy', 'Add 1 tsp sriracha or red pepper flakes to the glaze.'],
      ['Asian-style', 'Use soy sauce, ginger and sesame oil instead of Dijon.'],
      ['Maple', 'Swap the honey for maple syrup for a deeper sweetness.']
    ],
    nutrition: { calories: 380, protein: 34, carbs: 10, fat: 22, fiber: 0 },
    faq: [
      ['Can I use frozen salmon?', 'Yes. Thaw it overnight in the fridge and pat it very dry before glazing.'],
      ['Should I remove the skin?', 'No need. It peels right off after roasting, and it keeps the fish extra moist.']
    ]
  },
  {
    id: 'mediterranean-grain-bowl',
    title: 'Mediterranean Grain Bowl',
    subtitle: 'Fluffy quinoa, crispy spiced chickpeas, crunchy vegetables and feta with a zesty lemon dressing.',
    category: 'Salads', tags: ['healthy'],
    img: 'images/grain-bowl.jpg', prep: 15, cook: 20, serves: 4, level: 'Medium',
    desc: 'Colorful, fresh and satisfying.',
    intro: [
      'This bowl is all about contrast: warm quinoa and cool cucumber, crispy chickpeas and creamy feta, salty olives and a squeeze of lemon. Every bite is a little different.',
      'It is naturally vegetarian, keeps well in the fridge and tastes even better the next day, which makes it our favorite recipe for weekday lunches.'
    ],
    why: [
      ['Plant-powered', 'About 18 g of plant protein and plenty of fiber.'],
      ['Better the next day', 'Perfect for Sunday meal prep.'],
      ['Fully customizable', 'Use whatever vegetables you have on hand.']
    ],
    ingredients: [
      { group: 'For the base', items: [
        { q: 1, u: 'cup', n: 'quinoa', note: 'rinsed well' },
        { q: 2, u: 'cups', n: 'water or vegetable broth' }
      ]},
      { group: 'For the crispy chickpeas', items: [
        { q: 1, u: 'can', n: 'chickpeas', note: '15 oz / 425 g, drained and dried' },
        { q: 1, u: 'tbsp', n: 'olive oil' },
        { q: 1, u: 'tsp', n: 'ground cumin' },
        { q: 0.5, u: 'tsp', n: 'smoked paprika' }
      ]},
      { group: 'For the bowl', items: [
        { q: 1, u: '', n: 'English cucumber', note: 'diced' },
        { q: 1, u: 'cup', n: 'cherry tomatoes', note: 'halved' },
        { q: 0.5, u: '', n: 'red onion', note: 'thinly sliced' },
        { q: 0.5, u: 'cup', n: 'Kalamata olives' },
        { q: 0.5, u: 'cup', n: 'crumbled feta' },
        { q: null, u: '', n: 'fresh parsley', note: 'chopped' }
      ]},
      { group: 'For the dressing', items: [
        { q: 3, u: 'tbsp', n: 'extra-virgin olive oil' },
        { q: 2, u: 'tbsp', n: 'lemon juice' },
        { q: 1, u: 'tsp', n: 'dried oregano' }
      ]}
    ],
    steps: [
      { t: 'Roast the chickpeas', d: 'Heat the oven to 425°F (220°C). Toss the dried chickpeas with olive oil, cumin, paprika and a pinch of salt. Roast on a sheet pan for 20–25 minutes, shaking halfway, until crisp.', tip: 'Dry the chickpeas very well with a towel. Moisture is the enemy of crunch.' },
      { t: 'Cook the quinoa', d: 'Bring the quinoa and water to a boil, then cover and simmer on low for 15 minutes. Turn off the heat and leave it covered for 5 minutes, then fluff with a fork.' },
      { t: 'Prep the vegetables', d: 'While everything cooks, dice the cucumber, halve the tomatoes and thinly slice the onion. Soak the onion in cold water for 5 minutes to soften its bite.' },
      { t: 'Make the dressing', d: 'Whisk the olive oil, lemon juice, oregano, salt and pepper until combined.' },
      { t: 'Build the bowls', d: 'Divide the quinoa into bowls and arrange the vegetables, olives and chickpeas in sections on top. Sprinkle with feta and parsley, then drizzle with dressing.' }
    ],
    tips: [
      'Rinse the quinoa before cooking to remove its natural bitter coating.',
      'Add a spoonful of hummus to each bowl for extra creaminess.',
      'Add the chickpeas just before eating so they stay crunchy.'
    ],
    storage: 'Store assembled bowls, without dressing or chickpeas, for up to 4 days. Keep the chickpeas in an open container at room temperature so they stay crisp.',
    variations: [
      ['Swap the grain', 'Try farro, bulgur, couscous or brown rice.'],
      ['Add protein', 'Top with grilled chicken, falafel or a jammy boiled egg.'],
      ['Make it vegan', 'Skip the feta and add avocado or a tahini drizzle.']
    ],
    nutrition: { calories: 470, protein: 16, carbs: 52, fat: 23, fiber: 11 },
    faq: [
      ['Is this gluten-free?', 'Yes, as written. Just check that your broth is certified gluten-free.'],
      ['Can I serve it warm?', 'Definitely. Warm quinoa with cold toppings is delicious.']
    ]
  },
  {
    id: 'tomato-basil-soup',
    title: 'Creamy Tomato Basil Soup',
    subtitle: 'Velvety, deeply flavorful tomato soup finished with fresh basil and a swirl of cream.',
    category: 'Soups', tags: ['healthy'],
    img: 'images/tomato-soup.jpg', prep: 10, cook: 25, serves: 4, level: 'Easy',
    desc: 'Simple, flavorful and cozy.',
    intro: [
      'This is tomato soup the way it should taste: rich, a little sweet, a little tangy and so much better than the canned kind. Good canned whole tomatoes are the key. They taste like summer all year long.',
      'Serve it with a grilled cheese or a slice of crusty bread for dunking, and you have the coziest dinner of the week.'
    ],
    why: [
      ['Made with pantry staples', 'Canned tomatoes, onion, garlic and broth.'],
      ['Freezer-friendly', 'Make a double batch for busy weeks.'],
      ['Easy to make vegan', 'Use coconut cream instead of dairy.']
    ],
    ingredients: [
      { group: 'For the soup', items: [
        { q: 2, u: 'tbsp', n: 'olive oil' },
        { q: 1, u: '', n: 'yellow onion', note: 'chopped' },
        { q: 3, u: '', n: 'garlic cloves', note: 'minced' },
        { q: 2, u: 'cans', n: 'whole peeled tomatoes', note: '28 oz / 800 g each' },
        { q: 2, u: 'cups', n: 'vegetable broth' },
        { q: 1, u: 'tsp', n: 'sugar', note: 'balances the acidity' },
        { q: 0.5, u: 'cup', n: 'fresh basil leaves', note: 'packed' }
      ]},
      { group: 'To finish', items: [
        { q: 0.33, u: 'cup', n: 'heavy cream', note: 'plus extra to swirl' },
        { q: null, u: '', n: 'salt and black pepper', note: 'to taste' },
        { q: null, u: '', n: 'crusty bread', note: 'to serve' }
      ]}
    ],
    steps: [
      { t: 'Soften the aromatics', d: 'Heat the olive oil in a large pot over medium heat. Add the onion with a pinch of salt and cook for 6–8 minutes, until soft and translucent. Add the garlic and cook for 1 minute more.' },
      { t: 'Simmer', d: 'Add the tomatoes with their juices, crushing them with a spoon. Stir in the broth and sugar, bring to a boil, then simmer uncovered for 15 minutes.', tip: 'Simmering uncovered concentrates the flavor and lets the soup thicken naturally.' },
      { t: 'Blend until silky', d: 'Add the basil and blend with an immersion blender until completely smooth. If using a regular blender, work in batches and leave the lid vent open so steam can escape.' },
      { t: 'Add the cream', d: 'Return the pot to low heat and stir in the cream. Taste and season with salt and pepper.' },
      { t: 'Serve', d: 'Ladle into bowls, swirl in a little extra cream and top with torn basil and cracked pepper. Serve hot with crusty bread.' }
    ],
    tips: [
      'San Marzano tomatoes give the sweetest, least acidic result.',
      'A Parmesan rind added during simmering brings incredible savory depth. Remove it before blending.',
      'Too thick? Add broth. Too thin? Simmer a few more minutes.'
    ],
    storage: 'Refrigerate for up to 5 days or freeze for up to 3 months. For best texture, freeze before adding the cream and stir it in when reheating.',
    variations: [
      ['Roasted red pepper', 'Blend in a jar of roasted red peppers for a smoky twist.'],
      ['Vegan', 'Use coconut cream or blended soaked cashews.'],
      ['Spicy', 'Add a pinch of chili flakes with the garlic.']
    ],
    nutrition: { calories: 210, protein: 4, carbs: 20, fat: 14, fiber: 5 },
    faq: [
      ['Can I use fresh tomatoes?', 'Yes. Use about 3 lb (1.4 kg) of ripe tomatoes, roasted first for the deepest flavor.'],
      ['Why add sugar?', 'Just a little balances the natural acidity of the tomatoes. You will not taste sweetness.']
    ]
  },
  {
    id: 'beef-tacos',
    title: 'Weeknight Beef Tacos',
    subtitle: 'Saucy homemade taco meat with a from-scratch spice blend, fresh pico de gallo and all the toppings.',
    category: 'Main Dishes', tags: ['quick'],
    img: 'images/beef-tacos.jpg', prep: 10, cook: 15, serves: 4, level: 'Easy',
    desc: 'Bold flavors, easy to make.',
    intro: [
      'Taco night is a tradition for a reason: everyone builds their own, and dinner feels like a party. Our homemade spice blend takes one minute to mix and has way more flavor, and less salt, than the packets.',
      'A splash of water at the end turns the spices into a light sauce, so the meat is juicy and never dry.'
    ],
    why: [
      ['Ready in 25 minutes', 'Perfect for busy weeknights.'],
      ['Homemade seasoning', 'Six spices you probably already have.'],
      ['Fun for everyone', 'Set out the toppings and let people build their own.']
    ],
    ingredients: [
      { group: 'For the taco meat', items: [
        { q: 1, u: 'lb', n: 'ground beef', note: '450 g, 85% lean' },
        { q: 1, u: 'tbsp', n: 'chili powder' },
        { q: 1, u: 'tsp', n: 'ground cumin' },
        { q: 1, u: 'tsp', n: 'smoked paprika' },
        { q: 0.5, u: 'tsp', n: 'garlic powder' },
        { q: 0.5, u: 'tsp', n: 'dried oregano' },
        { q: 0.75, u: 'tsp', n: 'kosher salt' },
        { q: 0.25, u: 'cup', n: 'water' }
      ]},
      { group: 'To serve', items: [
        { q: 8, u: '', n: 'taco shells or small tortillas' },
        { q: 2, u: 'cups', n: 'shredded lettuce' },
        { q: 1, u: 'cup', n: 'pico de gallo' },
        { q: 1, u: 'cup', n: 'shredded cheddar' },
        { q: null, u: '', n: 'lime wedges, cilantro and sour cream' }
      ]}
    ],
    steps: [
      { t: 'Mix the spices', d: 'Stir together the chili powder, cumin, paprika, garlic powder, oregano and salt in a small bowl.' },
      { t: 'Brown the beef', d: 'Heat a large skillet over medium-high heat. Add the beef and cook for 6–8 minutes, breaking it into small crumbles, until browned with some crispy bits. Drain any excess fat.', tip: 'Leave the meat alone for a minute or two between stirs. That is how you get flavorful browned edges.' },
      { t: 'Season and simmer', d: 'Sprinkle the spice mix over the beef and stir for 30 seconds until fragrant. Add the water and simmer for 3–5 minutes, until the liquid thickens and coats the meat.' },
      { t: 'Warm the shells', d: 'Warm taco shells in a 350°F (175°C) oven for 3–4 minutes, or heat tortillas in a dry skillet for 20 seconds per side.' },
      { t: 'Build your tacos', d: 'Fill each shell with beef, then top with lettuce, pico de gallo, cheese, cilantro and a squeeze of lime.' }
    ],
    tips: [
      'Make a big batch of the spice blend and keep it in a jar for next time.',
      'Leftover taco meat makes a great nacho topping or burrito bowl.',
      'For extra richness, stir in 1 tbsp tomato paste with the spices.'
    ],
    storage: 'Refrigerate cooked taco meat for up to 4 days or freeze for up to 3 months. Reheat in a skillet with a splash of water.',
    variations: [
      ['Turkey or chicken', 'Ground turkey or chicken works perfectly with the same spices.'],
      ['Vegetarian', 'Use black beans and diced sweet potato instead of beef.'],
      ['Bowl style', 'Serve over rice with beans, corn and avocado.']
    ],
    nutrition: { calories: 480, protein: 28, carbs: 26, fat: 29, fiber: 4 },
    faq: [
      ['Hard or soft shells?', 'Both work. Soft corn tortillas are the most traditional choice.'],
      ['How spicy is it?', 'Mild and family-friendly. Add cayenne or jalapeños for heat.']
    ]
  },
  {
    id: 'chocolate-chip-cookies',
    title: 'Chewy Chocolate Chip Cookies',
    subtitle: 'Crisp golden edges, soft chewy centers and pools of melted chocolate with a touch of sea salt.',
    category: 'Desserts', tags: [],
    img: 'images/desserts.jpg', pos: '25% 60%', prep: 15, cook: 12, serves: 24, servesLabel: 'cookies', level: 'Easy',
    desc: 'Soft, chewy and classic.',
    intro: [
      'After many (delicious) test batches, this is our forever chocolate chip cookie. Melted butter and extra brown sugar give it the chewiness, and chopped chocolate instead of chips creates those irresistible melty pools.',
      'No mixer, no chilling required, just one bowl and a spoon. Although if you can wait, an overnight rest in the fridge makes them even better.'
    ],
    why: [
      ['One bowl, no mixer', 'Minimal dishes and maximum reward.'],
      ['Chewy every time', 'Melted butter plus brown sugar is the secret.'],
      ['Freezer-friendly dough', 'Bake fresh cookies whenever you want.']
    ],
    ingredients: [
      { group: 'Wet ingredients', items: [
        { q: 1, u: 'cup', n: 'unsalted butter', note: '225 g, melted and slightly cooled' },
        { q: 1, u: 'cup', n: 'packed brown sugar' },
        { q: 0.5, u: 'cup', n: 'granulated sugar' },
        { q: 2, u: '', n: 'large eggs', note: 'room temperature' },
        { q: 2, u: 'tsp', n: 'vanilla extract' }
      ]},
      { group: 'Dry ingredients', items: [
        { q: 3, u: 'cups', n: 'all-purpose flour', note: '375 g, spooned and leveled' },
        { q: 1, u: 'tsp', n: 'baking soda' },
        { q: 1, u: 'tsp', n: 'fine salt' }
      ]},
      { group: 'Mix-ins', items: [
        { q: 2, u: 'cups', n: 'chopped dark chocolate or chunks' },
        { q: null, u: '', n: 'flaky sea salt', note: 'to finish' }
      ]}
    ],
    steps: [
      { t: 'Preheat', d: 'Heat the oven to 350°F (175°C) and line two baking sheets with parchment paper.' },
      { t: 'Mix the wet ingredients', d: 'Whisk the melted butter with both sugars for about 1 minute, until smooth and glossy. Add the eggs and vanilla and whisk until lighter in color.' },
      { t: 'Add the dry ingredients', d: 'Add the flour, baking soda and salt. Stir with a spatula until just combined and no dry streaks remain, then fold in the chocolate.', tip: 'Stop mixing as soon as the flour disappears. Overmixing makes cookies tough.' },
      { t: 'Scoop', d: 'Scoop 2-tablespoon balls of dough onto the sheets, leaving 2 inches (5 cm) between them. For the best texture, chill the scooped dough for 30 minutes or up to 24 hours.' },
      { t: 'Bake', d: 'Bake one sheet at a time for 10–12 minutes, until the edges are golden but the centers still look slightly underdone.' },
      { t: 'Finish and cool', d: 'Sprinkle with flaky salt right away. Cool on the pan for 5 minutes, which lets the centers set, then move to a wire rack.' }
    ],
    tips: [
      'Pull them out when they look a little underbaked. They keep cooking on the hot pan.',
      'For perfectly round cookies, swirl a large glass around each one right out of the oven.',
      'Mix dark and milk chocolate for a deeper flavor.'
    ],
    storage: 'Keep baked cookies in an airtight container for up to 5 days. Freeze dough balls for up to 3 months and bake from frozen, adding 1–2 minutes.',
    variations: [
      ['Brown butter', 'Brown the butter first for a nutty, toffee-like flavor.'],
      ['Add nuts', 'Fold in 1 cup of toasted walnuts or pecans.'],
      ['Double chocolate', 'Replace ¼ cup flour with cocoa powder.']
    ],
    nutrition: { calories: 230, protein: 3, carbs: 29, fat: 12, fiber: 1 },
    faq: [
      ['Why did my cookies spread too much?', 'The butter was probably too warm. Let it cool, or chill the dough for 30 minutes before baking.'],
      ['Can I use chocolate chips?', 'Yes, but chopped chocolate melts into bigger, gooier pools.']
    ]
  },
  {
    id: 'chocolate-mousse-cake',
    title: 'No-Bake Chocolate Mousse Cake',
    subtitle: 'A crunchy cookie crust topped with a cloud of silky dark chocolate mousse and fresh raspberries.',
    category: 'Desserts', tags: [],
    img: 'images/desserts.jpg', pos: '85% 30%', prep: 30, cook: 5, chill: 360, serves: 10, level: 'Medium',
    desc: 'Silky, rich and made for celebrations.',
    intro: [
      'This cake looks like it came from a fancy bakery, but it only takes about 30 minutes of hands-on time and no oven at all. The fridge does most of the work.',
      'It is rich without being heavy. Whipped cream folded into melted chocolate creates a mousse that is light, airy and melts on your tongue.'
    ],
    why: [
      ['No oven needed', 'Perfect for hot days or small kitchens.'],
      ['Make-ahead friendly', 'Prepare it the day before your party.'],
      ['Show-stopping', 'Looks impressive with very little effort.']
    ],
    ingredients: [
      { group: 'For the crust', items: [
        { q: 20, u: '', n: 'chocolate sandwich cookies', note: 'finely crushed' },
        { q: 4, u: 'tbsp', n: 'unsalted butter', note: 'melted' }
      ]},
      { group: 'For the mousse', items: [
        { q: 10, u: 'oz', n: 'dark chocolate (60–70%)', note: '280 g, chopped' },
        { q: 2, u: 'cups', n: 'cold heavy cream', note: 'divided' },
        { q: 3, u: 'tbsp', n: 'powdered sugar' },
        { q: 1, u: 'tsp', n: 'vanilla extract' },
        { q: 1, u: 'pinch', n: 'salt' }
      ]},
      { group: 'To decorate', items: [
        { q: 1, u: 'cup', n: 'fresh raspberries' },
        { q: null, u: '', n: 'chocolate curls or cocoa powder' }
      ]}
    ],
    steps: [
      { t: 'Make the crust', d: 'Mix the cookie crumbs with the melted butter until it looks like wet sand. Press firmly into the bottom of a 9-inch (23 cm) springform pan and refrigerate while you make the mousse.' },
      { t: 'Melt the chocolate', d: 'Heat ½ cup of the cream until steaming, pour it over the chopped chocolate and let it sit for 2 minutes. Stir until smooth and glossy, add the salt and let it cool until just barely warm.', tip: 'If the chocolate is too warm, it will melt the whipped cream and the mousse will not set.' },
      { t: 'Whip the cream', d: 'Beat the remaining 1½ cups of cold cream with the powdered sugar and vanilla until soft peaks form, when the peaks gently fold over.' },
      { t: 'Fold gently', d: 'Fold one third of the whipped cream into the chocolate to lighten it, then gently fold in the rest in two additions until no white streaks remain.' },
      { t: 'Chill', d: 'Spread the mousse over the crust and smooth the top. Cover and refrigerate for at least 6 hours, or overnight, until set.' },
      { t: 'Decorate and slice', d: 'Release the springform ring and top with raspberries and chocolate curls. Slice with a knife dipped in hot water and wiped dry between cuts.' }
    ],
    tips: [
      'Use a good chocolate bar, not chips. It is the star of the dessert.',
      'Fold with a spatula in big, gentle strokes to keep the air in the mousse.',
      'A thin layer of raspberry jam on the crust adds a lovely fruity surprise.'
    ],
    storage: 'Keep covered in the fridge for up to 4 days. You can also freeze the whole cake, without toppings, for up to 1 month and thaw it overnight in the fridge.',
    variations: [
      ['Mocha', 'Dissolve 1 tsp instant espresso into the warm cream.'],
      ['Orange', 'Add orange zest to the mousse and top with candied peel.'],
      ['Graham crust', 'Use graham crackers for a lighter, honeyed base.']
    ],
    nutrition: { calories: 440, protein: 4, carbs: 30, fat: 35, fiber: 3 },
    faq: [
      ['Can I use milk chocolate?', 'You can, but the mousse will be sweeter and softer. Reduce the powdered sugar to 1 tbsp.'],
      ['I don\'t have a springform pan.', 'Use a pie dish and serve it straight from the dish, or line a regular cake pan with plastic wrap.']
    ]
  }
];

RECIPES.forEach(r => { r.time = r.prep + r.cook + (r.chill || 0); });

const CATEGORIES = [
  { key: 'Salads', label: 'Salads', img: 'images/hero-bowl.jpg' },
  { key: 'Main Dishes', label: 'Main Dishes', img: 'images/sheet-pan-salmon.jpg' },
  { key: 'Soups', label: 'Soups', img: 'images/tomato-soup.jpg' },
  { key: 'Desserts', label: 'Desserts', img: 'images/desserts.jpg', pos: '25% 60%' },
  { key: 'quick', label: 'Quick & Easy', img: 'images/creamy-garlic-pasta.jpg' },
  { key: 'healthy', label: 'Healthy', img: 'images/grain-bowl.jpg' }
];
