const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const base=path.resolve(__dirname,'..'),models=JSON.parse(fs.readFileSync(path.join(base,'recipe_models.json'),'utf8'));
const engine=require('../dist/recipe-engine.js');
const salad=models['lemon-chickpea-salad'],skillet=models['lemon-white-bean-skillet'];
function ingredient(v,id){return v.ingredients.find(i=>i.id===id)}
const original=JSON.stringify(models);
let v=engine.calculate(salad,4,['feta','herb','beans']);
assert.equal(ingredient(v,'cucumber').amount,'2 cups (300 g)');
assert.equal(ingredient(v,'feta').amount,'100 g');
assert.match(v.steps[1].action,/white beans/);assert.match(v.steps[1].action,/dill/);
assert.match(v.steps[2].action,/avocado/);assert.match(v.allergen,/replaced/);
v=engine.calculate(salad,4,[]);assert.equal(ingredient(v,'feta').amount,'⅔ cup (100 g)');assert.match(v.steps[2].action,/feta/);
v=engine.calculate(skillet,4,['beans','oregano']);
assert.equal(v.steps.length,5);assert.equal(ingredient(v,'water').amount,'⅔ cup (160 ml)');
assert.equal(ingredient(v,'spinach').amount,'6 cups (180 g)');assert.equal(ingredient(v,'garlic').amount,'4 cloves');
assert.match(v.steps[2].action,/butter beans/);assert.match(v.steps[2].action,/thyme/);
assert.match(v.steps[2].care,/centres/);assert.match(v.allergen,/Bread/);assert(!JSON.stringify(v).includes('feta'));
assert.match(engine.calculate(skillet,6).batchNote,/two skillets/);
assert.equal(engine.calculate(skillet,99).people,8);assert.equal(engine.calculate(salad,99).people,12);assert.equal(engine.calculate(skillet,0).people,1);
assert.equal(engine.calculate(skillet,-1).people,1);
assert.equal(ingredient(engine.calculate(skillet,1),'garlic').amount,'1 clove');
assert.equal(ingredient(engine.calculate(skillet,1),'seasoning').amount,'');
assert.equal(JSON.stringify(models),original,'Calculations must not change base quantities or times');
// Same engine handles longer recipes, waits, whole items and no substitutions.
const longer={...skillet,base_people:3,max_people:9,times:[{label:'Rest',value:'Overnight'}],ingredients:[{id:'egg',qty:2,unit:'egg',unit_plural:'eggs',scale:'whole',name:'eggs'}],steps:Array.from({length:7},(_,i)=>({id:'s'+i,title:'Stage '+i,action:'Prepare {{egg}}.'}))};
v=engine.calculate(longer,5);assert.equal(v.steps.length,7);assert.equal(ingredient(v,'egg').amount,'3 eggs');assert.equal(v.steps[0].care,'');
console.log('PASS: two recipe models; proportional units, whole quantities, combined swaps, undo, bounds, batch guidance, immutable times, seven-step recipe.');
