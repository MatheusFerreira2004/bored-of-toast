#!/usr/bin/env python3
"""Photo review, round 3 (GPT vision review of candidate photos).

1. tuna-white-bean-salad: no free photo with visible white beans was found (Pexels, Unsplash, Pixabay,
   Wikimedia Commons, rawpixel). The recipe becomes "Tuna & Chickpea Salad with Soft Eggs" so it matches a
   real photo whose description names the dish:
     Pexels 6632288 "Delicious tuna salad with vibrant vegetables and soft-boiled eggs" (Alesia Kozik)
   The URL slug stays tuna-white-bean-salad for now, because older update scripts check that id.
2. baked-cinnamon-apples: the old photo showed apples that looked unbaked, with no yogurt. New photo:
     rawpixel 3282699 "Rustic table with plates of baked apples and cinnamon", original public-domain image
     from Wikimedia Commons (CC0). The apples sit in the lower left of a wide frame, so the photo is cropped
     to that area. The recipe already serves the yogurt alongside.

Nutrition (tuna & chickpea salad, 3 servings) is an ESTIMATE from USDA FoodData Central reference values
(rounded; double-check before relying on it):
  light tuna in water, drained 226 g 262 kcal/57.6 P/2 F; canned chickpeas, drained 250 g 348/17.6 P/56 C/6.9 F/
  16 fiber; 3 large eggs 150 g 215/18.9 P/14.3 F; cherry tomatoes 150 g 27/1.3 P; cucumber 150 g 23/1 P;
  red onion 20 g 8; parsley 5; extra-virgin olive oil 13.5 g 119/13.5 F; lemon 7; Dijon 5; arugula 60 g 15/1.5 P
  -> ~1034 kcal, 99 P, 75 C, 38 F, 20 fiber / 3 = ~345 kcal, 33 P, 25 C, 13 F, 7 fiber

Nothing is saved unless both photos download. Safe to re-run.
"""
import io, json, os, re, subprocess, sys, urllib.request

sys.stderr = sys.stdout

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
IMG = os.path.join(ROOT, 'images')
P = lambda n: os.path.join(HERE, n)

TUNA = 'tuna-white-bean-salad'
APPLES = 'baked-cinnamon-apples'
RAWPIXEL_PAGE = 'https://www.rawpixel.com/image/3282699/free-photo-image-food-table-dining'

PHOTOS = {
    TUNA: {
        'url': 'https://images.pexels.com/photos/6632288/pexels-photo-6632288.jpeg?auto=compress&cs=tinysrgb&w=2000',
        'crop_lower_left': None,
        'photographer': 'Alesia Kozik', 'photographer_url': 'https://www.pexels.com/@alesiakozik/',
        'photo_url': 'https://www.pexels.com/photo/close-up-photo-of-a-dish-with-chickpeas-and-tuna-6632288/',
        'source': 'Pexels',
        'alt': 'A bowl of tuna salad with chickpeas, halved soft-boiled eggs, greens and red onion.'},
    APPLES: {
        'url': 'https://images.rawpixel.com/image_1300/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIyLTA1L3Vwd2s2MTY2NzQ4Ny13aWtpbWVkaWEtaW1hZ2Uta293YXo3MjYuanBn.jpg',
        'crop_lower_left': 0.70,   # keep the left 70% of the width, bottom-aligned, 4:3
        'photographer': 'Public domain image', 'photographer_url': RAWPIXEL_PAGE,
        'photo_url': RAWPIXEL_PAGE,
        'source': 'Wikimedia Commons via rawpixel (CC0)',
        'alt': 'Golden baked apples with wrinkled skins on plates on a rustic table.'},
}

