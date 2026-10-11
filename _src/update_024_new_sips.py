#!/usr/bin/env python3
"""New content, batch 2 of 6: new "Sips" category with five NEW recipes (added, nothing replaced).

Photo-first rule: each photo was chosen first and the recipe written to match it. The Pexels
title or description names the dish:
  strawberry-protein-smoothie   4051784   "Delicious strawberry smoothie in a glass with strawberries" (alleksana)
  banana-protein-smoothie       4051764   "Delicious banana smoothie with a slice garnish" (alleksana)
  mixed-berry-protein-smoothie  4753639   "A vibrant berry smoothie topped with edible flower petals, served in a clear glass" (Antoni Shkraba)
  golden-milk-latte             38958695  "A glass of golden milk with turmeric and aromatic spices" (Masuma Rahaman)
  ginger-egg-drop-soup          12913641  "Close-up of a delicious homemade egg drop soup in a white bowl" (FOX)
Planned "chocolate cherry smoothie" had no matching free photo (the "chocolate smoothie" photo is described
as a layered yogurt dessert), so it became the mixed berry smoothie. Planned "ginger chicken broth" had no
free mug-of-broth photo, so it became ginger egg drop soup, which is still a sippable broth.

Nutrition per serving is an ESTIMATE from USDA FoodData Central reference values (rounded):
  Strawberry (2): frozen strawberries 280 g 90/1.9 P/22 C/6 fib; nonfat Greek yogurt 227 g 134/23 P/8 C/0.9 F;
    2% milk 244 g 122/8 P/12 C/4.8 F; honey 7 g 21/6 C -> 367 kcal, 33 P, 48 C, 6 F, 6 fib / 2 = ~184 kcal, 16 P, 24 C, 3 F, 3 fib
  Banana (2): banana 118 g 105/1.3 P/27 C/0.4 F/3 fib; nonfat Greek yogurt 227 g 134/23 P/8 C/0.9 F; 2% milk 244 g 122/8 P/12 C/4.8 F;
    vanilla 12 -> 373 kcal, 32 P, 48 C, 6 F, 3 fib / 2 = ~187 kcal, 16 P, 24 C, 3 F, 2 fib
  Mixed berry (2): frozen mixed berries 210 g 105/1.4 P/25 C/0.6 F/5 fib; nonfat Greek yogurt 227 g 134/23 P/8 C/0.9 F;
    2% milk 183 g 92/6 P/9 C/3.6 F; chia 12 g 58/2 P/5 C/3.7 F/4 fib; honey 7 g 21/6 C -> 410 kcal, 32 P, 53 C, 9 F, 9 fib
    / 2 = ~205 kcal, 16 P, 27 C, 4 F, 5 fib
  Golden milk (2): ultra-filtered 2% milk 480 ml 240/26 P/12 C/9 F (label values vary by brand); honey 14 g 43/12 C;
    turmeric, cinnamon, ginger, vanilla ~21/0.3 P/3 C/1 fib -> 304 kcal, 26 P, 27 C, 9 F, 1 fib / 2 = ~152 kcal, 13 P, 14 C, 5 F, 1 fib
  Egg drop soup (4): chicken bone broth 960 ml 160/36 P/2 C/1 F (label values vary by brand); 4 eggs 286/25 P/1.4 C/19 F;
    cornstarch 8 g 30/7 C; soy sauce 16 g 9/1 P/1 C; sesame oil 4.5 g 40/4.5 F; ginger, scallions 10/2 C
    -> 535 kcal, 62 P, 13 C, 25 F, 1 fib / 4 = ~134 kcal, 16 P, 3 C, 6 F, 0 fib

Also adds "Sips" to the category list (build.py CATS). Nothing is saved unless every download succeeds. Safe to re-run.
"""
import io, json, os, re, subprocess, sys, urllib.request

sys.stderr = sys.stdout

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
IMG = os.path.join(ROOT, 'images')
P = lambda n: os.path.join(HERE, n)

