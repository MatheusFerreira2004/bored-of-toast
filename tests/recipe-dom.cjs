const fs = require('fs');
const assert = require('assert');
const { JSDOM } = require('jsdom');

const html = fs.readFileSync('dist/recipes/lemon-chickpea-salad/index.html', 'utf8');
const engineJs = fs.readFileSync('dist/recipe-engine.js', 'utf8');
const pilotJs = fs.readFileSync('dist/pilot.js', 'utf8');

// Set up JSDOM with scripts executed and a valid URL to allow sessionStorage
const dom = new JSDOM(html, { 
    url: "http://localhost:8000/recipes/lemon-chickpea-salad/",
    runScripts: "outside-only" 
});
const window = dom.window;
const document = window.document;

// Fail test on any unexpected window errors
window.addEventListener("error", (event) => {
    console.error("Unexpected error in DOM:", event.error);
    process.exit(1);
});

try {
    // Load engine first
    window.eval(engineJs);
    // Load pilot
    window.eval(pilotJs);

    // Helper for clicks
    function tap(selector) {
        const el = document.querySelector(selector);
        if (!el) throw new Error("Element not found: " + selector);
        el.click();
    }

    const item = id => {
        const el = document.querySelector(`[data-ingredient-id="${id}"] .ingredient-text`);
        return el ? el.textContent : '';
    }
    const steps = document.querySelectorAll('[data-method-step]');

    // Catch dispatched events
    let eventDetail = null;
    document.addEventListener('bot:recipe-change', e => eventDetail = e.detail);

    // Tests
    assert.match(item('beans'), /240 g/);

    tap('[data-servings-step="1"]'); 
    tap('[data-servings-step="1"]');
    assert.match(item('cucumber'), /2 cups \(300 g\)/);
    assert.match(item('beans'), /480 g/);
    
    // Check if swap amount is updated dynamically with people scaling!
    // The feta swap original is 50 g avocado per person (data says qty 1 cup -> wait what is the qty).
    // The test in the file originally checked for "100 g diced avocado" after tap, because servings=4 (4 * 25g? let's see)

    tap('[data-use-swap="feta"]');
    assert.match(item('feta'), /100 g diced avocado/);
    assert.match(steps[2].querySelector('[data-step-action]').textContent, /avocado/);
    assert(eventDetail.items.some(i => i.text.includes('100 g diced avocado')));
    assert.equal(eventDetail.servings, 4);

    tap('[data-undo-swap="feta"]');
    assert.match(item('feta'), /⅔ cup \(100 g\) crumbled feta/);

    tap('[data-use-swap="beans"]');
    tap('[data-use-swap="herb"]');
    assert.match(item('beans'), /480 g cooked white beans/);
    assert.match(steps[1].querySelector('[data-step-action]').textContent, /white beans/);
    assert.match(steps[1].querySelector('[data-step-action]').textContent, /dill/);

    tap('.servings-reset');
    assert.match(item('beans'), /240 g/);
    assert.equal(eventDetail.servings, 2);

    // bounds
    for(let i=0; i<20; i++) {
        const btn = document.querySelector('[data-servings-step="-1"]');
        if (!btn.disabled) btn.click();
    }
    assert.equal(eventDetail.servings, 1);

    for(let i=0; i<20; i++) {
        const btn = document.querySelector('[data-servings-step="1"]');
        if (!btn.disabled) btn.click();
    }
    assert.equal(eventDetail.servings, 12);
    
    // Verify sessionStorage works
    assert.ok(window.sessionStorage.getItem('bot_recipe_state_lemon-chickpea-salad'), 'Session storage should be saved');

    console.log('PASS: actual pilot.js in simulated JSDOM: scaling, substitutions, undo, method updates, shopping payload, reset, bounds.');
} catch (e) {
    console.error("Test failed:", e);
    process.exit(1);
}