NEW_TUNA = {
    "title": "Tuna & Chickpea Salad with Soft Eggs",
    "subtitle": "Canned tuna and chickpeas tossed with tomatoes, cucumber, parsley and a lemon dressing, topped with a soft-boiled egg. About 33 g protein per serving.",
    "category": "Salads",
    "tags": ["quick", "healthy", "high-protein", "small-plates", "make-ahead"],
    "prep": 15, "cook": 10, "time": 25, "serves": 3, "level": "Easy",
    "desc": "Tuna, chickpeas and a soft egg with lemon.",
    "intro": [
        "This is a pantry salad with a soft egg on top: two cans of tuna and one can of chickpeas, brightened with lemon, parsley and a few crunchy vegetables. The only cooking is a pot of water for the eggs, and each small bowl has about 33 g of protein.",
        "The dressing goes on the chickpeas first. Letting them sit in the lemon and olive oil while the eggs cook helps them absorb flavor, so the salad tastes seasoned all the way through. The tuna goes in last, folded gently so it stays in flakes, and the eggs are halved on top just before serving."
    ],
    "why": [
        ["About 33 g protein per bowl", "Tuna, chickpeas and a soft-boiled egg."],
        ["Almost no cooking", "Just a pot of water for the eggs; everything else comes from a can or the fridge."],
        ["Good the next day", "Keeps well in the fridge for packed lunches, with the eggs stored separately."]
    ],
    "ingredients": [
        {"group": "For the eggs", "items": [
            {"q": 3, "u": "", "n": "large eggs"}
        ]},
        {"group": "For the dressing", "items": [
            {"q": 1, "u": "tbsp", "n": "extra-virgin olive oil"},
            {"q": 2, "u": "tbsp", "n": "fresh lemon juice"},
            {"q": 1, "u": "tsp", "n": "Dijon mustard"},
            {"q": 0.25, "u": "tsp", "n": "kosher salt"},
            {"q": None, "u": "", "n": "black pepper", "note": "to taste"}
        ]},
        {"group": "For the salad", "items": [
            {"q": 15, "u": "oz", "n": "chickpeas", "note": "1 can, rinsed and drained"},
            {"q": 2, "u": "", "n": "cans light tuna in water", "note": "5 oz each, drained"},
            {"q": 1, "u": "cup", "n": "cherry tomatoes", "note": "halved", "g": 150},
            {"q": 0.5, "u": "", "n": "English cucumber", "note": "diced"},
            {"q": 2, "u": "tbsp", "n": "red onion", "note": "thinly sliced, optional"},
            {"q": 0.25, "u": "cup", "n": "fresh parsley", "note": "chopped"},
            {"q": 3, "u": "cups", "n": "arugula or mixed greens", "note": "to serve"}
        ]}
    ],
    "steps": [
        {"t": "Cook the eggs", "d": "Bring a small pot of water to a boil. Lower in the eggs with a spoon, reduce to a gentle boil and cook for 7 minutes for soft, jammy yolks. Move them to a bowl of ice water for 3 minutes, then peel.",
         "tip": "Cook 9 to 10 minutes if you prefer fully set yolks; they travel better in a packed lunch."},
        {"t": "Dress the chickpeas", "d": "While the eggs cook, whisk the olive oil, lemon juice, Dijon, salt and a few grinds of pepper in a large bowl. Add the chickpeas and toss to coat. Let them sit while you prepare the vegetables.",
         "tip": "Dressing the chickpeas first gives them time to absorb the lemon, which seasons the whole salad."},
        {"t": "Add the vegetables", "d": "Add the tomatoes, cucumber, red onion if using and parsley, and toss gently."},
        {"t": "Fold in the tuna", "d": "Break the tuna into large flakes and fold it in gently. Taste and add more lemon, salt or pepper if needed."},
        {"t": "Serve", "d": "Divide the greens among three small bowls, spoon the salad over the top and finish each bowl with a halved egg."}
    ],
    "tips": [
        "Light tuna in water keeps the salad lighter; tuna packed in olive oil is richer, so you can skip the oil in the dressing.",
        "Rinse canned chickpeas well to remove the starchy liquid and some of the salt.",
        "Keep the greens and eggs separate until serving if you are packing it for later.",
        "Small-portion tip: half a bowl with one egg half is a complete small lunch. The rest keeps for tomorrow."
    ],
    "storage": "Refrigerate the salad, without the greens, in an airtight container for up to 3 days. Keep peeled eggs in a separate container in the fridge for up to 2 days. Stir the salad and add a squeeze of lemon before serving.",
    "variations": [
        ["White beans", "Use cannellini beans instead of chickpeas for a softer, creamier salad."],
        ["Salmon", "Swap the tuna for canned salmon, flaked and with skin and bones removed if you prefer."],
        ["Vegetarian", "Skip the tuna, add a second egg per bowl and a little crumbled feta (no longer dairy-free)."],
        ["Make it gentler", "Leave out the red onion and Dijon, use fully set eggs and serve it cool rather than cold."],
        ["Protein boost", "Add a second egg half to each bowl."]
    ],
    "nutrition": {"calories": 345, "protein": 33, "carbs": 25, "fat": 13, "fiber": 7},
    "faq": [
        ["Which tuna should I use?", "Light tuna in water, drained, is what the nutrition estimate is based on. Brands vary, so check the label."],
        ["Can I make it ahead?", "Yes. The salad keeps for 3 days in the fridge. Add the greens and eggs just before serving."],
        ["Is it gluten-free?", "Yes, as written. Check your mustard label if you are very sensitive."]
    ],
    "note": "This is the salad for days when cooking sounds like too much. Everything except the eggs comes from a can or the crisper drawer, and a small bowl still covers a good share of the day's protein.",
    "diet": ["gluten-free", "dairy-free"],
}

