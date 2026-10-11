#!/usr/bin/env python3
"""New content, batch 4 of 6: five NEW freezer-friendly soups (nothing replaced).

Photo-first rule (Pexels title/description names the dish):
  split-pea-soup          28354410  "Vegan split pea watercress soup" / creamy green soup (Nic Wood)
  chicken-minestrone      16811678  "Minestrone soup with noodles" (fajri nugroho)
  chickpea-black-bean-chili 6546422 "Vegan chickpea chili with fresh vegetables" (Alesia Kozik)
  tomato-white-bean-stew  19870150  "Soup with beans" / hearty bean stew with bread (Boryslav Shoot)
  red-lentil-lemon-soup   12077978  "Turkish red lentil soup drizzled with oil" (Alex Bayev)
Planned "chicken tortilla soup" and "turkey chili" had no matching free photo; they became the bean stew and
chickpea chili. The lentil soup is a Turkish-style lemon version (no carrot), different from the Starter Kit soup.

Nutrition per serving is an ESTIMATE from USDA FoodData Central reference values (rounded):
  Split pea (6): dried split peas 196 g 690/48 P/118 C/2 F/50 fib; onion, carrot, celery 250 g 90/2 P/20 C/8 fib;
    olive oil 13.5 g 119/13.5 F; chicken bone broth 960 ml 160/36 P/2 C/1 F (label values vary); spinach 30 g 7/1 P/1 C
    -> 1066 kcal, 87 P, 141 C, 17 F, 58 fib / 6 = ~178 kcal, 15 P, 24 C, 3 F, 10 fib
  Minestrone (8): chicken breast 454 g 545/102 P/12 F; ditalini 50 g 186/6.5 P/37 C/1 F/2 fib; cannellini 240 g 274/18 P/50 C/1 F/15 fib;
    diced tomatoes 400 g 80/4 P/16 C/4 fib; vegetables 400 g 120/4 P/26 C/1 F/9 fib; olive oil 13.5 g 119/13.5 F;
    low-sodium chicken broth 1440 ml 90/12 P/6 C/3 F; parmesan 30 g 117/10 P/1 C/8 F
    -> 1531 kcal, 157 P, 136 C, 39 F, 30 fib / 8 = ~191 kcal, 20 P, 17 C, 5 F, 4 fib
  Chili (6): chickpeas 480 g 667/34 P/110 C/12 F/36 fib; black beans 240 g 218/14 P/38 C/1 F/17 fib; crushed tomatoes 800 g
    256/13 P/58 C/2 F/15 fib; onion, pepper 300 g 105/3 P/24 C/6 fib; olive oil 13.5 g 119/13.5 F; spices 20/1 P/3 C/2 fib;
    nonfat Greek yogurt 113 g 67/11.5 P/4 C -> 1452 kcal, 77 P, 237 C, 29 F, 76 fib / 6 = ~242 kcal, 13 P, 40 C, 5 F, 13 fib
  Bean stew (6): lean turkey sausage 340 g 544/54 P/34 F (label values vary); white beans 480 g 548/36 P/100 C/2 F/30 fib;
    diced tomatoes 400 g 80/4 P/16 C/4 fib; onion, carrot, garlic 200 g 70/2 P/16 C/4 fib; olive oil 7 g 60/7 F;
    broth 480 ml 30/4 P/2 C; spices 10 -> 1342 kcal, 100 P, 134 C, 43 F, 38 fib / 6 = ~224 kcal, 17 P, 22 C, 7 F, 6 fib
  Lentil (6): red lentils 192 g 687/46 P/121 C/4 F/21 fib; onion 150 g 60/1.6 P/14 C/2 fib; olive oil 13.5 g 119/13.5 F;
    tomato paste 16 g 13/0.7 P/3 C; chicken bone broth 960 ml 160/36 P/2 C/1 F; spices, mint, lemon 20/4 C/1 fib
    -> 1059 kcal, 84 P, 144 C, 19 F, 24 fib / 6 = ~177 kcal, 14 P, 24 C, 3 F, 4 fib
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batchlib import add_recipes

N = None
PHOTOS = {
    'split-pea-soup': {'id': 28354410, 'photographer': 'Nic Wood', 'photographer_url': 'https://www.pexels.com/@nic-scrollstoppingphotos/',
        'photo_url': 'https://www.pexels.com/photo/vegan-split-pea-watercress-soup-28354410/', 'alt': 'Two bowls of creamy green split pea soup seen from above.'},
    'chicken-minestrone': {'id': 16811678, 'photographer': 'fajri nugroho', 'photographer_url': 'https://www.pexels.com/@fajrinugroho/',
        'photo_url': 'https://www.pexels.com/photo/minestrone-soup-with-noodles-16811678/', 'alt': 'A bowl of minestrone with small pasta and vegetables.'},
    'chickpea-black-bean-chili': {'id': 6546422, 'photographer': 'Alesia Kozik', 'photographer_url': 'https://www.pexels.com/@alesiakozik/',
        'photo_url': 'https://www.pexels.com/photo/vegan-chili-bowl-6546422/', 'alt': 'A bowl of chickpea chili with fresh vegetables.'},
    'tomato-white-bean-stew': {'id': 19870150, 'photographer': 'Boryslav Shoot', 'photographer_url': 'https://www.pexels.com/@boryslav/',
        'photo_url': 'https://www.pexels.com/photo/soup-with-beans-19870150/', 'alt': 'A bowl of hearty tomato bean stew with slices of bread.'},
    'red-lentil-lemon-soup': {'id': 12077978, 'photographer': 'Alex Bayev', 'photographer_url': 'https://www.pexels.com/@alexbayev/',
        'photo_url': 'https://www.pexels.com/photo/turkish-creamy-soup-12077978/', 'alt': 'Bowls of smooth red lentil soup drizzled with oil.'},
}

NEW = {}
NEW['split-pea-soup'] = {
    "title": "Creamy Split Pea Soup",
    "subtitle": "Split peas simmered in chicken bone broth with onion, carrot and celery, then blended smooth with a handful of spinach. About 15 g protein and 10 g fiber per small bowl.",
    "category": "Soups",
    "tags": ["healthy", "high-protein", "small-plates", "make-ahead", "gentle"],
    "prep": 10, "cook": 50, "time": 60, "serves": 6, "servesLabel": "small bowls", "level": "Easy",
    "desc": "Smooth, filling and about 15 g protein.",
    "intro": [
        "Split peas cook down into a naturally creamy soup without any cream. Simmered in chicken bone broth, each small bowl has about 15 g of protein and plenty of fiber, which makes it one of the most filling soups on the site for its size.",
        "It is blended smooth, so it is easy to sip from a mug, and it freezes beautifully in single portions for harder days."
    ],
    "why": [["About 15 g protein per bowl", "Split peas plus bone broth."], ["Creamy without cream", "Split peas thicken it naturally."], ["Freezer-friendly", "Freeze in 1-cup portions."]],
    "ingredients": [
        {"group": "For the soup", "items": [
            {"q": 1, "u": "tbsp", "n": "olive oil"},
            {"q": 1, "u": "", "n": "onion", "note": "chopped"},
            {"q": 1, "u": "", "n": "carrot", "note": "chopped"},
            {"q": 1, "u": "", "n": "celery stalk", "note": "chopped"},
            {"q": 1, "u": "cup", "n": "dried green split peas", "note": "rinsed", "g": 196},
            {"q": 4, "u": "cups", "n": "low-sodium chicken bone broth"},
            {"q": 1, "u": "cup", "n": "water"},
            {"q": 1, "u": "", "n": "bay leaf"},
            {"q": 1, "u": "cup", "n": "baby spinach"},
            {"q": N, "u": "", "n": "salt and pepper", "note": "to taste"}]}
    ],
    "steps": [
        {"t": "Soften the vegetables", "d": "Warm the oil in a large pot over medium heat. Add the onion, carrot and celery and cook for 6 to 8 minutes, until soft."},
        {"t": "Simmer", "d": "Add the split peas, broth, water and bay leaf. Bring to a boil, then lower the heat, cover partly and simmer for 40 to 45 minutes, stirring now and then, until the peas are completely soft.", "tip": "Split peas do not need soaking, but they do need stirring near the end so they do not stick."},
        {"t": "Add the spinach", "d": "Remove the bay leaf. Stir in the spinach until wilted."},
        {"t": "Blend", "d": "Blend with an immersion blender until smooth, adding a splash of water if it is too thick. Season with salt and pepper."},
        {"t": "Serve small", "d": "Ladle into small bowls or mugs."}
    ],
    "tips": ["The soup thickens as it cools. Thin with water or broth when reheating.", "Taste before salting; broth varies a lot.", "A squeeze of lemon brightens it just before serving.", "Small-portion tip: freeze in 1-cup containers so you only reheat what you need."],
    "storage": "Refrigerate for up to 4 days or freeze in portions for up to 3 months. Thaw overnight in the fridge and reheat gently, adding a little water.",
    "variations": [["With ham", "Stir in 1/2 cup diced lean ham after blending for about 3 g more protein per bowl."], ["Vegetarian", "Use vegetable broth; the protein drops to about 9 g per bowl."], ["Chunky", "Blend only half the soup for more texture."], ["Make it gentler", "Skip the bay leaf and pepper and serve warm rather than hot."], ["Protein boost", "Swirl in 2 tablespoons Greek yogurt per bowl for about 3 g more protein."]],
    "nutrition": {"calories": 178, "protein": 15, "carbs": 24, "fat": 3, "fiber": 10},
    "faq": [["Do I need to soak split peas?", "No. They soften in about 45 minutes of simmering."], ["Is it gluten-free?", "Yes, if your broth is gluten-free."], ["Can I use yellow split peas?", "Yes; the soup will be golden instead of green, with the same nutrition."]],
    "note": "A mug of this on a cold evening is about as comforting as food gets, and it quietly does a lot of nutritional work.",
    "diet": ["dairy-free", "gluten-free"],
}
NEW['chicken-minestrone'] = {
    "title": "Chicken Minestrone with Small Pasta",
    "subtitle": "A light tomato-vegetable broth with tender chicken, white beans and a little small pasta. About 20 g protein per 1 1/2-cup bowl, and it freezes well.",
    "category": "Soups",
    "tags": ["healthy", "high-protein", "small-plates", "make-ahead"],
    "prep": 15, "cook": 35, "time": 50, "serves": 8, "servesLabel": "bowls", "level": "Easy",
    "desc": "Vegetables, chicken and beans in every bowl.",
    "intro": [
        "Classic minestrone is mostly vegetables and pasta. This version adds chicken and white beans, so each bowl has about 20 g of protein while still tasting like the soup you know.",
        "The pasta is kept small and modest, and it makes a big pot that freezes well, so there is always a warm bowl ready."
    ],
    "why": [["About 20 g protein per bowl", "Chicken plus white beans."], ["Lots of vegetables", "Carrot, celery, zucchini and tomato."], ["Big batch", "Eight bowls from one pot."]],
    "ingredients": [
        {"group": "For the soup", "items": [
            {"q": 1, "u": "tbsp", "n": "olive oil"},
            {"q": 1, "u": "", "n": "onion", "note": "chopped"},
            {"q": 2, "u": "", "n": "carrots", "note": "diced"},
            {"q": 2, "u": "", "n": "celery stalks", "note": "diced"},
            {"q": 1, "u": "", "n": "small zucchini", "note": "diced"},
            {"q": 2, "u": "", "n": "garlic cloves", "note": "minced"},
            {"q": 1, "u": "lb", "n": "boneless skinless chicken breast", "g": 454},
            {"q": 1, "u": "can (14 oz)", "n": "diced tomatoes"},
            {"q": 6, "u": "cups", "n": "low-sodium chicken broth"},
            {"q": 1, "u": "tsp", "n": "dried Italian herbs"},
            {"q": 1, "u": "can (15 oz)", "n": "cannellini beans", "note": "drained and rinsed"},
            {"q": 0.5, "u": "cup", "n": "ditalini or other small pasta", "g": 50}]},
        {"group": "To serve", "items": [{"q": 0.33, "u": "cup", "n": "grated parmesan"}, {"q": N, "u": "", "n": "fresh basil or parsley"}]}
    ],
    "steps": [
        {"t": "Cook the vegetables", "d": "Warm the oil in a large pot over medium heat. Add the onion, carrots and celery and cook for 8 minutes, until softened. Add the zucchini and garlic and cook for 2 minutes more."},
        {"t": "Poach the chicken", "d": "Add the tomatoes, broth and herbs, then lay the chicken breasts in the pot. Bring to a simmer and cook gently for 15 to 18 minutes, until the chicken reaches 165°F (74°C).", "tip": "Poaching the chicken in the soup keeps it tender and flavors the broth."},
        {"t": "Shred", "d": "Lift out the chicken and shred it finely with two forks."},
        {"t": "Add pasta and beans", "d": "Add the pasta and beans to the pot and simmer for 8 to 10 minutes, until the pasta is tender. Return the chicken and season with salt and pepper."},
        {"t": "Serve", "d": "Ladle into bowls and top each with a spoonful of parmesan and some fresh herbs."}
    ],
    "tips": ["If freezing, cook the pasta separately and add it when reheating so it does not go soft.", "Any small pasta works: ditalini, small shells or orzo.", "A parmesan rind simmered in the broth adds lots of flavor.", "Small-portion tip: a 1-cup bowl is plenty on low-appetite days."],
    "storage": "Refrigerate for up to 4 days. Freeze without the pasta for up to 3 months; add freshly cooked pasta when reheating.",
    "variations": [["Turkey", "Use leftover roast turkey instead of chicken."], ["Greens", "Stir in a handful of chopped kale or spinach at the end."], ["Gluten-free", "Use a gluten-free small pasta or 1/2 cup rice."], ["Make it gentler", "Skip the garlic, shred the chicken very finely and serve warm."], ["Protein boost", "Add an extra 1/2 can of white beans for about 2 g more protein per bowl."]],
    "nutrition": {"calories": 191, "protein": 20, "carbs": 17, "fat": 5, "fiber": 4},
    "faq": [["Can I use rotisserie chicken?", "Yes. Skip the poaching step and add 3 cups shredded chicken with the beans."], ["Why is the pasta soft after a day?", "Pasta keeps absorbing broth. Add a splash of broth when reheating, or cook pasta separately."], ["Is it dairy-free?", "Yes, if you skip the parmesan."]],
    "note": "A big pot of this on Sunday means warm, protein-rich bowls ready all week, one small portion at a time.",
    "diet": [],
}
NEW['chickpea-black-bean-chili'] = {
    "title": "Smoky Chickpea and Black Bean Chili",
    "subtitle": "A thick, smoky vegetarian chili with chickpeas, black beans and tomatoes, topped with Greek yogurt. About 13 g protein and 13 g fiber per bowl.",
    "category": "Soups",
    "tags": ["healthy", "small-plates", "make-ahead"],
    "prep": 10, "cook": 30, "time": 40, "serves": 6, "servesLabel": "bowls", "level": "Easy",
    "desc": "Thick, smoky and full of beans.",
    "intro": [
        "This chili is built on two kinds of beans: chickpeas for a firm, nutty bite and black beans for creaminess. Smoked paprika and cumin give it a deep, smoky flavor without any meat.",
        "A spoonful of Greek yogurt on top replaces sour cream and adds a little extra protein. It tastes even better the next day."
    ],
    "why": [["About 13 g protein", "Two kinds of beans plus yogurt."], ["13 g fiber per bowl", "Very filling for its size."], ["Better the next day", "Great for batch cooking."]],
    "ingredients": [
        {"group": "For the chili", "items": [
            {"q": 1, "u": "tbsp", "n": "olive oil"},
            {"q": 1, "u": "", "n": "onion", "note": "chopped"},
            {"q": 1, "u": "", "n": "bell pepper", "note": "chopped"},
            {"q": 2, "u": "", "n": "garlic cloves", "note": "minced"},
            {"q": 1, "u": "tbsp", "n": "smoked paprika"},
            {"q": 2, "u": "tsp", "n": "ground cumin"},
            {"q": 1, "u": "tsp", "n": "chili powder", "note": "or to taste"},
            {"q": 2, "u": "cans (15 oz)", "n": "chickpeas", "note": "drained"},
            {"q": 1, "u": "can (15 oz)", "n": "black beans", "note": "drained"},
            {"q": 1, "u": "can (28 oz)", "n": "crushed tomatoes"},
            {"q": 1, "u": "cup", "n": "water or vegetable broth"}]},
        {"group": "To serve", "items": [{"q": 0.5, "u": "cup", "n": "plain nonfat Greek yogurt"}, {"q": N, "u": "", "n": "cilantro and sliced cucumber"}]}
    ],
    "steps": [
        {"t": "Sauté", "d": "Warm the oil in a large pot over medium heat. Cook the onion and pepper for 6 to 8 minutes, until soft. Add the garlic and spices and stir for 1 minute."},
        {"t": "Simmer", "d": "Add the chickpeas, black beans, tomatoes and water. Bring to a simmer and cook uncovered for 20 minutes, stirring now and then, until thick.", "tip": "Mash a few spoonfuls of beans against the side of the pot for a thicker chili."},
        {"t": "Season", "d": "Taste and add salt, a pinch more chili or a squeeze of lime."},
        {"t": "Serve", "d": "Ladle into bowls and top with a spoonful of Greek yogurt, cilantro and a few cucumber slices."}
    ],
    "tips": ["Start with less chili powder; you can always add more.", "Leftovers thicken overnight. Add a splash of water when reheating.", "Serve over a little rice for a more filling meal.", "Small-portion tip: 3/4 cup with a spoonful of yogurt is a satisfying small plate."],
    "storage": "Refrigerate for up to 5 days or freeze in portions for up to 3 months.",
    "variations": [["With turkey", "Brown 1/2 lb lean ground turkey with the onion for about 8 g more protein per bowl."], ["Sweet potato", "Add 1 diced sweet potato with the tomatoes and simmer 10 minutes longer."], ["Vegan", "Top with avocado instead of yogurt."], ["Make it gentler", "Skip the chili powder and garlic and use sweet paprika instead of smoked."], ["Protein boost", "Top with 2 tablespoons shredded cheese and extra yogurt for about 6 g more protein."]],
    "nutrition": {"calories": 242, "protein": 13, "carbs": 40, "fat": 5, "fiber": 13},
    "faq": [["Is it spicy?", "Mildly. Adjust the chili powder to taste."], ["Can I use dried beans?", "Yes, about 4 1/2 cups cooked beans in total."], ["Is it gluten-free?", "Yes, check that your spices and broth are gluten-free."]],
    "note": "A pot of chili is one of the most forgiving things to cook. Make it once, and small bowls are ready all week.",
    "diet": ["vegetarian", "gluten-free"],
}
NEW['tomato-white-bean-stew'] = {
    "title": "Hearty Tomato White Bean Stew",
    "subtitle": "White beans and lean turkey sausage simmered in a smoky tomato broth. About 17 g protein per bowl, ready in 35 minutes.",
    "category": "Soups",
    "tags": ["high-protein", "small-plates", "make-ahead"],
    "prep": 10, "cook": 25, "time": 35, "serves": 6, "servesLabel": "bowls", "level": "Easy",
    "desc": "Beans and sausage in a smoky tomato broth.",
    "intro": [
        "This stew sits between a soup and a chili: tender white beans and slices of lean turkey sausage in a thick, smoky tomato broth. It is warming, filling and has about 17 g of protein per bowl.",
        "Serve a small bowl with a slice of bread for dipping, or on its own. It reheats and freezes well."
    ],
    "why": [["About 17 g protein", "Turkey sausage and beans."], ["35 minutes", "Mostly hands-off simmering."], ["Freezes well", "Make a double batch."]],
    "ingredients": [
        {"group": "For the stew", "items": [
            {"q": 0.5, "u": "tbsp", "n": "olive oil"},
            {"q": 12, "u": "oz", "n": "lean turkey sausage", "note": "sliced or casings removed", "g": 340},
            {"q": 1, "u": "", "n": "onion", "note": "chopped"},
            {"q": 1, "u": "", "n": "carrot", "note": "diced"},
            {"q": 2, "u": "", "n": "garlic cloves", "note": "minced"},
            {"q": 1, "u": "tsp", "n": "smoked paprika"},
            {"q": 1, "u": "can (14 oz)", "n": "diced tomatoes"},
            {"q": 2, "u": "cans (15 oz)", "n": "white beans", "note": "drained"},
            {"q": 2, "u": "cups", "n": "low-sodium chicken broth"},
            {"q": N, "u": "", "n": "fresh parsley", "note": "to serve"}]}
    ],
    "steps": [
        {"t": "Brown the sausage", "d": "Warm the oil in a large pot over medium-high heat. Brown the sausage for 5 minutes, breaking it up if loose. Move to a plate."},
        {"t": "Soften the vegetables", "d": "Lower the heat to medium. Add the onion and carrot and cook for 6 minutes. Add the garlic and paprika and cook 1 minute."},
        {"t": "Simmer", "d": "Add the tomatoes, beans, broth and sausage. Simmer for 15 minutes, until thick.", "tip": "Mash some of the beans for a creamier stew."},
        {"t": "Serve", "d": "Season to taste and serve in small bowls with parsley."}
    ],
    "tips": ["Check sausage labels; brands vary a lot in fat and salt.", "A splash of vinegar or lemon at the end brightens the flavor.", "Add a handful of spinach for color.", "Small-portion tip: 3/4 cup with a small piece of bread is a complete small meal."],
    "storage": "Refrigerate for up to 4 days or freeze for up to 3 months.",
    "variations": [["Chicken sausage", "Use chicken sausage instead of turkey."], ["Vegetarian", "Skip the sausage and add a third can of beans."], ["Kale", "Stir in chopped kale for the last 5 minutes."], ["Make it gentler", "Use a mild sausage, skip the paprika and garlic, and mash most of the beans."], ["Protein boost", "Top with grated parmesan for about 3 g more protein."]],
    "nutrition": {"calories": 224, "protein": 17, "carbs": 22, "fat": 7, "fiber": 6},
    "faq": [["What beans work best?", "Cannellini or great northern beans."], ["Is it gluten-free?", "Check your sausage and broth labels."], ["Can I make it in a slow cooker?", "Yes. Brown the sausage, then cook everything on low for 6 hours."]],
    "note": "This is cozy, simple food: a small bowl of beans in tomato broth, a little bread, and you are done.",
    "diet": ["dairy-free"],
}
NEW['red-lentil-lemon-soup'] = {
    "title": "Turkish-Style Red Lentil Soup with Lemon",
    "subtitle": "Red lentils simmered in bone broth with onion, cumin and paprika, blended silky smooth and finished with lemon and mint. About 14 g protein per small bowl.",
    "category": "Soups",
    "tags": ["healthy", "small-plates", "make-ahead", "gentle"],
    "prep": 10, "cook": 30, "time": 40, "serves": 6, "servesLabel": "small bowls", "level": "Easy",
    "desc": "Silky, lemony and very easy to sip.",
    "intro": [
        "Red lentils fall apart as they cook, so this soup blends into something silky and smooth with no cream at all. It is inspired by Turkish mercimek çorbası: gently spiced with cumin and paprika and finished with a squeeze of lemon.",
        "Using bone broth adds protein, giving each small bowl about 14 g. It is a mild, soothing soup that is easy to sip from a mug."
    ],
    "why": [["About 14 g protein", "Lentils plus bone broth."], ["Silky smooth", "Easy to sip."], ["Pantry staples", "Mostly cupboard ingredients."]],
    "ingredients": [
        {"group": "For the soup", "items": [
            {"q": 1, "u": "tbsp", "n": "olive oil"},
            {"q": 1, "u": "", "n": "onion", "note": "chopped"},
            {"q": 1, "u": "tbsp", "n": "tomato paste"},
            {"q": 1, "u": "tsp", "n": "ground cumin"},
            {"q": 1, "u": "tsp", "n": "sweet paprika"},
            {"q": 1, "u": "cup", "n": "red lentils", "note": "rinsed", "g": 192},
            {"q": 4, "u": "cups", "n": "low-sodium chicken bone broth"},
            {"q": 1, "u": "cup", "n": "water"}]},
        {"group": "To finish", "items": [{"q": 1, "u": "", "n": "lemon", "note": "juiced"}, {"q": 1, "u": "tsp", "n": "dried mint"}, {"q": N, "u": "", "n": "salt", "note": "to taste"}]}
    ],
    "steps": [
        {"t": "Soften the onion", "d": "Warm the oil in a pot over medium heat and cook the onion for 6 minutes, until soft."},
        {"t": "Toast the spices", "d": "Stir in the tomato paste, cumin and paprika and cook for 1 minute."},
        {"t": "Simmer", "d": "Add the lentils, broth and water. Bring to a boil, then simmer partly covered for 20 to 25 minutes, until the lentils have completely broken down."},
        {"t": "Blend", "d": "Blend until silky smooth. Add water if it is too thick.", "tip": "Blend a little longer than you think for the silkiest texture."},
        {"t": "Finish", "d": "Stir in most of the lemon juice and season with salt. Serve with a sprinkle of dried mint and a little more lemon."}
    ],
    "tips": ["Add lemon at the end, to taste; it lifts the whole soup.", "The soup thickens as it sits. Thin with water when reheating.", "A drizzle of olive oil warmed with paprika is a traditional topping.", "Small-portion tip: a mug of this counts as a small meal."],
    "storage": "Refrigerate for up to 4 days or freeze in portions for up to 3 months.",
    "variations": [["Vegetarian", "Use vegetable broth; the protein drops to about 9 g per bowl."], ["Bulgur", "Add 2 tablespoons fine bulgur with the lentils for a more traditional texture."], ["Spiced butter", "Top with a teaspoon of butter melted with paprika."], ["Make it gentler", "Skip the paprika and use just a little lemon."], ["Protein boost", "Swirl 2 tablespoons Greek yogurt into each bowl for about 3 g more protein."]],
    "nutrition": {"calories": 177, "protein": 14, "carbs": 24, "fat": 3, "fiber": 4},
    "faq": [["Do red lentils need soaking?", "No. They cook in about 20 minutes."], ["Is it gluten-free?", "Yes, if your broth is gluten-free and you skip the bulgur."], ["Can I use green lentils?", "They hold their shape and take longer; the soup will not be as smooth."]],
    "note": "This is a gentle, golden soup for slow days. A squeeze of lemon at the end makes it taste bright and fresh.",
    "diet": ["dairy-free", "gluten-free"],
}

add_recipes(NEW, PHOTOS, label='5 soups')