PHOTOS = {
    'strawberry-protein-smoothie': {
        'id': 4051784, 'photographer': 'alleksana', 'photographer_url': 'https://www.pexels.com/@alleksana/',
        'photo_url': 'https://www.pexels.com/photo/drink-with-strawberries-4051784/',
        'alt': 'A strawberry smoothie in a glass with fresh strawberries in sunlight.'},
    'banana-protein-smoothie': {
        'id': 4051764, 'photographer': 'alleksana', 'photographer_url': 'https://www.pexels.com/@alleksana/',
        'photo_url': 'https://www.pexels.com/photo/banana-smoothie-in-glass-4051764/',
        'alt': 'A creamy banana smoothie in a glass with a banana slice on the rim.'},
    'mixed-berry-protein-smoothie': {
        'id': 4753639, 'photographer': 'Antoni Shkraba', 'photographer_url': 'https://www.pexels.com/@shkrabaanthony/',
        'photo_url': 'https://www.pexels.com/photo/close-up-of-a-smoothie-in-a-glass-4753639/',
        'alt': 'A mixed berry smoothie in a clear glass topped with edible flower petals.'},
    'golden-milk-latte': {
        'id': 38958695, 'photographer': 'Masuma Rahaman', 'photographer_url': 'https://www.pexels.com/@masuma-rahaman-437541976/',
        'photo_url': 'https://www.pexels.com/photo/golden-milk-with-spices-and-ingredients-38958695/',
        'alt': 'A glass of golden turmeric milk with spices around it.'},
    'ginger-egg-drop-soup': {
        'id': 12913641, 'photographer': 'FOX', 'photographer_url': 'https://www.pexels.com/@fox-58267/',
        'photo_url': 'https://www.pexels.com/photo/a-close-up-shot-of-a-delicious-soup-12913641/',
        'alt': 'A white bowl of egg drop soup with silky ribbons of egg.'},
}

