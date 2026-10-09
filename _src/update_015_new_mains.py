#!/usr/bin/env python3
"""New recipes 3/3: replace the last four off-focus recipes.

  creamy-garlic-pasta          -> lighter-chicken-alfredo
  beef-tacos                   -> turkey-taco-rice-bowls
  honey-garlic-chicken-thighs  -> crispy-baked-chicken-bites
  mushroom-risotto             -> turkey-meatballs-tomato-sauce

Same approach as update_013/014. Photo rule: the Pexels title or description must name the dish; when no
free photo of the planned dish existed, the recipe was adapted to a real photo instead.
  lighter-chicken-alfredo        37118296  "Close-up of creamy chicken Alfredo pasta topped with Parmesan and parsley" (Kemal Can)
  turkey-taco-rice-bowls         4929692   "Mexican-inspired bowl with corn, ground beef, rice, and salsa" (Justin Doherty)
  crispy-baked-chicken-bites     30882821  "Golden Crispy Chicken Bites with Fresh Salad", with a dip (Đậu Photograph)
  turkey-meatballs-tomato-sauce  34314421  "Delicious Meatballs in Rich Tomato Sauce", parsley (ERIVELTO Martins)
Planned "taco lettuce cups" and "honey garlic chicken bites" had no matching free photo, so they became
taco rice bowls and crispy baked chicken bites with a yogurt dip.

Also: the "Everyday Favorites" category is removed (no recipe carries the 'everyday' tag any more), step
photos of the old recipes are removed, and any quoted reference to an old id in other _src files is
pointed at the new id.

Nutrition per serving is an ESTIMATE from USDA FoodData Central reference values (rounded):
  Lighter chicken alfredo (5): fettuccine 170 g dry 631/22.1 P/127.5 C/2.6 F; chicken breast 340 g raw
    408/76.5 P/8.8 F; 2% cottage cheese 226 g 183/23.7 P/8.1 C/5.1 F; Parmesan 40 g 157/14.3 P/10.4 F;
    2% milk 122 g 61/4 P/6 C/2.4 F; butter 14 g 100/11.4 F; garlic 13; spinach 60 g 14/1.7 P; oil 4.5 g 40
    -> 1607 kcal, 142 P, 148 C, 45 F, 7 fiber / 5 = ~320 kcal, 28 P, 30 C, 9 F, 1 fiber
  Turkey taco rice bowls (5): 93% lean turkey 454 g raw 681/85 P/37.7 F; cooked rice 210 g 273/5.7 P/59 C;
    corn 150 g 132/4.5 P/28 C; black beans 172 g 157/10.3 P/28 C/11.8 fiber; salsa 130 g 47/2 P/9 C;
    nonfat Greek yogurt 120 g 71/12.2 P; oil 40; spices 20; lettuce 10
    -> 1431 kcal, 120 P, 134 C, 45 F, 19 fiber / 5 = ~285 kcal, 24 P, 27 C, 9 F, 4 fiber
  Crispy baked chicken bites (4): chicken breast 454 g raw 545/102 P/11.8 F; egg 72/6.3 P/4.8 F; panko 40 g
    158/5 P/31 C; Parmesan 20 g 78/7.1 P/5.2 F; oil 40; nonfat Greek yogurt 180 g 106/18.3 P/6.5 C;
    honey 7 g 21; Dijon 10; spices and lemon 13
    -> 1043 kcal, 139 P, 46 C, 29 F, 1 fiber / 4 = ~260 kcal, 35 P, 11 C, 7 F, 0 fiber
  Turkey meatballs in tomato sauce (5): 93% lean turkey 454 g 681/85 P/37.7 F; egg 72/6.3 P/4.8 F;
    breadcrumbs 36 g 142/4.8 P/26 C; Parmesan 20 g 78/7.1 P/5.2 F; onion 22; garlic 13; crushed tomatoes
    794 g 254/12.7 P/58 C/15 fiber; olive oil 13.5 g 119; herbs 5
    -> 1386 kcal, 117 P, 93 C, 65 F, 17 fiber / 5 = ~277 kcal, 23 P, 19 C, 13 F, 3 fiber

Nothing in recipes.json changes unless every download succeeds. Safe to re-run.
"""
import glob, io, json, os, re, subprocess, sys, urllib.request

sys.stderr = sys.stdout

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
IMG = os.path.join(ROOT, 'images')
P = lambda n: os.path.join(HERE, n)

OLD_TO_NEW = {
    'creamy-garlic-pasta': 'lighter-chicken-alfredo',
    'beef-tacos': 'turkey-taco-rice-bowls',
    'honey-garlic-chicken-thighs': 'crispy-baked-chicken-bites',
    'mushroom-risotto': 'turkey-meatballs-tomato-sauce',
}

