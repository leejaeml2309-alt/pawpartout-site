(function () {
  const root = document.querySelector('[data-dossier-filters]');
  if (!root) return;
  const items = Array.from(document.querySelectorAll('.jl-grid > li'));
  const shownEl = document.querySelector('#jl-shown');
  const emptyEl = document.querySelector('[data-dossier-empty]');
  let current = 'all';

  function apply() {
    let n = 0;
    items.forEach(function (li) {
      const card = li.querySelector('[data-dossier]');
      const ok = current === 'all' || (card && card.getAttribute('data-dossier') === current);
      li.hidden = !ok;
      if (ok) n += 1;
    });
    if (shownEl) shownEl.textContent = String(n);
    if (emptyEl) emptyEl.hidden = n !== 0;
  }

  root.querySelectorAll('.jl-pill').forEach(function (btn) {
    btn.addEventListener('click', function () {
      current = btn.getAttribute('data-value') || 'all';
      root.querySelectorAll('.jl-pill').forEach(function (b) {
        b.setAttribute('aria-pressed', b === btn ? 'true' : 'false');
      });
      apply();
    });
  });
  apply();
})();
