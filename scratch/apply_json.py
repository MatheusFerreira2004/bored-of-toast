import json
import traceback

try:
    with open('recipe_models.json', 'r', encoding='utf-8') as f:
        d = json.load(f)

    # Fix 2: Safety link and Fix 3: Before you begin
    rice = d['cabbage-egg-skillet-rice']
    rice['ahead'] = 'This recipe uses leftover rice. Ensure the rice was cooled quickly and stored correctly before using.'
    rice['safety_link'] = {
        'url': 'https://www.foodsafety.gov/keep-food-safe/4-steps-to-food-safety',
        'text': 'Food safety guide'
    }
    rice['before_prep'] = 'This recipe requires pre-cooked rice that has been properly cooled and stored. The estimated 20 minutes does not include the time to cook the rice.'

    pasta = d['lemon-pea-ricotta-pasta']
    pasta['before_prep'] = 'The estimated 20 minutes depends on the cooking time specified on your pasta package and how long your water takes to boil.'

    # Fix 5: Times
    rice['times'] = [
        {'label': 'Estimated total', 'value': '~20 min', 'note': '(starting from cooked rice)'},
        {'label': 'Method', 'value': 'Skillet'}
    ]
    pasta['times'] = [
        {'label': 'Estimated total', 'value': '~20 min', 'note': '(subject to pasta and boiling time)'},
        {'label': 'Method', 'value': 'Stovetop'}
    ]

    # Fix 6: Related recipes
    rice['relatedRecipes'] = ['lemon-white-bean-skillet', 'crispy-sheet-pan-gnocchi']
    pasta['relatedRecipes'] = ['lemon-white-bean-skillet']

    with open('recipe_models.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
    print("SUCCESS")
except Exception as e:
    traceback.print_exc()
