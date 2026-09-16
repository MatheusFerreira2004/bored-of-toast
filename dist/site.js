// Print handlers
document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => window.print()));

// Smooth in-page scrolling for anchor clicks without leaving a hash that triggers automatic scroll on reload
document.querySelectorAll('a[href*="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const url = new URL(this.href, window.location.href);
    if (url.pathname === window.location.pathname && url.hash && url.hash.length > 1) {
      const target = document.querySelector(url.hash);
      if (target) {
        e.preventDefault();
        if(target.tagName==='DETAILS')target.open=true;
        target.scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth' });
        if (window.history.replaceState) {
          window.history.replaceState(null, '', window.location.pathname + window.location.search);
        }
      }
    }
  });
});

// Prevent browser from automatically jumping or smooth-scrolling on page reload
if (window.location.hash && window.history.replaceState) {
  window.history.replaceState(null, '', window.location.pathname + window.location.search);
}
if ('scrollRestoration' in history) {
  history.scrollRestoration = 'manual';
}

// Elements remain visible without JavaScript. Enter once when they reach view.
const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
if (!motionPreference.matches && 'IntersectionObserver' in window) {
  const entranceObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('enter-once');
      entranceObserver.unobserve(entry.target);
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.section-top, .recipe-card, .notes-copy, .future-note, .footer-statement, .recipe-box, .note-row, .swaps-card, .tips-card, .guidance-panel, .home-path-card').forEach(element => entranceObserver.observe(element));
  motionPreference.addEventListener('change', event => {
    if (event.matches) {
      entranceObserver.disconnect();
      document.querySelectorAll('.enter-once').forEach(element => element.classList.remove('enter-once'));
    }
  });
}

// ---------------------------------------------------------------------------
// Category descriptions (must mirror CATEGORIES in build.py)
// ---------------------------------------------------------------------------
const CATEGORY_DESCS = {
  'quick-easy':     'Short active prep and few steps — ready in 25 minutes or less. Overnight resting is noted separately.',
  'budget-friendly':'Meals built around pantry staples and everyday affordable ingredients.',
  'plant-forward':  'Vegetables, fruits, grains, and legumes take the lead. Not necessarily vegan.',
  'protein-forward':'Recipes centred on legumes, eggs, tofu, or other protein sources.',
  'make-ahead':     'Suited to preparing in advance or starting the night before — breakfast included.',
  'pantry-meals':   'Built around shelf-stable ingredients you are likely to have at home.',
  'fresh-lunches':  'No-cook or minimal-cook options that feel light and lively at midday.',
  'cozy-dinners':   'Warm skillet and stovetop meals that are comforting after a long day.',
};

// ---------------------------------------------------------------------------
// Category filter for /recipes/ page
// Reads ?category= (or legacy ?cat=) from the URL.
// Shows matching cards, updates pill state and active description.
// No-JS fallback: all cards remain visible (server renders them all).
// ---------------------------------------------------------------------------
(function initCategoryFilter() {
  const grid = document.getElementById('recipe-grid');
  if (!grid) return; // not on /recipes/ page

  const filterList = document.querySelector('.cat-filter-list');
  const emptyState = document.getElementById('empty-state');
  const statusLabel = document.getElementById('active-filter-label');
  const catDesc = document.getElementById('active-cat-desc');

  function getActiveSlug() {
    try {
      const params = new URLSearchParams(window.location.search);
      // Support both ?category= (new) and ?cat= (legacy)
      return params.get('category') || params.get('cat') || '';
    } catch (e) {
      return '';
    }
  }

  function applyFilter(slug) {
    const cards = Array.from(grid.querySelectorAll('.recipe-card[data-categories]'));

    // Update pills
    if (filterList) {
      filterList.querySelectorAll('.cat-pill').forEach(pill => {
        const href = pill.getAttribute('href') || '';
        let pillSlug = '';
        try {
          const pillUrl = new URL(href, window.location.href);
          pillSlug = pillUrl.searchParams.get('category') || pillUrl.searchParams.get('cat') || '';
        } catch(e) {}
        const active = pillSlug === slug;
        pill.classList.toggle('is-active', active);
        pill.setAttribute('aria-current', active ? 'true' : 'false');
        // "All recipes" pill (no ?category)
        if (pill.id === 'cat-all') {
          const allActive = slug === '';
          pill.classList.toggle('is-active', allActive);
          pill.setAttribute('aria-current', allActive ? 'true' : 'false');
        }
      });
    }

    // Filter cards
    let visibleCount = 0;
    cards.forEach(card => {
      const cats = (card.getAttribute('data-categories') || '').split(' ').filter(Boolean);
      const show = slug === '' || cats.includes(slug);
      card.hidden = !show;
      if (show) visibleCount++;
    });

    // Empty state
    if (emptyState) {
      emptyState.hidden = visibleCount > 0;
    }

    // Status label and category description
    if (statusLabel) {
      if (slug === '') {
        statusLabel.textContent = `All ${cards.length} recipes`;
        if (catDesc) { catDesc.hidden = true; catDesc.textContent = ''; }
      } else {
        const pill = filterList && filterList.querySelector(`#cat-${slug}`);
        const label = pill ? pill.textContent.replace(/\(\d+\)/, '').trim() : slug;
        const noun = visibleCount === 1 ? 'recipe' : 'recipes';
        statusLabel.textContent = `${label} — ${visibleCount} ${noun}`;
        if (catDesc) {
          const desc = CATEGORY_DESCS[slug] || '';
          catDesc.textContent = desc;
          catDesc.hidden = !desc;
        }
      }
    }
  }

  // Handle pill clicks via History API — no full page reload
  if (filterList) {
    filterList.addEventListener('click', e => {
      const pill = e.target.closest('.cat-pill');
      if (!pill) return;
      e.preventDefault();
      const href = pill.getAttribute('href');
      const url = new URL(href, window.location.href);
      const slug = url.searchParams.get('category') || url.searchParams.get('cat') || '';
      history.pushState({ category: slug }, '', href);
      applyFilter(slug);
    });
  }

  // Handle browser back/forward
  window.addEventListener('popstate', () => {
    applyFilter(getActiveSlug());
  });

  // Initial render
  applyFilter(getActiveSlug());
})();

// Measure the real sticky header, including font loading and wrapped mobile links.
(function initStickyMeasurements(){
  const header=document.querySelector('body > header');
  const filters=document.querySelector('.recipe-index-body .cat-filter');
  if(!header)return;
  const update=()=>{
    const height=Math.ceil(header.getBoundingClientRect().height);
    document.documentElement.style.setProperty('--site-header-height',height+'px');
    if(filters)filters.setAttribute('data-sticky-ready','');
  };
  update();
  if('ResizeObserver' in window)new ResizeObserver(update).observe(header);
  window.addEventListener('resize',update,{passive:true});
  if(document.fonts)document.fonts.ready.then(update);
})();
