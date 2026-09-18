import json

with open('recipe_models.json', 'r', encoding='utf-8') as f:
    models = json.load(f)

for recipe_id, equip in [
    ('lemon-pea-ricotta-pasta', ['Large pot', 'Large mixing bowl']),
    ('cabbage-egg-skillet-rice', ['Large skillet', 'Cutting board', 'Chef\\'s knife'])
]:
    models[recipe_id]['equipment'] = equip
    models[recipe_id]['serves_default'] = 2
    models[recipe_id]['max_people'] = 4
    models[recipe_id]['difficulty'] = 'Easy'
    models[recipe_id]['card_time'] = '~20 min'
    models[recipe_id]['batch'] = []
    models[recipe_id]['faq'] = []
    models[recipe_id]['related_notes'] = []
    models[recipe_id]['sources'] = []
    models[recipe_id]['source'] = ''
    models[recipe_id]['variation'] = ''
    models[recipe_id]['recipe_cuisine'] = ''
    models[recipe_id]['suitable_for_diet'] = []
    models[recipe_id]['primary_goal'] = ''
    models[recipe_id]['keywords'] = ''

with open('recipe_models.json', 'w', encoding='utf-8') as f:
    json.dump(models, f, indent=2, ensure_ascii=False)