# ------------------------------------------------------------------ what is left to do
raw = open(P('recipes.json'), encoding='utf-8').read()
recipes = json.loads(raw)
by_id = {r['id']: r for r in recipes}
missing = [rid for rid in PHOTOS if rid not in by_id]
if missing:
    print(f'ERROR: recipes not found: {missing}. Nothing was saved.')
    sys.exit(1)

craw = open(P('credits.json'), encoding='utf-8').read()
credits = json.loads(craw)
todo = [rid for rid, ph in PHOTOS.items() if credits.get(rid, {}).get('photo_url') != ph['photo_url']]
recipe_todo = by_id[TUNA]['title'] != NEW_TUNA['title']
if not todo and not recipe_todo:
    print('Already applied. Nothing to do.')
    sys.exit(0)

titles = {rid: by_id[rid]['title'] for rid in PHOTOS}
titles[TUNA] = NEW_TUNA['title']

# ------------------------------------------------------------------ images (in memory first)
out = {}
if todo:
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

    for rid in todo:
        ph = PHOTOS[rid]
        req = urllib.request.Request(ph['url'], headers={'User-Agent': 'Mozilla/5.0 (bored-of-toast site build)'})
        try:
            data = urllib.request.urlopen(req, timeout=60).read()
            im = Image.open(io.BytesIO(data)).convert('RGB')
        except Exception as ex:
            print(f'ERROR: could not download or open the {rid} photo ({ex}). Nothing was saved.')
            sys.exit(1)
        frac = ph['crop_lower_left']
        if frac:
            W, H = im.size
            w = int(W * frac)
            h = int(w * 3 / 4)
            if h > H:
                h = H
                w = int(H * 4 / 3)
            im = im.crop((0, H - h, w, H))
            print(f'- {rid}: source {W}x{H}, cropped to lower-left {w}x{h}')
        main = cover(im, 1200, 900)
        for q in (80, 74, 68, 62, 56):
            buf = io.BytesIO()
            main.save(buf, 'WEBP', quality=q, method=6)
            if buf.tell() <= 195 * 1024:
                break
        else:
            print(f'ERROR: {rid} photo is still over 200 KB. Nothing was saved.')
            sys.exit(1)
        out[rid] = {'webp': buf.getvalue(), 'og': jpg(cover(im, 1200, 630)), 'pin': jpg(make_pin(im, titles[rid]))}
        print(f"- photo {rid}: {len(out[rid]['webp']) // 1024} KB webp, og and pin generated")
elif recipe_todo:
    print(f'ERROR: the {TUNA} photo is already applied but the recipe is not; its pin would show the old title. '
          'Remove its credit entry and re-run. Nothing was saved.')
    sys.exit(1)

# ------------------------------------------------------------------ write images and credits
if out:
    for rid, b in out.items():
        for f in os.listdir(IMG):
            if re.fullmatch(re.escape(rid) + r'-\d+w\.webp', f):
                os.remove(os.path.join(IMG, f))
        open(os.path.join(IMG, f'{rid}.webp'), 'wb').write(b['webp'])
        open(os.path.join(IMG, 'og', f'{rid}.jpg'), 'wb').write(b['og'])
        open(os.path.join(IMG, 'pins', f'{rid}.jpg'), 'wb').write(b['pin'])
    subprocess.check_call([sys.executable, P('make_images.py')])
    for rid in out:
        ph = PHOTOS[rid]
        credits[rid] = {'photographer': ph['photographer'], 'photographer_url': ph['photographer_url'],
                        'photo_url': ph['photo_url'], 'source': ph['source'], 'alt': ph['alt']}
    m = re.match(r'\{\s*\n([ \t]+)"', craw)
    with open(P('credits.json'), 'w', encoding='utf-8') as f:
        json.dump(credits, f, ensure_ascii=False, indent=len(m.group(1)) if m else 1)
        f.write('\n')
    print(f"- OK: new photo and credit for {', '.join(out)}")

# ------------------------------------------------------------------ recipes.json (last)
if recipe_todo:
    for i, r in enumerate(recipes):
        if r['id'] == TUNA:
            new = {'id': TUNA}
            new.update(NEW_TUNA)
            new['img'] = r['img']
            recipes[i] = new
    m = re.match(r'\[\s*\n([ \t]+)\{', raw)
    with open(P('recipes.json'), 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=len(m.group(1)) if m else None)
        f.write('\n')
    print(f"- OK: {TUNA} is now '{NEW_TUNA['title']}' (~{NEW_TUNA['nutrition']['protein']} g protein, ~{NEW_TUNA['nutrition']['calories']} kcal per serving)")
else:
    print('- already applied: tuna recipe text')
print('Done.')
