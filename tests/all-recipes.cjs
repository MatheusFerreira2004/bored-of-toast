// Integration checks against the actual generated models, after python build.py.
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..'),engine=require('../dist/recipe-engine.js'),models={};
for(const slug of fs.readdirSync(path.join(root,'dist/recipes'))){
 const file=path.join(root,'dist/recipes',slug,'index.html');if(!fs.existsSync(file))continue;
 const html=fs.readFileSync(file,'utf8');
 assert.equal((html.match(/id="pilot-recipe"/g)||[]).length,1);
 assert(!html.includes('ingredient-checkbox'));
 const match=html.match(/<script type="application\/json" id="pilot-recipe-data">(.*?)<\/script>/s);
 const m=JSON.parse(match[1]);models[slug]=m;
 const v=engine.calculate(m,m.base_people*2);
 assert.equal(v.steps.length,m.steps.length);assert.equal(v.ingredients.length,m.ingredients.length);
 assert(!JSON.stringify(v).includes('{{'));
 for(const [i,x] of m.ingredients.entries())if(x.qty!==undefined)assert.equal(v.ingredients[i].amount,engine.amount(x,2));
}
assert.equal(Object.keys(models).length,10);
assert.equal(engine.calculate(models['blueberry-overnight-oats'],2).ingredients[0].amount,'1 cup (80 g)');
const gn=engine.calculate(models['crispy-sheet-pan-gnocchi'],4);
assert.equal(gn.ingredients[0].amount,'2 packages');assert.match(gn.ingredients[0].note,/450 g/);
assert.match(engine.calculate(models['spiced-apple-cinnamon-porridge'],4).steps[0].action,/1 tsp/);
assert.equal((fs.readFileSync(path.join(root,'dist/index.html'),'utf8').match(/class="recipe-card"/g)||[]).length,3);
console.log('PASS: all ten generated recipes, scaling, fixed package sizes, cinnamon instructions, three home cards.');
