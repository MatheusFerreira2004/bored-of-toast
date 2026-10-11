#!/usr/bin/env python3
"""New content, batch 1 of 6: five NEW breakfast recipes (added, nothing replaced).

Photo-first rule: each photo was chosen first, and the recipe was written to match it. The Pexels
title or description names the dish:
  greek-yogurt-berry-parfaits     14122621  "Fresh yogurt parfait topped with strawberries and blueberries in a glass jar" (Karina Ustiuzhanina)
  smoked-salmon-bagel-halves      36392562  "Tasty everything bagel with salmon, cucumber, and dill on a white plate" (Eddie O.)
  cottage-cheese-scrambled-eggs   19745150  "A vibrant plate featuring scrambled eggs, avocado, toast, and salad greens" (Sai Kuen Leung)
  berry-greek-yogurt-muffins      4051608   "Delicious homemade berry muffins in a baking tin" (alleksana)
  strawberry-cottage-cheese-bowl  32065590  "A sunlit plate of strawberries and cottage cheese perfect for breakfast" (Helen Brudna)
Planned "savory oatmeal" and "banana muffins" had no matching free photo, so they became the cottage
cheese bowl and berry muffins.

Nutrition per serving is an ESTIMATE from USDA FoodData Central reference values (rounded):
  Parfaits (4): nonfat Greek yogurt 680 g 401/69 P/24 C/2 F; honey 21 g 64/17 C; strawberries 250 g 80/1.7 P/19 C/5 fib;
    blueberries 148 g 84/1.1 P/21 C/3.5 fib; granola 60 g 270/6 P/38 C/10 F/3 fib; chia 12 g 58/2 P/5 C/3.7 F/4 fib
    -> 957 kcal, 80 P, 124 C, 16 F, 15 fib / 4 = ~240 kcal, 20 P, 31 C, 4 F, 4 fib
  Salmon bagel halves (4): 2 everything bagels 200 g 540/21 P/106 C/3.4 F/4.6 fib; light cream cheese 60 g 120/6 P/4 C/9 F;
    nonfat Greek yogurt 60 g 35/6 P/2 C; smoked salmon 170 g 199/31 P/7.4 F; cucumber 8; capers, dill, lemon 7
    -> 909 kcal, 64 P, 114 C, 20 F, 5 fib / 4 = ~227 kcal, 16 P, 28 C, 5 F, 1 fib
  Cottage cheese scrambled eggs (2): 4 eggs 286/25 P/1.4 C/19 F; low-fat cottage cheese 113 g 92/12 P/4 C/2.5 F;
    butter 5 g 34/3.8 F; whole-grain bread 70 g 180/8 P/32 C/2.4 F/4 fib; avocado 50 g 80/1 P/4 C/7.4 F/3.4 fib; greens 5
    -> 677 kcal, 47 P, 42 C, 35 F, 8 fib / 2 = ~340 kcal, 24 P, 21 C, 18 F, 4 fib
  Berry muffins (12): flour 125 g 455/13 P/95 C/1.2 F/3.4 fib; vanilla protein powder 45 g ~170/36 P/3 C/1 F;
    nonfat Greek yogurt 227 g 134/23 P/8 C; 2 eggs 143/12.6 P/9.5 F; maple syrup 107 g 278/72 C; oil 40 g 357/40 F;
    milk 61 g 30/2 P/3 C/1.2 F; berries 160 g 85/1.5 P/20 C/7 fib; leaveners, salt, vanilla 10
    -> 1662 kcal, 88 P, 201 C, 53 F, 10 fib / 12 = ~139 kcal, 7 P, 17 C, 4 F, 1 fib (protein powder varies by brand)
  Strawberry cottage cheese bowl (2): 2% cottage cheese 452 g 366/47 P/19 C/10 F; strawberries 300 g 96/2 P/23 C/6 fib;
    honey 14 g 43/12 C; sliced almonds 14 g 81/3 P/3 C/7 F/1.7 fib
    -> 586 kcal, 52 P, 57 C, 17 F, 8 fib / 2 = ~295 kcal, 26 P, 29 C, 9 F, 4 fib

Nothing is saved unless every download succeeds. Safe to re-run.
"""
import io, json, os, re, subprocess, sys, urllib.request

