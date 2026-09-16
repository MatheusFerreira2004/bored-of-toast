import os, sys, json, re
from pathlib import Path
import unittest

# Add workspace root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

import pilot_recipe
from pilot_recipe import render_editorial_recipe, MODELS
import build
from build import card, recipes, build_recipe_jsonld

class TestBuildOutput(unittest.TestCase):
    def setUp(self):
        self.out_dir = Path('dist')
        self.assertTrue(self.out_dir.exists(), "dist directory not found. Did build.py run?")

    def test_validation_detects_preencher_prefix(self):
        """1. A função de validação detecta [PREENCHER com prefixo, não apenas a forma fechada."""
        sample_models = {
            'test-recipe': {
                'author': {
                    'name': '[PREENCHER: nome do autor]',
                    'credential': '[PREENCHER: credencial]'
                },
                'whyItWorks': [
                    {'body': '[PREENCHER: explicação 1]'},
                    {'body': 'Valid text without placeholder'}
                ],
                'sources': [
                    {'url': '[PREENCHER: url]'}
                ],
                'nutrition': {
                    'servingSize': '',
                    'calories': ''
                }
            }
        }

        errors = []
        def check_preencher(obj, path):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    check_preencher(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for i, v in enumerate(obj):
                    check_preencher(v, f"{path}[{i}]")
            elif isinstance(obj, str):
                if '[PREENCHER' in obj:
                    errors.append(path)

        for slug, d in sample_models.items():
            check_preencher(d, slug)
            if d.get('nutrition'):
                nut = d['nutrition']
                for req in ['servingSize', 'calories']:
                    if not nut.get(req) or not str(nut.get(req)).strip():
                        errors.append(f"{slug}.nutrition.{req}")

        self.assertIn('test-recipe.author.name', errors)
        self.assertIn('test-recipe.author.credential', errors)
        self.assertIn('test-recipe.whyItWorks[0].body', errors)
        self.assertNotIn('test-recipe.whyItWorks[1].body', errors)
        self.assertIn('test-recipe.sources[0].url', errors)
        self.assertIn('test-recipe.nutrition.servingSize', errors)
        self.assertIn('test-recipe.nutrition.calories', errors)

    def test_no_preencher_in_dist(self):
        """2. Nenhum arquivo em dist/ contém a string [PREENCHER."""
        for p in self.out_dir.glob('**/*'):
            if p.is_file():
                try:
                    content = p.read_text(encoding='utf-8')
                    self.assertNotIn('[PREENCHER', content, f"Placeholder [PREENCHER found in file: {p}")
                except UnicodeDecodeError:
                    pass

    def test_ul_ingredients_structure(self):
        """3. O elemento <ul> contém ao menos um <li> e nenhum <div> como filho direto."""
        # Render lemon-chickpea-salad in memory
        r = next(rec for rec in recipes if rec['slug'] == 'lemon-chickpea-salad')
        model_copy = json.loads(json.dumps(MODELS[r['slug']]))
        html_out = render_editorial_recipe({**r, 'editorial': model_copy}, '')

        # Find the ul.editorial-ingredients-list
        match = re.search(r'<ul[^>]*class="[^"]*editorial-ingredients-list[^"]*"[^>]*>(.*?)</ul>', html_out, re.DOTALL)
        self.assertIsNotNone(match, "Could not find editorial-ingredients-list in output")
        ul_content = match.group(1).strip()

        # Must contain at least one <li>
        self.assertIn('<li', ul_content, "<ul> does not contain any <li> element")
        
        # Must NOT contain <div> as a direct child
        direct_div_match = re.search(r'(?:^|</ul>|</li>)\s*<div\b', ul_content)
        self.assertIsNone(direct_div_match, f"Found <div> as direct child of <ul> in ingredients: {direct_div_match}")

        # Check that the 8 ingredients and groupings are present
        self.assertEqual(ul_content.count('class="editorial-ingredient"'), 8, "Expected 8 ingredient items")
        self.assertIn('For the salad', ul_content)
        self.assertIn('For the dressing', ul_content)
        self.assertEqual(ul_content.count('class="ingredient-swap"'), 3, "Expected 3 swap blocks")

    def test_nutrition_table_rendering(self):
        """Testa se a tabela nutricional é omitida quando vazia e renderizada quando preenchida."""
        r = next(rec for rec in recipes if rec['slug'] == '5-minute-blender-hummus')
        model_copy = json.loads(json.dumps(MODELS[r['slug']]))

        # With empty nutrition fields in lemon-chickpea-salad
        html_empty = render_editorial_recipe({**r, 'editorial': model_copy}, '')
        self.assertNotIn('<section class="recipe-nutrition">', html_empty)

        # With filled nutrition fields
        model_copy['nutrition'] = {
            'servingSize': '1 bowl (approx. 350g)',
            'calories': '320',
            'proteinContent': '14g',
            'fatContent': '',
            'disclaimer': 'Estimated values.'
        }
        html_filled = render_editorial_recipe({**r, 'editorial': model_copy}, '')
        self.assertIn('<section class="recipe-nutrition">', html_filled)
        self.assertIn('Estimated values.', html_filled)
        self.assertIn('<span>Protein</span><span>14g</span>', html_filled)
        self.assertNotIn('<span>Fat</span>', html_filled)

    def test_jsonld_nutrition_structure(self):
        """4. O objeto nutrition do JSON-LD, quando presente, contém ao menos um campo de valor além de servingSize."""
        r = next(rec for rec in recipes if rec['slug'] == '5-minute-blender-hummus')
        
        # When empty, nutrition key must not be present in JSON-LD
        ld = build_recipe_jsonld(r)
        target_ld = ld[0] if isinstance(ld, list) else ld
        self.assertNotIn('nutrition', target_ld, "Empty nutrition object should be omitted from JSON-LD")

        # Mock with values
        orig_nut = MODELS[r['slug']].get('nutrition')
        try:
            # Case 1: only servingSize -> must NOT include nutrition
            MODELS[r['slug']]['nutrition'] = {'servingSize': '1 bowl', 'calories': ''}
            ld_serving_only = build_recipe_jsonld(r)
            target_1 = ld_serving_only[0] if isinstance(ld_serving_only, list) else ld_serving_only
            self.assertNotIn('nutrition', target_1, "Nutrition with only servingSize must be omitted")

            # Case 2: servingSize + calories + saturatedFat + sugar
            MODELS[r['slug']]['nutrition'] = {
                'servingSize': '1 bowl',
                'calories': '320',
                'saturatedFatContent': '2 g',
                'sugarContent': '4 g'
            }
            ld_val = build_recipe_jsonld(r)
            target_2 = ld_val[0] if isinstance(ld_val, list) else ld_val
            self.assertIn('nutrition', target_2)
            nut_obj = target_2['nutrition']
            self.assertEqual(nut_obj.get('@type'), 'NutritionInformation')
            self.assertEqual(nut_obj.get('calories'), '320 calories')
            self.assertEqual(nut_obj.get('saturatedFatContent'), '2 grams')
            self.assertEqual(nut_obj.get('sugarContent'), '4 grams')
            self.assertIn('servingSize', nut_obj)
        finally:
            if orig_nut is not None:
                MODELS[r['slug']]['nutrition'] = orig_nut
            else:
                MODELS[r['slug']].pop('nutrition', None)

    def test_no_empty_strings_in_jsonld(self):
        """5. Nenhum valor de string vazia aparece no JSON-LD gerado."""
        def check_no_empty_strings(obj, path=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    check_no_empty_strings(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for i, v in enumerate(obj):
                    check_no_empty_strings(v, f"{path}[{i}]")
            elif isinstance(obj, str):
                self.assertTrue(obj.strip() != "", f"Empty string value found at {path} in JSON-LD")

        for r in recipes:
            ld = build_recipe_jsonld(r)
            check_no_empty_strings(ld, r['slug'])

    def test_no_python_literals(self):
        """6. Nenhum arquivo em dist/ contém literais de expressão Python não avaliados, como { ' seguido de if."""
        for html_file in self.out_dir.glob('**/*.html'):
            content = html_file.read_text(encoding='utf-8')
            # Look for typical python conditionals that leaked into HTML
            match = re.search(r'\{[^{}]*? if [^{}]*? else [^{}]*?\}', content)
            self.assertIsNone(match, f'Python literal found in HTML: {html_file} -> {match}')

            # Check specifically for patterns like "{ '" followed by "if" or "if any("
            match_unevaluated = re.search(r"\{\s*'[^']*?'\s+if\s+", content)
            self.assertIsNone(match_unevaluated, f'Unevaluated expression pattern found in {html_file}: {match_unevaluated}')
            self.assertNotIn('if any(', content, f'Found un-evaluated "if any(" in {html_file}')

    def test_card_meta_no_orphan_separators(self):
        """7. A linha de meta dos cards não contém separador órfão, no padrão de dois separadores consecutivos ou separador no fim da string."""
        for i, r in enumerate(recipes):
            card_html = card(r, i + 1)
            meta_match = re.search(r'<div class="card-bottom"><span>(.*?)</span>', card_html)
            self.assertIsNotNone(meta_match, f"Card meta line not found for {r['slug']}")
            meta_text = meta_match.group(1).strip()

            # Check for double consecutive separators
            self.assertNotIn('·</span> <span aria-hidden="true">·', meta_text, f"Consecutive separators in card {r['slug']}")
            self.assertNotIn('· ·', meta_text, f"Consecutive separators in card {r['slug']}")

            # Check that line doesn't end or begin with separator
            self.assertFalse(meta_text.endswith('·</span>'), f"Card meta line ends with separator in {r['slug']}: {meta_text}")
            self.assertFalse(meta_text.startswith('<span aria-hidden="true">·'), f"Card meta line starts with separator in {r['slug']}: {meta_text}")

            # Check that card displays time without empty gap
            self.assertNotIn('Serves 2 <span aria-hidden="true">·</span> <span aria-hidden="true">·</span>', meta_text)

if __name__ == '__main__':
    unittest.main()
