import os, sys, json, re
from pathlib import Path
import unittest

class TestBuildOutput(unittest.TestCase):
    def setUp(self):
        self.out_dir = Path('dist')
        self.assertTrue(self.out_dir.exists(), "dist directory not found. Did build.py run?")
        
    def test_no_python_literals(self):
        for html_file in self.out_dir.glob('**/*.html'):
            content = html_file.read_text(encoding='utf-8')
            # Look for typical python conditionals that leaked into HTML
            match = re.search(r'\{[^{}]*? if [^{}]*? else [^{}]*?\}', content)
            self.assertIsNone(match, f'Python literal found in HTML: {html_file} -> {match}')
            
    def test_jsonld_structure(self):
        for html_file in self.out_dir.glob('**/*.html'):
            content = html_file.read_text(encoding='utf-8')
            scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, flags=re.DOTALL)
            for s in scripts:
                j = json.loads(s.replace('\\u003c', '<'))
                if isinstance(j, dict) and j.get('@type') == 'Recipe':
                    self.assertTrue(j.get('name'), f'Missing name in {html_file}')
                    self.assertTrue(j.get('recipeIngredient'), f'Missing ingredients in {html_file}')
                    self.assertTrue(j.get('recipeInstructions'), f'Missing instructions in {html_file}')
                    self.assertNotEqual(j.get('cookTime'), 'PT0M', f'cookTime cannot be PT0M in {html_file}')
                    
if __name__ == '__main__':
    unittest.main()
