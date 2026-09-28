/* ---------- Icons ---------- */
const ICON = {
  clock: '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
  chef: '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 13.9A4 4 0 0 1 7 6a5 5 0 0 1 10 0 4 4 0 0 1 1 7.9V20H6z"/><path d="M6 17h12"/></svg>',
  users: '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6 6 0 0 1 3.5 6"/></svg>',
  arrow: '<svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
  search: '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
  user: '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>',
  menu: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
  up: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M12 19V5M6 11l6-6 6 6"/></svg>',
  print: '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 9V3h12v6"/><rect x="3" y="9" width="18" height="8" rx="2"/><path d="M7 14h10v7H7z"/></svg>',
  share: '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/></svg>',
  down: '<svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14M6 13l6 6 6-6"/></svg>',
  bulb: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/></svg>',
  box: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M3 7l9-4 9 4-9 4z"/><path d="M3 7v10l9 4 9-4V7M12 11v10"/></svg>',
  swap: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M7 4 3 8l4 4M3 8h14M17 20l4-4-4-4M21 16H7"/></svg>',
  check: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="m5 12 5 5L20 7"/></svg>',
  heart: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg>',
  bolt: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg>',
  instagram: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
  facebook: '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H8v4h2v8h4v-8h3l1-4h-4V8.5c0-.3.2-.5.5-.5z"/></svg>',
  pinterest: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M9 21l2.5-10"/><path d="M8.5 14.5A5 5 0 1 1 17 11c0 3-1.8 5-4 5-1.4 0-2.2-1-2-2.3"/></svg>',
  youtube: '<svg width="19" height="19" viewBox="0 0 24 24" fill="currentColor"><path d="M22 8.2a3 3 0 0 0-2.1-2.1C18 5.6 12 5.6 12 5.6s-6 0-7.9.5A3 3 0 0 0 2 8.2 31 31 0 0 0 1.6 12a31 31 0 0 0 .4 3.8 3 3 0 0 0 2.1 2.1c1.9.5 7.9.5 7.9.5s6 0 7.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .4-3.8 31 31 0 0 0-.4-3.8zM10 15.1V8.9l5.2 3.1z"/></svg>'
};
const WHY_ICONS = [ICON.bolt, ICON.heart, ICON.check];

const WAVE = '<svg class="hero-wave" viewBox="0 0 1440 70" preserveAspectRatio="none"><path fill="currentColor" d="M0 40c160 30 320 30 480 10s320-40 480-20 320 40 480 20v20H0z"/></svg>';

/* ---------- Helpers ---------- */
const $ = (s, el = document) => el.querySelector(s);
const PAGE = document.body.dataset.page;
const recipeUrl = r => `recipe.html?id=${r.id}`;
function fmtTime(min) {
  if (min < 60) return `${min} min`;
  const h = Math.floor(min / 60), m = min % 60;
  return m ? `${h} h ${m} min` : `${h} h`;
}
function fmtQty(q) {
  if (q == null) return '';
  const whole = Math.floor(q + 0.01), frac = q - whole;
  const map = [[0.125, '⅛'], [0.25, '¼'], [0.33, '⅓'], [0.5, '½'], [0.67, '⅔'], [0.75, '¾']];
  let best = '', diff = 1;
  map.forEach(([v, s]) => { if (Math.abs(frac - v) < diff) { diff = Math.abs(frac - v); best = s; } });
  if (frac < 0.07) return String(whole);
  if (frac > 0.9) return String(whole + 1);
  if (diff > 0.08) return (Math.round(q * 10) / 10).toString();
  return (whole ? whole + ' ' : '') + best;
}

/* ---------- Header / footer ---------- */
const NAV = [['index.html', 'Home', 'home'], ['recipes.html', 'Recipes', 'recipes'], ['about.html', 'About', 'about'], ['about.html#contact', 'Contact', 'contact']];