N = None
NEW = {}
NEW['strawberry-protein-smoothie'] = {
    "title": "Strawberry Greek Yogurt Smoothie",
    "subtitle": "Frozen strawberries blended with Greek yogurt and milk into a thick, cold smoothie. About 16 g protein per small glass, no protein powder needed.",
    "category": "Sips",
    "tags": ["quick", "healthy", "high-protein", "small-plates", "gentle"],
    "prep": 5, "cook": 0, "time": 5, "serves": 2, "servesLabel": "small glasses", "level": "Easy",
    "desc": "Thick, cold and about 16 g protein a glass.",
    "intro": [
        "On days when chewing feels like work, a smoothie is often the easiest way to get some protein in. This one uses Greek yogurt instead of protein powder, so it tastes like strawberries and cream rather than a supplement, with about 16 g of protein in each small glass.",
        "Frozen strawberries do two jobs: they make the smoothie cold and thick without ice, and they keep well in the freezer so you can make a glass whenever you want one."
    ],
    "why": [
        ["About 16 g protein per glass", "From Greek yogurt and milk, no powder."],
        ["Five minutes", "Everything goes straight into the blender."],
        ["Easy to sip slowly", "A small glass you can finish over half an hour."]
    ],
    "ingredients": [
        {"group": "For the smoothie", "items": [
            {"q": 2, "u": "cups", "n": "frozen strawberries", "g": 280},
            {"q": 1, "u": "cup", "n": "plain nonfat Greek yogurt", "g": 227},
            {"q": 1, "u": "cup", "n": "milk", "note": "any kind"},
            {"q": 1, "u": "tsp", "n": "honey", "note": "optional"},
            {"q": 0.5, "u": "tsp", "n": "vanilla extract"}
        ]}
    ],
    "steps": [
        {"t": "Add the liquid first", "d": "Pour the milk into the blender, then add the yogurt, honey and vanilla.",
         "tip": "Liquid at the bottom helps the blades move and keeps the blender from stalling."},
        {"t": "Add the strawberries", "d": "Add the frozen strawberries on top."},
        {"t": "Blend", "d": "Blend on low for a few seconds, then on high for 45 to 60 seconds, until completely smooth. Add a splash more milk if it is too thick to pour."},
        {"t": "Serve small", "d": "Pour into two small glasses. Drink one now and keep the other covered in the fridge for later in the day."}
    ],
    "tips": [
        "Taste before adding honey; ripe frozen strawberries are often sweet enough.",
        "For a thicker, spoonable smoothie, use 3/4 cup milk.",
        "Fresh strawberries work too; add a few ice cubes for chill.",
        "Small-portion tip: sip it slowly over 20 to 30 minutes. It does not need to be finished in one go."
    ],
    "storage": "Best fresh. Refrigerate a covered glass for up to 24 hours and shake or stir before drinking. Freeze leftovers in ice pop molds for up to 1 month.",
    "variations": [
        ["Strawberry banana", "Replace 1 cup of strawberries with half a frozen banana."],
        ["Dairy-free", "Use a soy yogurt and soy milk; the protein will be a little lower."],
        ["Oat boost", "Blend in 2 tablespoons rolled oats for a more filling glass."],
        ["Make it gentler", "Use a mild, plain yogurt, skip the honey and let it sit for a few minutes so it is cool rather than icy."],
        ["Protein boost", "Blend in one scoop of vanilla protein powder for about 12 g more protein per glass."]
    ],
    "nutrition": {"calories": 184, "protein": 16, "carbs": 24, "fat": 3, "fiber": 3},
    "faq": [
        ["Can I make it ahead?", "Yes, up to a day. It separates a little; shake or stir it before drinking."],
        ["Do I need a high-powered blender?", "No. Add the milk first and blend in short bursts if your blender struggles."],
        ["Is it gluten-free?", "Yes, as written."]
    ],
    "note": "When a plate of food feels like too much, a small glass often does not. Keep a bag of frozen strawberries in the freezer for exactly those days.",
    "diet": ["vegetarian", "gluten-free"],
}
NEW['banana-protein-smoothie'] = {
    "title": "Banana Vanilla Protein Smoothie",
    "subtitle": "A creamy banana smoothie with Greek yogurt, milk, vanilla and a pinch of cinnamon. Tastes like a milkshake, with about 16 g protein per small glass.",
    "category": "Sips",
    "tags": ["quick", "healthy", "high-protein", "small-plates", "gentle"],
    "prep": 5, "cook": 0, "time": 5, "serves": 2, "servesLabel": "small glasses", "level": "Easy",
    "desc": "A milkshake-style smoothie with real protein.",
    "intro": [
        "A frozen banana blends into something that tastes surprisingly close to a vanilla milkshake. Add Greek yogurt and milk and each small glass has about 16 g of protein, with nothing more than a pinch of cinnamon for flavor.",
        "Bananas are also one of the mildest fruits there is, which makes this a good choice on days when strong flavors or acidic fruit do not sit well."
    ],
    "why": [
        ["About 16 g protein per glass", "Greek yogurt and milk do the work."],
        ["Mild and creamy", "Banana, vanilla and a little cinnamon."],
        ["No added sugar needed", "A ripe banana sweetens it."]
    ],
    "ingredients": [
        {"group": "For the smoothie", "items": [
            {"q": 1, "u": "", "n": "ripe banana", "note": "sliced and frozen", "g": 118},
            {"q": 1, "u": "cup", "n": "plain nonfat Greek yogurt", "g": 227},
            {"q": 1, "u": "cup", "n": "milk", "note": "any kind"},
            {"q": 1, "u": "tsp", "n": "vanilla extract"},
            {"q": N, "u": "", "n": "pinch of ground cinnamon"},
            {"q": 3, "u": "", "n": "ice cubes", "note": "optional"}
        ]}
    ],
    "steps": [
        {"t": "Freeze the banana", "d": "Peel a ripe banana, slice it and freeze the slices on a plate or in a bag for at least 2 hours.",
         "tip": "Freeze several bananas at once. Spotty, very ripe bananas make the sweetest smoothies."},
        {"t": "Blend", "d": "Add the milk, yogurt, vanilla and cinnamon to the blender, then the frozen banana. Blend until smooth and thick, about 45 seconds."},
        {"t": "Adjust", "d": "Add ice for a colder, frothier smoothie, or a splash of milk if it is too thick."},
        {"t": "Serve", "d": "Pour into two small glasses and dust with a little more cinnamon."}
    ],
    "tips": [
        "No frozen banana? Use a fresh one and add 4 or 5 ice cubes.",
        "The riper the banana, the sweeter and less starchy the smoothie.",
        "Vanilla Greek yogurt works too; skip the vanilla extract.",
        "Small-portion tip: one small glass is a full snack. Save the second for the afternoon."
    ],
    "storage": "Best fresh. Refrigerate a covered glass for up to 12 hours; banana smoothies darken a little as they sit, which is harmless. Stir before drinking.",
    "variations": [
        ["Peanut butter", "Blend in 1 tablespoon peanut butter for extra flavor and about 2 g more protein per glass."],
        ["Coffee", "Replace half the milk with cold brewed coffee."],
        ["Dairy-free", "Use soy yogurt and soy milk."],
        ["Make it gentler", "Skip the cinnamon and ice, and use a very ripe banana for the softest flavor."],
        ["Protein boost", "Add a scoop of vanilla protein powder and a splash more milk for about 12 g more protein per glass."]
    ],
    "nutrition": {"calories": 187, "protein": 16, "carbs": 24, "fat": 3, "fiber": 2},
    "faq": [
        ["Why freeze the banana?", "It makes the smoothie thick and cold without watering it down with lots of ice."],
        ["Can I use a green banana?", "It works, but it tastes starchy and less sweet. Ripe is best."],
        ["Is it gluten-free?", "Yes, as written."]
    ],
    "note": "This is the smoothie for days when nothing sounds good. Mild, sweet, cold, and easy to sip slowly.",
    "diet": ["vegetarian", "gluten-free"],
}
NEW['mixed-berry-protein-smoothie'] = {
    "title": "Mixed Berry Protein Smoothie",
    "subtitle": "Frozen mixed berries, Greek yogurt, milk and a spoonful of chia blended into a thick, deep-purple smoothie. About 16 g protein and 5 g fiber per small glass.",
    "category": "Sips",
    "tags": ["quick", "healthy", "high-protein", "small-plates", "gentle"],
    "prep": 5, "cook": 0, "time": 5, "serves": 2, "servesLabel": "small glasses", "level": "Easy",
    "desc": "Bright berries, 16 g protein, 5 g fiber.",
    "intro": [
        "A bag of frozen mixed berries is one of the most useful things to keep in the freezer. Blended with Greek yogurt and milk, it makes a thick, bright smoothie with about 16 g of protein in each small glass.",
        "A spoonful of chia seeds adds fiber and makes the smoothie a little thicker as it sits, which is helpful when you want something that feels more like a small meal."
    ],
    "why": [
        ["About 16 g protein per glass", "Greek yogurt plus milk."],
        ["5 g fiber", "Berries and chia seeds."],
        ["Freezer staples", "Ready any day of the week."]
    ],
    "ingredients": [
        {"group": "For the smoothie", "items": [
            {"q": 1.5, "u": "cups", "n": "frozen mixed berries", "note": "strawberries, blueberries, raspberries", "g": 210},
            {"q": 1, "u": "cup", "n": "plain nonfat Greek yogurt", "g": 227},
            {"q": 0.75, "u": "cup", "n": "milk", "note": "any kind"},
            {"q": 1, "u": "tbsp", "n": "chia seeds"},
            {"q": 1, "u": "tsp", "n": "honey", "note": "optional"}
        ]},
        {"group": "To serve (optional)", "items": [
            {"q": N, "u": "", "n": "a few fresh berries or edible flowers"}
        ]}
    ],
    "steps": [
        {"t": "Load the blender", "d": "Add the milk, yogurt, chia seeds and honey to the blender, then the frozen berries."},
        {"t": "Blend", "d": "Blend on high for about 60 seconds, until completely smooth and no chia specks remain whole.",
         "tip": "If you prefer a smoother texture, soak the chia in the milk for 5 minutes before blending."},
        {"t": "Thin if needed", "d": "Add milk a tablespoon at a time if the smoothie is too thick to sip through a straw."},
        {"t": "Serve", "d": "Pour into two small glasses and top with a few fresh berries if you like."}
    ],
    "tips": [
        "Mixed berries vary in tartness; taste and add honey only if needed.",
        "Raspberries and blackberries have seeds. Strain through a sieve for a seed-free smoothie.",
        "The smoothie thickens as it sits because of the chia. Stir in a splash of milk before drinking.",
        "Small-portion tip: a small glass now and the rest later counts just as much."
    ],
    "storage": "Refrigerate a covered glass for up to 24 hours. It will thicken; stir in a little milk before drinking.",
    "variations": [
        ["Blueberry only", "Use all blueberries for a milder, sweeter smoothie."],
        ["Green", "Blend in a small handful of baby spinach; the berries hide the color and flavor."],
        ["Dairy-free", "Use soy yogurt and soy milk."],
        ["Make it gentler", "Use blueberries and strawberries only, skip the chia and strain out any seeds."],
        ["Protein boost", "Blend in a scoop of unflavored or vanilla protein powder for about 12 g more protein per glass."]
    ],
    "nutrition": {"calories": 205, "protein": 16, "carbs": 27, "fat": 4, "fiber": 5},
    "faq": [
        ["Fresh or frozen berries?", "Frozen give the best thick, cold texture. With fresh berries, add a handful of ice."],
        ["Can I skip the chia?", "Yes. The smoothie will be a little thinner, with about 2 g less fiber per glass."],
        ["Is it gluten-free?", "Yes, as written."]
    ],
    "note": "Bright, cold and a little tart. On slow mornings, one small glass of this is often enough to get started.",
    "diet": ["vegetarian", "gluten-free"],
}
NEW['golden-milk-latte'] = {
    "title": "Golden Milk Turmeric Latte",
    "subtitle": "Warm or iced milk gently spiced with turmeric, cinnamon and ginger. Made with ultra-filtered milk for about 13 g protein per glass.",
    "category": "Sips",
    "tags": ["quick", "small-plates", "gentle"],
    "prep": 2, "cook": 5, "time": 7, "serves": 2, "servesLabel": "glasses", "level": "Easy",
    "desc": "A soothing spiced milk with real protein.",
    "intro": [
        "Golden milk is warm milk spiced with turmeric, cinnamon and ginger. It is soothing, lightly sweet and easy to sip slowly, which makes it a good evening drink or a gentle start to the day.",
        "Using ultra-filtered milk, the kind sold with higher protein on the label, gives each glass about 13 g of protein without changing the taste. Regular milk works too, with about 8 g per glass."
    ],
    "why": [
        ["About 13 g protein per glass", "From ultra-filtered milk."],
        ["Warm or iced", "Sip it hot in winter or over ice in summer."],
        ["Gently spiced", "Turmeric, cinnamon and a little ginger."]
    ],
    "ingredients": [
        {"group": "For the golden milk", "items": [
            {"q": 2, "u": "cups", "n": "ultra-filtered 2% milk", "note": "or regular milk"},
            {"q": 1, "u": "tsp", "n": "ground turmeric"},
            {"q": 0.5, "u": "tsp", "n": "ground cinnamon"},
            {"q": 0.25, "u": "tsp", "n": "ground ginger"},
            {"q": N, "u": "", "n": "pinch of black pepper"},
            {"q": 2, "u": "tsp", "n": "honey or maple syrup"},
            {"q": 0.5, "u": "tsp", "n": "vanilla extract"}
        ]}
    ],
    "steps": [
        {"t": "Whisk the spices", "d": "Add the milk, turmeric, cinnamon, ginger and pepper to a small saucepan and whisk until no lumps remain."},
        {"t": "Warm gently", "d": "Heat over medium-low, whisking often, until steaming but not boiling, about 4 to 5 minutes.",
         "tip": "Do not let it boil. Ultra-filtered milk can catch on the bottom of the pan if the heat is too high."},
        {"t": "Sweeten", "d": "Take the pan off the heat and stir in the honey and vanilla. Taste and adjust."},
        {"t": "Serve warm or iced", "d": "Pour into two glasses or mugs. For iced golden milk, let it cool, then pour over ice."}
    ],
    "tips": [
        "Turmeric stains. Rinse the pan and whisk right away.",
        "Whisking or frothing the milk before serving gives it a latte-style foam.",
        "A pinch of black pepper is traditional; leave it out if you prefer.",
        "Small-portion tip: half a glass is perfectly fine. Keep the rest in the fridge and warm it later."
    ],
    "storage": "Refrigerate in a covered jar for up to 3 days. Shake well, then warm gently or serve over ice.",
    "variations": [
        ["Dairy-free", "Use soy milk for the most protein among plant milks."],
        ["Chai-style", "Add a pinch of cardamom and a small pinch of cloves."],
        ["Fresh spices", "Use 1 teaspoon each grated fresh turmeric and ginger, then strain."],
        ["Make it gentler", "Halve the turmeric, skip the pepper and ginger, and serve it warm rather than hot."],
        ["Protein boost", "Whisk in a scoop of unflavored collagen or vanilla protein powder off the heat."]
    ],
    "nutrition": {"calories": 152, "protein": 13, "carbs": 14, "fat": 5, "fiber": 1},
    "faq": [
        ["What is ultra-filtered milk?", "Milk filtered to concentrate the protein and reduce the sugar. Check labels; most have around 13 g protein per cup."],
        ["Does it contain caffeine?", "No. That makes it a good evening drink."],
        ["Is it gluten-free?", "Yes, as written."]
    ],
    "note": "A warm glass of golden milk is one of the gentlest ways to end the day. It counts as a small meal on nights when dinner does not happen.",
    "diet": ["vegetarian", "gluten-free"],
}
NEW['ginger-egg-drop-soup'] = {
    "title": "Ginger Egg Drop Soup",
    "subtitle": "Hot chicken bone broth with fresh ginger and silky ribbons of egg, ready in 15 minutes. About 16 g protein per mug, easy to sip on hard days.",
    "category": "Sips",
    "tags": ["quick", "high-protein", "small-plates", "gentle", "make-ahead"],
    "prep": 5, "cook": 10, "time": 15, "serves": 4, "servesLabel": "mugs", "level": "Easy",
    "desc": "Silky egg ribbons in a gingery broth.",
    "intro": [
        "Egg drop soup is one of the fastest soups there is: hot broth, a little cornstarch to give it body, and beaten eggs poured in slowly so they turn into soft, silky ribbons. It is light, warm and easy to sip from a mug.",
        "Using chicken bone broth instead of regular stock adds a surprising amount of protein. With the eggs, each mug has about 16 g, and fresh ginger keeps it bright and soothing."
    ],
    "why": [
        ["About 16 g protein per mug", "Bone broth and eggs together."],
        ["15 minutes", "Faster than most takeout."],
        ["Sippable", "Soft, warm and light."]
    ],
    "ingredients": [
        {"group": "For the broth", "items": [
            {"q": 4, "u": "cups", "n": "low-sodium chicken bone broth"},
            {"q": 1, "u": "tbsp", "n": "fresh ginger", "note": "thinly sliced or grated"},
            {"q": 1, "u": "tbsp", "n": "low-sodium soy sauce or tamari"},
            {"q": 1, "u": "tbsp", "n": "cornstarch", "note": "mixed with 2 tbsp cold water"}
        ]},
        {"group": "To finish", "items": [
            {"q": 4, "u": "", "n": "large eggs"},
            {"q": 1, "u": "tsp", "n": "toasted sesame oil"},
            {"q": 2, "u": "", "n": "scallions", "note": "thinly sliced"},
            {"q": N, "u": "", "n": "white pepper", "note": "to taste"}
        ]}
    ],
    "steps": [
        {"t": "Infuse the broth", "d": "Bring the broth, ginger and soy sauce to a simmer in a saucepan and simmer for 5 minutes. Remove the ginger slices if you used them."},
        {"t": "Thicken", "d": "Stir the cornstarch slurry, then whisk it into the simmering broth. Cook for 1 minute, until the broth turns slightly glossy."},
        {"t": "Beat the eggs", "d": "Beat the eggs in a jug or bowl until completely smooth."},
        {"t": "Make the ribbons", "d": "Stir the broth in a slow circle with one hand while you pour the eggs in a thin stream with the other. Stop stirring and let the soup sit for 30 seconds, until the ribbons set.",
         "tip": "A slow, thin stream gives fine, silky ribbons. Pouring fast gives larger, fluffier pieces. Both are good."},
        {"t": "Finish", "d": "Turn off the heat, stir in the sesame oil and season with white pepper. Ladle into mugs or small bowls and scatter with scallions."}
    ],
    "tips": [
        "Bone broth brands vary a lot in protein. Check the label; most have 8 to 10 g per cup.",
        "Taste before adding more soy sauce; broth is often salty enough.",
        "For the softest ribbons, keep the broth at a gentle simmer, not a rolling boil.",
        "Small-portion tip: a single mug is a full small meal. Reheat the rest one mug at a time."
    ],
    "storage": "Refrigerate in a covered container for up to 3 days. Reheat gently on the stove or in the microwave; the ribbons stay soft. Not ideal for freezing, as the eggs turn spongy.",
    "variations": [
        ["Tofu", "Add 1/2 cup diced soft tofu with the eggs for about 3 g more protein per mug."],
        ["Spinach", "Stir in a handful of baby spinach just before the eggs."],
        ["Corn", "Add 1/2 cup sweet corn for a classic egg drop and corn soup."],
        ["Make it gentler", "Skip the white pepper and scallions, use less ginger and let it cool to warm before sipping."],
        ["Protein boost", "Stir in 1/2 cup shredded cooked chicken per mug."]
    ],
    "nutrition": {"calories": 134, "protein": 16, "carbs": 3, "fat": 6, "fiber": 0},
    "faq": [
        ["Is it gluten-free?", "Use tamari or a gluten-free soy sauce and check that your broth is gluten-free."],
        ["Can I use regular chicken broth?", "Yes, but the protein will drop to about 8 g per mug."],
        ["Why add cornstarch?", "It gives the broth a little body so the egg ribbons stay suspended."]
    ],
    "note": "This is the soup to make when you are tired, cold or not very hungry. Ten minutes on the stove, then a warm mug to sip slowly.",
    "diet": ["dairy-free"],
}

