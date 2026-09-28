/* ---------- Recipe data ---------- */
const RECIPES = [
  {
    id: 'chicken-avocado-salad', title: 'Grilled Chicken Avocado Salad', category: 'Salads', tags: ['quick', 'healthy'],
    img: 'images/hero-bowl.jpg', time: 25, level: 'Easy', serves: 2,
    desc: 'Juicy chicken, creamy avocado and peppery greens.',
    ingredients: ['2 boneless chicken breasts', '1 tsp smoked paprika', '1 tsp garlic powder', 'Salt and black pepper', '4 cups arugula and mixed greens', '1 cup cherry tomatoes, halved', '1 ripe avocado, sliced', '1 tbsp sesame seeds', '3 tbsp olive oil', '1 tbsp lemon juice', '1 tsp honey'],
    steps: ['Season the chicken with paprika, garlic powder, salt and pepper.', 'Grill or pan-sear over medium-high heat for 5–6 minutes per side, until cooked through. Rest 5 minutes, then slice.', 'Whisk olive oil, lemon juice, honey and a pinch of salt for the dressing.', 'Toss greens and tomatoes with half the dressing and divide into bowls.', 'Top with chicken and avocado, drizzle with the remaining dressing and finish with sesame seeds.']
  },
  {
    id: 'creamy-garlic-pasta', title: 'Creamy Garlic Pasta', category: 'Main Dishes', tags: ['quick'],
    img: 'images/creamy-garlic-pasta.jpg', time: 20, level: 'Easy', serves: 4,
    desc: 'Rich, comforting and ready in 20 minutes.',
    ingredients: ['12 oz (340 g) fettuccine', '2 tbsp butter', '6 garlic cloves, 3 minced and 3 thinly sliced', '1 cup heavy cream', '¾ cup grated Parmesan', '½ cup reserved pasta water', 'Salt and black pepper', 'Fresh parsley, chopped'],
    steps: ['Cook the pasta in well-salted water until al dente. Reserve ½ cup of pasta water, then drain.', 'Melt butter in a large skillet over medium heat. Add the garlic and cook until golden and fragrant, about 2 minutes.', 'Pour in the cream and simmer gently for 3 minutes.', 'Stir in the Parmesan until smooth, then add the pasta and toss, loosening with pasta water as needed.', 'Season with salt and pepper and finish with parsley and extra Parmesan.']
  },
  {
    id: 'sheet-pan-salmon', title: 'Sheet Pan Salmon', category: 'Main Dishes', tags: ['healthy'],
    img: 'images/sheet-pan-salmon.jpg', time: 30, level: 'Easy', serves: 4,
    desc: 'Fresh, healthy and full of flavor.',
    ingredients: ['4 salmon fillets (about 6 oz each)', '2 tbsp olive oil', '2 tbsp honey', '1 tbsp Dijon mustard', '2 garlic cloves, minced', '1 lemon, thinly sliced', 'Fresh thyme and dill', 'Salt and black pepper'],
    steps: ['Heat the oven to 400°F (200°C) and line a sheet pan with parchment.', 'Arrange the salmon on the pan and season with salt and pepper.', 'Mix olive oil, honey, Dijon and garlic, then brush it over the fillets.', 'Top with lemon slices and herbs.', 'Roast for 12–15 minutes, until the salmon flakes easily with a fork.']
  },
  {
    id: 'mediterranean-grain-bowl', title: 'Mediterranean Grain Bowl', category: 'Salads', tags: ['healthy'],
    img: 'images/grain-bowl.jpg', time: 35, level: 'Medium', serves: 4,
    desc: 'Colorful, fresh and satisfying.',
    ingredients: ['1 cup quinoa, rinsed', '1 can (15 oz) chickpeas, drained', '1 tsp cumin', '1 English cucumber, diced', '1 cup cherry tomatoes, halved', '½ red onion, thinly sliced', '½ cup Kalamata olives', '½ cup crumbled feta', 'Fresh parsley', '3 tbsp olive oil + 2 tbsp lemon juice'],
    steps: ['Cook the quinoa in 2 cups of water for 15 minutes, then fluff and cool slightly.', 'Toss the chickpeas with 1 tbsp olive oil and cumin and roast at 425°F (220°C) for 20 minutes until crisp.', 'Whisk the remaining olive oil with lemon juice, salt and pepper.', 'Divide the quinoa into bowls and arrange chickpeas, cucumber, tomatoes, onion and olives on top.', 'Sprinkle with feta and parsley and drizzle with dressing.']
  },
  {
    id: 'tomato-basil-soup', title: 'Tomato Basil Soup', category: 'Soups', tags: ['healthy'],
    img: 'images/tomato-soup.jpg', time: 30, level: 'Easy', serves: 4,
    desc: 'Simple, flavorful and cozy.',
    ingredients: ['2 tbsp olive oil', '1 yellow onion, chopped', '3 garlic cloves, minced', '2 cans (28 oz) whole peeled tomatoes', '2 cups vegetable broth', '1 tsp sugar', '½ cup fresh basil leaves', '⅓ cup heavy cream', 'Salt and black pepper'],
    steps: ['Heat the olive oil in a pot and cook the onion until soft, about 6 minutes. Add the garlic for 1 minute.', 'Add the tomatoes, broth and sugar. Simmer for 15 minutes.', 'Add the basil and blend until smooth.', 'Stir in the cream and season to taste.', 'Serve with a swirl of cream, fresh basil and crusty bread.']
  },
  {
    id: 'beef-tacos', title: 'Weeknight Beef Tacos', category: 'Main Dishes', tags: ['quick'],
    img: 'images/beef-tacos.jpg', time: 25, level: 'Easy', serves: 4,
    desc: 'Bold flavors, easy to make.',
    ingredients: ['1 lb (450 g) ground beef', '1 tbsp chili powder', '1 tsp cumin', '1 tsp smoked paprika', '½ tsp garlic powder', '8 taco shells', 'Shredded lettuce', '1 cup pico de gallo', '1 cup shredded cheddar', 'Lime wedges and cilantro'],
    steps: ['Brown the beef in a skillet over medium-high heat, breaking it up as it cooks. Drain excess fat.', 'Add the spices with ¼ cup water and simmer for 5 minutes until thick.', 'Warm the taco shells in the oven for 3–4 minutes.', 'Fill with beef, lettuce, pico de gallo and cheese.', 'Serve with lime wedges and cilantro.']
  },
  {
    id: 'chocolate-chip-cookies', title: 'Chewy Chocolate Chip Cookies', category: 'Desserts', tags: [],
    img: 'images/desserts.jpg', pos: '25% 60%', time: 25, level: 'Easy', serves: 24,
    desc: 'Soft, chewy and classic.',
    ingredients: ['1 cup (225 g) butter, melted', '1 cup packed brown sugar', '½ cup granulated sugar', '2 eggs', '2 tsp vanilla extract', '3 cups all-purpose flour', '1 tsp baking soda', '1 tsp salt', '2 cups chocolate chunks', 'Flaky sea salt'],
    steps: ['Heat the oven to 350°F (175°C).', 'Whisk melted butter with both sugars, then beat in the eggs and vanilla.', 'Stir in the flour, baking soda and salt, then fold in the chocolate.', 'Scoop 2-tbsp balls onto lined baking sheets, leaving space between them.', 'Bake for 10–12 minutes until golden at the edges. Sprinkle with sea salt and cool on the pan.']
  },
  {
    id: 'chocolate-mousse-cake', title: 'Chocolate Mousse Cake', category: 'Desserts', tags: [],
    img: 'images/desserts.jpg', pos: '85% 30%', time: 45, level: 'Medium', serves: 10,
    desc: 'Silky, rich and made for celebrations.',
    ingredients: ['20 chocolate sandwich cookies, crushed', '4 tbsp butter, melted', '10 oz (280 g) dark chocolate', '2 cups heavy cream, divided', '3 tbsp powdered sugar', '1 tsp vanilla extract', 'Fresh raspberries and chocolate curls'],
    steps: ['Mix the cookie crumbs with melted butter and press into a 9-inch springform pan. Chill.', 'Melt the chocolate with ½ cup cream and let it cool to room temperature.', 'Whip the remaining cream with powdered sugar and vanilla to soft peaks.', 'Fold the whipped cream into the chocolate in three additions, then spread over the crust.', 'Chill for at least 6 hours, then top with raspberries and chocolate curls.']
  }
];