raw = open(P('recipes.json'), encoding='utf-8').read()
recipes = json.loads(raw)
ids = [r['id'] for r in recipes]
if all(n in ids for n in OLD_TO_NEW.values()) and not any(o in ids for o in OLD_TO_NEW):
    print('Already applied. Nothing to do.')
    sys.exit(0)
missing = [o for o in OLD_TO_NEW if o not in ids]
if missing:
    print(f'ERROR: old recipes not found: {missing}. Nothing was saved.')
    sys.exit(1)

# Step photos used only by the recipes being replaced.
EXTRA_OLD_IMAGES = []
for r in recipes:
    if r['id'] in OLD_TO_NEW:
        for s in r.get('steps', []):
            if s.get('img'):
                EXTRA_OLD_IMAGES.append(os.path.basename(s['img'])[:-5])

PHOTOS = {
    'lighter-chicken-alfredo': {
        'id': 37118296, 'photographer': 'Kemal Can', 'photographer_url': 'https://www.pexels.com/@kemalcanfilm/',
        'photo_url': 'https://www.pexels.com/photo/delicious-chicken-alfredo-pasta-dish-37118296/',
        'alt': 'Creamy chicken Alfredo pasta topped with Parmesan and parsley.'},
    'turkey-taco-rice-bowls': {
        'id': 4929692, 'photographer': 'Justin Doherty', 'photographer_url': 'https://www.pexels.com/@justindoherty/',
        'photo_url': 'https://www.pexels.com/photo/traditional-meal-of-vegetables-with-rice-and-meat-4929692/',
        'alt': 'A rice bowl with seasoned ground meat, corn and salsa.'},
    'crispy-baked-chicken-bites': {
        'id': 30882821, 'photographer': 'Đậu Photograph', 'photographer_url': 'https://www.pexels.com/@dauphotographer/',
        'photo_url': 'https://www.pexels.com/photo/golden-crispy-chicken-bites-with-fresh-salad-30882821/',
        'alt': 'Golden crispy chicken bites with a dipping sauce and fresh salad.'},
    'turkey-meatballs-tomato-sauce': {
        'id': 34314421, 'photographer': 'ERIVELTO Martins', 'photographer_url': 'https://www.pexels.com/@erivas/',
        'photo_url': 'https://www.pexels.com/photo/delicious-meatballs-in-rich-tomato-sauce-34314421/',
        'alt': 'Meatballs in tomato sauce garnished with parsley.'},
}