# ------------------------------------------------------------------ idempotency
raw = open(P('recipes.json'), encoding='utf-8').read()
recipes = json.loads(raw)
ids = {r['id'] for r in recipes}
if all(n in ids for n in NEW):
    print('Already applied. Nothing to do.')
    sys.exit(0)
clash = [n for n in NEW if n in ids]
if clash:
    print(f'ERROR: some new ids already exist: {clash}. Nothing was saved.')
    sys.exit(1)

b = open(P('build.py'), encoding='utf-8').read()
CAT_ANCHOR = "    ('Soups', 'Soups', 'butternut-squash-soup'),\n"
if "('Sips'" not in b and CAT_ANCHOR not in b:
    print('ERROR: could not find the Soups line in CATS (build.py). Nothing was saved.')
    sys.exit(1)
if not re.search(r'FOCUS_IDS = (\[.*?\])', b):
    print('ERROR: FOCUS_IDS not found in build.py. Nothing was saved.')
    sys.exit(1)

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

# ------------------------------------------------------------------ write images
for rid, bb in out.items():
    open(os.path.join(IMG, f'{rid}.webp'), 'wb').write(bb['webp'])
    open(os.path.join(IMG, 'og', f'{rid}.jpg'), 'wb').write(bb['og'])
    open(os.path.join(IMG, 'pins', f'{rid}.jpg'), 'wb').write(bb['pin'])
