#!/usr/bin/env python3
"""New recipes 1/3: replace the three off-focus desserts.

  chocolate-chip-cookies -> peanut-butter-protein-bites
  chocolate-mousse-cake  -> chocolate-yogurt-mousse-cups
  apple-crisp            -> baked-cinnamon-apples

- New recipes in the small-plates format (smaller portions, protein estimates, gentler swaps).
- New photos from Pexels (free license, no AI), credited on the site. Recipe image (4:3 WebP),
  Open Graph image (1200x630) and Pinterest pin (1000x1500 with title) are generated here.
- Old URLs become redirect stubs (recipes/<old>/ -> recipes/<new>/), listed in _src/redirects.json.
- Old photos, step photos and their credits are removed.
- build.py: recipe redirects, new recipes added to FOCUS_IDS, leftover "Fall" filter chip removed.
- checks.py: any "Redirecting…" stub is treated as a redirect page.

Nutrition per serving is an ESTIMATE from USDA FoodData Central reference values and typical labels
(rounded; double-check before relying on them):
  Protein bites (16): oats 90 g 341 kcal/11.9 P; peanut butter 128 g 753/32.0 P/64 F; protein powder 60 g
    240/48 P; honey 85 g 258; flax 14 g 75/2.6 P; dark chocolate chips 45 g 216/1.9 P; milk 45 g 23/1.5 P
    -> 1906 kcal, 98 P, 197 C, 93 F, 23 fiber / 16 = ~120 kcal, 6 P, 12 C, 6 F, 1 fiber per bite
  Mousse cups (4): nonfat Greek yogurt 480 g 283/49 P; cocoa 15 g 34/2.9 P; maple 60 g 156;
    70% chocolate 56 g 335/4.4 P/23.9 F; raspberries 60 g 31
    -> 839 kcal, 57 P, 99 C, 28 F, 16 fiber / 4 = ~210 kcal, 14 P, 25 C, 7 F, 4 fiber
  Baked apples (4): apples 600 g 312; butter 14 g 100; maple 20 g 52; oats 22 g 83/2.9 P;
    walnuts 15 g 98/2.3 P; dried cranberries 20 g 62; nonfat Greek yogurt 240 g 142/24.5 P
    -> 849 kcal, 32 P, 138 C, 25 F, 19 fiber / 4 = ~210 kcal, 8 P, 35 C, 6 F, 5 fiber

Nothing in recipes.json changes unless every download succeeds. Safe to re-run.
"""
import glob, io, json, os, re, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
IMG = os.path.join(ROOT, 'images')
P = lambda n: os.path.join(HERE, n)

OLD_TO_NEW = {
    'chocolate-chip-cookies': 'peanut-butter-protein-bites',
    'chocolate-mousse-cake': 'chocolate-yogurt-mousse-cups',
    'apple-crisp': 'baked-cinnamon-apples',
}
EXTRA_OLD_IMAGES = ['step-cookies-dough']

raw = open(P('recipes.json'), encoding='utf-8').read()
recipes = json.loads(raw)
ids = [r['id'] for r in recipes]
if all(n in ids for n in OLD_TO_NEW.values()) and not any(o in ids for o in OLD_TO_NEW):
    print('Already applied. Nothing to do.')
    sys.exit(0)
missing = [o for o in OLD_TO_NEW if o not in ids]
if missing:
    sys.exit(f'ERROR: old recipes not found: {missing}. Nothing was saved.')

PHOTOS = {
    'peanut-butter-protein-bites': {
        'id': 4637456, 'photographer': 'Milan', 'photographer_url': 'https://www.pexels.com/@milan-3053700',
        'photo_url': 'https://www.pexels.com/photo/brown-energy-balls-on-plate-for-dessert-4637456/',
        'alt': 'Homemade oat energy bites arranged on a textured glass plate.'},
    'chocolate-yogurt-mousse-cups': {
        'id': 6261275, 'photographer': 'Eva Bronzini', 'photographer_url': 'https://www.pexels.com/@eva-bronzini',
        'photo_url': 'https://www.pexels.com/photo/chocolate-mousse-in-tall-glass-6261275/',
        'alt': 'Chocolate mousse in a glass topped with fresh raspberries.'},
    'baked-cinnamon-apples': {
        'id': 6210957, 'photographer': 'Tim Douglas', 'photographer_url': 'https://www.pexels.com/@tim-douglas',
        'photo_url': 'https://www.pexels.com/photo/tasty-apples-with-assorted-filling-in-baking-pan-6210957/',
        'alt': 'Red apples filled with walnuts, cashews and dried cranberries in a baking dish.'},
}

