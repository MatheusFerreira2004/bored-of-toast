#!/usr/bin/env python3
"""New recipes 2/3: replace three more off-focus recipes.

  buttermilk-pancakes    -> cottage-cheese-pancakes
  cinnamon-french-toast  -> spinach-feta-mini-frittata
  harvest-kale-salad     -> tuna-white-bean-salad

Same approach as update_013: small-plates format, new Pexels photos (free license, no AI) with credits,
recipe image + Open Graph image + Pinterest pin generated here, old URLs become redirect stubs
(listed in _src/redirects.json), old photos, step photos and credits removed.

Photo check (done by reading the Pexels photo pages before choosing):
  cottage-cheese-pancakes    38917193  "Delicious homemade cheese pancakes on a plate" (Natalia Sevruk)
  spinach-feta-mini-frittata 5639282   "Homemade frittata in a skillet, garnished with fresh spinach and cheese" (Shameel mukkath)
  tuna-white-bean-salad      19572489  "Top view of a fresh tuna salad with vibrant vegetables and a fork" (Tugba Ozturk)
The first version of this lote used an egg-bites photo that did not show egg bites; no free Pexels photo of
egg bites was found, so the recipe became a small oven frittata, which has real photos.

Nutrition per serving is an ESTIMATE from USDA FoodData Central reference values and typical labels
(rounded; double-check before relying on them):
  Cottage cheese pancakes (4 servings of 2 small pancakes): 2% cottage cheese 226 g 183 kcal/23.7 P;
    eggs 150 g 215/18.9 P/14.3 F; oats 45 g 171/6 P/30 C; maple 20 g 52; butter 5 g 36;
    berries 150 g 75/1 P; nonfat Greek yogurt 120 g 71/12.2 P
    -> 803 kcal, 62 P, 75 C, 27 F, 8 fiber / 4 = ~200 kcal, 15 P, 19 C, 7 F, 2 fiber
  Spinach feta mini frittata (6 wedges): eggs 400 g 572/50.4 P/38 F; egg whites 120 g 62/13 P;
    2% cottage cheese 113 g 92/11.9 P; spinach 140 g 32/4 P; feta 50 g 132/7.1 P/10.6 F;
    red pepper 60 g 19; green onions 10; oil 4.5 g 40
    -> 959 kcal, 88 P, 21 C, 57 F, 5 fiber / 6 = ~160 kcal, 15 P, 3 C, 9 F, 1 fiber
  Tuna white bean salad (3 servings): light tuna in water, drained 226 g 262/57.6 P; cannellini 250 g
    223/16.8 P/39 C/11.5 fiber; tomatoes 150 g 27; cucumber 150 g 23; red onion 8; parsley 5;
    extra-virgin olive oil 20 g 177; lemon 7; dijon 5; arugula 60 g 15/1.5 P
    -> 752 kcal, 79 P, 58 C, 23 F, 16 fiber / 3 = ~250 kcal, 26 P, 19 C, 8 F, 5 fiber

Nothing in recipes.json changes unless every download succeeds. Safe to re-run.
"""
import glob, io, json, os, re, subprocess, sys, urllib.request

# Send errors and tracebacks to stdout so they show up in the Auto build summary.
sys.stderr = sys.stdout

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
IMG = os.path.join(ROOT, 'images')
P = lambda n: os.path.join(HERE, n)

OLD_TO_NEW = {
    'buttermilk-pancakes': 'cottage-cheese-pancakes',
    'cinnamon-french-toast': 'spinach-feta-mini-frittata',
    'harvest-kale-salad': 'tuna-white-bean-salad',
}
EXTRA_OLD_IMAGES = ['step-pancakes-batter', 'step-pancakes-flip']

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

PHOTOS = {
    'cottage-cheese-pancakes': {
        'id': 38917193, 'photographer': 'Natalia Sevruk', 'photographer_url': 'https://www.pexels.com/@natalia-sevruk-636238602/',
        'photo_url': 'https://www.pexels.com/photo/delicious-homemade-cheese-pancakes-on-a-plate-38917193/',
        'alt': 'Golden brown cottage cheese pancakes on a decorative plate.'},
    'spinach-feta-mini-frittata': {
        'id': 5639282, 'photographer': 'Shameel mukkath', 'photographer_url': 'https://www.pexels.com/@shameel-mukkath-3421394/',
        'photo_url': 'https://www.pexels.com/photo/scrambled-eggs-with-green-onions-on-black-skillet-pan-5639282/',
        'alt': 'A spinach and cheese frittata in a cast iron skillet.'},
    'tuna-white-bean-salad': {
        'id': 19572489, 'photographer': 'Tuğba ÖZTÜRK', 'photographer_url': 'https://www.pexels.com/@tugba-ozturk-368300535/',
        'photo_url': 'https://www.pexels.com/photo/bowl-of-salad-and-fork-near-19572489/',
        'alt': 'Top view of a tuna salad with fresh vegetables and a fork.'},
}

