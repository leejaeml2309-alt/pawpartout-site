(function () {
  const grid = document.querySelector('.ev-grid');
  if (!grid) return;
  const lis = Array.from(grid.children);
  const shownEl = document.getElementById('ev-shown');
  const totalEl = document.getElementById('ev-total');
  const countEl = document.querySelector('.ev-count');
  const resetBtn = document.querySelector('.ev-reset');
  const emptyEl = document.querySelector('.ev-empty');

  const state = { category: 'all', country: 'all', species: 'all' };

  function todayISO() {
    const d = new Date();
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return y + '-' + m + '-' + day;
  }

  const today = todayISO();

  function isExpired(card) {
    const end = card && card.getAttribute('data-end-date');
    return !!(end && end < today);
  }

  const liveLis = [];
  lis.forEach(function (li) {
    const card = li.querySelector('.ev-card');
    if (!card || isExpired(card)) {
      li.hidden = true;
      li.setAttribute('data-expired', 'true');
    } else {
      liveLis.push(li);
    }
  });

  function speciesMatch(cardSpecies, filter) {
    if (filter === 'all') return true;
    if (filter === 'Dogs') return cardSpecies.indexOf('Dogs') !== -1;
    if (filter === 'Cats') return cardSpecies.indexOf('Cats') !== -1;
    return cardSpecies === filter;
  }

  function updatePillCounts() {
    const catCounts = {};
    liveLis.forEach(function (li) {
      const card = li.querySelector('.ev-card');
      const cat = card.getAttribute('data-category') || '';
      catCounts[cat] = (catCounts[cat] || 0) + 1;
    });
    document.querySelectorAll('.ev-pill[data-group="category"]').forEach(function (btn) {
      const value = btn.getAttribute('data-value');
      const n = value === 'all' ? liveLis.length : (catCounts[value] || 0);
      const label = btn.textContent.replace(/\s*\(\d+\)\s*$/, '');
      btn.textContent = label + ' (' + n + ')';
    });
    if (totalEl) totalEl.textContent = String(liveLis.length);
    else if (countEl) {
      countEl.innerHTML = 'Showing <span id="ev-shown">' + (shownEl ? shownEl.textContent : '0') + '</span> of <span id="ev-total">' + liveLis.length + '</span> events';
    }
  }

  function apply() {
    let n = 0;
    liveLis.forEach(function (li) {
      const card = li.querySelector('.ev-card');
      const okCat = state.category === 'all' || card.getAttribute('data-category') === state.category;
      const okCtry = state.country === 'all' || card.getAttribute('data-country') === state.country;
      const okSp = speciesMatch(card.getAttribute('data-species') || '', state.species);
      const show = okCat && okCtry && okSp;
      li.hidden = !show;
      if (show) n += 1;
    });
    lis.forEach(function (li) {
      if (li.getAttribute('data-expired') === 'true') li.hidden = true;
    });
    const shown = document.getElementById('ev-shown');
    if (shown) shown.textContent = String(n);
    const total = document.getElementById('ev-total');
    if (total) total.textContent = String(liveLis.length);
    const filtered = state.category !== 'all' || state.country !== 'all' || state.species !== 'all';
    if (resetBtn) resetBtn.hidden = !filtered;
    if (emptyEl) emptyEl.hidden = n !== 0;
  }

  function setGroup(group, value) {
    state[group] = value;
    document.querySelectorAll('.ev-pill[data-group="' + group + '"]').forEach(function (btn) {
      btn.setAttribute('aria-pressed', btn.getAttribute('data-value') === value ? 'true' : 'false');
    });
    apply();
  }

  document.querySelectorAll('.ev-pill').forEach(function (btn) {
    btn.addEventListener('click', function () {
      setGroup(btn.getAttribute('data-group'), btn.getAttribute('data-value'));
    });
  });

  if (resetBtn) {
    resetBtn.addEventListener('click', function () {
      setGroup('category', 'all');
      setGroup('country', 'all');
      setGroup('species', 'all');
    });
  }

  updatePillCounts();
  apply();
})();
