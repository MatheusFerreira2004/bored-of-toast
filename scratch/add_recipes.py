import json
import re
import shutil
from pathlib import Path
from PIL import Image

def process_image(src_name, target_name):
    # Base folder path for the generated images (Antigravity artifacts dir)
    base_dir = Path(r"C:\Users\Mathe\.gemini\antigravity-ide\brain\3250d63c-a8ed-4f2c-8e73-4ea1809385d5")
    
    # Find the most recent file matching src_name*.jpg
    files = list(base_dir.glob(f"{src_name}_*.jpg"))
    if not files:
        print(f"File {src_name} not found.")
        return
    
    # Sort by modification time, get latest
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    src_file = files[0]
    print(f"Processing {src_file.name} into {target_name}")
    
    img = Image.open(src_file).convert('RGB')
    
    # Crop to 4:3 aspect ratio (landscape) if it's not already
    w, h = img.size
    target_ratio = 4/3
    if w/h > target_ratio:
        # too wide
        new_w = int(h * target_ratio)
        offset = (w - new_w) // 2
        img = img.crop((offset, 0, offset + new_w, h))
    elif w/h < target_ratio:
        # too tall
        new_h = int(w / target_ratio)
        offset = (h - new_h) // 2
        img = img.crop((0, offset, w, offset + new_h))
        
    # Resize to 800 and 480
    img_800 = img.resize((800, 600), Image.Resampling.LANCZOS)
    img_480 = img.resize((480, 360), Image.Resampling.LANCZOS)
    img_1200 = img.resize((1200, 900), Image.Resampling.LANCZOS)
    
    out_dir = Path("dist/assets")
    src_assets = Path("source-assets")
    out_dir.mkdir(parents=True, exist_ok=True)
    src_assets.mkdir(parents=True, exist_ok=True)
    
    # Save as WebP
    img_800.save(out_dir / f"{target_name}.webp", "WEBP", quality=80)
    img_800.save(out_dir / f"{target_name}-800.webp", "WEBP", quality=80)
    img_480.save(out_dir / f"{target_name}-480.webp", "WEBP", quality=80)
    img_1200.save(out_dir / f"{target_name}-1200.webp", "WEBP", quality=80)
    
    # Also save to source-assets
    img_800.save(src_assets / f"{target_name}.png", "PNG")