NEW = {}
NEW['lighter-chicken-alfredo'] = {
    "title": "Lighter Chicken Alfredo",
    "subtitle": "Fettuccine and tender chicken in a creamy Parmesan sauce made with blended cottage cheese instead of heavy cream. About 28 g protein in a small bowl.",
    "category": "Main Dishes",
    "tags": ["quick", "high-protein", "small-plates"],
    "prep": 10, "cook": 20, "time": 30, "serves": 5, "level": "Easy",
    "desc": "Creamy Alfredo, built on cottage cheese.",
    "intro": [
        "Classic Alfredo is mostly butter, cream and cheese, which makes it rich but heavy for a small appetite. This version keeps the creamy, garlicky Parmesan sauce and builds it on blended cottage cheese and a little milk, so a small bowl carries about 28 g of protein.",
        "The sauce is blended smooth before it ever touches the pan, then warmed gently. Cottage cheese can turn grainy if it boils, so low heat and a splash of pasta water are what keep it silky. Less pasta and more chicken per bowl keeps the portion small without feeling like a side dish."
    ],
    "why": [
        ["About 28 g protein per bowl", "Chicken, cottage cheese and Parmesan share the work."],
        ["Creamy without heavy cream", "Blended cottage cheese gives the sauce its body."],
        ["Ready in 30 minutes", "The chicken cooks while the pasta water heats."]
    ],
    "ingredients": [
        {"group": "For the pasta and chicken", "items": [
            {"q": 6, "u": "oz", "n": "fettuccine", "note": "170 g"},
            {"q": 12, "u": "oz", "n": "boneless, skinless chicken breast", "note": "cut into small, thin strips"},
            {"q": 1, "u": "tsp", "n": "olive oil"},
            {"q": 0.5, "u": "tsp", "n": "kosher salt"},
            {"q": 2, "u": "cups", "n": "baby spinach", "g": 60}
        ]},
        {"group": "For the sauce", "items": [
            {"q": 1, "u": "cup", "n": "low-fat cottage cheese", "g": 226},
            {"q": 0.5, "u": "cup", "n": "milk", "g": 122},
            {"q": 0.5, "u": "cup", "n": "finely grated Parmesan", "note": "plus more to serve", "g": 40},
            {"q": 1, "u": "tbsp", "n": "butter"},
            {"q": 3, "u": "", "n": "garlic cloves", "note": "minced"},
            {"q": None, "u": "", "n": "black pepper and chopped parsley", "note": "to finish"}
        ]}
    ],
    "steps": [
        {"t": "Blend the sauce base", "d": "Blend the cottage cheese, milk and Parmesan for about 30 seconds, until completely smooth with no curds left. Set aside.",
         "tip": "A smooth blend now is what keeps the finished sauce silky instead of grainy."},
        {"t": "Cook the pasta", "d": "Cook the fettuccine in well-salted boiling water until just tender. Scoop out 1 cup of the cooking water before draining."},
        {"t": "Cook the chicken", "d": "While the pasta cooks, heat the oil in a large skillet over medium-high heat. Season the chicken with the salt and cook for 5 to 7 minutes, stirring now and then, until golden and cooked through to 165°F (74°C). Move it to a plate."},
        {"t": "Warm the garlic", "d": "Turn the heat to low. Melt the butter in the same skillet, add the garlic and stir for about 1 minute, until fragrant but not browned."},
        {"t": "Finish gently", "d": "Pour in the blended sauce and warm it over low heat, stirring, for 1 to 2 minutes. Do not let it boil. Add the pasta, chicken and spinach and toss until the spinach wilts, loosening with pasta water a splash at a time until glossy.",
         "tip": "If the sauce looks thick or tight, add more pasta water rather than turning up the heat."},
        {"t": "Serve", "d": "Season with black pepper, scatter with parsley and a little extra Parmesan, and serve in small bowls."}
    ],
    "tips": [
        "Grate the Parmesan finely so it melts quickly at low heat.",
        "Cut the chicken into thin strips so it cooks fast and is easy to eat in small bites.",
        "Keep the heat low once the sauce is in the pan. Cottage cheese sauces can split if they boil.",
        "Small-portion tip: serve a small bowl with more chicken than pasta. Leftovers make tomorrow's lunch."
    ],
    "storage": "Refrigerate leftovers in an airtight container for up to 3 days. Reheat gently in a skillet over low heat with a splash of milk or water, stirring until creamy again.",
    "variations": [
        ["Broccoli", "Add small broccoli florets to the pasta water for the last 3 minutes of cooking."],
        ["Lemon", "Stir in the zest of half a lemon at the end for a brighter sauce."],
        ["Gluten-free", "Use a gluten-free fettuccine and cook it according to the package."],
        ["Make it gentler", "Use 1 clove of garlic, skip the black pepper and serve it warm rather than hot."],
        ["Protein boost", "Add 4 more ounces of chicken, or use a protein pasta."]
    ],
    "nutrition": {"calories": 320, "protein": 28, "carbs": 30, "fat": 9, "fiber": 1},
    "faq": [
        ["Will it taste like cottage cheese?", "Not really. Blended with Parmesan and garlic, it tastes like a mild, creamy cheese sauce."],
        ["Why did my sauce turn grainy?", "The heat was probably too high. Keep it on low, never let it boil, and loosen it with pasta water."],
        ["Can I make it ahead?", "It is best fresh, but leftovers reheat well over low heat with a splash of milk."]
    ],
    "note": "This is the creamy pasta for days when you want comfort food but only have room for a small bowl. More chicken than pasta, and the sauce does the rest.",
    "diet": [],
}
NEW['turkey-taco-rice-bowls'] = {
    "title": "Turkey Taco Rice Bowls",
    "subtitle": "Lean ground turkey in a homemade taco seasoning over a small scoop of rice, with corn, black beans, salsa and a spoonful of Greek yogurt. About 24 g protein per bowl.",
    "category": "Main Dishes",
    "tags": ["quick", "healthy", "high-protein", "small-plates", "make-ahead"],
    "prep": 10, "cook": 15, "time": 25, "serves": 5, "level": "Easy",
    "desc": "Taco night in a small bowl.",
    "intro": [
        "Everything you like about taco night, in a bowl that is easy to portion. Lean ground turkey cooks in a homemade spice blend, then goes over a small scoop of rice with corn, black beans and salsa. Each bowl has about 24 g of protein.",
        "A splash of water at the end of cooking turns the spices into a light glaze that keeps the turkey moist, since lean turkey dries out faster than beef. Greek yogurt stands in for sour cream and adds a little more protein on top."
    ],
    "why": [
        ["About 24 g protein per bowl", "Lean turkey, black beans and Greek yogurt."],
        ["Easy to portion", "Build one small bowl now and pack the rest for later."],
        ["Mild or spicy", "The seasoning is homemade, so you control the heat."]
    ],
    "ingredients": [
        {"group": "For the turkey", "items": [
            {"q": 1, "u": "lb", "n": "93% lean ground turkey", "note": "450 g"},
            {"q": 1, "u": "tsp", "n": "olive oil"},
            {"q": 2, "u": "tsp", "n": "chili powder", "note": "mild"},
            {"q": 1, "u": "tsp", "n": "ground cumin"},
            {"q": 0.5, "u": "tsp", "n": "smoked paprika"},
            {"q": 0.5, "u": "tsp", "n": "garlic powder"},
            {"q": 0.5, "u": "tsp", "n": "kosher salt"},
            {"q": 0.25, "u": "cup", "n": "water"}
        ]},
        {"group": "For the bowls", "items": [
            {"q": 1.33, "u": "cups", "n": "cooked rice", "note": "white or brown"},
            {"q": 1, "u": "cup", "n": "corn kernels", "note": "frozen and thawed, or canned and drained"},
            {"q": 1, "u": "cup", "n": "black beans", "note": "rinsed and drained"},
            {"q": 0.5, "u": "cup", "n": "salsa", "g": 130},
            {"q": 0.5, "u": "cup", "n": "plain nonfat Greek yogurt", "g": 120},
            {"q": 2, "u": "cups", "n": "shredded lettuce"},
            {"q": None, "u": "", "n": "lime wedges and cilantro", "note": "to serve"}
        ]}
    ],
    "steps": [
        {"t": "Mix the seasoning", "d": "Stir together the chili powder, cumin, smoked paprika, garlic powder and salt in a small bowl."},
        {"t": "Brown the turkey", "d": "Heat the oil in a large skillet over medium-high heat. Add the turkey and cook for 6 to 8 minutes, breaking it into small crumbles, until browned and no pink remains.",
         "tip": "Let the turkey sit for a minute between stirs so it browns instead of steaming."},
        {"t": "Season and glaze", "d": "Sprinkle the seasoning over the turkey and stir for 30 seconds. Add the water, scrape up any browned bits and simmer for 2 to 3 minutes, until the liquid reduces to a light glaze."},
        {"t": "Warm the sides", "d": "Warm the rice, corn and beans in the microwave or a small pan."},
        {"t": "Build the bowls", "d": "Divide the lettuce and a small scoop of rice among five bowls. Top with the turkey, corn, beans and salsa, and finish with a spoonful of Greek yogurt, a squeeze of lime and cilantro."}
    ],
    "tips": [
        "Make a double batch of the seasoning and keep it in a jar for next time.",
        "Lean turkey dries out easily, so stop cooking as soon as the glaze coats the meat.",
        "Pack the yogurt, salsa and lettuce separately if you are making bowls ahead.",
        "Small-portion tip: build a half bowl with extra turkey and less rice. The rest keeps for tomorrow."
    ],
    "storage": "Refrigerate the turkey, rice, corn and beans in airtight containers for up to 4 days. Reheat the turkey in a skillet with a splash of water. The cooked turkey also freezes for up to 3 months.",
    "variations": [
        ["Chicken", "Use ground chicken instead of turkey. Cook it the same way."],
        ["No rice", "Skip the rice and add extra lettuce and beans."],
        ["Dairy-free", "Replace the Greek yogurt with sliced avocado."],
        ["Make it gentler", "Use mild chili powder, skip the smoked paprika and choose a mild salsa. Serve it warm, not hot."],
        ["Protein boost", "Add an extra spoonful of Greek yogurt or a few more black beans."]
    ],
    "nutrition": {"calories": 285, "protein": 24, "carbs": 27, "fat": 9, "fiber": 4},
    "faq": [
        ["Can I use store-bought taco seasoning?", "Yes. Use about 2 tablespoons per pound and skip the salt, since most packets are salted."],
        ["Is it gluten-free?", "Yes, as written. Check your salsa and spice labels if you are very sensitive."],
        ["Can I meal prep it?", "Yes. Keep the components in separate containers and build a bowl in a few minutes."]
    ],
    "note": "Cook the turkey once and you have small bowls ready for several days. Build a half bowl when that is all that sounds good.",
    "diet": ["gluten-free"],
}
NEW['crispy-baked-chicken-bites'] = {
    "title": "Crispy Baked Chicken Bites",
    "subtitle": "Small pieces of chicken breast in a Parmesan panko coating, baked until golden and served with a honey-mustard Greek yogurt dip. About 35 g protein per serving.",
    "category": "Main Dishes",
    "tags": ["quick", "high-protein", "small-plates"],
    "prep": 15, "cook": 15, "time": 30, "serves": 4, "level": "Easy",
    "desc": "Golden, crunchy and baked, not fried.",
    "intro": [
        "Bite-size pieces are easy to eat a few at a time, and these get their crunch from the oven rather than a fryer. A light coating of panko and Parmesan browns on a hot sheet pan in about 15 minutes, and each serving has about 35 g of protein.",
        "Two small steps make the difference. Toasting the panko in a dry pan before coating gives it color, since chicken bites cook through before raw crumbs have time to brown. And a hot oven with space between the pieces lets the coating crisp instead of steam."
    ],
    "why": [
        ["About 35 g protein per serving", "Chicken breast, Parmesan and a Greek yogurt dip."],
        ["Baked, not fried", "A hot oven and toasted panko give the crunch."],
        ["Easy to eat in small bites", "Stop after a few pieces and save the rest."]
    ],
    "ingredients": [
        {"group": "For the chicken", "items": [
            {"q": 1, "u": "lb", "n": "boneless, skinless chicken breast", "note": "cut into 1-inch pieces"},
            {"q": 1, "u": "", "n": "large egg"},
            {"q": 0.67, "u": "cup", "n": "panko breadcrumbs", "g": 40},
            {"q": 0.25, "u": "cup", "n": "finely grated Parmesan", "g": 20},
            {"q": 0.5, "u": "tsp", "n": "garlic powder"},
            {"q": 0.5, "u": "tsp", "n": "paprika"},
            {"q": 0.5, "u": "tsp", "n": "kosher salt"},
            {"q": None, "u": "", "n": "olive oil spray"}
        ]},
        {"group": "For the dip", "items": [
            {"q": 0.75, "u": "cup", "n": "plain nonfat Greek yogurt", "g": 180},
            {"q": 1, "u": "tbsp", "n": "Dijon mustard"},
            {"q": 1, "u": "tsp", "n": "honey"},
            {"q": 1, "u": "tsp", "n": "lemon juice"}
        ]},
        {"group": "To serve", "items": [
            {"q": None, "u": "", "n": "mixed greens or a simple salad"}
        ]}
    ],
    "steps": [
        {"t": "Heat the oven", "d": "Heat the oven to 425°F (220°C). Line a sheet pan with parchment and spray it lightly with oil."},
        {"t": "Toast the panko", "d": "Toast the panko in a dry skillet over medium heat for 2 to 3 minutes, stirring, until light golden. Move it to a shallow bowl and mix in the Parmesan, garlic powder, paprika and salt.",
         "tip": "Pre-toasted crumbs brown in the time the chicken takes to cook."},
        {"t": "Coat the chicken", "d": "Beat the egg in a second bowl. Dip the chicken pieces in the egg, let the excess drip off, then press them into the crumb mixture. Arrange on the pan with space between each piece."},
        {"t": "Bake", "d": "Spray the tops lightly with oil and bake for 12 to 15 minutes, until golden and cooked through to 165°F (74°C).",
         "tip": "Leave space between the pieces. Crowded bites steam and stay soft."},
        {"t": "Make the dip and serve", "d": "Stir together the yogurt, Dijon, honey and lemon juice. Serve the chicken bites warm with the dip and a small salad."}
    ],
    "tips": [
        "Cut the chicken into even pieces so they finish at the same time.",
        "An air fryer works too: cook at 400°F (200°C) for 8 to 10 minutes, shaking halfway.",
        "Pat the chicken dry before coating so the egg and crumbs stick.",
        "Small-portion tip: start with four or five pieces and a spoonful of dip. They reheat well later."
    ],
    "storage": "Refrigerate the cooled chicken bites in an airtight container for up to 3 days, with the dip stored separately. Reheat in a 400°F (200°C) oven or air fryer for 5 to 6 minutes to re-crisp. They also freeze for up to 2 months.",
    "variations": [
        ["Lemon herb", "Add the zest of one lemon and 1 teaspoon dried oregano to the crumbs."],
        ["Gluten-free", "Use gluten-free panko or crushed gluten-free cornflakes."],
        ["Spicy", "Add a pinch of cayenne to the crumbs and a little hot sauce to the dip."],
        ["Make it gentler", "Skip the paprika and mustard, and use a plain yogurt and lemon dip. Serve warm rather than hot."],
        ["Protein boost", "Serve with an extra spoonful of the Greek yogurt dip."]
    ],
    "nutrition": {"calories": 260, "protein": 35, "carbs": 11, "fat": 7, "fiber": 0},
    "faq": [
        ["Why is my coating soggy?", "The pan was likely crowded or the oven not hot enough. Space the pieces out and bake at 425°F."],
        ["Can I use chicken thighs?", "Yes. Boneless thighs stay juicier. Bake them for 15 to 18 minutes, to 175°F (80°C)."],
        ["Can I make them ahead?", "Yes. Bake, cool and refrigerate, then re-crisp in a hot oven or air fryer."]
    ],
    "note": "Small, crunchy pieces are easy to stop and start, which makes them a good fit for low-appetite days. Keep a few in the fridge and re-crisp them in minutes.",
    "diet": [],
}
NEW['turkey-meatballs-tomato-sauce'] = {
    "title": "Turkey Meatballs in Tomato Sauce",
    "subtitle": "Tender turkey and Parmesan meatballs simmered in a simple tomato sauce with basil. About 23 g protein in four small meatballs, and they freeze well.",
    "category": "Main Dishes",
    "tags": ["high-protein", "small-plates", "gentle", "make-ahead"],
    "prep": 20, "cook": 30, "time": 50, "serves": 5, "level": "Easy",
    "desc": "Soft meatballs, simple sauce, freezer-friendly.",
    "intro": [
        "Meatballs are one of the most useful things to keep in the freezer: soft, easy to eat and ready to reheat a few at a time. These are made with lean ground turkey, a little Parmesan and grated onion, then simmered gently in tomato sauce. Four small meatballs have about 23 g of protein.",
        "Grated onion and breadcrumbs soaked in milk are what keep lean turkey tender. They add moisture that stays inside the meatballs as they cook, and the gentle simmer in sauce finishes them without drying them out."
    ],
    "why": [
        ["About 23 g protein per serving", "Four small turkey meatballs with sauce."],
        ["Soft and easy to eat", "A gentle simmer keeps them tender."],
        ["Freezer-friendly", "Reheat a few at a time on harder days."]
    ],
    "ingredients": [
        {"group": "For the meatballs", "items": [
            {"q": 1, "u": "lb", "n": "93% lean ground turkey", "note": "450 g"},
            {"q": 0.33, "u": "cup", "n": "plain breadcrumbs", "g": 36},
            {"q": 2, "u": "tbsp", "n": "milk"},
            {"q": 1, "u": "", "n": "large egg"},
            {"q": 0.25, "u": "cup", "n": "finely grated Parmesan", "g": 20},
            {"q": 0.5, "u": "", "n": "small onion", "note": "finely grated"},
            {"q": 1, "u": "", "n": "garlic clove", "note": "minced"},
            {"q": 0.5, "u": "tsp", "n": "kosher salt"},
            {"q": 2, "u": "tbsp", "n": "chopped parsley"}
        ]},
        {"group": "For the sauce", "items": [
            {"q": 1, "u": "tbsp", "n": "olive oil"},
            {"q": 2, "u": "", "n": "garlic cloves", "note": "sliced"},
            {"q": 28, "u": "oz", "n": "crushed tomatoes", "note": "1 can"},
            {"q": 0.5, "u": "tsp", "n": "dried oregano"},
            {"q": None, "u": "", "n": "fresh basil and salt", "note": "to taste"}
        ]}
    ],
    "steps": [
        {"t": "Soak the breadcrumbs", "d": "In a large bowl, stir the breadcrumbs with the milk and let them sit for 5 minutes, until soft."},
        {"t": "Mix and shape", "d": "Add the turkey, egg, Parmesan, grated onion, garlic, salt and parsley. Mix gently with your hands until just combined, then roll into 20 small meatballs, about 1 inch across.",
         "tip": "Mix only until combined. Overworked meatballs turn dense."},
        {"t": "Start the sauce", "d": "Heat the olive oil in a large, deep skillet over medium heat. Add the sliced garlic and cook for 1 minute, until fragrant. Stir in the crushed tomatoes and oregano and bring to a gentle simmer."},
        {"t": "Simmer the meatballs", "d": "Lower the meatballs into the sauce in a single layer. Cover and simmer gently for 20 to 25 minutes, turning them once, until cooked through to 165°F (74°C).",
         "tip": "Keep the sauce at a gentle bubble. A hard boil can break the meatballs apart."},
        {"t": "Finish and serve", "d": "Taste the sauce and add salt if needed. Tear over some basil and serve four meatballs per plate, with a little pasta, rice or bread if you like."}
    ],
    "tips": [
        "Wet your hands lightly while rolling so the mixture does not stick.",
        "Grate the onion on the fine side of a box grater so it melts into the meatballs.",
        "For browner meatballs, bake them at 400°F (200°C) for 12 minutes before adding them to the sauce.",
        "Small-portion tip: two or three meatballs with sauce make a small plate. Freeze the rest in portions."
    ],
    "storage": "Refrigerate the meatballs in their sauce for up to 4 days. Freeze in small portions for up to 3 months, then thaw overnight in the fridge and reheat gently in a covered pan or the microwave.",
    "variations": [
        ["Chicken", "Use ground chicken instead of turkey."],
        ["Gluten-free", "Use gluten-free breadcrumbs or 1/3 cup quick oats."],
        ["Spinach", "Mix 1/2 cup finely chopped, squeezed-dry spinach into the meatballs."],
        ["Make it gentler", "Skip the sliced garlic in the sauce and serve the meatballs warm with plain rice."],
        ["Protein boost", "Serve with a spoonful of ricotta or extra Parmesan on top."]
    ],
    "nutrition": {"calories": 277, "protein": 23, "carbs": 19, "fat": 13, "fiber": 3},
    "faq": [
        ["Why are my meatballs dry?", "Lean turkey needs moisture. Do not skip the soaked breadcrumbs or the grated onion, and keep the simmer gentle."],
        ["Can I freeze them uncooked?", "Yes. Freeze the shaped meatballs on a tray, then bag them. Simmer from frozen for about 30 minutes."],
        ["What should I serve with them?", "A small scoop of pasta, rice or polenta, or a slice of bread for the sauce."]
    ],
    "note": "Make the full batch and freeze them in portions of two or three. A small, warm plate is then only a few minutes away.",
    "diet": [],
}

