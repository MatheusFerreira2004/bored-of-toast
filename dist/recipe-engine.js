(function(scope){
 'use strict';
 function format(n){const whole=Math.floor(n),rem=n-whole;for(const [v,c] of [[0,''],[.125,'⅛'],[.25,'¼'],[1/3,'⅓'],[.375,'⅜'],[.5,'½'],[.625,'⅝'],[2/3,'⅔'],[.75,'¾'],[.875,'⅞']])if(Math.abs(rem-v)<.008)return (whole?whole+(c?' ':''):'')+c||'0';return String(Math.round(n*100)/100);}
 function amount(item,multiplier){
  if(item.qty===undefined)return '';
  let n=item.qty*multiplier;if(item.scale==='whole')n=Math.max(1,Math.round(n));
  const unit=n!==1?(item.unit_plural||({cup:'cups',clove:'cloves',slice:'slices'}[item.unit])||item.unit):item.unit;
  const readableUnit=(item.unit==='cup' && n<1)?'cup':unit;
  if(item.metric && /\d\.\d/.test(format(n)))return format(item.metric*multiplier)+' '+(item.metric_unit||'g');
  return format(n)+' '+readableUnit+(item.metric?' ('+format(item.metric*multiplier)+' '+(item.metric_unit||'g')+')':'');
 }
 function calculate(data,requestedPeople,selected=[]){
  const people=Math.max(1,Math.min(data.max_people||12,Math.round(Number.isFinite(Number(requestedPeople))?Number(requestedPeople):data.base_people)));
  const multiplier=people/data.base_people,active=new Set(selected),names={},effects=[];
  const inline=text=>(text||'').replace(/\{\{amount:([\d.]+):([^}]+)\}\}/g,(_,n,u)=>format(Number(n)*multiplier)+' '+u);
  const ingredients=data.ingredients.map(original=>{
   const swapped=active.has(original.id)&&!!original.swap,item=swapped?original.swap:original;
   names[original.id]=item.method_name||item.name;
   if(swapped)effects.push(item);
   let note=item.note||'';
   if(item.package){const count=item.package.qty*multiplier;note=`About ${format(count)} ${count===1?'can':'cans'} (${item.package.label}).`;}
   return {id:original.id,name:inline(item.name),amount:amount(item,multiplier),note,swapped,swapAmount:original.swap?amount(original.swap,multiplier):null};
  });
  const interpolate=text=>inline(text).replace(/\{\{(\w+)\}\}/g,(_,id)=>names[id]||id);
  const steps=data.steps.map(base=>{
   const step={...base};for(const effect of effects)Object.assign(step,effect.step_overrides?.[base.id]||{});
   for(const key of ['title','action','cue','care'])step[key]=interpolate(step[key]);
   const notes=effects.map(e=>e.step_notes?.[base.id]).filter(Boolean);if(notes.length)step.care=[step.care,...notes].filter(Boolean).join(' ');
   return step;
  });
  return {people,ingredients,steps,allergen:effects.map(e=>e.allergen).filter(Boolean).join(' ')||data.allergen,batchNote:data.batch&&people>data.batch.above?data.batch.note:data.batch_default};
 }
 const api={calculate,amount,format};if(typeof module!=='undefined'&&module.exports)module.exports=api;else scope.BoredRecipeEngine=api;
})(typeof window==='undefined'?globalThis:window);