const CATEGORIES = [
  { key: 'Salads', label: 'Salads', img: 'images/hero-bowl.jpg' },
  { key: 'Main Dishes', label: 'Main Dishes', img: 'images/sheet-pan-salmon.jpg' },
  { key: 'Soups', label: 'Soups', img: 'images/tomato-soup.jpg' },
  { key: 'Desserts', label: 'Desserts', img: 'images/desserts.jpg', pos: '25% 60%' },
  { key: 'quick', label: 'Quick & Easy', img: 'images/creamy-garlic-pasta.jpg' },
  { key: 'healthy', label: 'Healthy', img: 'images/grain-bowl.jpg' }
];

/* ---------- Icons ---------- */
const ICON = {
  clock: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
  chef: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 13.9A4 4 0 0 1 7 6a5 5 0 0 1 10 0 4 4 0 0 1 1 7.9V20H6z"/><path d="M6 17h12"/></svg>',
  users: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6 6 0 0 1 3.5 6"/></svg>',
  arrow: '<svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
  search: '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
  user: '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>',
  menu: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
  instagram: '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
  facebook: '<svg width="19" height="19" viewBox="0 0 24 24" fill="currentColor"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H8v4h2v8h4v-8h3l1-4h-4V8.5c0-.3.2-.5.5-.5z"/></svg>',
  pinterest: '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M9 21l2.5-10"/><path d="M8.5 14.5A5 5 0 1 1 17 11c0 3-1.8 5-4 5-1.4 0-2.2-1-2-2.3"/></svg>',
  youtube: '<svg width="21" height="21" viewBox="0 0 24 24" fill="currentColor"><path d="M22 8.2a3 3 0 0 0-2.1-2.1C18 5.6 12 5.6 12 5.6s-6 0-7.9.5A3 3 0 0 0 2 8.2 31 31 0 0 0 1.6 12a31 31 0 0 0 .4 3.8 3 3 0 0 0 2.1 2.1c1.9.5 7.9.5 7.9.5s6 0 7.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .4-3.8 31 31 0 0 0-.4-3.8zM10 15.1V8.9l5.2 3.1z"/></svg>'
};