function renderHeader() {
  const el = $('#site-header');
  if (!el) return;
  el.className = 'site-header';
  const current = PAGE === 'recipe' ? 'recipes' : PAGE;
  el.innerHTML = `
    <div class="container">
      <a href="index.html" class="brand" aria-label="Bored of Toast home"><img src="images/logo-white.png" alt="Bored of Toast"></a>
      <nav class="nav" id="nav">
        ${NAV.map(([href, label, key]) => `<a href="${href}" class="${key === current ? 'active' : ''}">${label}</a>`).join('')}
        <div class="nav-icons">
          <a href="recipes.html#search" aria-label="Search recipes">${ICON.search}</a>
          <a href="about.html#contact" aria-label="Contact us">${ICON.user}</a>
        </div>
      </nav>
      <button class="menu-toggle" id="menu-toggle" aria-label="Open menu">${ICON.menu}</button>
    </div>`;
  $('#menu-toggle').addEventListener('click', () => $('#nav').classList.toggle('open'));
  window.addEventListener('scroll', () => el.classList.toggle('scrolled', window.scrollY > 10), { passive: true });
}

function renderFooter() {
  const el = $('#site-footer');
  if (!el) return;
  el.className = 'site-footer';
  el.innerHTML = `
    <div class="container footer-grid">
      <div>
        <a href="index.html" class="brand" aria-label="Bored of Toast home"><img src="images/logo-white.png" alt="Bored of Toast"></a>
        <p class="footer-tagline">Good food without the fuss. Simple, tested recipes for real life.</p>
        <div class="socials">
          <a href="#" aria-label="Instagram">${ICON.instagram}</a>
          <a href="#" aria-label="Facebook">${ICON.facebook}</a>
          <a href="#" aria-label="Pinterest">${ICON.pinterest}</a>
          <a href="#" aria-label="YouTube">${ICON.youtube}</a>
        </div>
      </div>
      <div><h4>Explore</h4><ul>${NAV.map(([h, l]) => `<li><a href="${h}">${l}</a></li>`).join('')}</ul></div>
      <div><h4>Recipes</h4><ul>${CATEGORIES.slice(0, 5).map(c => `<li><a href="recipes.html?cat=${encodeURIComponent(c.key)}">${c.label}</a></li>`).join('')}</ul></div>
      <div class="footer-cta"><h4>Can't decide?</h4><p>Let us pick tonight's dinner for you.</p><button class="btn btn-yellow" data-random>Surprise me ${ICON.arrow}</button></div>
    </div>
    <div class="copyright">© ${new Date().getFullYear()} Bored of Toast. All rights reserved.</div>`;
}

function renderStamps() {
  document.querySelectorAll('.stamp').forEach(s => {
    s.innerHTML = `
      <svg class="ring" viewBox="0 0 120 120"><defs><path id="circ" d="M60 60m-48 0a48 48 0 1 1 96 0a48 48 0 1 1-96 0"/></defs>
        <text font-family="Inter, sans-serif" font-size="11.5" font-weight="600" letter-spacing="3.2" fill="#f7f2e7"><textPath href="#circ">GOOD FOOD • NO FUSS • TESTED AT HOME •</textPath></text></svg>
      <div class="stamp-core"><img src="images/favicon.png" alt=""></div>`;
  });
}

function bindRandom() {
  document.addEventListener('click', e => {
    if (e.target.closest('[data-random]')) {
      const r = RECIPES[Math.floor(Math.random() * RECIPES.length)];
      location.href = recipeUrl(r);
    }
  });
}

function backToTop() {
  const b = document.createElement('button');
  b.className = 'to-top no-print'; b.setAttribute('aria-label', 'Back to top'); b.innerHTML = ICON.up;
  document.body.appendChild(b);
  b.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  window.addEventListener('scroll', () => b.classList.toggle('show', window.scrollY > 700), { passive: true });
}

/* ---------- Cards ---------- */
function cardHTML(r, showDesc = true) {
  return `
    <a class="card reveal" href="${recipeUrl(r)}">
      <div class="card-img"><img src="${r.img}" alt="${r.title}" loading="lazy" style="object-position:${r.pos || 'center'}"><span class="card-badge">${r.category}</span></div>
      <div class="card-body">
        <h3>${r.title}</h3>
        ${showDesc ? `<p class="desc">${r.desc}</p>` : ''}
        <div class="meta"><span>${ICON.clock}${fmtTime(r.time)}</span><span>${ICON.chef}${r.level}</span></div>
      </div>
    </a>`;
}

/* ---------- Reveal ---------- */
const observer = new IntersectionObserver(entries => {
  entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add('visible'); observer.unobserve(en.target); } });
}, { threshold: 0.1 });
function observeReveals() { document.querySelectorAll('.reveal:not(.visible)').forEach(el => observer.observe(el)); }

