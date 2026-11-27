(function () {
  const root = document.querySelector('[data-stay-filters]');
  if (!root) return;
  const items = Array.from(document.querySelectorAll('.st-stays > li'));
  const shownEl = document.querySelector('#st-stay-shown');
  const resetBtn = document.querySelector('[data-stay-reset]');
  const testers = [
    { group: 'country', attr: 'data-country' },
    { group: 'species', attr: 'data-species' },
    { group: 'type', attr: 'data-type' }
  ];
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
    document.querySelectorAll('[data-section-empty]').forEach(function (el) {
      const sel = el.getAttribute('data-section-empty');
      const visible = document.querySelectorAll(sel + ' > li:not([hidden])').length;
      el.hidden = visible !== 0;
    });
  }

  function setGroup(group, value) {
    state[group] = value;
    root.querySelectorAll('.st-pill[data-group="' + group + '"]').forEach(function (btn) {
      btn.setAttribute('aria-pressed', btn.getAttribute('data-value') === value ? 'true' : 'false');
    });
    apply();
  }

  root.querySelectorAll('.st-pill').forEach(function (btn) {
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
})();
