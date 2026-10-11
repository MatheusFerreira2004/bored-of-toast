#!/usr/bin/env python3
"""New content, batch 3 of 6: new "Snacks" category with five NEW recipes (nothing replaced).

Photo-first rule (Pexels title/description names the dish):
  bacon-deviled-eggs     23784968  "Savory deviled eggs topped with crispy bacon" (Adriana Coulson)
  garlic-sesame-edamame  38594582  "A steaming bowl of fresh edamame" (Amine Kubranur Cakiroglu)
  yogurt-hummus          31610382  "Creamy hummus with spiced chickpeas and herbs in a bowl" (Anil Sharma)
  tzatziki-yogurt-dip    6271896   "Tzatziki dip garnished with mint, surrounded by fresh vegetables" (Shameel mukkath)
  frozen-yogurt-berry-bars 32055276 "Frozen berries on a creamy yogurt bar" (Meryemce)
Planned "cottage cheese ranch dip", "turkey roll-ups" had no matching free photo; they became the hummus and
tzatziki. The planned "yogurt bark" became bars to match the photo.

Nutrition per serving is an ESTIMATE from USDA FoodData Central reference values (rounded):
  Deviled eggs (4): 6 eggs 429/38 P/2 C/29 F; nonfat Greek yogurt 57 g 33/5.7 P/2 C; mayo 14 g 100/11 F; Dijon 3;
    bacon 2 slices cooked 16 g 86/6 P/6.7 F -> 651 kcal, 50 P, 4 C, 47 F / 4 = ~163 kcal, 13 P, 1 C, 12 F, 0 fib
  Edamame (2): shelled-equivalent ~230 g 280/27 P/20 C/12 F/12 fib; sesame oil 4.5 g 40/4.5 F; tamari, garlic 6/0.5 P/1 C
    -> 326 kcal, 28 P, 21 C, 17 F, 12 fib / 2 = ~163 kcal, 14 P, 11 C, 8 F, 6 fib
  Hummus (4): chickpeas 240 g 334/17 P/55 C/6 F/18 fib; nonfat Greek yogurt 113 g 67/11.5 P/4 C; tahini 30 g 179/5 P/6 C/16 F/3 fib;
    olive oil 13.5 g 119/13.5 F; lemon, garlic, spices 15/0.5 P/3 C -> 714 kcal, 34 P, 68 C, 36 F, 21 fib / 4 = ~179 kcal, 9 P, 17 C, 9 F, 5 fib
  Tzatziki (4): nonfat Greek yogurt 340 g 201/34.5 P/12 C/1.4 F; cucumber 150 g 23/1 P/5 C; olive oil 13.5 g 119/13.5 F;
    garlic, dill, lemon 10/2 C; vegetables to serve 250 g 75/2.5 P/16 C/0.5 F/5 fib -> 428 kcal, 38 P, 35 C, 15 F, 6 fib
    / 4 = ~107 kcal, 10 P, 9 C, 4 F, 2 fib
  Bars (8): 2% Greek yogurt 454 g 332/46 P/18 C/8.8 F; honey 42 g 128/35 C; vanilla 12; berries 130 g 65/1.6 P/15 C/0.8 F/8 fib
    -> 537 kcal, 48 P, 68 C, 10 F, 8 fib / 8 = ~67 kcal, 6 P, 9 C, 1 F, 1 fib
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batchlib import add_recipes

N = None
PHOTOS = {
    'bacon-deviled-eggs': {'id': 23784968, 'photographer': 'Adriana Coulson', 'photographer_url': 'https://www.pexels.com/@adriana-coulson-1070894176/',
        'photo_url': 'https://www.pexels.com/photo/eggs-with-meat-23784968/', 'alt': 'Deviled eggs topped with crispy bacon on a serving plate.'},
    'garlic-sesame-edamame': {'id': 38594582, 'photographer': 'Amine Kübranur Çakıroğlu', 'photographer_url': 'https://www.pexels.com/@amine-kubranur-cakiroglu-689611212/',
        'photo_url': 'https://www.pexels.com/photo/steaming-bowl-of-fresh-edamame-on-table-38594582/', 'alt': 'A steaming bowl of edamame pods on a table.'},
    'yogurt-hummus': {'id': 31610382, 'photographer': 'Anil Sharma', 'photographer_url': 'https://www.pexels.com/@shootsaga/',
        'photo_url': 'https://www.pexels.com/photo/delicious-creamy-hummus-with-garnishes-31610382/', 'alt': 'A bowl of creamy hummus topped with spiced chickpeas and herbs.'},
    'tzatziki-yogurt-dip': {'id': 6271896, 'photographer': 'Shameel mukkath', 'photographer_url': 'https://www.pexels.com/@shameel-mukkath-3421394/',
        'photo_url': 'https://www.pexels.com/photo/overhead-shot-of-tzatziki-in-a-bowl-6271896/', 'alt': 'A bowl of tzatziki garnished with mint, surrounded by fresh vegetables.'},
    'frozen-yogurt-berry-bars': {'id': 32055276, 'photographer': 'Meryemce', 'photographer_url': 'https://www.pexels.com/@meryemce/',
        'photo_url': 'https://www.pexels.com/photo/frozen-berries-on-creamy-yogurt-bar-close-up-32055276/', 'alt': 'A frozen Greek yogurt bar topped with raspberries and blackberries.'},
}

NEW = {}
NEW['bacon-deviled-eggs'] = {
    "title": "Greek Yogurt Deviled Eggs with Crispy Bacon",
    "subtitle": "Classic deviled eggs made lighter with Greek yogurt and topped with a little crispy bacon. Three halves make a small snack with about 13 g protein.",
    "category": "Snacks",
    "tags": ["small-plates", "make-ahead"],
    "prep": 15, "cook": 12, "time": 27, "serves": 4, "level": "Easy",
    "desc": "Creamy, savory and about 13 g protein.",
    "intro": [
        "Deviled eggs are one of the most useful snacks to keep in the fridge: small, savory, already portioned and full of protein. This version swaps most of the mayonnaise for Greek yogurt, so the filling stays creamy and tangy with a little less fat.",
        "Two slices of bacon go a long way here. Crumbled over the top, they add a salty crunch that makes three halves feel like a proper snack."
    ],
    "why": [["About 13 g protein per serving", "Eggs and Greek yogurt."], ["Already portioned", "Three halves is one serving."], ["Make-ahead", "Keeps in the fridge for 2 days."]],
    "ingredients": [
        {"group": "For the eggs", "items": [{"q": 6, "u": "", "n": "large eggs"}]},
        {"group": "For the filling", "items": [
            {"q": 0.25, "u": "cup", "n": "plain nonfat Greek yogurt", "g": 57},
            {"q": 1, "u": "tbsp", "n": "mayonnaise"},
            {"q": 1, "u": "tsp", "n": "Dijon mustard"},
            {"q": N, "u": "", "n": "salt and pepper", "note": "to taste"}]},
        {"group": "To top", "items": [
            {"q": 2, "u": "slices", "n": "bacon", "note": "cooked crisp and crumbled"},
            {"q": 1, "u": "tbsp", "n": "chives", "note": "finely chopped"},
            {"q": N, "u": "", "n": "pinch of paprika"}]}
    ],
    "steps": [
        {"t": "Cook the eggs", "d": "Lower the eggs into a pot of gently boiling water and cook for 12 minutes. Move them straight into a bowl of ice water for 5 minutes.", "tip": "Older eggs peel more easily than very fresh ones."},
        {"t": "Peel and halve", "d": "Peel the eggs, cut them in half lengthwise and pop the yolks into a bowl. Arrange the whites on a plate."},
        {"t": "Make the filling", "d": "Mash the yolks with a fork, then stir in the yogurt, mayonnaise and mustard until smooth. Season with salt and pepper."},
        {"t": "Fill", "d": "Spoon or pipe the filling back into the whites."},
        {"t": "Top and serve", "d": "Scatter with crumbled bacon, chives and a pinch of paprika just before serving."}
    ],
    "tips": ["A zip-top bag with one corner snipped off makes an easy piping bag.", "Add the bacon just before serving so it stays crisp.", "For the smoothest filling, press the yolks through a sieve.", "Small-portion tip: plate three halves and keep the rest covered in the fridge for later."],
    "storage": "Refrigerate filled eggs in a covered container for up to 2 days. Keep the bacon separate and add it before eating. Not suitable for freezing.",
    "variations": [["No bacon", "Top with smoked paprika and chives for a vegetarian version."], ["Avocado", "Mash 1/4 avocado into the filling for extra creaminess."], ["Smoked salmon", "Top each half with a small piece of smoked salmon instead of bacon."], ["Make it gentler", "Skip the mustard, paprika and bacon and season the filling with just a little salt."], ["Protein boost", "Serve with a small cup of cottage cheese or a few slices of turkey for about 8 g more protein."]],
    "nutrition": {"calories": 163, "protein": 13, "carbs": 1, "fat": 12, "fiber": 0},
    "faq": [["Can I make them ahead?", "Yes. Make the filling and cook the eggs up to 2 days ahead; fill on the day for the neatest look."], ["Can I skip the mayonnaise?", "Yes. Use 1/3 cup Greek yogurt in total; the filling will be a little tangier."], ["Are they gluten-free?", "Yes, as long as your bacon and mustard are gluten-free."]],
    "note": "Keep a few of these in the fridge for the moments when you know you should eat something but nothing sounds good.",
    "diet": ["gluten-free"],
}
NEW['garlic-sesame-edamame'] = {
    "title": "Warm Garlic Sesame Edamame",
    "subtitle": "Steamed edamame tossed with sesame oil, a little garlic and flaky salt. Ready in 10 minutes, with about 14 g protein and 6 g fiber per bowl.",
    "category": "Snacks",
    "tags": ["quick", "healthy", "small-plates"],
    "prep": 3, "cook": 7, "time": 10, "serves": 2, "level": "Easy",
    "desc": "A warm, salty bowl with real protein.",
    "intro": [
        "A bag of frozen edamame is one of the easiest high-protein snacks there is. Steam the pods, toss them with a little sesame oil and garlic, sprinkle with salt and eat them warm, one pod at a time.",
        "Popping the beans out of the pods slows you down, which is often helpful when your appetite is small. Each bowl has about 14 g of plant protein."
    ],
    "why": [["About 14 g protein per bowl", "Plant protein from soybeans."], ["10 minutes", "Straight from the freezer."], ["Slow to eat", "One pod at a time."]],
    "ingredients": [
        {"group": "For the edamame", "items": [
            {"q": 12, "u": "oz", "n": "frozen edamame in pods", "g": 340},
            {"q": 1, "u": "tsp", "n": "toasted sesame oil"},
            {"q": 1, "u": "", "n": "garlic clove", "note": "finely grated"},
            {"q": 1, "u": "tsp", "n": "low-sodium tamari or soy sauce"},
            {"q": N, "u": "", "n": "flaky sea salt"},
            {"q": 1, "u": "tsp", "n": "sesame seeds", "note": "optional"}]}
    ],
    "steps": [
        {"t": "Steam", "d": "Bring an inch of water to a boil in a pot with a steamer basket, or use a pot of boiling salted water. Cook the edamame for 5 to 6 minutes, until hot and tender. Drain well."},
        {"t": "Warm the garlic", "d": "In the same pot, warm the sesame oil and garlic over low heat for 30 seconds, just until fragrant.", "tip": "Keep the heat low; garlic turns bitter if it browns."},
        {"t": "Toss", "d": "Add the edamame and tamari and toss to coat."},
        {"t": "Serve warm", "d": "Tip into two small bowls and sprinkle with flaky salt and sesame seeds. Squeeze the beans out of the pods with your teeth and discard the pods."}
    ],
    "tips": ["Microwave option: cook the pods in a covered bowl with 2 tablespoons water for 4 to 5 minutes.", "Shelled edamame works too; toss and eat with a spoon.", "Put out a small empty bowl for the pods.", "Small-portion tip: one bowl is a full snack. The second keeps well in the fridge and is good cold."],
    "storage": "Refrigerate cooked edamame in a covered container for up to 3 days. Eat cold or rewarm briefly in the microwave.",
    "variations": [["Chili lime", "Toss with lime zest and a pinch of chili flakes instead of garlic."], ["Plain salted", "Skip the garlic and tamari; just salt."], ["Shelled bowl", "Use shelled edamame and add diced cucumber for a quick salad."], ["Make it gentler", "Use shelled edamame, skip the garlic and season with a little salt only."], ["Protein boost", "Serve alongside a soft-boiled egg for about 6 g more protein."]],
    "nutrition": {"calories": 163, "protein": 14, "carbs": 11, "fat": 8, "fiber": 6},
    "faq": [["Do you eat the pods?", "No. The pods are tough; squeeze the beans out and discard the shells."], ["Is it gluten-free?", "Yes, with tamari or a gluten-free soy sauce."], ["Fresh or frozen?", "Frozen is easier to find and already blanched, so it cooks faster."]],
    "note": "A warm bowl of edamame is a good snack for slow afternoons. It takes ten minutes, and eating it pod by pod is almost relaxing.",
    "diet": ["vegan", "vegetarian", "dairy-free", "gluten-free"],
}
NEW['yogurt-hummus'] = {
    "title": "Greek Yogurt Hummus with Spiced Chickpeas",
    "subtitle": "Extra-creamy hummus blended with Greek yogurt, topped with warm spiced chickpeas and herbs. About 9 g protein per small bowl, great with vegetables.",
    "category": "Snacks",
    "tags": ["healthy", "small-plates", "make-ahead"],
    "prep": 10, "cook": 5, "time": 15, "serves": 4, "level": "Easy",
    "desc": "Extra-creamy hummus with a protein lift.",
    "intro": [
        "Blending a little Greek yogurt into hummus makes it extra smooth and adds a bit more protein, while keeping the familiar flavor of chickpeas, tahini and lemon.",
        "A handful of chickpeas warmed in olive oil with paprika and cumin goes on top. Serve a small bowl with vegetables or a few crackers for a snack that keeps well in the fridge all week."
    ],
    "why": [["Extra creamy", "Greek yogurt makes it silky."], ["About 9 g protein", "Chickpeas, tahini and yogurt."], ["Keeps all week", "Make once, snack for days."]],
    "ingredients": [
        {"group": "For the hummus", "items": [
            {"q": 1, "u": "can (15 oz)", "n": "chickpeas", "note": "drained, liquid reserved", "g": 240},
            {"q": 0.5, "u": "cup", "n": "plain nonfat Greek yogurt", "g": 113},
            {"q": 2, "u": "tbsp", "n": "tahini"},
            {"q": 2, "u": "tbsp", "n": "lemon juice"},
            {"q": 1, "u": "", "n": "small garlic clove"},
            {"q": 0.5, "u": "tsp", "n": "salt"}]},
        {"group": "For the topping", "items": [
            {"q": 1, "u": "tbsp", "n": "olive oil"},
            {"q": 0.5, "u": "tsp", "n": "smoked paprika"},
            {"q": 0.25, "u": "tsp", "n": "ground cumin"},
            {"q": 1, "u": "tbsp", "n": "parsley or cilantro", "note": "chopped"}]}
    ],
    "steps": [
        {"t": "Save some chickpeas", "d": "Set aside 1/3 cup of the drained chickpeas for the topping."},
        {"t": "Blend", "d": "Blend the remaining chickpeas with the yogurt, tahini, lemon juice, garlic and salt for 2 minutes, scraping down the sides, until very smooth. Add a tablespoon or two of the reserved chickpea liquid if it is too thick.", "tip": "Blending longer than you think makes the smoothest hummus."},
        {"t": "Warm the topping", "d": "Warm the olive oil in a small skillet over medium heat. Add the saved chickpeas, paprika and cumin and cook for 3 to 4 minutes, until lightly crisp."},
        {"t": "Serve", "d": "Spread the hummus in a bowl, spoon the warm chickpeas and their oil on top and scatter with herbs."}
    ],
    "tips": ["Taste and add more lemon or salt after blending.", "Serve with cucumber, carrots, bell pepper or a few whole-grain crackers.", "For a dairy-free version, use 1/4 cup extra chickpea liquid instead of yogurt.", "Small-portion tip: spoon 1/3 cup into a small bowl rather than eating from the big one."],
    "storage": "Refrigerate the hummus in a covered container for up to 5 days. Store the topping separately and rewarm briefly before serving.",
    "variations": [["Roasted red pepper", "Blend in 1/2 cup jarred roasted red peppers."], ["Lemon herb", "Blend in a handful of parsley and extra lemon zest."], ["Dairy-free", "Replace the yogurt with chickpea liquid and a little more tahini."], ["Make it gentler", "Skip the garlic, paprika and cumin and serve with soft cucumber slices."], ["Protein boost", "Serve with a hard-boiled egg or a few slices of chicken for about 6 to 8 g more protein."]],
    "nutrition": {"calories": 179, "protein": 9, "carbs": 17, "fat": 9, "fiber": 5},
    "faq": [["Do I need to peel the chickpeas?", "No. Blending for 2 minutes gives a smooth result without peeling."], ["Can I use dried chickpeas?", "Yes, about 1 1/2 cups cooked chickpeas replaces one can."], ["Is it gluten-free?", "Yes. Choose gluten-free crackers if serving with crackers."]],
    "note": "A small bowl of hummus and some crunchy vegetables is one of the easiest snacks to put together when you are tired.",
    "diet": ["vegetarian", "gluten-free"],
}
NEW['tzatziki-yogurt-dip'] = {
    "title": "Greek Yogurt Tzatziki with Crunchy Vegetables",
    "subtitle": "Thick Greek yogurt with grated cucumber, dill, mint and lemon, served with fresh vegetables. A cool, refreshing snack with about 10 g protein per serving.",
    "category": "Snacks",
    "tags": ["quick", "healthy", "small-plates", "make-ahead", "gentle"],
    "prep": 10, "cook": 0, "time": 10, "serves": 4, "level": "Easy",
    "desc": "Cool, creamy and about 10 g protein.",
    "intro": [
        "Tzatziki is mostly Greek yogurt, which makes it one of the few dips that is genuinely high in protein. Grated cucumber, dill, mint and lemon keep it cool and fresh, and it takes ten minutes with no cooking.",
        "Served cold with crunchy vegetables, it is a good snack for warm days or for when hot food does not appeal."
    ],
    "why": [["About 10 g protein", "Mostly Greek yogurt."], ["No cooking", "Ten minutes with a grater."], ["Cool and fresh", "Easy on hot days."]],
    "ingredients": [
        {"group": "For the tzatziki", "items": [
            {"q": 1.5, "u": "cups", "n": "plain nonfat Greek yogurt", "g": 340},
            {"q": 1, "u": "", "n": "small cucumber", "note": "grated and squeezed dry", "g": 150},
            {"q": 1, "u": "tbsp", "n": "olive oil"},
            {"q": 1, "u": "tbsp", "n": "lemon juice"},
            {"q": 1, "u": "", "n": "small garlic clove", "note": "finely grated"},
            {"q": 1, "u": "tbsp", "n": "fresh dill", "note": "chopped"},
            {"q": 1, "u": "tbsp", "n": "fresh mint", "note": "chopped"},
            {"q": 0.5, "u": "tsp", "n": "salt"}]},
        {"group": "To serve", "items": [
            {"q": 2, "u": "cups", "n": "crunchy vegetables", "note": "carrots, bell pepper, cucumber, radishes", "g": 250}]}
    ],
    "steps": [
        {"t": "Grate and squeeze", "d": "Grate the cucumber on the coarse side of a box grater. Wrap it in a clean towel and squeeze out as much liquid as you can.", "tip": "Squeezing the cucumber keeps the tzatziki thick instead of watery."},
        {"t": "Mix", "d": "Stir the yogurt, cucumber, olive oil, lemon juice, garlic, dill, mint and salt together in a bowl."},
        {"t": "Rest", "d": "If you have time, chill for 15 minutes so the flavors come together."},
        {"t": "Serve", "d": "Spoon into a bowl, drizzle with a little more olive oil and serve with the vegetables."}
    ],
    "tips": ["Use full-fat Greek yogurt for an even creamier dip; the protein stays about the same.", "Tzatziki also works as a sauce for chicken, salmon or meatballs.", "Grate the garlic finely so it blends in.", "Small-portion tip: about 1/3 cup with a handful of vegetables is one serving."],
    "storage": "Refrigerate in a covered container for up to 4 days. Stir before serving; a little liquid may collect on top. Store the cut vegetables separately.",
    "variations": [["Lemon-only", "Skip the mint and add lemon zest."], ["Herb swap", "Use parsley or chives instead of dill and mint."], ["Pita", "Serve with warm pita triangles instead of vegetables."], ["Make it gentler", "Skip the garlic and serve with soft peeled cucumber slices."], ["Protein boost", "Serve with a few slices of grilled chicken for about 10 g more protein."]],
    "nutrition": {"calories": 107, "protein": 10, "carbs": 9, "fat": 4, "fiber": 2},
    "faq": [["Why is my tzatziki watery?", "The cucumber was not squeezed enough. Pour off any liquid and stir."], ["Can I use regular yogurt?", "Strain it in a coffee filter for an hour first, or the dip will be thin and lower in protein."], ["Is it gluten-free?", "Yes, served with vegetables."]],
    "note": "On days when everything feels too heavy, a cold bowl of tzatziki and crunchy vegetables often still sounds good.",
    "diet": ["vegetarian", "gluten-free"],
}
NEW['frozen-yogurt-berry-bars'] = {
    "title": "Frozen Greek Yogurt Berry Bars",
    "subtitle": "Creamy Greek yogurt sweetened with a little honey, topped with raspberries and blackberries and frozen into small bars. About 6 g protein each.",
    "category": "Snacks",
    "tags": ["healthy", "small-plates", "make-ahead", "gentle"],
    "prep": 10, "cook": 0, "chill": 240, "time": 250, "serves": 8, "servesLabel": "bars", "level": "Easy",
    "desc": "A cold, creamy bite with real protein.",
    "intro": [
        "These bars taste like frozen yogurt, cut into small squares. Greek yogurt sweetened with a little honey is spread in a pan, topped with berries and frozen until firm.",
        "Each bar has about 6 g of protein and only around 70 calories, which makes them a good cold treat for warm days or when you want something small and sweet."
    ],
    "why": [["About 6 g protein per bar", "Made with Greek yogurt."], ["Cold and soothing", "Good on hot or queasy days."], ["Freezer-friendly", "One bar at a time."]],
    "ingredients": [
        {"group": "For the bars", "items": [
            {"q": 2, "u": "cups", "n": "plain 2% Greek yogurt", "g": 454},
            {"q": 2, "u": "tbsp", "n": "honey or maple syrup"},
            {"q": 1, "u": "tsp", "n": "vanilla extract"}]},
        {"group": "To top", "items": [
            {"q": 1, "u": "cup", "n": "raspberries and blackberries", "note": "fresh or frozen", "g": 130}]}
    ],
    "steps": [
        {"t": "Line the pan", "d": "Line an 8 x 4-inch loaf pan with parchment paper, leaving some hanging over the sides."},
        {"t": "Sweeten the yogurt", "d": "Stir the yogurt, honey and vanilla together until smooth."},
        {"t": "Fill and top", "d": "Spread the yogurt evenly in the pan. Press the berries gently into the top."},
        {"t": "Freeze", "d": "Freeze uncovered for at least 4 hours, until firm.", "tip": "A loaf pan makes thicker, creamier bars than a baking sheet."},
        {"t": "Cut", "d": "Lift the block out using the parchment, let it sit for 5 minutes, then cut into 8 bars with a warm knife."}
    ],
    "tips": ["Halve large blackberries so they sit flat.", "Let a bar sit at room temperature for 5 minutes before eating for a softer bite.", "Vanilla Greek yogurt works; skip the honey.", "Small-portion tip: one bar is a full treat. Keep the rest in the freezer."],
    "storage": "Freeze the cut bars in a container with parchment between layers for up to 1 month.",
    "variations": [["Strawberry", "Use sliced strawberries instead of mixed berries."], ["Crunchy", "Sprinkle with 2 tablespoons granola or chopped nuts before freezing."], ["Chocolate drizzle", "Drizzle with 1 ounce melted dark chocolate after cutting."], ["Make it gentler", "Use blueberries, which are softer and less tart, and let the bar soften before eating."], ["Protein boost", "Stir 1 scoop vanilla protein powder into the yogurt for about 3 g more protein per bar."]],
    "nutrition": {"calories": 67, "protein": 6, "carbs": 9, "fat": 1, "fiber": 1},
    "faq": [["Can I use nonfat yogurt?", "Yes, but the bars freeze harder and icier. 2% gives a creamier bite."], ["Do I need to thaw them?", "Just 5 minutes at room temperature."], ["Are they gluten-free?", "Yes, as written."]],
    "note": "A bar from the freezer is a small, cold treat that still counts toward your protein. Good on hot afternoons.",
    "diet": ["vegetarian", "gluten-free"],
}

add_recipes(NEW, PHOTOS, new_cat=('Snacks', 'Snacks', 'tzatziki-yogurt-dip'), after_cat='Sips', label='5 snacks')