/* ---------- Shared header & footer ---------- */
const PAGE = document.body.dataset.page;
const NAV = [['index.html', 'Home', 'home'], ['recipes.html', 'Recipes', 'recipes'], ['about.html', 'About', 'about'], ['about.html#contact', 'Contact', 'contact']];

function renderHeader() {
  const el = document.getElementById('site-header');
  if (!el) return;
  el.className = 'site-header';
  el.innerHTML = `
    <div class="container">
      <a href="index.html" class="brand" aria-label="Bored of Toast home"><img src="images/logo-white.png" alt="Bored of Toast"></a>
      <nav class="nav" id="nav">
        ${NAV.map(([href, label, key]) => `<a href="${href}" class="${key === PAGE ? 'active' : ''}">${label}</a>`).join('')}
        <div class="nav-icons">
          <a href="recipes.html#search" aria-label="Search recipes">${ICON.search}</a>
          <a href="about.html#contact" aria-label="Account">${ICON.user}</a>
        </div>
      </nav>
      <button class="menu-toggle" id="menu-toggle" aria-label="Open menu">${ICON.menu}</button>
    </div>`;
  document.getElementById('menu-toggle').addEventListener('click', () => document.getElementById('nav').classList.toggle('open'));
}

function renderFooter() {
  const el = document.getElementById('site-footer');
  if (!el) return;
  el.className = 'site-footer';
  el.innerHTML = `
    <div class="container">
      <div>
        <a href="index.html" class="brand" aria-label="Bored of Toast home"><img src="images/logo-white.png" alt="Bored of Toast"></a>
        <div class="footer-tagline">Good food without the fuss.</div>
      </div>
      <nav class="footer-nav">${NAV.map(([href, label]) => `<a href="${href}">${label}</a>`).join('')}</nav>
      <div class="socials">
        <a href="#" aria-label="Instagram">${ICON.instagram}</a>
        <a href="#" aria-label="Facebook">${ICON.facebook}</a>
        <a href="#" aria-label="Pinterest">${ICON.pinterest}</a>
        <a href="#" aria-label="YouTube">${ICON.youtube}</a>
      </div>
    </div>
    <div class="copyright">© ${new Date().getFullYear()} Bored of Toast. All rights reserved.</div>
    <img src="images/leaf.svg" alt="" class="leaf">`;
}

