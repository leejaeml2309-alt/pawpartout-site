(function () {
  function bindFilter(rootSel, itemSel, shownSel, resetSel, emptySel, testers) {
    const root = document.querySelector(rootSel);
    if (!root) return;
    const items = Array.from(document.querySelectorAll(itemSel));
    const shownEl = document.querySelector(shownSel);
    const resetBtn = document.querySelector(resetSel);
    const emptyEl = document.querySelector(emptySel);
    const state = {};
    testers.forEach(function (t) { state[t.group] = 'all'; });

    function apply() {
      let n = 0;
      items.forEach(function (li) {
        const card = li.querySelector('[data-filter-item]') || li.firstElementChild;
        const ok = testers.every(function (t) {
          const want = state[t.group];
          if (want === 'all') return true;
          return (card.getAttribute(t.attr) || '') === want;
        });
        li.hidden = !ok;
        if (ok) n += 1;
      });
      if (shownEl) shownEl.textContent = String(n);
      const filtered = testers.some(function (t) { return state[t.group] !== 'all'; });
      if (resetBtn) resetBtn.hidden = !filtered;
      if (emptyEl) emptyEl.hidden = n !== 0;
    }

    function setGroup(group, value) {
      state[group] = value;
      root.querySelectorAll('.cm-pill[data-group="' + group + '"]').forEach(function (btn) {
        btn.setAttribute('aria-pressed', btn.getAttribute('data-value') === value ? 'true' : 'false');
      });
      apply();
    }

    root.querySelectorAll('.cm-pill').forEach(function (btn) {
      btn.addEventListener('click', function () {
        setGroup(btn.getAttribute('data-group'), btn.getAttribute('data-value'));
      });
    });
    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        testers.forEach(function (t) { setGroup(t.group, 'all'); });
      });
    }
    apply();
  }

  bindFilter(
    '[data-spot-filters]',
    '.cm-spots > li',
    '#cm-spot-shown',
    '[data-spot-reset]',
    '[data-spot-empty]',
    [
      { group: 'country', attr: 'data-country' },
      { group: 'type', attr: 'data-type' },
      { group: 'species', attr: 'data-species' }
    ]
  );

  bindFilter(
    '[data-gear-filters]',
    '.cm-gear > li',
    '#cm-gear-shown',
    '[data-gear-reset]',
    '[data-gear-empty]',
    [
      { group: 'subtheme', attr: 'data-subtheme' }
    ]
  );
})();