subprocess.check_call([sys.executable, P('make_images.py')])

# ------------------------------------------------------------------ credits
craw = open(P('credits.json'), encoding='utf-8').read()
credits = json.loads(craw)
for rid, ph in PHOTOS.items():
    credits[rid] = {'photographer': ph['photographer'], 'photographer_url': ph['photographer_url'],
                    'photo_url': ph['photo_url'], 'source': 'Pexels', 'alt': ph['alt']}
m = re.match(r'\{\s*\n([ \t]+)"', craw)
with open(P('credits.json'), 'w', encoding='utf-8') as f:
    json.dump(credits, f, ensure_ascii=False, indent=len(m.group(1)) if m else 1)
    f.write('\n')

# ------------------------------------------------------------------ build.py: focus list + Sips category
m = re.search(r'FOCUS_IDS = (\[.*?\])', b)
focus = json.loads(m.group(1))
for rid in NEW:
    if rid not in focus:
        focus.append(rid)
b = b[:m.start(1)] + json.dumps(focus) + b[m.end(1):]
if "('Sips'" not in b:
    b = b.replace(CAT_ANCHOR, CAT_ANCHOR + "    ('Sips', 'Sips', 'strawberry-protein-smoothie'),\n", 1)
    print('- added the Sips category')
open(P('build.py'), 'w', encoding='utf-8').write(b)

# ------------------------------------------------------------------ recipes.json (last)
for rid, data in NEW.items():
    new = {'id': rid}
    new.update(data)
    new['img'] = f'images/{rid}.webp'
    recipes.append(new)
    print(f"- added {rid} ({data['title']}, ~{data['nutrition']['protein']} g protein, ~{data['nutrition']['calories']} kcal per serving)")
m = re.match(r'\[\s*\n([ \t]+)\{', raw)
with open(P('recipes.json'), 'w', encoding='utf-8') as f:
    json.dump(recipes, f, ensure_ascii=False, indent=len(m.group(1)) if m else None)
    f.write('\n')
print(f'OK: 5 sips added. The site now has {len(recipes)} recipes.')
