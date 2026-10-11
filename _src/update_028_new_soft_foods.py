#!/usr/bin/env python3
"""New content, batch 6 of 6: five NEW soft foods for harder days (nothing replaced).

Photo-first rule (Pexels title/description names the dish):
  chicken-rice-congee          38790905  "Traditional Thai Chicken Congee with Toppings", soft-boiled egg (Archudio Studio)
  cottage-cheese-mashed-potatoes 30635679 "Creamy Mashed Potatoes with Green Onions" (IARA MELO)
  savory-cottage-cheese-bowl   4198171   "Cottage cheese garnished with fresh green onions in a white bowl" (Kaboompics)
  greek-yogurt-chia-pudding    4397294   "Homemade chia seed pudding with almond flakes and blueberries" in a jar (Antoni Shkraba)
  protein-rice-pudding         116725    "Creamy rice pudding with fresh red berries" (Markus Spiske)
Planned salmon cakes, ricotta scrambled eggs and silken tofu pudding had no clean matching free photo (the only
fish-cake photo shows fried cakes with chips); they became the cottage cheese bowl, chia pudding and rice pudding.

Nutrition per serving is an ESTIMATE from USDA FoodData Central reference values and typical labels (rounded):
  Congee (6): jasmine rice 100 g dry 365/7 P/80 C/0.7 F; chicken breast 340 g raw 408/77 P/9 F; low-sodium chicken
    bone broth 960 ml 160/36 P/2 C/1 F (labels vary); ginger, scallion 10/2 C; 3 eggs 215/19 P/1 C/14 F;
    sesame oil 4.5 g 40/4.5 F; low-sodium soy 16 g 9/1.3 P/1 C
    -> 1207 kcal, 140 P, 86 C, 29 F / 6 = ~201 kcal, 23 P, 14 C, 5 F, 0 fib
  Mash (4): Yukon Gold potatoes 680 g 524/13.6 P/119 C/0.7 F/9 fib; 1% cottage cheese 226 g 163/28 P/6 C/2.3 F;
    nonfat Greek yogurt 60 g 35/6 P/2 C; butter 14 g 100/11.4 F; milk 60 ml 30/2 P/3 C/1 F; green onion 10/2 C/1 fib
    -> 862 kcal, 50 P, 132 C, 15 F, 10 fib / 4 = ~216 kcal, 12 P, 33 C, 4 F, 3 fib
  Cottage bowl (2): 2% cottage cheese 452 g 366/48 P/19 C/10 F; cucumber 150 g 23/1 P/5 C; cherry tomatoes 100 g
    18/0.9 P/3.9 C/1.2 fib; green onion 15 g 5/1 C/0.4 fib; olive oil 4.5 g 40/4.5 F; seasoning 5
    -> 457 kcal, 50 P, 29 C, 15 F, 2 fib / 2 = ~229 kcal, 25 P, 15 C, 7 F, 1 fib
  Chia pudding (3): chia 36 g 175/6 P/15 C/11 F/12 fib; 2% milk 240 ml 122/8 P/12 C/4.8 F; nonfat Greek yogurt 227 g
    134/23 P/8 C/0.9 F; maple 20 g 52/13 C; vanilla 6; blueberries 75 g 43/0.5 P/11 C/1.8 fib; almonds 10 g
    58/2 P/2 C/5 F/1.2 fib -> 590 kcal, 40 P, 61 C, 22 F, 15 fib / 3 = ~197 kcal, 13 P, 20 C, 7 F, 5 fib
  Rice pudding (4): arborio rice 65 g dry 230/4.5 P/51 C/0.4 F; ultra-filtered 2% milk 720 ml 360/39 P/18 C/13.5 F
    (label values); maple 30 g 78/20 C; vanilla, cinnamon 10/2 C; berries 80 g 45/1 P/11 C/3.4 fib
    -> 723 kcal, 45 P, 102 C, 14 F, 4 fib / 4 = ~181 kcal, 11 P, 26 C, 4 F, 1 fib
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batchlib import add_recipes

N = None
PHOTOS = {
    'chicken-rice-congee': {'id': 38790905, 'photographer': 'Archudio Studio', 'photographer_url': 'https://www.pexels.com/@archudio/',
        'photo_url': 'https://www.pexels.com/photo/traditional-thai-chicken-congee-with-toppings-38790905/', 'alt': 'A bowl of chicken rice congee topped with fresh herbs and a soft-boiled egg.'},
    'cottage-cheese-mashed-potatoes': {'id': 30635679, 'photographer': 'IARA MELO', 'photographer_url': 'https://www.pexels.com/@iara-melo-558346607/',
        'photo_url': 'https://www.pexels.com/photo/creamy-mashed-potatoes-with-green-onions-30635679/', 'alt': 'Creamy mashed potatoes topped with green onions in a white bowl.'},
    'savory-cottage-cheese-bowl': {'id': 4198171, 'photographer': 'Kaboompics', 'photographer_url': 'https://www.pexels.com/@karola-g/',
        'photo_url': 'https://www.pexels.com/photo/bowl-with-healthy-food-in-kitchen-4198171/', 'alt': 'Cottage cheese with chopped green onions in a white bowl.'},
    'greek-yogurt-chia-pudding': {'id': 4397294, 'photographer': 'Antoni Shkraba', 'photographer_url': 'https://www.pexels.com/@shkrabaanthony/',
        'photo_url': 'https://www.pexels.com/photo/homemade-chia-seed-pudding-with-almond-flakes-and-blueberries-4397294/', 'alt': 'A jar of chia pudding topped with blueberries and almond flakes.'},
    'protein-rice-pudding': {'id': 116725, 'photographer': 'Markus Spiske', 'photographer_url': 'https://www.pexels.com/@markusspiske/',
        'photo_url': 'https://www.pexels.com/photo/food-healthy-meal-breakfast-116725/', 'alt': 'Creamy rice pudding topped with fresh red berries.'},
}

NEW = {}
NEW['chicken-rice-congee'] = {
    "title": "Gentle Chicken Rice Congee with Soft Egg",
    "subtitle": "Rice simmered slowly in chicken bone broth until soft and porridge-like, with finely shredded chicken, ginger and half a soft-boiled egg. About 23 g protein per small bowl.",
    "category": "Soups",
    "tags": ["healthy", "high-protein", "small-plates", "make-ahead", "gentle"],
    "prep": 10, "cook": 60, "time": 70, "serves": 6, "servesLabel": "small bowls", "level": "Easy",
    "desc": "Soft, warm and about 23 g protein.",
    "intro": [
        "Congee is rice cooked in plenty of broth until the grains break down into a soft, silky porridge. It is one of the gentlest warm foods there is: mild, smooth and easy to eat a few spoonfuls at a time.",
        "Cooking the rice in chicken bone broth and stirring in finely shredded chicken gives each small bowl about 23 g of protein. Half a soft-boiled egg, a little ginger and green onion finish it."
    ],
    "why": [["About 23 g protein", "Chicken, bone broth and egg."], ["Very soft", "The rice breaks down completely."], ["Freezer-friendly", "Freeze in single portions."]],
    "ingredients": [
        {"group": "For the congee", "items": [
            {"q": 0.5, "u": "cup", "n": "jasmine rice", "note": "rinsed", "g": 100},
            {"q": 4, "u": "cups", "n": "low-sodium chicken bone broth"},
            {"q": 3, "u": "cups", "n": "water"},
            {"q": 12, "u": "oz", "n": "boneless skinless chicken breast", "g": 340},
            {"q": 1, "u": "inch", "n": "fresh ginger", "note": "sliced"},
            {"q": N, "u": "", "n": "salt", "note": "to taste"}]},
        {"group": "To serve", "items": [
            {"q": 3, "u": "", "n": "eggs", "note": "soft-boiled and halved"},
            {"q": 2, "u": "", "n": "green onions", "note": "thinly sliced"},
            {"q": 1, "u": "tsp", "n": "toasted sesame oil"},
            {"q": 1, "u": "tbsp", "n": "low-sodium soy sauce"},
            {"q": N, "u": "", "n": "cilantro", "note": "optional"}]}
    ],
    "steps": [
        {"t": "Simmer the rice", "d": "Put the rice, broth, water and ginger in a large pot. Bring to a boil, then lower the heat and simmer partly covered for 45 minutes, stirring every 10 minutes, until the rice has broken down into a thick porridge.", "tip": "Stir more often near the end so the rice does not stick."},
        {"t": "Poach the chicken", "d": "After 20 minutes, add the whole chicken breast to the pot and simmer for 15 to 18 minutes, until it reaches 165°F (74°C). Lift it out."},
        {"t": "Shred finely", "d": "Shred the chicken very finely with two forks and stir it back into the congee. Remove the ginger and season with a little salt."},
        {"t": "Cook the eggs", "d": "Lower the eggs into simmering water for 7 minutes, cool in cold water, peel and halve."},
        {"t": "Serve small", "d": "Ladle into small bowls and top each with half an egg, green onion, a few drops of sesame oil and soy sauce."}
    ],
    "tips": ["Add hot water when reheating; congee thickens a lot as it cools.", "For a smoother texture, blend a ladleful and stir it back in.", "A slow cooker works too: 6 hours on low.", "Small-portion tip: a 3/4-cup bowl with half an egg is a complete small meal."],
    "storage": "Refrigerate for up to 4 days. Freeze without the eggs for up to 3 months and reheat with a splash of water.",
    "variations": [["Fish", "Stir in small pieces of white fish for the last 5 minutes instead of chicken."], ["Vegetarian", "Use vegetable broth and silken tofu; the protein drops to about 9 g per bowl."], ["Brown rice", "Use brown rice and simmer 20 minutes longer."], ["Make it gentler", "Skip the ginger, sesame oil and soy sauce and serve warm, not hot."], ["Protein boost", "Top with a whole egg instead of half for about 3 g more protein."]],
    "nutrition": {"calories": 201, "protein": 23, "carbs": 14, "fat": 5, "fiber": 0},
    "faq": [["Why so much liquid?", "Congee needs about 14 parts liquid to 1 part rice to become soft and porridge-like."], ["Is it gluten-free?", "Yes, with tamari or a gluten-free soy sauce and broth."], ["Can I use leftover rice?", "Yes. Simmer 1 1/2 cups cooked rice in the broth for about 25 minutes."]],
    "note": "Congee is what many people reach for when they feel unwell, and for good reason. It is warm, soft and easy, and this version quietly carries a good amount of protein.",
    "diet": ["dairy-free"],
}
NEW['cottage-cheese-mashed-potatoes'] = {
    "title": "Creamy Cottage Cheese Mashed Potatoes",
    "subtitle": "Soft Yukon Gold potatoes mashed with blended cottage cheese, a little Greek yogurt and butter, topped with green onion. About 12 g protein per small bowl.",
    "category": "Main Dishes",
    "tags": ["small-plates", "make-ahead", "gentle"],
    "prep": 10, "cook": 20, "time": 30, "serves": 4, "servesLabel": "small bowls", "level": "Easy",
    "desc": "Soft, creamy mash with a protein lift.",
    "intro": [
        "Mashed potatoes are one of the softest, most comforting foods there is. Blending cottage cheese until smooth and folding it in keeps them creamy and adds protein, so each small bowl has about 12 g instead of the usual 4.",
        "Eat a small bowl on its own on hard days, or serve it next to a little salmon, chicken or turkey meatballs for a fuller plate."
    ],
    "why": [["About 12 g protein", "Blended cottage cheese and yogurt."], ["Very soft", "Easy to eat in small spoonfuls."], ["Reheats well", "Make once, eat for days."]],
    "ingredients": [
        {"group": "For the mash", "items": [
            {"q": 1.5, "u": "lb", "n": "Yukon Gold potatoes", "note": "peeled and cut into chunks", "g": 680},
            {"q": 1, "u": "cup", "n": "low-fat cottage cheese", "g": 226},
            {"q": 0.25, "u": "cup", "n": "plain nonfat Greek yogurt"},
            {"q": 1, "u": "tbsp", "n": "butter"},
            {"q": 0.25, "u": "cup", "n": "warm milk", "note": "plus more as needed"},
            {"q": N, "u": "", "n": "salt and pepper", "note": "to taste"},
            {"q": 2, "u": "", "n": "green onions", "note": "thinly sliced"}]}
    ],
    "steps": [
        {"t": "Boil the potatoes", "d": "Cover the potatoes with cold salted water, bring to a boil and simmer for 15 to 18 minutes, until a knife slides in easily."},
        {"t": "Blend the cottage cheese", "d": "While they cook, blend the cottage cheese and yogurt until completely smooth.", "tip": "Blending removes the curds, so the mash stays silky."},
        {"t": "Mash", "d": "Drain the potatoes well and return them to the warm pot. Mash with the butter, then stir in the blended cottage cheese and enough warm milk for a soft texture."},
        {"t": "Season and serve", "d": "Season with salt and pepper and serve in small bowls, topped with green onion."}
    ],
    "tips": ["Yukon Golds make the creamiest mash; russets are fluffier.", "Keep the heat off once the dairy goes in so it stays smooth.", "Reheat with a splash of milk.", "Small-portion tip: a 1/2-cup scoop next to a few bites of protein is a complete small plate."],
    "storage": "Refrigerate for up to 4 days. Reheat gently in a covered pot or the microwave with a little milk.",
    "variations": [["Garlic", "Simmer 2 peeled garlic cloves with the potatoes and mash them in."], ["Cauliflower", "Replace half the potatoes with cauliflower florets."], ["Cheesy", "Stir in 2 tablespoons grated Parmesan."], ["Make it gentler", "Skip the pepper and green onion and keep the mash extra smooth."], ["Protein boost", "Top with a soft egg or serve with shredded chicken for 6 to 10 g more protein."]],
    "nutrition": {"calories": 216, "protein": 12, "carbs": 33, "fat": 4, "fiber": 3},
    "faq": [["Can I taste the cottage cheese?", "Barely. Blended smooth, it tastes like a creamy, slightly tangy mash."], ["Is it gluten-free?", "Yes, as written."], ["Can I freeze it?", "Yes, for up to 2 months; stir well when reheating."]],
    "note": "A warm bowl of mashed potatoes asks very little of a small appetite, and this one does more nutritional work than most.",
    "diet": ["vegetarian", "gluten-free"],
}
NEW['savory-cottage-cheese-bowl'] = {
    "title": "Savory Herbed Cottage Cheese Bowl",
    "subtitle": "Cool cottage cheese with green onion, cucumber, cherry tomatoes, a drizzle of olive oil and everything seasoning. No cooking, about 25 g protein per bowl.",
    "category": "Snacks",
    "tags": ["quick", "healthy", "high-protein", "small-plates", "gentle"],
    "prep": 5, "cook": 0, "time": 5, "serves": 2, "servesLabel": "bowls", "level": "Easy",
    "desc": "Five minutes, no cooking, about 25 g protein.",
    "intro": [
        "Cottage cheese is one of the easiest high-protein foods to keep in the fridge, and it does not have to be sweet. Topped with green onion, cucumber and tomatoes, it becomes a cool, savory bowl in five minutes.",
        "Each bowl has about 25 g of protein, and it needs no cooking at all, which makes it a good option for warm days or tired evenings."
    ],
    "why": [["About 25 g protein", "Almost all from cottage cheese."], ["No cooking", "Ready in five minutes."], ["Cool and mild", "Easy when hot food does not appeal."]],
    "ingredients": [
        {"group": "For the bowls", "items": [
            {"q": 2, "u": "cups", "n": "2% cottage cheese", "g": 452},
            {"q": 2, "u": "", "n": "green onions", "note": "thinly sliced"},
            {"q": 0.5, "u": "", "n": "cucumber", "note": "diced"},
            {"q": 0.5, "u": "cup", "n": "cherry tomatoes", "note": "halved"},
            {"q": 1, "u": "tsp", "n": "olive oil"},
            {"q": 1, "u": "tsp", "n": "everything bagel seasoning", "note": "or salt and pepper"},
            {"q": N, "u": "", "n": "fresh dill or chives", "note": "optional"}]}
    ],
    "steps": [
        {"t": "Divide", "d": "Spoon the cottage cheese into two bowls."},
        {"t": "Top", "d": "Scatter over the green onion, cucumber and tomatoes."},
        {"t": "Finish", "d": "Drizzle with olive oil and sprinkle with seasoning and herbs. Serve cold."}
    ],
    "tips": ["Small-curd cottage cheese feels softer and smoother.", "Blend the cottage cheese first if you do not like the curds.", "Add a few whole-grain crackers for crunch.", "Small-portion tip: half a bowl is still about 12 g protein."],
    "storage": "Best fresh. Cottage cheese keeps in the fridge until its date once opened; add the vegetables just before eating.",
    "variations": [["Mediterranean", "Top with olives, a little feta and oregano."], ["Avocado", "Add a few slices of avocado."], ["On toast", "Spread on a small slice of whole-grain toast."], ["Make it gentler", "Skip the onion and seasoning and top with peeled cucumber only."], ["Protein boost", "Add a chopped hard-boiled egg for about 6 g more protein."]],
    "nutrition": {"calories": 229, "protein": 25, "carbs": 15, "fat": 7, "fiber": 1},
    "faq": [["Is cottage cheese salty?", "It can be. Low-sodium versions are available; skip the seasoning if using regular."], ["Is it gluten-free?", "Yes, if your seasoning is gluten-free."], ["Can I make it ahead?", "Keep the vegetables chopped in a separate container and assemble when ready."]],
    "note": "This is the bowl to make when you know you need protein and cannot face cooking.",
    "diet": ["vegetarian", "gluten-free"],
}
NEW['greek-yogurt-chia-pudding'] = {
    "title": "Blueberry Greek Yogurt Chia Pudding",
    "subtitle": "Chia seeds soaked overnight in milk and Greek yogurt, topped with blueberries and almond flakes. Soft, cool and about 13 g protein per jar.",
    "category": "Snacks",
    "tags": ["healthy", "small-plates", "make-ahead", "gentle"],
    "prep": 5, "cook": 0, "chill": 240, "time": 245, "serves": 3, "servesLabel": "small jars", "level": "Easy",
    "desc": "Make it tonight, eat it cold tomorrow.",
    "intro": [
        "Chia seeds soak up liquid and turn into a soft, spoonable pudding with no cooking. Mixing in Greek yogurt makes it creamier and adds protein, so each small jar has about 13 g.",
        "It needs a few hours in the fridge, so it is ideal to make in the evening. Top with blueberries and a few almond flakes before eating."
    ],
    "why": [["About 13 g protein", "Greek yogurt, milk and chia."], ["5 g fiber", "From the chia seeds."], ["No cooking", "Stir, chill, eat."]],
    "ingredients": [
        {"group": "For the pudding", "items": [
            {"q": 3, "u": "tbsp", "n": "chia seeds", "g": 36},
            {"q": 1, "u": "cup", "n": "2% milk", "note": "or any milk"},
            {"q": 1, "u": "cup", "n": "plain nonfat Greek yogurt", "g": 227},
            {"q": 1, "u": "tbsp", "n": "maple syrup"},
            {"q": 1, "u": "tsp", "n": "vanilla extract"}]},
        {"group": "To top", "items": [
            {"q": 0.5, "u": "cup", "n": "blueberries"},
            {"q": 1, "u": "tbsp", "n": "sliced almonds"}]}
    ],
    "steps": [
        {"t": "Mix", "d": "Whisk the milk, yogurt, maple syrup and vanilla until smooth, then whisk in the chia seeds."},
        {"t": "Stir again", "d": "Wait 5 minutes and whisk again to break up any clumps.", "tip": "This second stir is what keeps the pudding smooth."},
        {"t": "Chill", "d": "Divide among three small jars, cover and refrigerate for at least 4 hours or overnight."},
        {"t": "Top and serve", "d": "Stir, then top with blueberries and almonds."}
    ],
    "tips": ["For a completely smooth texture, blend the pudding after it sets.", "Add a splash of milk if it is too thick.", "Frozen blueberries work; thaw them first.", "Small-portion tip: a few spoonfuls is enough on hard days; the rest keeps."],
    "storage": "Refrigerate in covered jars for up to 4 days. Add toppings just before eating.",
    "variations": [["Chocolate", "Whisk in 1 tablespoon cocoa powder."], ["Mango", "Top with diced mango instead of blueberries."], ["Dairy-free", "Use soy milk and a thick plant yogurt; protein will be lower."], ["Make it gentler", "Blend it smooth and skip the almonds."], ["Protein boost", "Whisk in 1 scoop vanilla protein powder with extra milk for about 7 g more protein per jar."]],
    "nutrition": {"calories": 197, "protein": 13, "carbs": 20, "fat": 7, "fiber": 5},
    "faq": [["Why is my pudding lumpy?", "Whisk again after 5 minutes; the seeds clump at first."], ["Is it gluten-free?", "Yes, as written."], ["Can I skip the yogurt?", "Yes, use 2 cups milk total, but the protein drops to about 6 g."]],
    "note": "A jar waiting in the fridge makes the first meal of a hard day one less decision.",
    "diet": ["vegetarian", "gluten-free"],
}
NEW['protein-rice-pudding'] = {
    "title": "Creamy Protein Rice Pudding with Berries",
    "subtitle": "Arborio rice cooked slowly in ultra-filtered milk with vanilla and cinnamon, served warm or cold with fresh berries. About 11 g protein per small bowl.",
    "category": "Desserts",
    "tags": ["small-plates", "make-ahead", "gentle"],
    "prep": 5, "cook": 35, "time": 40, "serves": 4, "servesLabel": "small bowls", "level": "Easy",
    "desc": "Soft, creamy and comforting, warm or cold.",
    "intro": [
        "Rice pudding is soft, mild and comforting, and it is good warm or straight from the fridge. Cooking it in ultra-filtered milk, which has more protein than regular milk, gives each small bowl about 11 g.",
        "A little maple syrup, vanilla and cinnamon keep it lightly sweet, and fresh berries add brightness on top."
    ],
    "why": [["About 11 g protein", "From ultra-filtered milk."], ["Very soft", "Easy to eat a few spoonfuls."], ["Warm or cold", "Good both ways."]],
    "ingredients": [
        {"group": "For the pudding", "items": [
            {"q": 0.33, "u": "cup", "n": "arborio or short-grain rice", "g": 65},
            {"q": 3, "u": "cups", "n": "ultra-filtered 2% milk", "note": "such as Fairlife"},
            {"q": 2, "u": "tbsp", "n": "maple syrup"},
            {"q": 1, "u": "tsp", "n": "vanilla extract"},
            {"q": 0.25, "u": "tsp", "n": "ground cinnamon"},
            {"q": 1, "u": "pinch", "n": "salt"}]},
        {"group": "To serve", "items": [{"q": 0.5, "u": "cup", "n": "fresh berries", "note": "redcurrants, raspberries or blueberries"}]}
    ],
    "steps": [
        {"t": "Simmer", "d": "Put the rice, milk and salt in a heavy saucepan. Bring to a gentle simmer over medium heat, stirring."},
        {"t": "Cook slowly", "d": "Lower the heat and cook uncovered for 30 to 35 minutes, stirring often, until the rice is very soft and the pudding is thick and creamy.", "tip": "Keep the heat low; milk scorches easily."},
        {"t": "Flavor", "d": "Stir in the maple syrup, vanilla and cinnamon."},
        {"t": "Serve", "d": "Serve warm, or chill for a thicker pudding. Top with berries."}
    ],
    "tips": ["The pudding thickens a lot as it cools; stir in a splash of milk to loosen.", "Regular milk works, but the protein drops to about 7 g per bowl.", "A strip of lemon zest in the milk adds a fresh note.", "Small-portion tip: a 1/2-cup bowl is a satisfying small dessert."],
    "storage": "Refrigerate for up to 4 days. Eat cold or rewarm with a little milk.",
    "variations": [["Coconut", "Use half coconut milk; protein will be lower."], ["Cardamom", "Add a pinch of ground cardamom with the cinnamon."], ["Apple", "Top with soft cooked apple instead of berries."], ["Make it gentler", "Skip the cinnamon and serve with blueberries, which are less tart."], ["Protein boost", "Stir 1/2 cup Greek yogurt into the cooled pudding for about 3 g more protein per bowl."]],
    "nutrition": {"calories": 181, "protein": 11, "carbs": 26, "fat": 4, "fiber": 1},
    "faq": [["What is ultra-filtered milk?", "Milk filtered to concentrate the protein; check labels, as values vary by brand."], ["Is it gluten-free?", "Yes, as written."], ["Can I use leftover rice?", "Yes. Simmer 1 cup cooked rice in 2 cups milk for about 15 minutes."]],
    "note": "Soft, sweet and familiar, this is a small dessert that is easy to say yes to.",
    "diet": ["vegetarian", "gluten-free"],
}

add_recipes(NEW, PHOTOS, label='5 soft foods')