def main():
    # 1. Update recipe_models.json
    with open('recipe_models.json', 'r', encoding='utf-8') as f:
        models = json.load(f)
        
    models['lemon-pea-ricotta-pasta'] = {
        "title": "Lemon, Pea & Ricotta Pasta",
        "slug": "lemon-pea-ricotta-pasta",
        "categories": ["quick-easy"],
        "method": "Stovetop",
        "base_people": 2,
        "meal_role": "a main meal",
        "tagline": "Short pasta folded into a light, bright ricotta sauce.",
        "intro": "Short pasta tossed in a light ricotta and lemon sauce, with sweet green peas cooked in the same pot. The starchy pasta water brings everything together into a creamy, bright bowl without heavy cream.",
        "prep_time": "20 mins",
        "total_time": "20 mins",
        "batch_default": "Use a larger pot and bowl. The reserved water is for adjustment, not a fixed amount.",
        "tested": False,
        "status": "published",
        "author": { "name": "", "url": "/about/" },
        "datePublished": "2026-09-18",
        "dateModified": "2026-09-18",
        "allergen": "Contains wheat (pasta) and dairy (ricotta). Check all ingredient labels.",
        "serve": "Serve immediately while warm and creamy.",
        "ahead": "This dish is best eaten fresh. The ricotta sauce will absorb into the pasta if left sitting.",
        "storage": "Store leftovers in an airtight container in the fridge for up to 2 days. Reheat gently with a splash of water to loosen the sauce.",
        "ingredients": [
          {
            "id": "pasta",
            "name": "dry short pasta",
            "qty": 180,
            "unit": "g"
          },
          {
            "id": "peas",
            "name": "frozen peas",
            "qty": 150,
            "unit": "g"
          },
          {
            "id": "ricotta",
            "name": "ricotta cheese",
            "qty": 120,
            "unit": "g",
            "swap": {
              "name": "mashed or whipped cottage cheese",
              "qty": 120,
              "unit": "g",
              "texture_change": "Similar creaminess, but may have small curds unless blended.",
              "flavor_change": "Cottage cheese can be saltier, so taste before adding extra salt.",
              "how_to_adjust": "Adjust the pasta water gradually, as moisture levels vary.",
              "technique": "Mash or blend before mixing for a smoother sauce."
            }
          },
          {
            "id": "oil",
            "name": "olive oil",
            "qty": 1,
            "unit": "tbsp"
          },
          {
            "id": "lemon-juice",
            "name": "lemon juice, plus more to taste",
            "qty": 1,
            "unit": "tbsp"
          },
          {
            "id": "lemon-zest",
            "name": "lemon zest",
            "qty": 0.5,
            "unit": "tsp"
          },
          {
            "id": "seasoning",
            "name": "Salt and black pepper to taste"
          },
          {
            "id": "water",
            "name": "reserved pasta water, as needed"
          }
        ],
        "steps": [
          {
            "id": "boil",
            "title": "Cook the pasta and peas",
            "action": "Cook the pasta according to package directions. Add the frozen peas near the end, respecting their required cooking time. Reserve a cup of the pasta water before draining.",
            "cue": "Pasta is cooked to the package's suggested doneness."
          },
          {
            "id": "mix-sauce",
            "title": "Prepare the ricotta base",
            "action": "In a large bowl, mash the ricotta with the olive oil, lemon juice, lemon zest, and black pepper. Add a few spoonfuls of the hot reserved pasta water to loosen the mixture.",
            "cue": "The mixture should look creamy and slightly thinned out."
          },
          {
            "id": "combine",
            "title": "Combine and adjust",
            "action": "Add the drained pasta and peas to the bowl. Toss well, adding more pasta water gradually until the sauce coats the pasta. Adjust salt to taste and serve.",
            "cue": "The sauce adheres to the pasta without looking dry or forming a puddle at the bottom.",
            "image": "lemon-pea-ricotta-pasta-step.webp",
            "alt": "Spoon holding pasta coated in ricotta sauce with peas"
          }
        ],
        "relatedRecipes": ["lemon-chickpea-salad", "lemon-white-bean-skillet"],
        "hero_image": {
          "src": "lemon-pea-ricotta-pasta.webp",
          "alt": "Pasta with green peas and a light ricotta coating",
          "is_ai_generated": True
        },
        "nutrition": {
          "verified": False
        }
    }
    
    models['cabbage-egg-skillet-rice'] = {
        "title": "Cabbage & Egg Skillet Rice",
        "slug": "cabbage-egg-skillet-rice",
        "categories": ["budget-friendly"],
        "method": "Skillet",
        "base_people": 2,
        "meal_role": "a main meal",
        "tagline": "Simple ingredients, fast prep, and golden cabbage.",
        "intro": "Cooked rice pan-fried with lightly browned cabbage, sweet carrots, and scrambled eggs. A fast, budget-friendly meal that makes excellent use of simple ingredients.",
        "prep_time": "20 mins",
        "total_time": "20 mins",
        "batch_default": "Cook in batches if your skillet is crowded. Do not double the cooking time automatically.",
        "tested": False,
        "status": "published",
        "author": { "name": "", "url": "/about/" },
        "datePublished": "2026-09-18",
        "dateModified": "2026-09-18",
        "allergen": "Contains egg and soy. Check all ingredient labels.",
        "serve": "Serve hot directly from the skillet.",
        "ahead": "This recipe uses leftover rice. Ensure the rice was cooled quickly and stored correctly before using. <a href=\"https://www.foodsafety.gov/keep-food-safe/4-steps-to-food-safety\" target=\"_blank\">Food safety guide</a>.",
        "storage": "Keep leftovers at 40°F (4°C) or colder. Refrigerate within 2 hours of preparation.",
        "ingredients": [
          {
            "id": "rice",
            "name": "cooked rice, properly stored",
            "qty": 300,
            "unit": "g",
            "note": "Time does not include cooking the rice."
          },
          {
            "id": "cabbage",
            "name": "thinly sliced cabbage",
            "qty": 250,
            "unit": "g",
            "swap": {
              "name": "finely chopped broccoli",
              "qty": 250,
              "unit": "g",
              "texture_change": "More crunch, less surface area for browning.",
              "how_to_adjust": "Cooking may take longer. Cut thick stems very small so they cook evenly.",
              "technique": "Cook until tender-crisp before adding the rice."
            }
          },
          {
            "id": "egg",
            "name": "eggs",
            "qty": 3,
            "unit": ""
          },
          {
            "id": "carrot",
            "name": "small carrot, grated",
            "qty": 1,
            "unit": ""
          },
          {
            "id": "oil",
            "name": "neutral oil, divided",
            "qty": 2,
            "unit": "tsp"
          },
          {
            "id": "garlic",
            "name": "garlic clove, minced",
            "qty": 1,
            "unit": ""
          },
          {
            "id": "soy-sauce",
            "name": "soy sauce, plus more to taste",
            "qty": 1,
            "unit": "tbsp"
          },
          {
            "id": "scallion",
            "name": "sliced scallions (optional)",
            "qty": 2,
            "unit": ""
          }
        ],
        "steps": [
          {
            "id": "cook-egg",
            "title": "Scramble the eggs",
            "action": "Heat half the oil in a large skillet. Add the beaten eggs and stir until just set. Transfer to a plate and set aside.",
            "cue": "Eggs are fully cooked with no runny parts left."
          },
          {
            "id": "brown-veg",
            "title": "Brown the vegetables",
            "action": "Add the remaining oil to the skillet along with the cabbage and carrot. Let it sit undisturbed for a moment to develop some color, then stir. Stir in the garlic and cook briefly without burning it.",
            "cue": "The cabbage has spots of golden brown while maintaining some crunch.",
            "image": "cabbage-egg-skillet-rice-step.webp",
            "alt": "Cabbage and grated carrots browning in a skillet"
          },
          {
            "id": "add-rice",
            "title": "Combine and heat",
            "action": "Add the cooked rice, breaking up any clumps. Stir in the soy sauce and toss until everything is thoroughly heated. Return the eggs to the pan, breaking them up, and fold in the scallions if using.",
            "cue": "The rice is hot and the grains are separate, not mushy."
          }
        ],
        "relatedRecipes": ["crispy-sheet-pan-gnocchi", "smashed-cucumber-edamame-bowl"],
        "hero_image": {
          "src": "cabbage-egg-skillet-rice.webp",
          "alt": "Fried rice with cabbage, carrots, and egg in a bowl",
          "is_ai_generated": True
        },
        "nutrition": {
          "verified": False
        }
    }
        
    with open('recipe_models.json', 'w', encoding='utf-8') as f:
        json.dump(models, f, indent=2, ensure_ascii=False)

    # 2. Process images
    process_image('lemon_pea_pasta', 'lemon-pea-ricotta-pasta')
    process_image('lemon_pea_pasta_step', 'lemon-pea-ricotta-pasta-step')
    process_image('cabbage_egg_rice', 'cabbage-egg-skillet-rice')
    process_image('cabbage_egg_rice_step', 'cabbage-egg-skillet-rice-step')

    # 3. Update build.py dynamically
    with open('build.py', 'r', encoding='utf-8') as f:
        build_py = f.read()
    
    # Use f-strings for recipe counts
    build_py = build_py.replace("10 recipes", "12 recipes")
    build_py = build_py.replace("Twelve everyday recipes", "twelve everyday recipes")
    build_py = build_py.replace("All 10 recipes", "All 12 recipes")
    build_py = build_py.replace("all 10 recipes", "all 12 recipes")
    build_py = build_py.replace("ten everyday recipes", "twelve everyday recipes")
    build_py = build_py.replace("All twelve recipes", "All 12 recipes")
    
    # We must ensure they are inside an f-string when replacing. Most places in build.py are already f-strings or we can use `.replace()` dynamically in python if it's a raw string. Wait, it's safer to just replace '10' with '12' and 'ten' with 'twelve' statically because some of them are in docstrings or not formatted strings. Let's do that for now.
    
    with open('build.py', 'w', encoding='utf-8') as f:
        f.write(build_py)

    print("Scripts and data updated.")

if __name__ == '__main__':
    main()