/* ---------- Cards & modal ---------- */
function cardHTML(r, showDesc = true) {
  return `
    <article class="card reveal" data-id="${r.id}" tabindex="0">
      <div class="card-img"><img src="${r.img}" alt="${r.title}" loading="lazy" style="object-position:${r.pos || 'center'}"></div>
      <div class="card-body">
        <span class="tag">${r.category}</span>
        <h3>${r.title}</h3>
        ${showDesc ? `<p class="desc">${r.desc}</p>` : ''}
        <div class="meta"><span>${ICON.clock}${r.time} min</span><span>${ICON.chef}${r.level}</span></div>
      </div>
    </article>`;
}

function ensureModal() {
  let modal = document.getElementById('recipe-modal');
  if (modal) return modal;
  modal = document.createElement('div');
  modal.id = 'recipe-modal';
  modal.className = 'modal';
  modal.innerHTML = '<div class="modal-box" role="dialog" aria-modal="true"><button class="close" aria-label="Close">×</button><div class="modal-inner"></div></div>';
  document.body.appendChild(modal);
  modal.addEventListener('click', e => { if (e.target === modal || e.target.classList.contains('close')) closeModal(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
  return modal;
}

function openRecipe(id) {
  const r = RECIPES.find(x => x.id === id);
  if (!r) return;
  const modal = ensureModal();
  modal.querySelector('.modal-inner').innerHTML = `
    <div class="modal-hero"><img src="${r.img}" alt="${r.title}" style="object-position:${r.pos || 'center'}"></div>
    <div class="modal-content">
      <span class="tag">${r.category}</span>
      <h2>${r.title}</h2>
      <div class="meta"><span>${ICON.clock}${r.time} min</span><span>${ICON.chef}${r.level}</span><span>${ICON.users}Serves ${r.serves}</span></div>
      <p style="color:var(--muted)">${r.desc}</p>
      <div class="modal-cols">
        <div><h3>Ingredients</h3><ul>${r.ingredients.map(i => `<li>${i}</li>`).join('')}</ul></div>
        <div><h3>Instructions</h3><ol>${r.steps.map(s => `<li>${s}</li>`).join('')}</ol></div>
      </div>
    </div>`;
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
  history.replaceState(null, '', '#' + r.id);
}

function closeModal() {
  const modal = document.getElementById('recipe-modal');
  if (!modal || !modal.classList.contains('open')) return;
  modal.classList.remove('open');
  document.body.style.overflow = '';
  history.replaceState(null, '', location.pathname + location.search);
}

function bindCards(container) {
  container.addEventListener('click', e => {
    const card = e.target.closest('.card');
    if (card) openRecipe(card.dataset.id);
  });
  container.addEventListener('keydown', e => {
    const card = e.target.closest('.card');
    if (card && e.key === 'Enter') openRecipe(card.dataset.id);
  });
}

/* ---------- Reveal on scroll ---------- */
const observer = new IntersectionObserver(entries => {
  entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add('visible'); observer.unobserve(en.target); } });
}, { threshold: 0.12 });
function observeReveals() { document.querySelectorAll('.reveal:not(.visible)').forEach(el => observer.observe(el)); }