sys.stderr = sys.stdout

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
IMG = os.path.join(ROOT, 'images')
P = lambda n: os.path.join(HERE, n)

PHOTOS = {
    'greek-yogurt-berry-parfaits': {
        'id': 14122621, 'photographer': 'Karina Ustiuzhanina', 'photographer_url': 'https://www.pexels.com/@karina-ustiuzhanina-313369745/',
        'photo_url': 'https://www.pexels.com/photo/dessert-on-a-glass-jar-14122621/',
        'alt': 'A Greek yogurt parfait in a glass jar topped with strawberries and blueberries.'},
    'smoked-salmon-bagel-halves': {
        'id': 36392562, 'photographer': 'Eddie O.', 'photographer_url': 'https://www.pexels.com/@eddieo/',
        'photo_url': 'https://www.pexels.com/photo/delicious-everything-bagel-with-salmon-and-cucumber-36392562/',
        'alt': 'An everything bagel topped with smoked salmon, cucumber and dill on a white plate.'},
    'cottage-cheese-scrambled-eggs': {
        'id': 19745150, 'photographer': 'Sai Kuen Leung', 'photographer_url': 'https://www.pexels.com/@sai-kuen-leung-452610443/',
        'photo_url': 'https://www.pexels.com/photo/scrambled-eggs-served-for-breakfast-19745150/',
        'alt': 'Soft scrambled eggs with avocado, toast and salad greens on a plate.'},
    'berry-greek-yogurt-muffins': {
        'id': 4051608, 'photographer': 'alleksana', 'photographer_url': 'https://www.pexels.com/@alleksana/',
        'photo_url': 'https://www.pexels.com/photo/baked-muffins-in-a-muffin-tin-4051608/',
        'alt': 'Homemade berry muffins in a muffin tin.'},
    'strawberry-cottage-cheese-bowl': {
        'id': 32065590, 'photographer': 'Helen Brudna', 'photographer_url': 'https://www.pexels.com/@helen-brudna-2151730422/',
        'photo_url': 'https://www.pexels.com/photo/strawberry-and-cottage-cheese-morning-delight-32065590/',
        'alt': 'Cottage cheese with fresh strawberries on a sunlit plate.'},
}