NEW = {}
NEW['cottage-cheese-pancakes'] = {
    "title": "Cottage Cheese Pancakes",
    "subtitle": "Soft, small pancakes blended from cottage cheese, eggs and oats, served with berries and a spoonful of Greek yogurt. About 15 g protein per serving.",
    "category": "Beyond Toast",
    "tags": ["quick", "healthy", "high-protein", "small-plates", "gentle"],
    "prep": 10, "cook": 15, "time": 25, "serves": 4, "level": "Easy",
    "desc": "Blender pancakes with cottage cheese and oats.",
    "intro": [
        "These are not tall diner pancakes. They are small, soft and tender, made by blending cottage cheese, eggs and rolled oats into a smooth batter. Two pancakes with berries and a spoonful of Greek yogurt make a small breakfast with about 15 g of protein.",
        "Blending matters here. It turns the oats into flour and the cottage cheese curds into a creamy base, so the pancakes cook up custardy rather than lumpy. Because the batter is mostly eggs and cheese, it browns faster than a flour batter, so medium-low heat and a little patience give the best results."
    ],
    "why": [
        ["About 15 g protein per serving", "Cottage cheese, eggs and a spoonful of Greek yogurt."],
        ["One blender, no flour", "Oats blend into the batter, so there is no separate mixing bowl."],
        ["Small and soft", "Little pancakes are easy to eat a few bites at a time."]
    ],
    "ingredients": [
        {"group": "For the batter", "items": [
            {"q": 1, "u": "cup", "n": "low-fat cottage cheese", "note": "226 g", "g": 226},
            {"q": 3, "u": "", "n": "large eggs"},
            {"q": 0.5, "u": "cup", "n": "old-fashioned rolled oats", "note": "use certified gluten-free oats if needed", "g": 45},
            {"q": 1, "u": "tbsp", "n": "maple syrup"},
            {"q": 1, "u": "tsp", "n": "baking powder"},
            {"q": 0.5, "u": "tsp", "n": "vanilla extract"},
            {"q": 1, "u": "pinch", "n": "fine salt"},
            {"q": 1, "u": "tsp", "n": "butter or neutral oil", "note": "for the pan"}
        ]},
        {"group": "To serve", "items": [
            {"q": 1, "u": "cup", "n": "fresh berries", "g": 150},
            {"q": 0.5, "u": "cup", "n": "plain nonfat Greek yogurt", "g": 120}
        ]}
    ],
    "steps": [
        {"t": "Blend the batter", "d": "Add the cottage cheese, eggs, oats, maple syrup, baking powder, vanilla and salt to a blender. Blend for about 30 seconds, until completely smooth. Let the batter rest for 5 minutes so the oats can thicken it slightly.",
         "tip": "If the batter looks very thick after resting, blend in a tablespoon of milk."},
        {"t": "Heat the pan", "d": "Heat a nonstick skillet over medium-low heat and brush it lightly with butter or oil."},
        {"t": "Cook small pancakes", "d": "Pour 2 to 3 tablespoons of batter per pancake, leaving space between them. Cook for 2 to 3 minutes, until the edges look set and a few bubbles appear on top, then flip and cook 1 to 2 minutes more.",
         "tip": "These brown faster than flour pancakes. If they darken before the middle sets, turn the heat down a little."},
        {"t": "Keep warm", "d": "Move the cooked pancakes to a plate and cover loosely with a clean towel while you cook the rest. The batter makes about 8 small pancakes."},
        {"t": "Serve", "d": "Serve two pancakes per plate with a spoonful of Greek yogurt and a handful of berries."}
    ],
    "tips": [
        "Small pancakes are easier to flip. Keep each one to about 3 inches across.",
        "Full-fat or low-fat cottage cheese both work. Small-curd blends a little smoother.",
        "Blend the batter right before cooking. It thickens as it stands.",
        "Small-portion tip: start with one pancake and a spoonful of yogurt. A second one can wait."
    ],
    "storage": "Cool leftover pancakes completely, then refrigerate in an airtight container for up to 3 days or freeze with parchment between them for up to 2 months. Reheat in a toaster or in a dry skillet over low heat.",
    "variations": [
        ["Banana", "Blend half a ripe banana into the batter and skip the maple syrup."],
        ["Blueberry", "Drop a few blueberries onto each pancake right after pouring the batter."],
        ["Cinnamon", "Add 1/2 teaspoon ground cinnamon to the blender."],
        ["Make it gentler", "Skip the berries and serve with plain yogurt and a drizzle of maple syrup. Eat them warm, not hot."],
        ["Protein boost", "Blend 1 scoop of vanilla protein powder into the batter with 2 extra tablespoons of milk."]
    ],
    "nutrition": {"calories": 200, "protein": 15, "carbs": 19, "fat": 7, "fiber": 2},
    "faq": [
        ["Can I taste the cottage cheese?", "Not really. Once blended and cooked it tastes mild and slightly tangy, a bit like a soft cheese pancake."],
        ["Can I use flour instead of oats?", "Yes. Use 1/3 cup all-purpose flour instead of the oats. The pancakes will be a little lighter."],
        ["Are they gluten-free?", "They can be, if you use oats labeled certified gluten-free and a gluten-free baking powder."]
    ],
    "note": "Make the whole batch even if you only want one or two. Leftovers freeze well and reheat in the toaster in a couple of minutes, which is useful on mornings when cooking feels like too much.",
    "diet": ["vegetarian"],
}
NEW['spinach-feta-mini-frittata'] = {
    "title": "Spinach & Feta Mini Frittata",
    "subtitle": "A small oven frittata with spinach, feta and a little cottage cheese for a soft, custardy texture. Cut it into six wedges and reheat one or two at a time.",
    "category": "Beyond Toast",
    "tags": ["healthy", "high-protein", "small-plates", "make-ahead"],
    "prep": 15, "cook": 30, "time": 45, "serves": 6, "level": "Easy",
    "desc": "Six make-ahead wedges from one small pan.",
    "intro": [
        "A frittata is one of the easiest make-ahead breakfasts there is: one small pan in the oven gives you six wedges for the week, and a warm, high-protein small plate is about a minute away. Each wedge has about 15 g of protein.",
        "A little blended cottage cheese is what keeps it soft and custardy instead of rubbery. Squeezing the thawed spinach very dry keeps the frittata from turning watery, and a moderate oven lets the eggs set gently all the way to the center."
    ],
    "why": [
        ["About 15 g protein per wedge", "Eggs, egg whites, cottage cheese and feta."],
        ["Made once, eaten all week", "Keeps in the fridge for 4 days and in the freezer for 2 months."],
        ["Ready in a minute", "Reheat a wedge in the microwave for a fast breakfast."]
    ],
    "ingredients": [
        {"group": "For the frittata", "items": [
            {"q": 8, "u": "", "n": "large eggs"},
            {"q": 0.5, "u": "cup", "n": "liquid egg whites", "g": 120},
            {"q": 0.5, "u": "cup", "n": "low-fat cottage cheese", "g": 113},
            {"q": 5, "u": "oz", "n": "frozen chopped spinach", "note": "thawed and squeezed very dry", "g": 140},
            {"q": 0.33, "u": "cup", "n": "crumbled feta", "g": 50},
            {"q": 0.5, "u": "", "n": "small red bell pepper", "note": "finely diced"},
            {"q": 2, "u": "", "n": "green onions", "note": "thinly sliced"},
            {"q": 0.25, "u": "tsp", "n": "kosher salt"},
            {"q": 0.25, "u": "tsp", "n": "black pepper"},
            {"q": None, "u": "", "n": "olive oil spray", "note": "for the pan"}
        ]}
    ],
    "steps": [
        {"t": "Heat the oven", "d": "Heat the oven to 350°F (175°C). Spray a 9-inch oven-safe skillet or pie dish generously with oil."},
        {"t": "Blend the base", "d": "Blend the eggs, egg whites, cottage cheese, salt and pepper for about 20 seconds, until smooth and slightly frothy.",
         "tip": "No blender? Whisk well instead. The frittata will be a little less smooth but still good."},
        {"t": "Add the fillings", "d": "Scatter the spinach, feta, bell pepper and green onions evenly over the bottom of the pan. Pour the egg mixture over the top."},
        {"t": "Bake gently", "d": "Bake for 25 to 30 minutes, until the edges are lightly golden and the center is just set, with only a slight wobble when you nudge the pan.",
         "tip": "Take it out when the center barely wobbles. It finishes setting as it cools and stays softer."},
        {"t": "Rest and cut", "d": "Let the frittata rest for 10 minutes, then cut it into 6 wedges. Serve one or two per plate, or cool completely for storage."}
    ],
    "tips": [
        "Squeeze the spinach in a clean towel until no more water comes out. Wet spinach makes a watery frittata.",
        "A cast iron or nonstick oven-safe skillet releases the wedges most easily.",
        "Swap in any finely chopped cooked vegetable, as long as it is not watery.",
        "Small-portion tip: one wedge with a piece of fruit is a complete small breakfast on low-appetite days."
    ],
    "storage": "Refrigerate cooled wedges in an airtight container for up to 4 days. To freeze, wrap each wedge and keep in a freezer bag for up to 2 months. Reheat a wedge in the microwave for 45 to 60 seconds from the fridge, or about 90 seconds from frozen.",
    "variations": [
        ["Sun-dried tomato", "Replace the bell pepper with 2 tablespoons chopped sun-dried tomatoes."],
        ["Ham and cheddar", "Swap the feta for cheddar and add 1/2 cup diced lean ham."],
        ["Dairy-free", "Skip the cottage cheese and feta and add 2 extra egg whites. The frittata will be firmer."],
        ["Make it gentler", "Leave out the green onions and pepper and use a mild cheese. Eat it warm rather than hot."],
        ["Protein boost", "Serve with a small cup of Greek yogurt or a glass of milk."]
    ],
    "nutrition": {"calories": 160, "protein": 15, "carbs": 3, "fat": 9, "fiber": 1},
    "faq": [
        ["Why is my frittata watery?", "Usually the spinach was not squeezed dry enough. Wring it out in a towel until no more liquid comes out."],
        ["Can I use fresh spinach?", "Yes. Wilt about 5 cups of fresh spinach in a dry pan, cool it, then squeeze it dry and chop it."],
        ["Can I make egg bites instead?", "Yes. Divide the fillings and egg mixture among a greased 12-cup muffin pan and bake at 325°F (165°C) for 22 to 25 minutes. Two bites make a serving."],
        ["Is it gluten-free?", "Yes, as written. Check your feta label if you are very sensitive."]
    ],
    "note": "One wedge, a minute in the microwave, done. This is the recipe to make on a day you have energy, so the days you do not still start with something warm.",
    "diet": ["vegetarian", "gluten-free"],
}
NEW['tuna-white-bean-salad'] = {
    "title": "Tuna & White Bean Salad",
    "subtitle": "Canned tuna and cannellini beans tossed with tomatoes, cucumber, parsley and a lemon dressing. No cooking, about 26 g protein per serving.",
    "category": "Salads",
    "tags": ["quick", "healthy", "high-protein", "small-plates", "make-ahead"],
    "prep": 15, "cook": 0, "time": 15, "serves": 3, "level": "Easy",
    "desc": "No-cook tuna and beans with a lemon dressing.",
    "intro": [
        "This is a pantry salad: two cans of tuna and one can of white beans, brightened with lemon, parsley and a few crunchy vegetables. There is no stove involved, and each small bowl has about 26 g of protein.",
        "The dressing goes on the beans first. Letting them sit in the lemon and olive oil for a few minutes helps them absorb flavor, so the salad tastes seasoned all the way through instead of just on the surface. The tuna goes in last, folded gently so it stays in flakes."
    ],
    "why": [
        ["About 26 g protein per bowl", "Tuna and cannellini beans do most of the work."],
        ["No cooking", "Open the cans, chop a few vegetables and toss."],
        ["Good the next day", "Keeps well in the fridge for packed lunches."]
    ],
    "ingredients": [
        {"group": "For the dressing", "items": [
            {"q": 1.5, "u": "tbsp", "n": "extra-virgin olive oil"},
            {"q": 2, "u": "tbsp", "n": "fresh lemon juice"},
            {"q": 1, "u": "tsp", "n": "Dijon mustard"},
            {"q": 0.25, "u": "tsp", "n": "kosher salt"},
            {"q": None, "u": "", "n": "black pepper", "note": "to taste"}
        ]},
        {"group": "For the salad", "items": [
            {"q": 15, "u": "oz", "n": "cannellini beans", "note": "1 can, rinsed and drained"},
            {"q": 2, "u": "", "n": "cans light tuna in water", "note": "5 oz each, drained"},
            {"q": 1, "u": "cup", "n": "cherry tomatoes", "note": "halved", "g": 150},
            {"q": 0.5, "u": "", "n": "English cucumber", "note": "diced"},
            {"q": 2, "u": "tbsp", "n": "red onion", "note": "finely chopped, optional"},
            {"q": 0.25, "u": "cup", "n": "fresh parsley", "note": "chopped"},
            {"q": 3, "u": "cups", "n": "arugula or mixed greens", "note": "to serve"}
        ]}
    ],
    "steps": [
        {"t": "Make the dressing", "d": "In a large bowl, whisk the olive oil, lemon juice, Dijon, salt and a few grinds of pepper."},
        {"t": "Dress the beans", "d": "Add the rinsed beans to the bowl and toss to coat. Let them sit for 5 minutes while you prepare the vegetables.",
         "tip": "Dressing the beans first gives them time to absorb the lemon, which seasons the whole salad."},
        {"t": "Add the vegetables", "d": "Add the tomatoes, cucumber, red onion if using and parsley, and toss gently."},
        {"t": "Fold in the tuna", "d": "Break the tuna into large flakes and fold it in gently. Taste and add more lemon, salt or pepper if needed."},
        {"t": "Serve", "d": "Divide the greens among three small bowls and spoon the salad over the top."}
    ],
    "tips": [
        "Light tuna in water keeps the salad lighter; tuna packed in olive oil is richer and you can reduce the dressing oil.",
        "Rinse canned beans well to remove the starchy liquid and some of the salt.",
        "Keep the greens separate until serving if you are packing it for later.",
        "Small-portion tip: serve a half bowl on a few crackers or a slice of toast. The rest keeps for tomorrow."
    ],
    "storage": "Refrigerate the salad, without the greens, in an airtight container for up to 3 days. Stir and add a squeeze of lemon before serving.",
    "variations": [
        ["Chickpeas", "Use chickpeas instead of cannellini beans."],
        ["Salmon", "Swap the tuna for canned salmon, flaked and with skin and bones removed if you prefer."],
        ["Vegetarian", "Skip the tuna, use two cans of beans and add crumbled feta (no longer dairy-free)."],
        ["Make it gentler", "Leave out the red onion and Dijon and serve it cool rather than cold."],
        ["Protein boost", "Add a chopped hard-boiled egg to each bowl."]
    ],
    "nutrition": {"calories": 250, "protein": 26, "carbs": 19, "fat": 8, "fiber": 5},
    "faq": [
        ["Which tuna should I use?", "Light tuna in water, drained, is what the nutrition estimate is based on. Brands vary, so check the label."],
        ["Can I make it ahead?", "Yes. It keeps for 3 days in the fridge. Add the greens just before serving."],
        ["Is it gluten-free?", "Yes, as written. Check your mustard label if you are very sensitive."]
    ],
    "note": "This is the salad for days when turning on the stove sounds like too much. Everything comes from a can or the crisper drawer, and a small bowl still covers a good share of the day's protein.",
    "diet": ["gluten-free", "dairy-free"],
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
print(f'- removed {removed} old image files')
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

# ------------------------------------------------------------------ build.py (focus list and NEW_IDS)
b = open(P('build.py'), encoding='utf-8').read()
if 'RECIPE_REDIRECTS' not in b:
    print('ERROR: build.py has no recipe redirect support (run update_013 first).')
    sys.exit(1)
m = re.search(r'FOCUS_IDS = (\[.*?\])', b)
focus = json.loads(m.group(1))
for rid in NEW:
    if rid not in focus:
        focus.append(rid)
b = b[:m.start(1)] + json.dumps(focus) + b[m.end(1):]
m = re.search(r"NEW_IDS = (\[[^\n]*\])", b)
if m:
    new_ids = [OLD_TO_NEW.get(x, x) for x in json.loads(m.group(1).replace("'", '"'))]
    b = b[:m.start(1)] + json.dumps(new_ids) + b[m.end(1):]
open(P('build.py'), 'w', encoding='utf-8').write(b)

# ------------------------------------------------------------------ recipes.json (last)
for i, r in enumerate(recipes):
    if r['id'] in OLD_TO_NEW:
        rid = OLD_TO_NEW[r['id']]
        new = {'id': rid}
        new.update(NEW[rid])
        new['img'] = f'images/{rid}.webp'
        recipes[i] = new
        print(f"- {r['id']} -> {rid} ({new['title']}, ~{new['nutrition']['protein']} g protein, ~{new['nutrition']['calories']} kcal per serving)")
m = re.match(r'\[\s*\n([ \t]+)\{', raw)
with open(P('recipes.json'), 'w', encoding='utf-8') as f:
    json.dump(recipes, f, ensure_ascii=False, indent=len(m.group(1)) if m else None)
    f.write('\n')
print('OK: 2 breakfasts and 1 salad replaced, redirects added.')