/* ---------- Page: Home ---------- */
function initHome() {
  const cats = document.getElementById('categories');
  cats.innerHTML = CATEGORIES.map(c => `
    <a class="category reveal" href="recipes.html?cat=${encodeURIComponent(c.key)}">
      <div class="circle"><img src="${c.img}" alt="${c.label}" loading="lazy" style="object-position:${c.pos || 'center'}"></div>
      ${c.label}
    </a>`).join('');
  const featured = document.getElementById('featured');
  featured.innerHTML = RECIPES.slice(0, 5).map(r => cardHTML(r, false)).join('');
  bindCards(featured);
}

/* ---------- Page: Recipes ---------- */
function initRecipes() {
  const grid = document.getElementById('recipe-grid');
  const chips = document.getElementById('chips');
  const search = document.getElementById('search');
  const empty = document.getElementById('empty');
  const filters = [['all', 'All'], ['Main Dishes', 'Main Dishes'], ['Salads', 'Salads'], ['Soups', 'Soups'], ['Desserts', 'Desserts'], ['quick', 'Quick & Easy'], ['healthy', 'Healthy']];
  let active = new URLSearchParams(location.search).get('cat') || 'all';

  chips.innerHTML = filters.map(([k, l]) => `<button class="chip" data-key="${k}">${l}</button>`).join('');

  function render() {
    const q = search.value.trim().toLowerCase();
    chips.querySelectorAll('.chip').forEach(c => c.classList.toggle('active', c.dataset.key === active));
    const list = RECIPES.filter(r => {
      const catOk = active === 'all' || r.category === active || r.tags.includes(active);
      const qOk = !q || (r.title + ' ' + r.desc + ' ' + r.ingredients.join(' ')).toLowerCase().includes(q);
      return catOk && qOk;
    });
    grid.innerHTML = list.map(r => cardHTML(r)).join('');
    empty.style.display = list.length ? 'none' : 'block';
    observeReveals();
  }

  chips.addEventListener('click', e => {
    const chip = e.target.closest('.chip');
    if (!chip) return;
    active = chip.dataset.key;
    const url = active === 'all' ? location.pathname : `${location.pathname}?cat=${encodeURIComponent(active)}`;
    history.replaceState(null, '', url);
    render();
  });
  search.addEventListener('input', render);
  bindCards(grid);
  render();

  if (location.hash === '#search') search.focus();
  else if (location.hash) openRecipe(location.hash.slice(1));
}

/* ---------- Page: About ---------- */
function initAbout() {
  const form = document.getElementById('contact-form');
  if (!form) return;
  form.addEventListener('submit', e => {
    e.preventDefault();
    const data = new FormData(form);
    const subject = encodeURIComponent('Hello from ' + data.get('name'));
    const body = encodeURIComponent(data.get('message') + '\n\n— ' + data.get('name') + ' (' + data.get('email') + ')');
    window.location.href = `mailto:hello@boredoftoast.com?subject=${subject}&body=${body}`;
    document.getElementById('form-note').style.display = 'block';
    form.reset();
  });
}

/* ---------- Boot ---------- */
renderHeader();
renderFooter();
if (PAGE === 'home') initHome();
if (PAGE === 'recipes') initRecipes();
if (PAGE === 'about') initAbout();
observeReveals();