N = None
NEW = {}
NEW['greek-yogurt-berry-parfaits'] = {
    "title": "Greek Yogurt Berry Parfait Jars",
    "subtitle": "Layers of vanilla Greek yogurt, fresh strawberries, blueberries and a little granola in small jars. About 20 g protein each, ready in the fridge for the week.",
    "category": "Beyond Toast",
    "tags": ["quick", "healthy", "high-protein", "small-plates", "gentle", "make-ahead"],
    "prep": 10, "cook": 0, "time": 10, "serves": 4, "servesLabel": "jars", "level": "Easy",
    "desc": "Cold, creamy and ready when you are.",
    "intro": [
        "A parfait is one of the easiest ways to get protein in before the day gets busy. Thick Greek yogurt does most of the work, with about 20 g of protein in each small jar, and fresh berries keep it bright and light.",
        "The trick for make-ahead jars is keeping the granola crisp. A spoonful goes on top just before eating, or in a small separate container, so the layers stay creamy and the crunch stays crunchy."
    ],
    "why": [
        ["About 20 g protein per jar", "Most of it comes from thick Greek yogurt."],
        ["No cooking at all", "Ten minutes of layering covers four breakfasts."],
        ["Cold and gentle", "Easy on mornings when warm food does not appeal."]
    ],
    "ingredients": [
        {"group": "For the yogurt", "items": [
            {"q": 3, "u": "cups", "n": "plain nonfat Greek yogurt", "g": 680},
            {"q": 1, "u": "tbsp", "n": "honey or maple syrup"},
            {"q": 1, "u": "tsp", "n": "vanilla extract"}
        ]},
        {"group": "For the layers", "items": [
            {"q": 1.5, "u": "cups", "n": "strawberries", "note": "hulled and sliced"},
            {"q": 1, "u": "cup", "n": "blueberries"},
            {"q": 1, "u": "tbsp", "n": "chia seeds", "note": "optional"},
            {"q": 0.5, "u": "cup", "n": "granola", "note": "added just before eating"}
        ]}
    ],
    "steps": [
        {"t": "Sweeten the yogurt", "d": "Stir the Greek yogurt, honey and vanilla together in a bowl until smooth."},
        {"t": "Layer the jars", "d": "Spoon a layer of yogurt into four small jars or glasses (about 8 oz each). Add a layer of berries and a pinch of chia seeds, then repeat, finishing with berries on top.",
         "tip": "Small jars help: a full jar you can finish beats a big bowl you cannot."},
        {"t": "Chill", "d": "Cover and refrigerate for up to 4 days."},
        {"t": "Add the crunch", "d": "Just before eating, scatter about 2 tablespoons of granola over each jar."}
    ],
    "tips": [
        "Pat the berries dry after washing so the yogurt does not turn watery.",
        "Frozen berries work too. Layer them frozen and they thaw in the fridge overnight.",
        "Keep the granola in a small separate container if you are packing a jar to go.",
        "Small-portion tip: eat half a jar now and put the lid back on. It keeps well for later."
    ],
    "storage": "Refrigerate the covered jars, without granola, for up to 4 days. Do not freeze.",
    "variations": [
        ["Peach", "Use diced peaches and a pinch of cinnamon instead of the berries."],
        ["Chocolate", "Stir 1 tablespoon cocoa powder into the yogurt with a little extra honey."],
        ["Gluten-free", "Use a certified gluten-free granola."],
        ["Make it gentler", "Skip the granola and chia, and use soft berries like ripe strawberries or mashed raspberries."],
        ["Protein boost", "Stir 2 tablespoons vanilla protein powder into the yogurt, loosening with a splash of milk."]
    ],
    "nutrition": {"calories": 240, "protein": 20, "carbs": 31, "fat": 4, "fiber": 4},
    "faq": [
        ["Can I use flavored yogurt?", "Yes, but most flavored yogurts have more sugar and less protein. Plain Greek yogurt with a little honey gives you more control."],
        ["Why add the granola last?", "Granola softens in yogurt within a few hours. Adding it at the end keeps the crunch."],
        ["Is it dairy-free?", "Not as written. A thick coconut or soy yogurt works, though the protein will be lower."]
    ],
    "note": "Four jars on Sunday means four mornings where breakfast is already done. Cold, creamy and easy to stop halfway.",
    "diet": ["vegetarian"],
}
NEW['smoked-salmon-bagel-halves'] = {
    "title": "Smoked Salmon Bagel Halves",
    "subtitle": "Half an everything bagel with a whipped cream cheese and Greek yogurt spread, smoked salmon, cucumber and dill. About 16 g protein per half, no cooking.",
    "category": "Beyond Toast",
    "tags": ["quick", "high-protein", "small-plates"],
    "prep": 10, "cook": 0, "time": 10, "serves": 4, "servesLabel": "bagel halves", "level": "Easy",
    "desc": "A deli breakfast in a smaller portion.",
    "intro": [
        "A whole bagel with lox is a lot of food. Served open-faced as halves, it becomes a breakfast you can actually finish, with about 16 g of protein in each half from the smoked salmon and a lighter spread.",
        "The spread is half light cream cheese and half Greek yogurt, whipped with lemon and dill. It tastes like the deli version but adds protein and spreads more easily, so a thin layer is enough."
    ],
    "why": [
        ["About 16 g protein per half", "Smoked salmon and a Greek yogurt spread."],
        ["Ready in 10 minutes", "No stove, no oven."],
        ["Naturally portioned", "One half is a small plate. Two make a bigger one."]
    ],
    "ingredients": [
        {"group": "For the spread", "items": [
            {"q": 0.25, "u": "cup", "n": "light cream cheese", "note": "softened", "g": 60},
            {"q": 0.25, "u": "cup", "n": "plain nonfat Greek yogurt", "g": 60},
            {"q": 1, "u": "tsp", "n": "lemon juice"},
            {"q": 1, "u": "tbsp", "n": "chopped fresh dill", "note": "plus more to serve"}
        ]},
        {"group": "To assemble", "items": [
            {"q": 2, "u": "", "n": "everything bagels", "note": "sliced in half and toasted"},
            {"q": 6, "u": "oz", "n": "smoked salmon", "note": "170 g"},
            {"q": 0.5, "u": "", "n": "small cucumber", "note": "thinly sliced"},
            {"q": 1, "u": "tbsp", "n": "capers", "note": "optional"},
            {"q": N, "u": "", "n": "black pepper and lemon wedges", "note": "to serve"}
        ]}
    ],
    "steps": [
        {"t": "Whip the spread", "d": "Stir the cream cheese, Greek yogurt, lemon juice and dill together until smooth and fluffy."},
        {"t": "Toast the bagels", "d": "Toast the bagel halves until lightly golden. Let them cool for a minute so the spread does not melt."},
        {"t": "Spread and layer", "d": "Spread a thin layer of the cream cheese mixture over each half. Top with cucumber slices and fold the smoked salmon over the top.",
         "tip": "Cucumber under the salmon keeps the bagel from turning soggy if you pack it to go."},
        {"t": "Finish", "d": "Scatter with capers, extra dill and black pepper, and serve with lemon wedges."}
    ],
    "tips": [
        "Scoop out a little of the soft bagel center for an even lighter base.",
        "Smoked salmon is salty, so taste before adding capers.",
        "The spread keeps for 4 days, so make a double batch.",
        "Small-portion tip: one half is a full small plate. Cut it into quarters to eat slowly."
    ],
    "storage": "Best assembled fresh. Refrigerate the spread for up to 4 days and opened smoked salmon according to the package, usually 3 to 5 days.",
    "variations": [
        ["Egg", "Add a sliced hard-boiled egg for about 6 g more protein."],
        ["Avocado", "Swap the cucumber for thin slices of avocado."],
        ["Gluten-free", "Use a gluten-free bagel or a slice of gluten-free toast."],
        ["Make it gentler", "Skip the capers and pepper, use a plain bagel and choose a mild, lightly smoked salmon."],
        ["Protein boost", "Use 2 ounces of salmon per half instead of 1.5."]
    ],
    "nutrition": {"calories": 227, "protein": 16, "carbs": 28, "fat": 5, "fiber": 1},
    "faq": [
        ["Is smoked salmon cooked?", "Cold-smoked salmon is cured, not cooked. If you have been advised to avoid it, use hot-smoked or canned salmon."],
        ["Can I make it the night before?", "Make the spread ahead, but assemble the bagels the same day so they stay crisp."],
        ["Which bagel works best?", "Any you like. Everything, sesame and plain are classic. Mini bagels make an even smaller portion."]
    ],
    "note": "This is the weekend brunch plate made small enough for a weekday. One half, a cup of tea, done.",
    "diet": [],
}
NEW['cottage-cheese-scrambled-eggs'] = {
    "title": "Cottage Cheese Scrambled Eggs",
    "subtitle": "Soft, creamy scrambled eggs with cottage cheese stirred in, served with a slice of toast, a little avocado and greens. About 24 g protein per plate.",
    "category": "Beyond Toast",
    "tags": ["quick", "high-protein", "small-plates", "gentle"],
    "prep": 5, "cook": 5, "time": 10, "serves": 2, "level": "Easy",
    "desc": "The creamiest eggs, with extra protein.",
    "intro": [
        "Cottage cheese is the quiet trick behind some of the creamiest scrambled eggs you can make. It melts into the eggs as they cook, adding about 6 g of protein per plate and a soft, custardy texture without any cream.",
        "Low heat matters more than anything here. Eggs cooked slowly stay tender and moist, which makes them easier to eat on days when chewing feels like effort."
    ],
    "why": [
        ["About 24 g protein per plate", "Eggs and cottage cheese together."],
        ["Soft and easy to eat", "Low heat keeps the curds tender."],
        ["Ten minutes", "Faster than waiting for delivery."]
    ],
    "ingredients": [
        {"group": "For the eggs", "items": [
            {"q": 4, "u": "", "n": "large eggs"},
            {"q": 0.5, "u": "cup", "n": "low-fat cottage cheese", "g": 113},
            {"q": 1, "u": "tsp", "n": "butter"},
            {"q": N, "u": "", "n": "salt, black pepper and chopped chives", "note": "to taste"}
        ]},
        {"group": "To serve", "items": [
            {"q": 2, "u": "", "n": "slices whole-grain bread", "note": "toasted"},
            {"q": 0.25, "u": "", "n": "ripe avocado", "note": "sliced"},
            {"q": 1, "u": "cup", "n": "salad greens"}
        ]}
    ],
    "steps": [
        {"t": "Whisk", "d": "Whisk the eggs with a pinch of salt until no streaks of white remain. Stir in the cottage cheese."},
        {"t": "Cook low and slow", "d": "Melt the butter in a nonstick skillet over medium-low heat. Add the eggs and let them sit for 20 seconds, then push them gently across the pan with a spatula, forming large soft curds.",
         "tip": "If the eggs start to set too fast, lift the pan off the heat for a few seconds."},
        {"t": "Stop early", "d": "When the eggs are mostly set but still glossy, about 2 to 3 minutes, take the pan off the heat. They finish cooking from the warmth of the pan."},
        {"t": "Plate", "d": "Serve the eggs with toast, sliced avocado and greens. Finish with black pepper and chives."}
    ],
    "tips": [
        "Small-curd cottage cheese melts in most smoothly.",
        "Salt the eggs before cooking; cottage cheese is already salty, so go lightly.",
        "A nonstick pan makes low-heat scrambling much easier.",
        "Small-portion tip: start with the eggs and add the toast only if you still want it."
    ],
    "storage": "Best eaten fresh. Leftovers keep for 1 day in the fridge; reheat gently in the microwave in 15-second bursts.",
    "variations": [
        ["Spinach", "Wilt a handful of spinach in the pan before adding the eggs."],
        ["Herby", "Stir in chopped dill or parsley at the end."],
        ["Gluten-free", "Serve with gluten-free toast or roasted potatoes."],
        ["Make it gentler", "Skip the pepper and chives, cook the eggs very soft and serve them without the toast."],
        ["Protein boost", "Add one more egg, or top with a spoonful of extra cottage cheese."]
    ],
    "nutrition": {"calories": 340, "protein": 24, "carbs": 21, "fat": 18, "fiber": 4},
    "faq": [
        ["Will I see the cottage cheese?", "A few soft curds, but it mostly melts into the eggs."],
        ["Can I blend the cottage cheese first?", "Yes. Blending it with the eggs gives an even smoother scramble."],
        ["Can I make it for one?", "Yes. Halve everything and use a small pan."]
    ],
    "note": "Soft eggs are one of the gentlest breakfasts there is. The cottage cheese just makes them work a little harder for you.",
    "diet": ["vegetarian"],
}
NEW['berry-greek-yogurt-muffins'] = {
    "title": "Berry Greek Yogurt Muffins",
    "subtitle": "Soft, small berry muffins made with Greek yogurt and a scoop of vanilla protein powder. About 7 g protein each, and they freeze well.",
    "category": "Beyond Toast",
    "tags": ["small-plates", "make-ahead"],
    "prep": 15, "cook": 20, "time": 35, "serves": 12, "servesLabel": "muffins", "level": "Easy",
    "desc": "A small, soft muffin with a little extra protein.",
    "intro": [
        "Bakery muffins are often the size of a small cake. These are regular-size, soft and lightly sweet, and Greek yogurt plus a little vanilla protein powder gives each one about 7 g of protein.",
        "They are made for the freezer. Bake a batch, freeze them individually, and warm one for 20 seconds when you want something small with a cup of coffee."
    ],
    "why": [
        ["About 7 g protein per muffin", "Greek yogurt, eggs and protein powder."],
        ["Freezer-friendly", "Warm one at a time from frozen."],
        ["Soft and mild", "Easy to eat in a few small bites."]
    ],
    "ingredients": [
        {"group": "Dry ingredients", "items": [
            {"q": 1, "u": "cup", "n": "all-purpose flour", "g": 125},
            {"q": 0.5, "u": "cup", "n": "vanilla protein powder", "note": "whey or a whey blend", "g": 45},
            {"q": 1.5, "u": "tsp", "n": "baking powder"},
            {"q": 0.5, "u": "tsp", "n": "baking soda"},
            {"q": 0.25, "u": "tsp", "n": "salt"}
        ]},
        {"group": "Wet ingredients", "items": [
            {"q": 1, "u": "cup", "n": "plain nonfat Greek yogurt", "g": 227},
            {"q": 2, "u": "", "n": "large eggs"},
            {"q": 0.33, "u": "cup", "n": "maple syrup", "g": 107},
            {"q": 3, "u": "tbsp", "n": "neutral oil", "g": 40},
            {"q": 0.25, "u": "cup", "n": "milk"},
            {"q": 1, "u": "tsp", "n": "vanilla extract"},
            {"q": 1.25, "u": "cups", "n": "mixed berries", "note": "raspberries and blueberries, fresh or frozen"}
        ]}
    ],
    "steps": [
        {"t": "Heat the oven", "d": "Heat the oven to 375°F (190°C). Line or grease a 12-cup muffin tin."},
        {"t": "Mix the dry ingredients", "d": "Whisk the flour, protein powder, baking powder, baking soda and salt in a large bowl."},
        {"t": "Mix the wet ingredients", "d": "In another bowl, whisk the yogurt, eggs, maple syrup, oil, milk and vanilla until smooth."},
        {"t": "Combine gently", "d": "Pour the wet ingredients into the dry and fold with a spatula until just combined. Fold in the berries.",
         "tip": "Stop as soon as no dry flour remains. Overmixing makes protein muffins tough."},
        {"t": "Bake", "d": "Divide the batter among the cups and bake for 18 to 20 minutes, until the tops spring back and a toothpick comes out clean. Cool in the tin for 5 minutes, then on a rack."}
    ],
    "tips": [
        "If using frozen berries, add them straight from the freezer so they do not bleed into the batter.",
        "Protein powders vary a lot. If your batter is very thick, add another tablespoon of milk.",
        "Check them at 17 minutes; protein muffins can dry out if overbaked.",
        "Small-portion tip: half a muffin with a glass of milk makes a small, balanced snack."
    ],
    "storage": "Keep at room temperature for 1 day, in the fridge for up to 4 days, or freeze individually for up to 3 months. Warm from frozen in the microwave for 20 to 30 seconds.",
    "variations": [
        ["Lemon", "Add the zest of one lemon to the wet ingredients."],
        ["No protein powder", "Use 1 1/2 cups flour in total. Each muffin will have about 5 g protein."],
        ["Banana", "Replace the maple syrup with 1/2 cup mashed ripe banana and add 1 tablespoon sugar."],
        ["Make it gentler", "Use blueberries only and skip any crunchy topping. Serve slightly warm."],
        ["Protein boost", "Serve with a spoonful of Greek yogurt or a glass of milk."]
    ],
    "nutrition": {"calories": 139, "protein": 7, "carbs": 17, "fat": 4, "fiber": 1},
    "faq": [
        ["Can I use plant-based protein powder?", "Yes, but it absorbs more liquid. Add milk a tablespoon at a time until the batter is thick but scoopable."],
        ["Why are my muffins dry?", "Usually overbaking or overmixing. Pull them as soon as a toothpick comes out clean."],
        ["Can I make mini muffins?", "Yes. Bake in a mini tin for 10 to 12 minutes."]
    ],
    "note": "A muffin is often the only thing that sounds good with morning coffee. These are smaller, softer and do a little more for you.",
    "diet": ["vegetarian"],
}
NEW['strawberry-cottage-cheese-bowl'] = {
    "title": "Strawberry Cottage Cheese Bowl",
    "subtitle": "Creamy cottage cheese with fresh strawberries, a drizzle of honey and a few toasted almonds. About 26 g protein in five minutes.",
    "category": "Beyond Toast",
    "tags": ["quick", "healthy", "high-protein", "small-plates", "gentle"],
    "prep": 5, "cook": 0, "time": 5, "serves": 2, "level": "Easy",
    "desc": "Five minutes, 26 g of protein.",
    "intro": [
        "Some breakfasts are barely a recipe, and this is one of them. A cup of cottage cheese, a handful of ripe strawberries and a drizzle of honey add up to about 26 g of protein with no cooking at all.",
        "Cottage cheese has had a comeback for good reason: it is mild, cool and soft, which makes it easy to eat on low-appetite days. The berries add sweetness, and a few almonds add a little crunch."
    ],
    "why": [
        ["About 26 g protein per bowl", "Almost all of it from cottage cheese."],
        ["Five minutes, no cooking", "Spoon, slice, drizzle."],
        ["Cool and soft", "A gentle choice when warm food does not appeal."]
    ],
    "ingredients": [
        {"group": "For the bowls", "items": [
            {"q": 2, "u": "cups", "n": "2% cottage cheese", "g": 452},
            {"q": 2, "u": "cups", "n": "strawberries", "note": "hulled and sliced"},
            {"q": 2, "u": "tsp", "n": "honey"},
            {"q": 2, "u": "tbsp", "n": "sliced almonds", "note": "toasted"},
            {"q": N, "u": "", "n": "fresh mint", "note": "optional"}
        ]}
    ],
    "steps": [
        {"t": "Toast the almonds", "d": "Toast the almonds in a dry skillet over medium heat for 2 to 3 minutes, stirring, until golden. Let them cool.",
         "tip": "Toast a whole bag at once and keep it in a jar for the week."},
        {"t": "Slice the berries", "d": "Slice the strawberries. If they are not very sweet, toss them with half the honey and let them sit for 5 minutes."},
        {"t": "Build the bowls", "d": "Divide the cottage cheese between two bowls or plates. Top with the strawberries, drizzle with the remaining honey and scatter over the almonds and mint."}
    ],
    "tips": [
        "Whipped cottage cheese, blended for 30 seconds, gives a smoother, yogurt-like texture.",
        "Ripe, in-season strawberries need little or no honey.",
        "Frozen strawberries, thawed, release juice that makes a nice quick sauce.",
        "Small-portion tip: start with half a cup of cottage cheese and add more if you want it."
    ],
    "storage": "Best fresh. Sliced strawberries keep for 2 days in the fridge; assemble the bowls when you are ready to eat.",
    "variations": [
        ["Peach", "Use sliced peaches and a pinch of cinnamon."],
        ["Savory", "Skip the fruit and honey; top with cherry tomatoes, cucumber, olive oil and pepper."],
        ["Nut-free", "Use toasted pumpkin seeds or granola instead of almonds."],
        ["Make it gentler", "Blend the cottage cheese smooth, skip the almonds and use very ripe, soft berries."],
        ["Protein boost", "Stir in 2 tablespoons of hemp seeds or add a spoonful of Greek yogurt."]
    ],
    "nutrition": {"calories": 295, "protein": 26, "carbs": 29, "fat": 9, "fiber": 4},
    "faq": [
        ["I do not like the texture of cottage cheese. Any tips?", "Blend it for 30 seconds. It turns completely smooth, like thick yogurt."],
        ["Which cottage cheese is best?", "Small-curd 2% is creamy and mild. Check labels, since sodium and protein vary between brands."],
        ["Is it gluten-free?", "Yes, as written."]
    ],
    "note": "On mornings when cooking feels like too much, this is the five-minute answer. Spoon it onto a plate and you are done.",
    "diet": ["vegetarian", "gluten-free"],
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
for rid, b in out.items():
    open(os.path.join(IMG, f'{rid}.webp'), 'wb').write(b['webp'])
    open(os.path.join(IMG, 'og', f'{rid}.jpg'), 'wb').write(b['og'])
    open(os.path.join(IMG, 'pins', f'{rid}.jpg'), 'wb').write(b['pin'])
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

# ------------------------------------------------------------------ build.py focus list (adds the Starter Kit box)
b = open(P('build.py'), encoding='utf-8').read()
m = re.search(r'FOCUS_IDS = (\[.*?\])', b)
if not m:
    print('ERROR: FOCUS_IDS not found in build.py.')
    sys.exit(1)
focus = json.loads(m.group(1))
for rid in NEW:
    if rid not in focus:
        focus.append(rid)
b = b[:m.start(1)] + json.dumps(focus) + b[m.end(1):]
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
print(f'OK: 5 breakfasts added. The site now has {len(recipes)} recipes.')
