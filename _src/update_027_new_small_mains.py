#!/usr/bin/env python3
"""New content, batch 5 of 6: five NEW small-portion mains (nothing replaced).

Photo-first rule (Pexels title/description names the dish):
  chicken-zucchini-stir-fry      36979925  "Delicious Stir-Fry with Chicken and Zucchini" (Soc Nang Dong)
  lemon-herb-baked-cod           37367757  "Delicious Baked Fish with Lemon and Herbs", served with rice (Mahi Mog)
  turkey-stuffed-peppers         39206896  "Green bell peppers stuffed with rice and herbs" (Lena Ti)
  garlic-shrimp-zucchini-noodles 5597691   "Creamy zucchini noodles with shrimp" (Kenan Giffard)
  egg-salad-lettuce-wraps        37112189  "Lettuce wraps with egg filling and crackers" (Mike Art)
Planned "chicken lettuce wraps" had no matching free photo; it became egg salad lettuce wraps.
The cod photo is a generic white fish fillet; the recipe says any firm white fish works.

Nutrition per serving is an ESTIMATE from USDA FoodData Central reference values (rounded):
  Stir-fry (4): chicken breast 454 g raw 545/102 P/12 F; zucchini 400 g 68/4.8 P/12.4 C/4 fib; bell pepper 120 g
    31/1 P/7 C/2 fib; onion 75 g 30/0.8 P/7 C/1 fib; low-sodium soy sauce 32 g 17/2.6 P/1.6 C; honey 7 g 21/6 C;
    cornstarch 5 g 19/4.5 C; garlic, ginger 10/2 C; oil 13.5 g 119/13.5 F; sesame 3 g 17/0.5 P/1.5 F
    -> 877 kcal, 112 P, 41 C, 27 F, 7 fib / 4 = ~219 kcal, 28 P, 10 C, 7 F, 2 fib
  Cod (4): cod 454 g raw 372/81 P/3 F; olive oil 13.5 g 119/13.5 F; lemon, garlic, herbs 15/3 C;
    cooked rice 210 g 273/5.7 P/59 C -> 779 kcal, 87 P, 62 C, 17 F, 1 fib / 4 = ~195 kcal, 22 P, 16 C, 4 F, 0 fib
  Peppers (6): green peppers 720 g 144/6 P/33 C/12 fib; 93% lean turkey 454 g 681/85 P/38 F; cooked rice 158 g
    205/4.3 P/45 C; onion 110 g 44/1.2 P/10 C/2 fib; tomato sauce 425 g 102/5.5 P/22.5 C/6 fib; oil 4.5 g 40/4.5 F;
    herbs, garlic 10/2 C; nonfat Greek yogurt 120 g 71/12.2 P/4.3 C
    -> 1297 kcal, 114 P, 117 C, 43 F, 21 fib / 6 = ~216 kcal, 19 P, 19 C, 7 F, 4 fib
  Shrimp (4): shrimp 454 g raw 386/91 P/2.3 F; zucchini 600 g 102/7.2 P/18.6 C/6 fib; olive oil 9 g 80/9 F;
    garlic 13/3 C; nonfat Greek yogurt 120 g 71/12.2 P/4.3 C; Parmesan 20 g 78/7.1 P/5.2 F; lemon, herbs 8/2 C
    -> 738 kcal, 118 P, 28 C, 17 F, 6 fib / 4 = ~185 kcal, 29 P, 7 C, 4 F, 2 fib
  Egg salad (3): 6 eggs 432/37.8 P/2.4 C/28.8 F; nonfat Greek yogurt 80 g 47/8.1 P/2.9 C; light mayo 15 g 35/1 C/3.5 F;
    Dijon 5; celery 40 g 6/1 C; herbs, lemon 5/1 C; butter lettuce 10/1 P/2 C/1 fib; whole-grain crackers 30 g
    130/3 P/21 C/4 F/3 fib -> 670 kcal, 50 P, 31 C, 36 F, 4 fib / 3 = ~223 kcal, 17 P, 10 C, 12 F, 1 fib
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batchlib import add_recipes

N = None
PHOTOS = {
    'chicken-zucchini-stir-fry': {'id': 36979925, 'photographer': 'Sóc Năng Động', 'photographer_url': 'https://www.pexels.com/@soc-nang-d-ng-2150345854/',
        'photo_url': 'https://www.pexels.com/photo/delicious-stir-fry-with-chicken-and-zucchini-36979925/', 'alt': 'Sautéed chicken and zucchini in a pan.'},
    'lemon-herb-baked-cod': {'id': 37367757, 'photographer': 'Mahi Mog', 'photographer_url': 'https://www.pexels.com/@mahimoh/',
        'photo_url': 'https://www.pexels.com/photo/delicious-baked-fish-with-lemon-and-herbs-37367757/', 'alt': 'Baked white fish with lemon and herbs, served with rice.'},
    'turkey-stuffed-peppers': {'id': 39206896, 'photographer': 'Lena Ti', 'photographer_url': 'https://www.pexels.com/@lena-ti-2153986577/',
        'photo_url': 'https://www.pexels.com/photo/delicious-stuffed-bell-peppers-in-white-bowl-39206896/', 'alt': 'Green bell peppers stuffed with rice and herbs in a white bowl.'},
    'garlic-shrimp-zucchini-noodles': {'id': 5597691, 'photographer': 'Kenan Giffard', 'photographer_url': 'https://www.pexels.com/@kenan-giffard-3777259/',
        'photo_url': 'https://www.pexels.com/photo/zuchini-and-shrimp-in-white-sauce-5597691/', 'alt': 'Creamy zucchini noodles with shrimp and herbs, seen from above.'},
    'egg-salad-lettuce-wraps': {'id': 37112189, 'photographer': 'Mike Art', 'photographer_url': 'https://www.pexels.com/@mike-art-visual-creator-photography-and-video-2159421235/',
        'photo_url': 'https://www.pexels.com/photo/healthy-lettuce-wraps-on-wooden-platter-37112189/', 'alt': 'Lettuce wraps filled with egg salad, with crackers, on a wooden platter.'},
}

NEW = {}
NEW['chicken-zucchini-stir-fry'] = {
    "title": "Chicken and Zucchini Stir-Fry",
    "subtitle": "Tender strips of chicken and zucchini in a light garlic-ginger soy glaze, ready in 25 minutes. About 28 g protein per small plate.",
    "category": "Main Dishes",
    "tags": ["quick", "healthy", "high-protein", "small-plates"],
    "prep": 10, "cook": 15, "time": 25, "serves": 4, "level": "Easy",
    "desc": "Quick, light and about 28 g protein.",
    "intro": [
        "A stir-fry is one of the fastest ways to get a warm, protein-rich plate on the table. Thin strips of chicken breast cook in minutes, and zucchini adds volume without making the plate heavy. Each small plate has about 28 g of protein.",
        "The glaze is simple: low-sodium soy sauce, a little honey, garlic and ginger, thickened with a spoonful of cornstarch so it clings instead of pooling. Serve it on its own or over a small scoop of rice."
    ],
    "why": [["About 28 g protein", "Mostly from lean chicken breast."], ["25 minutes", "Everything cooks in one pan."], ["Light glaze", "Clings to the chicken without a heavy sauce."]],
    "ingredients": [
        {"group": "For the stir-fry", "items": [
            {"q": 1, "u": "lb", "n": "boneless skinless chicken breast", "note": "cut into thin strips", "g": 454},
            {"q": 2, "u": "tsp", "n": "cornstarch"},
            {"q": 1, "u": "tbsp", "n": "neutral oil"},
            {"q": 2, "u": "", "n": "medium zucchini", "note": "sliced into half-moons"},
            {"q": 1, "u": "", "n": "bell pepper", "note": "sliced"},
            {"q": 0.5, "u": "", "n": "onion", "note": "sliced"},
            {"q": 2, "u": "", "n": "garlic cloves", "note": "minced"},
            {"q": 1, "u": "tsp", "n": "fresh ginger", "note": "grated"}]},
        {"group": "For the glaze", "items": [
            {"q": 2, "u": "tbsp", "n": "low-sodium soy sauce"},
            {"q": 1, "u": "tsp", "n": "honey"},
            {"q": 3, "u": "tbsp", "n": "water"},
            {"q": 1, "u": "tsp", "n": "sesame seeds", "note": "to serve"}]}
    ],
    "steps": [
        {"t": "Coat the chicken", "d": "Toss the chicken strips with the cornstarch until lightly coated. Stir the soy sauce, honey and water together in a small bowl."},
        {"t": "Sear the chicken", "d": "Heat the oil in a large skillet or wok over medium-high heat. Add the chicken in a single layer and cook for 5 to 6 minutes, turning once, until golden and cooked through to 165°F (74°C). Move to a plate.", "tip": "Cook in two batches if your pan is small, so the chicken browns instead of steaming."},
        {"t": "Cook the vegetables", "d": "Add the onion, pepper and zucchini to the pan and stir-fry for 4 to 5 minutes, until just tender. Add the garlic and ginger and stir for 30 seconds."},
        {"t": "Glaze", "d": "Return the chicken, pour in the sauce and toss for 1 to 2 minutes, until glossy and slightly thickened."},
        {"t": "Serve small", "d": "Sprinkle with sesame seeds and serve on small plates, with a little rice if you like."}
    ],
    "tips": ["Slice the chicken thin and even so it cooks fast and stays tender.", "Do not overcook the zucchini; it should still have a little bite.", "Swap the honey for a pinch of sugar if you prefer.", "Small-portion tip: serve a small plate with more chicken than vegetables, and keep the rest for lunch tomorrow."],
    "storage": "Refrigerate for up to 3 days. Reheat gently in a skillet with a splash of water, or in the microwave.",
    "variations": [["Broccoli", "Use small broccoli florets instead of the pepper."], ["Gluten-free", "Use tamari instead of soy sauce."], ["Shrimp", "Use peeled shrimp and cook them for just 2 to 3 minutes."], ["Make it gentler", "Skip the garlic and ginger, and peel the zucchini for a softer texture."], ["Protein boost", "Add 1 cup shelled edamame with the vegetables for about 4 g more protein per plate."]],
    "nutrition": {"calories": 219, "protein": 28, "carbs": 10, "fat": 7, "fiber": 2},
    "faq": [["Can I use chicken thighs?", "Yes. Boneless thighs stay juicier; cook them to 175°F (80°C)."], ["Does the nutrition include rice?", "No. A 1/3-cup scoop of cooked rice adds about 70 kcal."], ["Is it dairy-free?", "Yes."]],
    "note": "This is a weeknight plate that comes together faster than takeout, in a portion that is easy to finish.",
    "diet": ["dairy-free"],
}
NEW['lemon-herb-baked-cod'] = {
    "title": "Lemon Herb Baked Cod with Rice",
    "subtitle": "Mild, flaky cod baked with olive oil, lemon, garlic and herbs, served with a small scoop of rice. About 22 g protein per plate, ready in 20 minutes.",
    "category": "Main Dishes",
    "tags": ["quick", "healthy", "high-protein", "small-plates", "gentle"],
    "prep": 5, "cook": 15, "time": 20, "serves": 4, "level": "Easy",
    "desc": "Mild, flaky and very easy to eat.",
    "intro": [
        "Cod is one of the gentlest proteins you can cook: mild in flavor, soft in texture and quick to bake. A drizzle of olive oil, lemon and herbs is all it needs, and each 4-ounce piece has about 20 g of protein.",
        "Serve it with a small scoop of rice and a squeeze of lemon. Any firm white fish works the same way, including haddock, pollock or tilapia."
    ],
    "why": [["About 22 g protein", "From a 4-ounce piece of cod plus rice."], ["Gentle", "Mild flavor and soft, flaky texture."], ["20 minutes", "Mostly hands-off baking."]],
    "ingredients": [
        {"group": "For the fish", "items": [
            {"q": 4, "u": "", "n": "cod fillets", "note": "about 4 oz (113 g) each", "g": 454},
            {"q": 1, "u": "tbsp", "n": "olive oil"},
            {"q": 1, "u": "", "n": "lemon", "note": "half juiced, half sliced"},
            {"q": 1, "u": "", "n": "garlic clove", "note": "minced"},
            {"q": 1, "u": "tsp", "n": "dried oregano or thyme"},
            {"q": 0.5, "u": "tsp", "n": "sweet paprika"},
            {"q": N, "u": "", "n": "salt and pepper", "note": "to taste"},
            {"q": N, "u": "", "n": "fresh parsley or dill", "note": "to serve"}]},
        {"group": "To serve", "items": [{"q": 1.33, "u": "cups", "n": "cooked rice", "note": "warm"}]}
    ],
    "steps": [
        {"t": "Heat the oven", "d": "Heat the oven to 400°F (200°C) and lightly oil a baking dish."},
        {"t": "Season", "d": "Pat the cod dry and place it in the dish. Mix the olive oil, lemon juice, garlic, herbs and paprika, then spoon it over the fish. Season with salt and pepper and lay a lemon slice on each piece."},
        {"t": "Bake", "d": "Bake for 12 to 15 minutes, until the fish flakes easily and reaches 145°F (63°C).", "tip": "Thin fillets cook faster; start checking at 10 minutes."},
        {"t": "Serve", "d": "Serve each piece with a small scoop of rice, spoon over the pan juices and finish with fresh herbs."}
    ],
    "tips": ["Frozen cod works; thaw it overnight in the fridge and pat it very dry.", "Spoon the pan juices over the rice for extra flavor.", "A few cherry tomatoes in the dish make a quick side.", "Small-portion tip: half a fillet with a spoonful of rice is a complete small plate."],
    "storage": "Best fresh. Refrigerate leftovers for up to 2 days and reheat gently, covered, in a low oven, or flake cold over a salad.",
    "variations": [["Other fish", "Use haddock, pollock or tilapia."], ["Potatoes", "Serve with small boiled potatoes instead of rice."], ["Crumb top", "Sprinkle 2 tablespoons panko over the fish before baking."], ["Make it gentler", "Skip the garlic and paprika and serve with plain rice."], ["Protein boost", "Serve with a spoonful of Greek yogurt mixed with dill and lemon for about 3 g more protein."]],
    "nutrition": {"calories": 195, "protein": 22, "carbs": 16, "fat": 4, "fiber": 0},
    "faq": [["How do I know it is done?", "The fish turns opaque and flakes easily with a fork, at 145°F (63°C)."], ["Is it gluten-free?", "Yes, as written."], ["Can I skip the rice?", "Yes. The fish alone is about 125 kcal and 20 g protein."]],
    "note": "This is a calm, simple plate for evenings when you want something warm and light that still does real work.",
    "diet": ["dairy-free", "gluten-free"],
}
NEW['turkey-stuffed-peppers'] = {
    "title": "Turkey and Rice Stuffed Peppers",
    "subtitle": "Small green peppers filled with lean ground turkey, rice, herbs and tomato, baked until tender and finished with Greek yogurt. About 19 g protein per pepper.",
    "category": "Main Dishes",
    "tags": ["healthy", "high-protein", "small-plates", "make-ahead"],
    "prep": 20, "cook": 40, "time": 60, "serves": 6, "servesLabel": "stuffed peppers", "level": "Easy",
    "desc": "One pepper is one small plate.",
    "intro": [
        "Stuffed peppers portion themselves: one pepper is one small plate. This filling is lean ground turkey with a modest amount of rice, onion, herbs and tomato, so each pepper has about 19 g of protein.",
        "The peppers bake in a little tomato sauce until soft, and a spoonful of Greek yogurt on top keeps them cool and creamy. They reheat well, so a batch covers several meals."
    ],
    "why": [["About 19 g protein", "Lean turkey plus a yogurt topping."], ["Built-in portions", "One pepper per plate."], ["Reheats well", "Great for the week ahead."]],
    "ingredients": [
        {"group": "For the peppers", "items": [
            {"q": 6, "u": "", "n": "small green bell peppers", "note": "tops cut off, seeds removed"},
            {"q": 1, "u": "tsp", "n": "olive oil"},
            {"q": 1, "u": "", "n": "onion", "note": "finely chopped"},
            {"q": 2, "u": "", "n": "garlic cloves", "note": "minced"},
            {"q": 1, "u": "lb", "n": "93% lean ground turkey", "g": 454},
            {"q": 1, "u": "cup", "n": "cooked rice"},
            {"q": 1, "u": "can (15 oz)", "n": "tomato sauce", "note": "divided"},
            {"q": 2, "u": "tbsp", "n": "chopped parsley and dill"},
            {"q": 0.5, "u": "tsp", "n": "kosher salt"}]},
        {"group": "To serve", "items": [{"q": 0.5, "u": "cup", "n": "plain nonfat Greek yogurt"}]}
    ],
    "steps": [
        {"t": "Heat the oven", "d": "Heat the oven to 375°F (190°C). Stand the peppers upright in a baking dish that holds them snugly."},
        {"t": "Cook the filling", "d": "Warm the oil in a skillet over medium heat. Cook the onion for 5 minutes, add the garlic, then the turkey. Cook for 6 to 8 minutes, breaking it up, until no pink remains."},
        {"t": "Mix", "d": "Stir in the rice, half the tomato sauce, the herbs and salt."},
        {"t": "Stuff and bake", "d": "Spoon the filling into the peppers. Pour the remaining sauce and 1/4 cup water around them. Cover with foil and bake for 30 minutes, then uncover and bake 10 minutes more, until the peppers are tender.", "tip": "For softer peppers, microwave them for 3 minutes before stuffing."},
        {"t": "Serve", "d": "Top each pepper with a spoonful of Greek yogurt and a little extra dill."}
    ],
    "tips": ["Choose small peppers that stand upright; they make better single portions.", "Red or yellow peppers are sweeter and softer than green.", "Leftover rice works perfectly in the filling.", "Small-portion tip: half a pepper with a spoonful of yogurt is enough on low-appetite days."],
    "storage": "Refrigerate for up to 4 days. Freeze cooked peppers individually for up to 3 months and reheat covered in the oven or microwave.",
    "variations": [["Chicken", "Use ground chicken instead of turkey."], ["Lentils", "Replace half the turkey with cooked lentils."], ["Cheese top", "Add 1 tablespoon shredded mozzarella per pepper for the last 10 minutes."], ["Make it gentler", "Use red peppers, skip the garlic and bake until very soft."], ["Protein boost", "Add 1/2 cup cottage cheese to the filling for about 3 g more protein per pepper."]],
    "nutrition": {"calories": 216, "protein": 19, "carbs": 19, "fat": 7, "fiber": 4},
    "faq": [["Do I need to precook the peppers?", "No, but a quick microwave makes them softer."], ["Is it gluten-free?", "Yes, if your tomato sauce is gluten-free."], ["Can I make them ahead?", "Yes. Stuff them, refrigerate up to a day, then bake."]],
    "note": "A tray of these in the fridge means a warm, ready portion every time you open it.",
    "diet": ["gluten-free"],
}
NEW['garlic-shrimp-zucchini-noodles'] = {
    "title": "Creamy Garlic Shrimp with Zucchini Noodles",
    "subtitle": "Shrimp and zucchini noodles in a light creamy sauce made with Greek yogurt and Parmesan. About 29 g protein per small plate, ready in 20 minutes.",
    "category": "Main Dishes",
    "tags": ["quick", "healthy", "high-protein", "small-plates"],
    "prep": 10, "cook": 10, "time": 20, "serves": 4, "level": "Easy",
    "desc": "Creamy, garlicky and very light.",
    "intro": [
        "Zucchini noodles make a light base, and shrimp cook in just a few minutes, so this plate is fast and easy on a small appetite. Each portion has about 29 g of protein.",
        "The creamy sauce is Greek yogurt and Parmesan stirred in off the heat, which keeps it smooth without any cream. Squeeze over lemon and finish with fresh herbs."
    ],
    "why": [["About 29 g protein", "Shrimp, Greek yogurt and Parmesan."], ["20 minutes", "Shrimp cook in 3 minutes."], ["No cream", "Greek yogurt makes the sauce creamy."]],
    "ingredients": [
        {"group": "For the shrimp and noodles", "items": [
            {"q": 1, "u": "lb", "n": "large shrimp", "note": "peeled and deveined", "g": 454},
            {"q": 2, "u": "tsp", "n": "olive oil"},
            {"q": 3, "u": "", "n": "garlic cloves", "note": "minced"},
            {"q": 3, "u": "", "n": "medium zucchini", "note": "spiralized"},
            {"q": N, "u": "", "n": "salt and pepper", "note": "to taste"}]},
        {"group": "For the sauce", "items": [
            {"q": 0.5, "u": "cup", "n": "plain nonfat Greek yogurt", "note": "at room temperature"},
            {"q": 0.25, "u": "cup", "n": "finely grated Parmesan"},
            {"q": 0.5, "u": "", "n": "lemon", "note": "juiced"},
            {"q": N, "u": "", "n": "fresh parsley and chili flakes", "note": "to serve"}]}
    ],
    "steps": [
        {"t": "Cook the shrimp", "d": "Pat the shrimp dry and season lightly. Warm the oil in a large skillet over medium-high heat and cook the shrimp for 1 to 2 minutes per side, until pink. Move to a plate."},
        {"t": "Cook the noodles", "d": "Lower the heat to medium. Add the garlic for 30 seconds, then the zucchini noodles. Toss for 2 to 3 minutes, just until warm.", "tip": "Do not overcook the zucchini noodles or they release water and turn soft."},
        {"t": "Make the sauce off the heat", "d": "Take the pan off the heat. Stir in the yogurt, Parmesan and lemon juice until creamy, then return the shrimp and toss.", "tip": "Adding yogurt off the heat keeps it from splitting."},
        {"t": "Serve", "d": "Divide among small plates and finish with parsley and a pinch of chili flakes."}
    ],
    "tips": ["Pat the zucchini noodles dry with a towel before cooking.", "Frozen shrimp work well; thaw them in cold water and dry well.", "Store-bought zucchini noodles save time.", "Small-portion tip: five or six shrimp with a small nest of noodles is a satisfying small plate."],
    "storage": "Best fresh. Refrigerate leftovers for up to 1 day and reheat gently; the noodles will soften.",
    "variations": [["Half pasta", "Mix the zucchini noodles with 2 oz cooked spaghetti for a heartier plate."], ["Chicken", "Use thin chicken strips, cooked through to 165°F (74°C)."], ["Dairy-free", "Use a dairy-free yogurt and skip the Parmesan."], ["Make it gentler", "Use 1 garlic clove, skip the chili flakes and serve warm."], ["Protein boost", "Add 2 tablespoons more Parmesan for about 4 g more protein."]],
    "nutrition": {"calories": 185, "protein": 29, "carbs": 7, "fat": 4, "fiber": 2},
    "faq": [["Why did my sauce split?", "The pan was too hot. Stir the yogurt in off the heat."], ["Is it gluten-free?", "Yes, as written."], ["Can I use pasta instead?", "Yes. Use about 6 oz pasta; the calories and carbs will go up."]],
    "note": "Light, quick and creamy: a plate that feels like a treat without being heavy.",
    "diet": ["gluten-free"],
}
NEW['egg-salad-lettuce-wraps'] = {
    "title": "Greek Yogurt Egg Salad Lettuce Wraps",
    "subtitle": "Creamy egg salad made with Greek yogurt and a little light mayo, spooned into butter lettuce cups and served with a few crackers. About 17 g protein per serving.",
    "category": "Main Dishes",
    "tags": ["quick", "high-protein", "small-plates", "gentle", "make-ahead"],
    "prep": 10, "cook": 12, "time": 22, "serves": 3, "servesLabel": "servings (2 wraps each)", "level": "Easy",
    "desc": "Soft, cool and easy to eat.",
    "intro": [
        "Egg salad is soft, cool and mild, which makes it a good fit for days when hot food does not sound good. This version uses mostly Greek yogurt with just a little light mayo, so it stays creamy and adds protein. Each serving has about 17 g.",
        "Spoon it into butter lettuce leaves for a light wrap, with a few whole-grain crackers on the side for crunch. The egg salad keeps for a few days in the fridge."
    ],
    "why": [["About 17 g protein", "Eggs plus Greek yogurt."], ["Cool and gentle", "No reheating needed."], ["Make-ahead", "Keeps 3 days in the fridge."]],
    "ingredients": [
        {"group": "For the egg salad", "items": [
            {"q": 6, "u": "", "n": "large eggs"},
            {"q": 0.33, "u": "cup", "n": "plain nonfat Greek yogurt"},
            {"q": 1, "u": "tbsp", "n": "light mayonnaise"},
            {"q": 1, "u": "tsp", "n": "Dijon mustard"},
            {"q": 1, "u": "", "n": "celery stalk", "note": "finely diced"},
            {"q": 1, "u": "tbsp", "n": "chopped chives or dill"},
            {"q": N, "u": "", "n": "salt, pepper and a squeeze of lemon", "note": "to taste"}]},
        {"group": "To serve", "items": [
            {"q": 6, "u": "", "n": "butter lettuce leaves"},
            {"q": 1, "u": "oz", "n": "whole-grain crackers", "note": "about 12 small"}]}
    ],
    "steps": [
        {"t": "Cook the eggs", "d": "Place the eggs in a pot, cover with cold water and bring to a boil. Turn off the heat, cover and let stand for 11 minutes."},
        {"t": "Cool and peel", "d": "Move the eggs to a bowl of ice water for 5 minutes, then peel.", "tip": "Peeling under running water makes it easier."},
        {"t": "Mix", "d": "Chop the eggs and stir with the yogurt, mayo, Dijon, celery and herbs. Season with salt, pepper and a squeeze of lemon."},
        {"t": "Fill and serve", "d": "Spoon the egg salad into the lettuce leaves and serve with crackers on the side."}
    ],
    "tips": ["Mash the eggs finely for a softer, smoother egg salad.", "Chill the egg salad for 20 minutes for the best flavor.", "Keep the lettuce and egg salad separate until serving.", "Small-portion tip: one wrap and two crackers make a light small plate."],
    "storage": "Refrigerate the egg salad in an airtight container for up to 3 days. Fill the lettuce just before eating.",
    "variations": [["Avocado", "Replace the mayo with 1/4 mashed avocado."], ["Curry", "Add 1/2 teaspoon mild curry powder."], ["On toast", "Serve on a small slice of whole-grain toast instead of lettuce."], ["Make it gentler", "Skip the mustard and celery and mash the eggs smooth."], ["Protein boost", "Add 2 tablespoons more Greek yogurt and serve with an extra egg white for about 5 g more protein."]],
    "nutrition": {"calories": 223, "protein": 17, "carbs": 10, "fat": 12, "fiber": 1},
    "faq": [["Can I make it without mayo?", "Yes. Use all Greek yogurt and a little extra Dijon."], ["Is it gluten-free?", "Yes, with gluten-free crackers or none."], ["How long does it keep?", "Up to 3 days in the fridge."]],
    "note": "A cool, soft plate for warm days or slow afternoons, ready in the fridge whenever you need it.",
    "diet": ["vegetarian"],
}

add_recipes(NEW, PHOTOS, label='5 small mains')