/* ---------- Home ---------- */
function initHome() {
  const count = key => RECIPES.filter(r => r.category === key || r.tags.includes(key)).length;
  $('#categories').innerHTML = CATEGORIES.map(c => `
    <a class="category reveal" href="recipes.html?cat=${encodeURIComponent(c.key)}">
      <div class="circle"><img src="${c.img}" alt="${c.label}" loading="lazy" style="object-position:${c.pos || 'center'}"></div>
      ${c.label}<small>${count(c.key)} recipes</small>
    </a>`).join('');
  $('#featured').innerHTML = RECIPES.slice(0, 5).map(r => cardHTML(r, false)).join('');

  const s = RECIPES.find(r => r.id === 'creamy-garlic-pasta');
  const keyIngr = s.ingredients.flatMap(g => g.items).filter(i => i.q != null).slice(0, 5).map(i => i.n.split(',')[0]);
  $('#spotlight').innerHTML = `
    <div class="spotlight-img"><img src="${s.img}" alt="${s.title}"><span class="ribbon">Recipe of the week</span></div>
    <div class="spotlight-body">
      <span class="tag">${s.category}</span>
      <h2>${s.title}</h2>
      <p>${s.subtitle}</p>
      <div class="meta" style="margin-bottom:18px"><span>${ICON.clock}${fmtTime(s.time)}</span><span>${ICON.chef}${s.level}</span><span>${ICON.users}Serves ${s.serves}</span></div>
      <div class="pills">${keyIngr.map(i => `<span class="pill">${i}</span>`).join('')}</div>
      <div><a href="${recipeUrl(s)}" class="btn btn-dark">Get the recipe ${ICON.arrow}</a></div>
    </div>`;
}

/* ---------- Recipes list ---------- */
function initRecipes() {
  const grid = $('#recipe-grid'), chips = $('#chips'), search = $('#search'), empty = $('#empty'), countEl = $('#results-count');
  const filters = [['all', 'All'], ['Main Dishes', 'Main Dishes'], ['Salads', 'Salads'], ['Soups', 'Soups'], ['Desserts', 'Desserts'], ['quick', 'Quick & Easy'], ['healthy', 'Healthy']];
  let active = new URLSearchParams(location.search).get('cat') || 'all';
  chips.innerHTML = filters.map(([k, l]) => `<button class="chip" data-key="${k}">${l}</button>`).join('');

  function render() {
    const q = search.value.trim().toLowerCase();
    chips.querySelectorAll('.chip').forEach(c => c.classList.toggle('active', c.dataset.key === active));
    const list = RECIPES.filter(r => {
      const catOk = active === 'all' || r.category === active || r.tags.includes(active);
      const text = (r.title + ' ' + r.desc + ' ' + r.ingredients.flatMap(g => g.items.map(i => i.n)).join(' ')).toLowerCase();
      return catOk && (!q || text.includes(q));
    });
    grid.innerHTML = list.map(r => cardHTML(r)).join('');
    empty.style.display = list.length ? 'none' : 'block';
    countEl.textContent = `Showing ${list.length} of ${RECIPES.length} recipes`;
    observeReveals();
  }
  chips.addEventListener('click', e => {
    const chip = e.target.closest('.chip');
    if (!chip) return;
    active = chip.dataset.key;
    history.replaceState(null, '', active === 'all' ? location.pathname : `${location.pathname}?cat=${encodeURIComponent(active)}`);
    render();
  });
  search.addEventListener('input', render);
  render();
  if (location.hash === '#search') search.focus();
}