# ------------------------------------------------------------------ images (in memory first)
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', 'pillow'])
    from PIL import Image, ImageDraw, ImageFont


def cover(im, w, h):
    sw, sh = im.size
    if sw / sh > w / h:
        nw = round(sh * w / h)
        im = im.crop(((sw - nw) // 2, 0, (sw - nw) // 2 + nw, sh))
    else:
        nh = round(sw * h / w)
        im = im.crop((0, (sh - nh) // 2, sw, (sh - nh) // 2 + nh))
    return im.resize((w, h), Image.LANCZOS)


def font(size):
    for path in (os.path.join(ROOT, 'fonts', 'fraunces-normal.woff2'),
                 '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
                 '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default(size=size)


def wrap(draw, text, f, width):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=f) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def make_pin(im, title):
    W, H, PH = 1000, 1500, 1020
    pin = Image.new('RGB', (W, H), (247, 242, 231))
    pin.paste(cover(im, W, PH), (0, 0))
    d = ImageDraw.Draw(pin)
    green = (63, 81, 48)
    small, big = font(30), font(62)
    d.text((W // 2, PH + 62), 'SMALL PLATES · BIG PROTEIN', font=small, fill=green, anchor='mm')
    y = PH + 140
    for ln in wrap(d, title, big, 880)[:3]:
        d.text((W // 2, y), ln, font=big, fill=(34, 34, 34), anchor='mm')
        y += 76
    d.text((W // 2, H - 52), 'Bored of Toast', font=small, fill=green, anchor='mm')
    return pin


def jpg(im, q=85):
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    return buf.getvalue()


out = {}
for rid, ph in PHOTOS.items():
    url = f"https://images.pexels.com/photos/{ph['id']}/pexels-photo-{ph['id']}.jpeg?auto=compress&cs=tinysrgb&w=2000"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (bored-of-toast site build)'})
    try:
        data = urllib.request.urlopen(req, timeout=60).read()
        im = Image.open(io.BytesIO(data)).convert('RGB')
    except Exception as ex:
        print(f'ERROR: could not download or open the {rid} photo from Pexels ({ex}). Nothing was saved.')
        sys.exit(1)
    main = cover(im, 1200, 900)
    for q in (80, 74, 68, 62, 56):
        buf = io.BytesIO()
        main.save(buf, 'WEBP', quality=q, method=6)
        if buf.tell() <= 195 * 1024:
            break
    else:
        print(f'ERROR: {rid} photo is still over 200 KB. Nothing was saved.')
        sys.exit(1)
    out[rid] = {'webp': buf.getvalue(), 'og': jpg(cover(im, 1200, 630)), 'pin': jpg(make_pin(im, NEW[rid]['title']))}
    print(f"- photo {rid}: {len(out[rid]['webp']) // 1024} KB webp, og and pin generated")

# ------------------------------------------------------------------ write images, remove old ones
for rid, b in out.items():
    open(os.path.join(IMG, f'{rid}.webp'), 'wb').write(b['webp'])
    open(os.path.join(IMG, 'og', f'{rid}.jpg'), 'wb').write(b['og'])
    open(os.path.join(IMG, 'pins', f'{rid}.jpg'), 'wb').write(b['pin'])
removed = 0
for old in list(OLD_TO_NEW) + EXTRA_OLD_IMAGES:
    files = glob.glob(os.path.join(IMG, f'{old}.webp')) + glob.glob(os.path.join(IMG, f'{old}-*w.webp'))
    files += glob.glob(os.path.join(IMG, 'og', f'{old}.jpg')) + glob.glob(os.path.join(IMG, 'pins', f'{old}.jpg'))
    for f in files:
        os.remove(f)
        removed += 1
print(f'- removed {removed} old image files (step photos: {EXTRA_OLD_IMAGES or "none"})')
subprocess.check_call([sys.executable, P('make_images.py')])

# ------------------------------------------------------------------ credits
craw = open(P('credits.json'), encoding='utf-8').read()
credits = json.loads(craw)
for old in list(OLD_TO_NEW) + EXTRA_OLD_IMAGES:
    credits.pop(old, None)
for rid, ph in PHOTOS.items():
    credits[rid] = {'photographer': ph['photographer'], 'photographer_url': ph['photographer_url'],
                    'photo_url': ph['photo_url'], 'source': 'Pexels', 'alt': ph['alt']}
m = re.match(r'\{\s*\n([ \t]+)"', craw)
with open(P('credits.json'), 'w', encoding='utf-8') as f:
    json.dump(credits, f, ensure_ascii=False, indent=len(m.group(1)) if m else 1)
    f.write('\n')

# ------------------------------------------------------------------ redirects.json
rpath = P('redirects.json')
redirects = json.load(open(rpath, encoding='utf-8')) if os.path.exists(rpath) else {}
redirects.update(OLD_TO_NEW)
with open(rpath, 'w', encoding='utf-8') as f:
    json.dump(redirects, f, ensure_ascii=False, indent=1, sort_keys=True)
    f.write('\n')

# ------------------------------------------------------------------ build.py (category, focus list, NEW_IDS)
b = open(P('build.py'), encoding='utf-8').read()
if 'RECIPE_REDIRECTS' not in b:
    print('ERROR: build.py has no recipe redirect support (run update_013 first).')
    sys.exit(1)
b2 = re.sub(r"\n[ \t]*\('everyday', 'Everyday Favorites', '[^']*'\),", '', b)
print('- "Everyday Favorites" category removed' if b2 != b else '- "Everyday Favorites" category not found (already removed)')
b = b2
m = re.search(r'FOCUS_IDS = (\[.*?\])', b)
focus = json.loads(m.group(1))
for rid in NEW:
    if rid not in focus:
        focus.append(rid)
b = b[:m.start(1)] + json.dumps(focus) + b[m.end(1):]
open(P('build.py'), 'w', encoding='utf-8').write(b)

# ------------------------------------------------------------------ other quoted references to old ids
SKIP = re.compile(r'^(update_|fix_|content_update|recipe_pilot|photo_review)')
KEEP = {'recipes.json', 'credits.json', 'redirects.json'}
changed = []
for dirpath, dirnames, filenames in os.walk(HERE):
    dirnames[:] = [d for d in dirnames if d not in ('site', '__pycache__')]
    for fn in filenames:
        if SKIP.match(fn) or fn in KEEP or not fn.endswith(('.py', '.json', '.js', '.html')):
            continue
        path = os.path.join(dirpath, fn)
        try:
            txt = open(path, encoding='utf-8').read()
        except Exception:
            continue
        new = txt
        for old, nid in OLD_TO_NEW.items():
            new = re.sub(r"(?<=['\"/])" + re.escape(old) + r"(?=['\"/.])", nid, new)
        if new != txt:
            open(path, 'w', encoding='utf-8').write(new)
            changed.append(os.path.relpath(path, HERE))
print(f"- old id references updated in: {', '.join(changed) or 'none'}")

# ------------------------------------------------------------------ recipes.json (last)
for i, r in enumerate(recipes):
    if r['id'] in OLD_TO_NEW:
        rid = OLD_TO_NEW[r['id']]
        new = {'id': rid}
        new.update(NEW[rid])
        new['img'] = f'images/{rid}.webp'
        recipes[i] = new
        print(f"- {r['id']} -> {rid} ({new['title']}, ~{new['nutrition']['protein']} g protein, ~{new['nutrition']['calories']} kcal per serving)")
left = [r['id'] for r in recipes if 'everyday' in r.get('tags', [])]
if left:
    print(f'- note: recipes still tagged everyday: {left}')
m = re.match(r'\[\s*\n([ \t]+)\{', raw)
with open(P('recipes.json'), 'w', encoding='utf-8') as f:
    json.dump(recipes, f, ensure_ascii=False, indent=len(m.group(1)) if m else None)
    f.write('\n')
print('OK: 4 mains replaced, redirects added. All 10 off-focus recipes are now replaced.')
