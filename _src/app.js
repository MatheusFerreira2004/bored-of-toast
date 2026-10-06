/* Bored of Toast: progressive enhancements for the static pages. */
(function () {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));
  const ROOT = document.body.dataset.root || '';
  const INDEX = window.BOT_INDEX || [];
  const LIST_KEY = 'bot_shopping_v1';
  window.__botReady = true;
  document.documentElement.classList.add('js');

  /* ---------- helpers ---------- */
  function toast(msg) {
    const t = $('#toast-msg'); if (!t) return;
    t.textContent = msg; t.classList.add('show');
    clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove('show'), 2600);
  }
  function fmtQty(q) {
    if (q == null) return '';
    const whole = Math.floor(q + 0.01), frac = q - whole;
    if (frac < 0.07) return String(whole);
    if (frac > 0.9) return String(whole + 1);
    const map = [[0.125, '⅛'], [0.25, '¼'], [0.33, '⅓'], [0.5, '½'], [0.67, '⅔'], [0.75, '¾']];
    let best = map[0], d = 1;
    map.forEach(m => { const x = Math.abs(frac - m[0]); if (x < d) { d = x; best = m; } });
    if (d > 0.08) return String(Math.round(q * 10) / 10);
    return (whole ? whole + ' ' : '') + best[1];
  }
  function roundMetric(v) {
    if (v < 10) return Math.round(v * 10) / 10;
    if (v < 1000) return Math.round(v / 5) * 5;
    return Math.round(v / 10) * 10;
  }
  function qtyText(i, f, units) {
    if (i.q == null) return '';
    const q = i.q * f, u = (i.u || '').toLowerCase();
    if (units === 'metric') {
      if (i.g) return roundMetric(i.g * f) + ' g';
      if (u === 'cup' || u === 'cups') { const ml = q * 240; return ml >= 1000 ? (Math.round(ml / 100) / 10) + ' L' : roundMetric(ml) + ' ml'; }
      if (u === 'oz') return roundMetric(q * 28.35) + ' g';
      if (u === 'lb' || u === 'lbs') return roundMetric(q * 453.6) + ' g';
    }
    return fmtQty(q) + (i.u ? ' ' + i.u : '');
  }
  const getList = () => { try { return JSON.parse(localStorage.getItem(LIST_KEY)) || []; } catch (_) { return []; } };
  const setList = l => { localStorage.setItem(LIST_KEY, JSON.stringify(l)); updateBag(); };
  function updateBag() {
    const n = getList().reduce((a, r) => a + r.items.filter(i => !i.done).length, 0);
    $$('[data-bag-count]').forEach(b => { b.textContent = n; b.hidden = n === 0; });
  }
  function addToList(entry) {
    const l = getList().filter(r => r.id !== entry.id);
    l.push(entry); setList(l);
  }

  /* ---------- header, reveal, images ---------- */
  const header = $('#site-header');
  window.addEventListener('scroll', () => {
    header && header.classList.toggle('scrolled', window.scrollY > 10);
    const tt = $('.to-top'); tt && tt.classList.toggle('show', window.scrollY > 700);
  }, { passive: true });
  const menuButton = $('#menu-toggle'), menu = $('#nav');
  function setMenu(open) {
    if (!menuButton || !menu) return;
    menu.classList.toggle('open', open);
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  menuButton && menuButton.addEventListener('click', () => setMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
  menu && menu.addEventListener('click', e => { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && menu && menu.classList.contains('open')) { setMenu(false); menuButton.focus(); }
  });
  document.addEventListener('click', e => {
    if (menu && menu.classList.contains('open') && !menu.contains(e.target) && !menuButton.contains(e.target)) setMenu(false);
  });
  $('.to-top') && $('.to-top').addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  const io = 'IntersectionObserver' in window ? new IntersectionObserver(es => es.forEach(en => {
    if (en.isIntersecting) { en.target.classList.add('visible'); io.unobserve(en.target); }
  }), { threshold: 0.08 }) : null;
  const observe = () => $$('.reveal:not(.visible)').forEach(el => io ? io.observe(el) : el.classList.add('visible'));
  observe();

  $$('.card-img img, .guide-img img, .arch img').forEach(img => {
    const done = () => img.classList.add('loaded');
    img.complete ? done() : (img.addEventListener('load', done), img.addEventListener('error', done));
  });

  document.addEventListener('click', e => {
    if (e.target.closest('[data-random]')) {
      const recs = INDEX.filter(x => x.k === 'recipe');
      location.href = ROOT + recs[Math.floor(Math.random() * recs.length)].u;
    }
    if (e.target.closest('[data-print]')) window.print();
  });
  updateBag();

  /* ---------- search overlay ---------- */
  const ov = $('#search-overlay'), si = $('#search-input'), sr = $('#search-results');
  function renderSearch() {
    const q = si.value.trim().toLowerCase();
    let res = q ? INDEX.filter(x => x.s.includes(q) || x.t.toLowerCase().includes(q)) : INDEX.filter(x => x.k === 'recipe').slice(0, 6);
    res.sort((a, b) => (b.t.toLowerCase().includes(q) - a.t.toLowerCase().includes(q)));
    res = res.slice(0, 8);
    sr.innerHTML = (q ? '' : '<p class="sr-label">Popular right now</p>') + (res.length ? res.map(x => `
      <a class="sr-item" href="${ROOT}${x.u}"><img src="${ROOT}${x.i}" alt="" width="56" height="56" loading="lazy"><span><strong>${x.t}</strong><small>${x.c} · ${x.m}</small></span></a>`).join('')
      : `<p class="sr-empty">No results for “${si.value}”. Try an ingredient like <b>eggs</b> or <b>chicken</b>.</p>`);
  }
  function openSearch() { if (!ov) return; ov.hidden = false; document.body.style.overflow = 'hidden'; renderSearch(); setTimeout(() => si.focus(), 30); }
  function closeSearch() { if (!ov) return; ov.hidden = true; document.body.style.overflow = ''; }
  document.addEventListener('click', e => {
    if (e.target.closest('[data-open-search]')) { e.preventDefault(); openSearch(); }
    if (e.target.closest('[data-close-search]') || e.target === ov) closeSearch();
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeSearch();
    if (e.key === '/' && !/input|textarea/i.test(document.activeElement.tagName)) { e.preventDefault(); openSearch(); }
  });
  si && si.addEventListener('input', renderSearch);
  si && si.addEventListener('keydown', e => { if (e.key === 'Enter') { const a = $('.sr-item', sr); if (a) location.href = a.href; } });

  /* ---------- recipe listing ---------- */
  const grid = $('#recipe-grid');
  if (grid && $('#chips')) {
    const params = new URLSearchParams(location.search);
    let cat = params.get('cat') || 'all';
    const diets = new Set((params.get('diet') || '').split(',').filter(Boolean));
    const input = $('#list-search'); input.value = params.get('q') || '';
    const cards = $$('.card', grid);
    function apply() {
      const q = input.value.trim().toLowerCase();
      let n = 0;
      cards.forEach(c => {
        const okCat = cat === 'all' || c.dataset.cat === cat || c.dataset.tags.split(' ').includes(cat);
        const cd = c.dataset.diet.split(' ');
        const okDiet = [...diets].every(d => cd.includes(d));
        const okQ = !q || c.dataset.text.includes(q);
        const show = okCat && okDiet && okQ;
        c.hidden = !show; if (show) { n++; c.classList.add('visible'); }
      });
      $$('#chips .chip').forEach(ch => ch.classList.toggle('active', ch.dataset.key === cat));
      $$('#diet-chips .chip').forEach(ch => ch.classList.toggle('active', diets.has(ch.dataset.diet)));
      $('#results-count').textContent = `Showing ${n} of ${cards.length} recipes`;
      $('#empty').style.display = n ? 'none' : 'block';
      const p = new URLSearchParams();
      if (cat !== 'all') p.set('cat', cat); if (diets.size) p.set('diet', [...diets].join(',')); if (q) p.set('q', q);
      history.replaceState(null, '', location.pathname + (p.toString() ? '?' + p : ''));
    }
    $('#chips').addEventListener('click', e => { const c = e.target.closest('.chip'); if (c) { cat = c.dataset.key; apply(); } });
    $('#diet-chips').addEventListener('click', e => { const c = e.target.closest('.chip'); if (c) { const d = c.dataset.diet; diets.has(d) ? diets.delete(d) : diets.add(d); apply(); } });
    input.addEventListener('input', apply);
    $('#clear-filters').addEventListener('click', () => { cat = 'all'; diets.clear(); input.value = ''; apply(); });
    apply();
  }

  /* ---------- single recipe ---------- */
  const rj = $('#recipe-json');
  if (rj) {
    const R = JSON.parse(rj.textContent);
    let serves = R.serves, units = localStorage.getItem('bot_units') || 'us';
    const step = R.serves >= 12 ? 6 : 1;
    const lines = f => R.ingredients.map(g => ({ group: g.group, items: g.items.map(i => {
      const q = qtyText(i, f, units);
      const note = i.note && (f === 1 || !/\d/.test(i.note)) ? i.note : '';
      return { q, n: i.n, note };
    }) }));
    function render() {
      const f = serves / R.serves;
      $('#serves-label').textContent = `${serves} ${R.unit}`;
      $('#print-serves').textContent = `${serves} ${R.unit} · ${units === 'metric' ? 'Metric' : 'US'} measurements`;
      $$('.seg button').forEach(b => b.classList.toggle('active', b.dataset.units === units));
      $('#ing-groups').innerHTML = lines(f).map(g => `<div class="ing-group"><h4>${g.group}</h4><ul class="ing-list">${g.items.map(i =>
        `<li><label><input type="checkbox"><span>${i.q ? `<b>${i.q}</b> ` : ''}${i.n}${i.note ? ` <em>(${i.note})</em>` : ''}</span></label></li>`).join('')}</ul></div>`).join('');
    }
    $('.scaler').addEventListener('click', e => {
      const b = e.target.closest('button'); if (!b) return;
      serves = Math.max(step, Math.min(step * 40, serves + Number(b.dataset.step) * step)); render();
    });
    $('.seg').addEventListener('click', e => {
      const b = e.target.closest('button'); if (!b) return;
      units = b.dataset.units; localStorage.setItem('bot_units', units); render();
    });
    if (units !== 'us') render();

    $('#add-to-list').addEventListener('click', () => {
      const f = serves / R.serves;
      const items = lines(f).flatMap(g => g.items).map(i => ({ t: (i.q ? i.q + ' ' : '') + i.n + (i.note ? ` (${i.note})` : ''), done: false }));
      addToList({ id: R.id, title: R.title, url: R.url, serves: `${serves} ${R.unit}`, items });
      toast('Added to your shopping list ✓');
    });

    let lock = null;
    const cm = $('#cook-mode');
    async function setCook(on) {
      try {
        if (on) { lock = await navigator.wakeLock.request('screen'); lock.addEventListener('release', () => { if (cm.getAttribute('aria-pressed') === 'true') setUI(false); }); }
        else if (lock) { await lock.release(); lock = null; }
        setUI(on); toast(on ? 'Cook mode on: your screen will stay awake' : 'Cook mode off');
      } catch (_) { toast('Cook mode is not supported on this browser'); }
    }
    function setUI(on) { cm.setAttribute('aria-pressed', on); cm.classList.toggle('on', on); cm.lastChild.textContent = ' Cook mode: ' + (on ? 'on' : 'off'); document.body.classList.toggle('cooking', on); }
    cm.addEventListener('click', () => {
      if (!('wakeLock' in navigator)) return toast('Cook mode is not supported on this browser');
      setCook(cm.getAttribute('aria-pressed') !== 'true');
    });
    document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible' && cm.getAttribute('aria-pressed') === 'true' && !lock) setCook(true); });

    $$('.step-num').forEach(el => {
      const t = () => el.closest('.step').classList.toggle('done');
      el.addEventListener('click', t);
      el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); t(); } });
    });
    $('#share-btn').addEventListener('click', async () => {
      const data = { title: R.title, text: document.querySelector('meta[name="description"]').content, url: location.href };
      if (navigator.share) { try { await navigator.share(data); } catch (_) {} }
      else { await navigator.clipboard.writeText(location.href); toast('Link copied ✓'); }
    });
  }

  /* ---------- meal plan ---------- */
  const pj = $('#plan-json');
  if (pj && $('#add-plan')) {
    const dinners = JSON.parse(pj.textContent);
    const status = $('#plan-status');
    function addDinners(recipes) {
      try {
        const existing = getList();
        const additions = recipes.filter(r => !existing.some(saved => saved.id === r.id));
        setList(existing.concat(additions.map(r => ({ id: r.id, title: r.title, url: r.url, serves: r.serves, items: r.items.map(t => ({ t, done: false })) }))));
        status.textContent = additions.length ? `${additions.length} dinner${additions.length === 1 ? '' : 's'} added. Open your shopping list below to review ingredients.` : 'These dinners are already on your list. Your quantities and checked items have been kept.';
      } catch (_) {
        status.textContent = 'Your browser could not save the list. Open a recipe to view or print its ingredients.';
      }
    }
    $('#add-plan').addEventListener('click', () => addDinners(dinners));
    $$('[data-add-dinner]').forEach(b => b.addEventListener('click', () => {
      addDinners(dinners.filter(r => r.id === b.dataset.addDinner));
      status.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }));
  }

  /* ---------- shopping list page ---------- */
  const sl = $('#shopping-list');
  if (sl) {
    function draw() {
      const l = getList();
      $('#list-empty').hidden = l.length > 0;
      $('.list-toolbar').style.display = l.length ? '' : 'none';
      sl.innerHTML = l.map((r, ri) => `
        <div class="list-group">
          <div class="list-head"><a href="${ROOT}${r.url}"><strong>${r.title}</strong></a>${r.serves ? `<small>${r.serves}</small>` : ''}<button class="link-btn" data-remove="${ri}">Remove</button></div>
          <ul class="ing-list">${r.items.map((i, ii) => `<li><label><input type="checkbox" data-r="${ri}" data-i="${ii}" ${i.done ? 'checked' : ''}><span>${i.t}</span></label></li>`).join('')}</ul>
        </div>`).join('');
      updateBag();
    }
    sl.addEventListener('change', e => { const c = e.target; if (c.dataset.r == null) return; const l = getList(); l[c.dataset.r].items[c.dataset.i].done = c.checked; setList(l); });
    sl.addEventListener('click', e => { const b = e.target.closest('[data-remove]'); if (b) { const l = getList(); l.splice(Number(b.dataset.remove), 1); setList(l); draw(); } });
    const asText = () => getList().map(r => `${r.title}${r.serves ? ' (' + r.serves + ')' : ''}\n` + r.items.filter(i => !i.done).map(i => '• ' + i.t).join('\n')).join('\n\n');
    $('#list-copy').addEventListener('click', async () => { await navigator.clipboard.writeText(asText()); toast('Shopping list copied ✓'); });
    $('#list-share').addEventListener('click', async () => {
      if (navigator.share) { try { await navigator.share({ title: 'Shopping list', text: asText() }); } catch (_) {} }
      else { await navigator.clipboard.writeText(asText()); toast('Copied. Paste it anywhere ✓'); }
    });
    $('#list-clear').addEventListener('click', () => { if (confirm('Clear your whole shopping list?')) { setList([]); draw(); } });
    draw();
  }

  /* ---------- contact ---------- */
  const form = $('#contact-form');
  form && form.addEventListener('submit', e => {
    e.preventDefault();
    const d = new FormData(form);
    const subject = encodeURIComponent('Hello from ' + d.get('name'));
    const body = encodeURIComponent(d.get('message') + '\n\n— ' + d.get('name') + ' (' + d.get('email') + ')');
    location.href = `mailto:${form.dataset.email}?subject=${subject}&body=${body}`;
    $('#form-note').style.display = 'block';
  });
})();