/* ---------- Single recipe page ---------- */
function initRecipe() {
  const id = new URLSearchParams(location.search).get('id');
  const r = RECIPES.find(x => x.id === id) || RECIPES[0];
  document.title = `${r.title} | Bored of Toast`;
  const metaDesc = document.querySelector('meta[name="description"]');
  if (metaDesc) metaDesc.setAttribute('content', r.subtitle);
  const unit = r.servesLabel || 'servings';
  const related = RECIPES.filter(x => x.id !== r.id).sort((a, b) => (b.category === r.category) - (a.category === r.category)).slice(0, 3);
  const n = r.nutrition;

  $('#recipe-root').innerHTML = `
    <section class="hero recipe-hero">
      <div class="container hero-grid">
        <div class="hero-copy">
          <nav class="breadcrumb"><a href="index.html">Home</a> / <a href="recipes.html">Recipes</a> / <a href="recipes.html?cat=${encodeURIComponent(r.category)}">${r.category}</a></nav>
          <p class="eyebrow">${r.category}${r.tags.includes('quick') ? ' · Quick & Easy' : ''}${r.tags.includes('healthy') ? ' · Healthy' : ''}</p>
          <h1>${r.title}</h1>
          <p>${r.subtitle}</p>
          <div class="recipe-facts">
            <div><small>Prep</small><strong>${fmtTime(r.prep)}</strong></div>
            <div><small>${r.chill ? 'Cook + chill' : 'Cook'}</small><strong>${fmtTime(r.cook + (r.chill || 0))}</strong></div>
            <div><small>Total</small><strong>${fmtTime(r.time)}</strong></div>
            <div><small>${r.servesLabel ? 'Makes' : 'Serves'}</small><strong>${r.serves}</strong></div>
          </div>
          <div class="hero-actions no-print">
            <a href="#ingredients" class="btn btn-yellow">Jump to recipe ${ICON.down}</a>
            <button class="btn btn-ghost" onclick="window.print()">${ICON.print} Print</button>
          </div>
        </div>
        <div class="hero-art">
          <div class="arch"><img src="${r.img}" alt="${r.title}" style="object-position:${r.pos || 'center'}"></div>
          <div class="stamp"></div>
          <img src="images/whisk.svg" alt="" class="doodle whisk">
          <img src="images/sparkle.svg" alt="" class="doodle sparkle">
          <img src="images/chili.svg" alt="" class="doodle chili">
        </div>
      </div>
      ${WAVE}
    </section>

    <div class="container section">
      <div class="recipe-layout">
        <article class="recipe-main">
          <section class="lead reveal">${r.intro.map(p => `<p>${p}</p>`).join('')}</section>

          <section class="reveal">
            <h2>Why you'll love it</h2>
            <div class="why-grid">${r.why.map(([t, d], i) => `
              <div class="why-card"><div class="icon-circle">${WHY_ICONS[i % 3]}</div><h3>${t}</h3><p>${d}</p></div>`).join('')}
            </div>
          </section>

          <section id="ingredients" class="ingredients-card reveal">
            <div class="ing-head">
              <h2>Ingredients</h2>
              <div class="scaler no-print"><button data-step="-1" aria-label="Fewer">−</button><span id="serves-label"></span><button data-step="1" aria-label="More">+</button></div>
            </div>
            <p class="ing-note no-print">Tap an ingredient to check it off as you go.</p>
            <div id="ing-groups"></div>
          </section>

          <section id="method" class="reveal">
            <h2>Instructions</h2>
            <p class="hint no-print">Tap a step number to mark it as done.</p>
            <ol class="steps">${r.steps.map((s, i) => `
              <li class="step">
                <div class="step-num" role="button" tabindex="0" aria-label="Mark step ${i + 1} done">${i + 1}</div>
                <div class="step-body">
                  <h3>${s.t}</h3>
                  <p>${s.d}</p>
                  ${s.tip ? `<div class="step-tip">${ICON.bulb}<div><strong>Tip:</strong> ${s.tip}</div></div>` : ''}
                </div>
              </li>`).join('')}
            </ol>
          </section>

          <section class="callout reveal">
            <h2>Tips for success</h2>
            <ul>${r.tips.map(t => `<li>${t}</li>`).join('')}</ul>
          </section>

          <section class="reveal">
            <h2>Make it your own</h2>
            <div class="two-col">
              <div class="info-card">
                <h3>${ICON.swap} Variations</h3>
                <div class="variation-list">${r.variations.map(([t, d]) => `
                  <div class="variation"><div class="icon-circle">${ICON.check}</div><div><strong>${t}</strong><span>${d}</span></div></div>`).join('')}
                </div>
              </div>
              <div class="info-card">
                <h3>${ICON.box} Storage & reheating</h3>
                <p>${r.storage}</p>
              </div>
            </div>
          </section>

          <section class="faq reveal">
            <h2>Recipe FAQ</h2>
            ${r.faq.map(([q, a], i) => `<details ${i === 0 ? 'open' : ''}><summary>${q}</summary><p>${a}</p></details>`).join('')}
          </section>
        </article>

        <aside class="sidebar">
          <div class="side-card">
            <h3>At a glance</h3>
            <div class="glance">
              <div><small>Total time</small><strong>${fmtTime(r.time)}</strong></div>
              <div><small>Difficulty</small><strong>${r.level}</strong></div>
              <div><small>${r.servesLabel ? 'Makes' : 'Serves'}</small><strong>${r.serves} ${r.servesLabel || ''}</strong></div>
              <div><small>Category</small><strong>${r.category}</strong></div>
            </div>
          </div>
          <div class="side-card side-toc no-print">
            <h3>On this page</h3>
            <a href="#ingredients">Ingredients <span>→</span></a>
            <a href="#method">Instructions <span>→</span></a>
            <a href="#nutrition">Nutrition <span>→</span></a>
          </div>
          <div class="side-card" id="nutrition">
            <h3>Nutrition</h3>
            <div class="nutrition-row"><span>Calories</span><b>${n.calories} kcal</b></div>
            <div class="nutrition-row"><span>Protein</span><b>${n.protein} g</b></div>
            <div class="nutrition-row"><span>Carbohydrates</span><b>${n.carbs} g</b></div>
            <div class="nutrition-row"><span>Fat</span><b>${n.fat} g</b></div>
            <div class="nutrition-row"><span>Fiber</span><b>${n.fiber} g</b></div>
            <p class="fine">Per ${r.servesLabel ? 'cookie' : 'serving'}. Estimated values, for reference only.</p>
          </div>
          <div class="side-card side-actions no-print">
            <button class="btn btn-dark" onclick="window.print()">${ICON.print} Print recipe</button>
            <button class="btn btn-outline" id="share-btn">${ICON.share} Share</button>
          </div>
        </aside>
      </div>
    </div>

    <section class="container related">
      <div class="section-head"><h2>You might also like</h2><a href="recipes.html" class="view-all">All recipes →</a></div>
      <div class="recipe-grid three">${related.map(x => cardHTML(x)).join('')}</div>
    </section>`;

  // Servings scaler
  let serves = r.serves;
  const step = r.serves >= 12 ? 6 : 1;
  function renderIngredients() {
    const f = serves / r.serves;
    $('#serves-label').textContent = `${serves} ${unit}`;
    $('#ing-groups').innerHTML = r.ingredients.map(g => `
      <div class="ing-group"><h4>${g.group}</h4><ul class="ing-list">${g.items.map(i => `
        <li><label><input type="checkbox"><span>${i.q != null ? `<b>${fmtQty(i.q * f)}${i.u ? ' ' + i.u : ''}</b> ` : ''}${i.n}${i.note && (f === 1 || !/\d/.test(i.note)) ? ` <em>(${i.note})</em>` : ''}</span></label></li>`).join('')}
      </ul></div>`).join('');
  }
  renderIngredients();
  document.querySelector('.scaler').addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b) return;
    serves = Math.max(step, Math.min(step * 40, serves + Number(b.dataset.step) * step));
    renderIngredients();
  });

  // Step completion
  document.querySelectorAll('.step-num').forEach(el => {
    const toggle = () => el.closest('.step').classList.toggle('done');
    el.addEventListener('click', toggle);
    el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); } });
  });

  // Share
  $('#share-btn').addEventListener('click', async () => {
    const data = { title: r.title, text: r.subtitle, url: location.href };
    if (navigator.share) { try { await navigator.share(data); } catch (_) {} }
    else { await navigator.clipboard.writeText(location.href); $('#share-btn').innerHTML = `${ICON.check} Link copied`; }
  });
}

/* ---------- About ---------- */
function initAbout() {
  const form = $('#contact-form');
  if (!form) return;
  form.addEventListener('submit', e => {
    e.preventDefault();
    const data = new FormData(form);
    const subject = encodeURIComponent('Hello from ' + data.get('name'));
    const body = encodeURIComponent(data.get('message') + '\n\n— ' + data.get('name') + ' (' + data.get('email') + ')');
    window.location.href = `mailto:hello@boredoftoast.com?subject=${subject}&body=${body}`;
    $('#form-note').style.display = 'block';
    form.reset();
  });
}

/* ---------- Boot ---------- */
renderHeader();
if (PAGE === 'home') initHome();
if (PAGE === 'recipes') initRecipes();
if (PAGE === 'recipe') initRecipe();
if (PAGE === 'about') initAbout();
renderFooter();
renderStamps();
bindRandom();
backToTop();
observeReveals();
