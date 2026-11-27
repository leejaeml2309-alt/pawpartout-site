(function () {
  const grid = document.querySelector('.ev-grid');
  if (!grid) return;
  const cards = Array.from(grid.querySelectorAll('.ev-card'));
  const lis = Array.from(grid.children);
  const shownEl = document.getElementById('ev-shown');
  const resetBtn = document.querySelector('.ev-reset');
  const emptyEl = document.querySelector('.ev-empty');
  const TOTAL = cards.length;

  const state = { category: 'all', country: 'all', species: 'all' };

  function speciesMatch(cardSpecies, filter) {
    if (filter === 'all') return true;
    if (filter === 'Dogs') return cardSpecies.indexOf('Dogs') !== -1;
    if (filter === 'Cats') return cardSpecies.indexOf('Cats') !== -1;
    return cardSpecies === filter;
  }

  function apply() {
    let n = 0;
    lis.forEach(function (li) {
      const card = li.querySelector('.ev-card');
      const okCat = state.category === 'all' || card.getAttribute('data-category') === state.category;
      const okCtry = state.country === 'all' || card.getAttribute('data-country') === state.country;
      const okSp = speciesMatch(card.getAttribute('data-species') || '', state.species);
      const show = okCat && okCtry && okSp;
      li.hidden = !show;
      if (show) n += 1;
    });
    if (shownEl) shownEl.textContent = String(n);
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

  apply();
})();