NEW = {}
NEW['peanut-butter-protein-bites'] = {
    "title": "No-Bake Peanut Butter Protein Bites",
    "subtitle": "Oats, peanut butter, a scoop of protein powder and a few dark chocolate chips, rolled into small bites. About 6 g protein each, no oven needed.",
    "category": "Desserts",
    "tags": ["quick", "healthy", "small-plates", "make-ahead"],
    "prep": 15, "cook": 0, "chill": 30, "time": 45, "serves": 16, "servesLabel": "bites", "level": "Easy",
    "desc": "Small no-bake bites, about 6 g protein each.",
    "intro": [
        "Sometimes a small appetite still wants something sweet. These bites are built for that moment: one or two is a satisfying treat, and each one carries about 6 g of protein from peanut butter and a scoop of protein powder. There is no oven involved, and a batch keeps in the fridge all week.",
        "The texture depends on balance. Rolled oats and ground flaxseed absorb moisture from the peanut butter and honey, so the mixture firms up as it rests. Chilling it for 15 minutes before rolling makes it much less sticky, and a splash of milk fixes a mix that feels too dry, since protein powders vary a lot in how much liquid they soak up."
    ],
    "why": [
        ["About 6 g protein per bite", "Peanut butter and protein powder in a one- or two-bite treat."],
        ["No oven, one bowl", "Stir, chill and roll. Ready in about 45 minutes, most of it hands-off."],
        ["Portioned by design", "Sixteen small bites make it easy to stop at one or two."]
    ],
    "ingredients": [
        {"group": "For the bites", "items": [
            {"q": 1, "u": "cup", "n": "old-fashioned rolled oats", "note": "use certified gluten-free oats if needed", "g": 90},
            {"q": 0.5, "u": "cup", "n": "natural creamy peanut butter", "note": "stirred well", "g": 128},
            {"q": 0.5, "u": "cup", "n": "vanilla protein powder", "note": "whey or plant-based, about 2 scoops", "g": 60},
            {"q": 0.25, "u": "cup", "n": "honey", "note": "or maple syrup", "g": 85},
            {"q": 2, "u": "tbsp", "n": "ground flaxseed", "g": 14},
            {"q": 0.5, "u": "tsp", "n": "vanilla extract"},
            {"q": 1, "u": "pinch", "n": "fine salt"},
            {"q": 3, "u": "tbsp", "n": "milk", "note": "any kind, plus more as needed"}
        ]},
        {"group": "To finish", "items": [
            {"q": 0.25, "u": "cup", "n": "mini dark chocolate chips", "g": 45}
        ]}
    ],
    "steps": [
        {"t": "Stir the base", "d": "In a medium bowl, stir together the peanut butter, honey, vanilla and salt until smooth. If the peanut butter is very thick, warm it in the microwave for 10 to 15 seconds first.",
         "tip": "Use a drippy, natural-style peanut butter. Very stiff no-stir brands make a crumbly mix."},
        {"t": "Add the dry ingredients", "d": "Add the oats, protein powder and ground flaxseed and stir with a sturdy spoon until no dry pockets remain. Add the milk a tablespoon at a time until the mixture holds together when you squeeze a little in your hand. Fold in the chocolate chips.",
         "tip": "Protein powders absorb very different amounts of liquid. Go by feel: the mix should be sticky but not wet."},
        {"t": "Chill briefly", "d": "Cover the bowl and refrigerate for 15 minutes. The oats and flax absorb moisture and the mixture firms up, which makes rolling much easier."},
        {"t": "Roll into bites", "d": "Scoop level tablespoons of the mixture and roll them between your palms into 16 balls, about 1 inch across. Dampen your hands slightly if the mix sticks."},
        {"t": "Chill and serve", "d": "Arrange the bites on a plate or in a container and refrigerate for another 15 minutes, until firm. Serve cold, one or two at a time."}
    ],
    "tips": [
        "Weigh the protein powder if you can. Scoops vary, and 60 g is roughly two standard scoops.",
        "If the mix is too wet to roll, add a tablespoon of oats. If it cracks, add a teaspoon of milk.",
        "Mini chocolate chips spread through the bites more evenly than regular ones, so every bite gets some.",
        "Small-portion tip: start with one bite. Two bites with a glass of milk make a small snack with about 20 g protein."
    ],
    "storage": "Keep the bites in an airtight container in the fridge for up to 1 week, with parchment between layers. They also freeze well for up to 2 months; let them sit at room temperature for 10 minutes before eating.",
    "variations": [
        ["Nut-free", "Use sunflower seed butter instead of peanut butter and check that your protein powder and chocolate are made in a nut-free facility."],
        ["Chocolate peanut butter", "Replace 2 tablespoons of the oats with unsweetened cocoa powder and add a splash more milk."],
        ["Without protein powder", "Replace the protein powder with 1/2 cup more oats. The bites will have about 3 g protein each."],
        ["Make it gentler", "Skip the chocolate chips and roll the bites a little smaller. A mild, soft bite is easier on unsettled days."],
        ["Protein boost", "Eat two bites with a glass of milk or a small cup of Greek yogurt."]
    ],
    "nutrition": {"calories": 120, "protein": 6, "carbs": 12, "fat": 6, "fiber": 1},
    "faq": [
        ["Do I have to use protein powder?", "No. Swap it for 1/2 cup more oats. The bites will taste much the same but have about half the protein."],
        ["Why is my mixture too sticky to roll?", "It probably needs more time in the fridge, or a tablespoon more oats. Chilling helps the oats and flax absorb moisture."],
        ["Are these gluten-free?", "They can be, if you use oats labeled certified gluten-free and check your protein powder and chocolate labels."]
    ],
    "note": "These are meant to be small. One bite with a cup of tea is a perfectly good snack, and two with a glass of milk is close to a light meal on low-appetite days. Keep them in the fridge where you can see them; that is half the reason they get eaten.",
    "diet": ["vegetarian"],
}
NEW['chocolate-yogurt-mousse-cups'] = {
    "title": "Chocolate Greek Yogurt Mousse Cups",
    "subtitle": "Thick Greek yogurt whipped with cocoa and a little melted dark chocolate, chilled in small cups and topped with raspberries. About 14 g protein per cup.",
    "category": "Desserts",
    "tags": ["healthy", "small-plates", "gentle", "make-ahead"],
    "prep": 10, "cook": 5, "chill": 60, "time": 75, "serves": 4, "level": "Easy",
    "desc": "Cool, creamy chocolate cups with Greek yogurt.",
    "intro": [
        "A classic chocolate mousse is mostly cream, eggs and sugar. This version starts with thick Greek yogurt, so it is cool, smooth and spoonable like mousse, with about 14 g of protein in a small cup. A little melted dark chocolate gives it a deeper, richer flavor than cocoa alone.",
        "The trick is to combine the chocolate and yogurt gently. Cold yogurt can make melted chocolate seize into small flecks, so the chocolate is cooled slightly and whisked into a spoonful of yogurt first, then folded into the rest. A short chill sets the cups and lets the cocoa flavor bloom."
    ],
    "why": [
        ["About 14 g protein per cup", "Two cups of Greek yogurt shared across four small servings."],
        ["Cool and soft", "Easy to eat a few spoonfuls at a time on days when hot food does not appeal."],
        ["Ready in about an hour", "Ten minutes of work, then the fridge does the rest."]
    ],
    "ingredients": [
        {"group": "For the mousse", "items": [
            {"q": 2, "u": "cups", "n": "plain nonfat Greek yogurt", "note": "480 g, well chilled", "g": 480},
            {"q": 2, "u": "oz", "n": "dark chocolate", "note": "about 70% cocoa, chopped", "g": 56},
            {"q": 3, "u": "tbsp", "n": "unsweetened cocoa powder", "g": 15},
            {"q": 3, "u": "tbsp", "n": "maple syrup", "note": "or honey, adjust to taste", "g": 60},
            {"q": 0.5, "u": "tsp", "n": "vanilla extract"},
            {"q": 1, "u": "pinch", "n": "fine salt"}
        ]},
        {"group": "To serve", "items": [
            {"q": 0.5, "u": "cup", "n": "fresh raspberries", "g": 60}
        ]}
    ],
    "steps": [
        {"t": "Melt the chocolate", "d": "Put the chopped chocolate in a small heatproof bowl and microwave in 20-second bursts, stirring between each, until about three quarters melted. Stir until smooth, then let it cool for 5 minutes, until barely warm.",
         "tip": "Stopping before it is fully melted and stirring the rest smooth keeps the chocolate from overheating and turning grainy."},
        {"t": "Mix the cocoa base", "d": "In a medium bowl, whisk the cocoa powder, maple syrup, vanilla and salt into a thick paste. Whisking the cocoa with the syrup first prevents dry lumps in the mousse."},
        {"t": "Temper the chocolate", "d": "Whisk 2 heaped tablespoons of the yogurt into the melted chocolate until glossy. Scrape this mixture into the cocoa paste and whisk until smooth.",
         "tip": "Adding cold yogurt to warm chocolate a little at a time keeps it from seizing into flecks."},
        {"t": "Fold in the yogurt", "d": "Add the rest of the yogurt and fold gently with a spatula until evenly brown with no streaks. Taste and add a little more maple syrup if you like it sweeter."},
        {"t": "Portion and chill", "d": "Divide the mousse among four small cups or jars, about 1/2 cup each. Cover and refrigerate for at least 1 hour, until set. Top with raspberries just before serving."}
    ],
    "tips": [
        "Use 2% Greek yogurt for a richer, softer mousse. The protein stays about the same.",
        "If your yogurt looks watery, strain it in a coffee filter for 30 minutes. Thicker yogurt gives a more mousse-like texture.",
        "Dark chocolate around 70% gives the most flavor with the least sugar. Milk chocolate makes a sweeter, milder cup.",
        "Small-portion tip: eat half a cup now and cover the rest. A few spoonfuls still count."
    ],
    "storage": "Cover the cups and refrigerate for up to 4 days. Add the raspberries on the day you eat them. The mousse does not freeze well, since the yogurt turns grainy when thawed.",
    "variations": [
        ["Mocha", "Dissolve 1 teaspoon instant espresso powder in the maple syrup before whisking in the cocoa."],
        ["Peanut butter swirl", "Swirl 1 teaspoon warmed peanut butter into each cup before chilling."],
        ["Dairy-free", "Use a thick, high-protein plant yogurt. Check the label, since many plant yogurts are thinner and lower in protein."],
        ["Make it gentler", "Skip the raspberries and use milk chocolate for a milder, sweeter cup. Serve straight from the fridge."],
        ["Protein boost", "Stir 1 tablespoon of chocolate protein powder into each cup with a splash of milk."]
    ],
    "nutrition": {"calories": 210, "protein": 14, "carbs": 25, "fat": 7, "fiber": 4},
    "faq": [
        ["Can I skip the dark chocolate?", "Yes. Use 4 tablespoons of cocoa instead of 3 and a little more maple syrup. The mousse will be lighter and slightly less rich."],
        ["Why did my mousse turn grainy?", "The chocolate likely seized when it hit the cold yogurt. Cool the chocolate slightly and loosen it with a little yogurt before folding it into the rest."],
        ["Is it gluten-free?", "Cocoa, chocolate and yogurt are naturally gluten-free, but check your chocolate label, since some brands are made alongside wheat."]
    ],
    "note": "This tastes like dessert first and protein second, which is the point. A half cup straight from the fridge is often easier to face than anything warm, and the raspberries add a little brightness. Make all four on a good day and they wait for you.",
    "diet": ["vegetarian", "gluten-free"],
}
NEW['baked-cinnamon-apples'] = {
    "title": "Baked Cinnamon Apples with Greek Yogurt",
    "subtitle": "Small apples filled with oats, walnuts and dried cranberries, baked until soft and served warm with a spoonful of vanilla Greek yogurt.",
    "category": "Desserts",
    "tags": ["healthy", "small-plates", "gentle", "make-ahead"],
    "prep": 15, "cook": 35, "time": 50, "serves": 4, "level": "Easy",
    "desc": "Soft baked apples with a spoonful of yogurt.",
    "intro": [
        "Baked apples are soft, warm and gently sweet, the kind of dessert that is easy to eat in small spoonfuls. Each small apple is filled with oats, walnuts and dried cranberries, baked until tender and served with a spoonful of vanilla Greek yogurt for about 8 g of protein.",
        "Coring the apples while leaving the bottoms intact turns each one into a little cup that holds the filling and catches the juices. A splash of water in the dish creates steam, which softens the apples evenly before the tops start to brown. Baking until a knife slides in with no resistance gives a texture closer to apple sauce than crisp fruit."
    ],
    "why": [
        ["Soft and warm", "Fork-tender apples that are easy to eat in small spoonfuls."],
        ["About 8 g protein", "A spoonful of vanilla Greek yogurt on each apple."],
        ["Make ahead and reheat", "Bake a pan, then warm one apple at a time during the week."]
    ],
    "ingredients": [
        {"group": "For the apples", "items": [
            {"q": 4, "u": "", "n": "small apples", "note": "such as Gala or Honeycrisp, about 5 oz / 150 g each", "g": 600},
            {"q": 0.25, "u": "cup", "n": "old-fashioned rolled oats", "g": 22},
            {"q": 2, "u": "tbsp", "n": "walnuts", "note": "chopped", "g": 15},
            {"q": 2, "u": "tbsp", "n": "dried cranberries", "g": 20},
            {"q": 1, "u": "tbsp", "n": "butter", "note": "melted, or coconut oil"},
            {"q": 1, "u": "tbsp", "n": "maple syrup"},
            {"q": 1, "u": "tsp", "n": "ground cinnamon"},
            {"q": 1, "u": "pinch", "n": "fine salt"},
            {"q": 0.33, "u": "cup", "n": "water", "note": "for the baking dish"}
        ]},
        {"group": "To serve", "items": [
            {"q": 1, "u": "cup", "n": "plain nonfat Greek yogurt", "g": 240},
            {"q": 0.5, "u": "tsp", "n": "vanilla extract"},
            {"q": 1, "u": "pinch", "n": "ground cinnamon"}
        ]}
    ],
    "steps": [
        {"t": "Heat the oven", "d": "Heat the oven to 375°F (190°C) and choose a small baking dish that holds the four apples snugly."},
        {"t": "Core the apples", "d": "Use a melon baller or small spoon to scoop the core out of each apple from the top, leaving about 1/2 inch at the bottom so the filling stays in. Widen the opening to about 1 1/2 inches.",
         "tip": "If an apple wobbles, slice a thin piece off the bottom so it sits flat."},
        {"t": "Make the filling", "d": "In a small bowl, stir together the oats, walnuts, cranberries, melted butter, maple syrup, cinnamon and salt until the oats are evenly coated."},
        {"t": "Fill and bake", "d": "Set the apples in the dish and pack the filling into each one, mounding any extra on top. Pour the water into the dish, cover loosely with foil and bake for 20 minutes. Uncover and bake 10 to 15 minutes more, until a knife slides into the side of an apple with no resistance and the tops are golden.",
         "tip": "Covering for the first part of baking steams the apples so they soften all the way through before the filling browns."},
        {"t": "Serve warm", "d": "Stir the vanilla into the yogurt. Let the apples cool for 5 minutes, spoon a little of the pan juices over each one and serve with a spoonful of the yogurt and a pinch of cinnamon."}
    ],
    "tips": [
        "Choose apples that hold their shape when baked, such as Gala, Honeycrisp or Braeburn. Very soft varieties can collapse.",
        "Smaller apples cook faster and make a better single portion than large ones.",
        "Spoon the pan juices back over the apples before serving; that is where much of the flavor ends up.",
        "Small-portion tip: half an apple with yogurt is a complete small dessert. Cover the other half and warm it later."
    ],
    "storage": "Refrigerate cooled apples in an airtight container for up to 4 days, with the yogurt kept separately. Reheat in the microwave for 45 to 60 seconds, or in a 350°F (175°C) oven for about 10 minutes, until warm through.",
    "variations": [
        ["Pears instead", "Use small ripe but firm pears, halved and cored, and bake cut side up for 20 to 25 minutes."],
        ["Nut-free", "Replace the walnuts with pumpkin seeds."],
        ["Dairy-free", "Use coconut oil instead of butter and serve with a thick plant yogurt."],
        ["Make it gentler", "Peel the apples before baking and skip the walnuts for a softer, smoother texture."],
        ["Protein boost", "Serve with a larger spoonful of Greek yogurt, or stir a little vanilla protein powder into the yogurt."]
    ],
    "nutrition": {"calories": 210, "protein": 8, "carbs": 35, "fat": 6, "fiber": 5},
    "faq": [
        ["Do I need to peel the apples?", "No. The skin helps the apples keep their shape. Peel them if you prefer a softer texture, and expect them to cook a few minutes faster."],
        ["How do I know when they are done?", "A thin knife should slide into the side of the apple with no resistance, and the skin will look slightly wrinkled."],
        ["Can I make them gluten-free?", "Yes. Use oats labeled certified gluten-free."]
    ],
    "note": "Warm, soft and gently sweet, this is the kind of dessert that does not ask much of a small appetite. A spoonful of yogurt on top turns it into something closer to a small meal. Bake the whole pan; the leftovers reheat well.",
    "diet": ["vegetarian"],
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
    except Exception as ex:
        sys.exit(f'ERROR: could not download {rid} from Pexels ({ex}). Nothing was saved.')
    im = Image.open(io.BytesIO(data)).convert('RGB')
    main = cover(im, 1200, 900)
    for q in (80, 74, 68, 62, 56):
        buf = io.BytesIO()
        main.save(buf, 'WEBP', quality=q, method=6)
        if buf.tell() <= 195 * 1024:
            break
    else:
        sys.exit(f'ERROR: {rid} photo is still over 200 KB. Nothing was saved.')
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

# ------------------------------------------------------------------ build.py
b = open(P('build.py'), encoding='utf-8').read()
if 'RECIPE_REDIRECTS' not in b:
    b, n = re.subn(r"(GUIDE_REDIRECTS = \{[^\n]*\}\n)",
                   lambda mm: mm.group(1) + "RECIPE_REDIRECTS = json.load(open(os.path.join(HERE, 'redirects.json'))) if os.path.exists(os.path.join(HERE, 'redirects.json')) else {}\n",
                   b, count=1)
    if n != 1:
        sys.exit('ERROR: GUIDE_REDIRECTS line not found in build.py.')
    FUNC = ('def build_recipe_redirects():\n'
            '    for old, new in RECIPE_REDIRECTS.items():\n'
            "        full = os.path.join(OUT, 'recipes', old, 'index.html')\n"
            '        os.makedirs(os.path.dirname(full), exist_ok=True)\n'
            "        open(full, 'w').write(f'<!DOCTYPE html><meta charset=\"utf-8\"><title>Redirecting…</title><link rel=\"canonical\" href=\"{SITE_URL}recipes/{new}/\"><meta http-equiv=\"refresh\" content=\"0; url=../{new}/\"><a href=\"../{new}/\">Continue</a>')\n\n")
    if b.count('def build_guides():') != 1:
        sys.exit('ERROR: build_guides() not found in build.py.')
    b = b.replace('def build_guides():', FUNC + 'def build_guides():')
    CALL_OLD = '    for g in GUIDES:\n        build_guide(g)\n    for old, new in GUIDE_REDIRECTS.items():'
    if b.count(CALL_OLD) != 1:
        sys.exit('ERROR: guide build loop not found in build.py.')
    b = b.replace(CALL_OLD, '    for g in GUIDES:\n        build_guide(g)\n    build_recipe_redirects()\n    for old, new in GUIDE_REDIRECTS.items():')

b = b.replace(" + [('fall', 'Fall')]", '')

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

# ------------------------------------------------------------------ checks.py
c = open(P('checks.py'), encoding='utf-8').read()
STUB = "    stub = path in REDIRECT_STUBS\n"
if "'<title>Redirecting…</title>' in text" not in c:
    if c.count(STUB) != 1:
        sys.exit('ERROR: redirect stub check not found in checks.py.')
    c = c.replace(STUB, "    stub = path in REDIRECT_STUBS or '<title>Redirecting…</title>' in text\n")
    open(P('checks.py'), 'w', encoding='utf-8').write(c)

# ------------------------------------------------------------------ recipes.json (last)
for i, r in enumerate(recipes):
    if r['id'] in OLD_TO_NEW:
        rid = OLD_TO_NEW[r['id']]
        new = {'id': rid}
        new.update(NEW[rid])
        new['img'] = f'images/{rid}.webp'
        recipes[i] = new
        print(f"- {r['id']} -> {rid} ({new['title']}, ~{new['nutrition']['protein']} g protein, ~{new['nutrition']['calories']} kcal per {'item' if new.get('servesLabel') else 'serving'})")
m = re.match(r'\[\s*\n([ \t]+)\{', raw)
with open(P('recipes.json'), 'w', encoding='utf-8') as f:
    json.dump(recipes, f, ensure_ascii=False, indent=len(m.group(1)) if m else None)
    f.write('\n')
print('OK: 3 desserts replaced, redirects added, Fall chip removed.')
