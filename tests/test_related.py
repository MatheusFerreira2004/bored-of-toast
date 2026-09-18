import json
import postbuild

def run_tests():
    # Mock data
    all_recipes = [
        {'slug': 'pasta1', 'title': 'Pasta 1', 'categories': ['quick-easy']},
        {'slug': 'pasta2', 'title': 'Pasta 2', 'categories': ['quick-easy'], 'method': 'stovetop'},
        {'slug': 'pasta3', 'title': 'Pasta 3', 'categories': ['budget-friendly']},
        {'slug': 'salad1', 'title': 'Salad', 'categories': ['quick-easy']},
        {'slug': 'soup1', 'title': 'Soup', 'categories': ['budget-friendly']}
    ]

    print("Test 1: Editorial with two items (no auto-fill)")
    current1 = {'slug': 'pasta1', 'editorial_related': ['pasta2', 'pasta3']}
    picks1 = postbuild.pick_related(current1, all_recipes, limit=3)
    assert len(picks1) == 2
    assert picks1[0]['slug'] == 'pasta2'
    assert picks1[1]['slug'] == 'pasta3'

    print("Test 2: Explicitly empty list (omits section)")
    current2 = {'slug': 'pasta1', 'editorial_related': []}
    picks2 = postbuild.pick_related(current2, all_recipes, limit=3)
    assert len(picks2) == 0

    print("Test 3: Missing field (uses automatic fallback)")
    current3 = {'slug': 'pasta1', 'categories': ['quick-easy']}
    picks3 = postbuild.pick_related(current3, all_recipes, limit=3)
    assert len(picks3) > 0

    print("Test 4: Exclude self, duplicates, and invalid slugs")
    current4 = {
        'slug': 'pasta1', 
        'editorial_related': ['pasta2', 'pasta1', 'pasta2', 'invalid-slug', 'salad1']
    }
    picks4 = postbuild.pick_related(current4, all_recipes, limit=3)
    assert len(picks4) == 2
    assert picks4[0]['slug'] == 'pasta2'
    assert picks4[1]['slug'] == 'salad1'
    
    print("Test 5: Editorial with custom reasons (list of dicts)")
    current5 = {
        'slug': 'pasta1',
        'editorial_related': [
            {'slug': 'pasta2', 'reason': 'Another pasta'},
            {'slug': 'soup1'}
        ]
    }
    picks5 = postbuild.pick_related(current5, all_recipes, limit=3)
    assert picks5[0]['slug'] == 'pasta2'
    assert picks5[0]['editorial_reason'] == 'Another pasta'
    assert picks5[1]['slug'] == 'soup1'
    assert 'editorial_reason' not in picks5[1]

    print("ALL TESTS PASSED")

if __name__ == '__main__':
    run_tests()
