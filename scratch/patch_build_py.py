import ast

with open('build.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.strip().startswith("dict(slug='oven-roasted-crispy-chickpeas'"):
        # This is the last recipe in the list
        lines[i] = line.rstrip().rstrip(',') + ',\n'
        
        new_recipes = [
            "    dict(slug='lemon-pea-ricotta-pasta', title='Lemon, Pea & Ricotta Pasta', cat='QUICK & BRIGHT · STOVETOP', categories=['quick-easy'], img='lemon-pea-ricotta-pasta.webp', alt='Pasta with green peas and a light ricotta coating', desc='Short pasta tossed in a light ricotta and lemon sauce, with sweet green peas cooked in the same pot.', serves='2', prep_time='20 min', total_time='20 min'), \n",
            "    dict(slug='cabbage-egg-skillet-rice', title='Cabbage & Egg Skillet Rice', cat='BUDGET PAN-FRIED · SKILLET', categories=['budget-friendly'], img='cabbage-egg-skillet-rice.webp', alt='Fried rice with cabbage, carrots, and egg in a bowl', desc='Cooked rice pan-fried with lightly browned cabbage, sweet carrots, and scrambled eggs.', serves='2', prep_time='20 min', total_time='20 min')\n"
        ]
        lines.insert(i + 1, new_recipes[0])
        lines.insert(i + 2, new_recipes[1])
        break

with open('build.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
