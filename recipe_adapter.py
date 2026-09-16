"""Adapt existing recipes to the shared UI without inventing ingredient swaps."""
import re

def editorial_model(r, parse):
    ingredients=[]
    for text in r['ingredients']:
        text=text['text'] if isinstance(text,dict) else text
        if text.startswith('SECTION:'):continue
        qty,_,name=parse(text)
        item={'id':f'ingredient-{len(ingredients)}','name':name}
        if qty is not None:
            item.update(qty=qty,unit='')
            unit=re.match(r'^(cups?|tbsp|tsp|oz|g|ml|can|package)\b\s*',name)
            if unit:
                u=unit[1];item['unit']='cup' if u=='cups' else u
                if u in ('can','package'):item['unit_plural']=u+'s'
                name=name[unit.end():]
            metric=re.match(r'^\((\d+(?:\.\d+)?) (g|ml)\)\s*',name)
            package=re.match(r'^\(([^)]+)\)\s*',name) if item['unit'] in ('can','package') else None
            if metric:
                item.update(metric=float(metric[1]),metric_unit=metric[2]);name=name[metric.end():]
            elif package:
                item['note']='Package size: '+package[1]+'.';name=name[package.end():]
            approx=re.search(r'\(approx\. (\d+) (g|ml)\)',name)
            if approx:
                item.update(metric=float(approx[1]),metric_unit=approx[2])
                name=name.replace(approx[0],'').strip()
            name=name.replace('¼ tsp dried thyme','{{amount:0.25:tsp}} dried thyme').replace('½ tsp grated lemon zest','{{amount:0.5:tsp}} grated lemon zest')
            item['name']=name
        ingredients.append(item)
    return dict(slug=r['slug'],base_people=int(r['serves']),max_people=12,
        meal_role='a comforting meal',tagline=r.get('desc',''),ingredients=ingredients,
        times=[{'label':'Prep','value':r['prep_time']},{'label':'Total / resting','value':r['total_time']}],
        batch_default='Times are estimates for the base recipe. Adjust pan size and check the texture when changing the yield.',
        steps=[{'id':f'step-{i}','title':title,'action':action.replace('½ tsp', '{{amount:0.5:tsp}}')} for i,(title,action) in enumerate(r['steps'])],
        equipment=[],allergen=r.get('allergens',''),serve=r.get('extra',''),variation=r.get('swap',''),
        technique=r.get('tip',''),ahead='',storage='This recipe awaits kitchen testing. A refrigerated shelf life has not yet been established.',source='')
