(function(){
 const root=document.getElementById('pilot-recipe');if(!root)return;
 const data=JSON.parse(document.getElementById('pilot-recipe-data').textContent),engine=window.BoredRecipeEngine;
 if(!engine)return;
 let people=data.base_people;const swaps=new Set();const q=s=>root.querySelector(s);
 const stateKey='bot_recipe_state_'+root.dataset.pilotRecipe;
 const signature=JSON.stringify(data);
 try{
  const saved=JSON.parse(sessionStorage.getItem(stateKey)||'null');
  if(saved&&saved.signature===signature){
   if(Number.isFinite(saved.people))people=saved.people;
   if(Array.isArray(saved.swaps))for(const id of saved.swaps)if(data.ingredients.some(i=>i.id===id&&i.swap))swaps.add(id);
  }
 }catch(e){/* The recipe still works when storage is unavailable. */}

 function render(userChange=false){
  const view=engine.calculate(data,people,[...swaps]);people=view.people;
  q('[data-servings-count]').textContent=people;
  q('[data-yield-note]').textContent=`Estimated to serve ${people} ${people===1?'person':'people'} as ${data.meal_role}.`;
  q('[data-servings-reset]').hidden=people===data.base_people;
  q('[data-servings-step="-1"]').disabled=people===1;q('[data-servings-step="1"]').disabled=people===(data.max_people||12);
  const bn = q('[data-batch-note]'); if (bn) bn.textContent=view.batchNote;
  for(const item of view.ingredients){
   const row=q(`[data-ingredient-id="${item.id}"]`),text=row.querySelector('.ingredient-text');text.replaceChildren();
   if(item.amount){const quantity=document.createElement('span');quantity.className='ingredient-qty';quantity.textContent=item.amount+' ';text.append(quantity);}const name=document.createElement('span');name.className='ingredient-name';name.textContent=item.name;text.append(name);
   row.querySelector('.ingredient-note').textContent=item.note;
   const applied=row.querySelector('[data-applied-swap]');
   if(applied){applied.hidden=!item.swapped;applied.textContent=item.swapped?'Replacing '+data.ingredients.find(i=>i.id===item.id).name:'';}

      if(item.swapAmount!==null){
    const swapNode = row.querySelector('[data-swap-amount]');
    if (swapNode) swapNode.textContent=item.swapAmount;
    const button=row.querySelector('[data-use-swap]');
    if (button) {
      button.textContent=item.swapped?'Substitution applied':'Use in this recipe';
      button.disabled=item.swapped;
    }
    const undo=row.querySelector('[data-undo-swap]');
    if (undo) undo.hidden=!item.swapped;
   }
  }
  root.querySelectorAll('[data-method-step]').forEach((element,index)=>{
   const step=view.steps[index];
   const h3 = element.querySelector('h3'); if(h3) h3.textContent=step.title;
   const action = element.querySelector('[data-step-action]'); if(action) action.textContent=step.action;
   const stepCue = element.querySelector('[data-step-cue]'); if(stepCue) stepCue.textContent=step.cue;
   const cue = element.querySelector('.step-cue'); if(cue) cue.hidden=!step.cue;
   const stepCare = element.querySelector('[data-step-care]'); if(stepCare) stepCare.textContent=step.care;
   const care = element.querySelector('.method-care-copy'); if(care) care.hidden=!step.care;
   const check = element.querySelector('[data-step-check]'); if(check) check.hidden=!step.cue&&!step.care;

  });
  q('[data-allergen]').textContent=view.allergen;
  if(!userChange)return;
  try{sessionStorage.setItem(stateKey,JSON.stringify({signature,people,swaps:[...swaps]}));}catch(e){}
  document.dispatchEvent(new CustomEvent('bot:recipe-change',{detail:{slug:root.dataset.pilotRecipe,servings:people,items:view.ingredients.map(i=>({id:i.id,text:[i.amount,i.name].filter(Boolean).join(' '),checked:false}))}}));
 }
 root.addEventListener('click',e=>{
  const step=e.target.closest('[data-servings-step]'),reset=e.target.closest('[data-servings-reset]'),use=e.target.closest('[data-use-swap]'),undo=e.target.closest('[data-undo-swap]');
  if(step)people+=Number(step.dataset.servingsStep);else if(reset)people=data.base_people;
  else if(use){swaps.add(use.dataset.useSwap);q('[data-change-status]').textContent='Substitution applied. Instructions have been updated.';}
  else if(undo){swaps.delete(undo.dataset.undoSwap);q('[data-change-status]').textContent='Original ingredient restored.';}else return;
  render(true);
 });render();
})();
