import sys

html = open('dist/recipes/cabbage-egg-skillet-rice/index.html', encoding='utf-8').read()

print("One way to change it up:", 'One way to change it up' in html)
print("Storage & Prep ahead:", 'Storage & Prep ahead' in html)
print("Food safety guide link:", '<a href="https://www.foodsafety.gov/keep-food-safe/4-steps-to-food-safety" target="_blank">Food safety guide</a>' in html)
print("srcset:", 'srcset=' in html)
print("sizes:", 'sizes="(max-width: 800px) 100vw, 800px"' in html)

if '<a href="https://www.foodsafety.gov' not in html:
    print("Safety link MISSING")
