/* Pawpartout luxury catalog — grid / shelf navigation + detail modal
   PPCatalog.init() is idempotent and scans [data-pp-catalog] roots.
*/
(function (global) {
  'use strict';

  var SHELF_MQ = '(max-width: 1023px)';
  var FOCUSABLE = 'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])';
  var modalState = null;

  function qs(root, sel) { return (root || document).querySelector(sel); }
  function qsa(root, sel) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  function cardLeft(track, card) {
    return card.getBoundingClientRect().left - track.getBoundingClientRect().left + track.scrollLeft;
  }

  function initCatalog(root) {
    if (root.getAttribute('data-pp-ready') === '1') return;
    var track = qs(root, '[data-pp-track]');
    var nav = qs(root, '[data-pp-nav]');
    if (!track) return;
    var cards = qsa(track, '[data-pp-card]');
    var total = cards.length;
    if (!total) return;
    root.setAttribute('data-pp-ready', '1');

    var prev = nav && qs(nav, '[data-pp-prev]');
    var next = nav && qs(nav, '[data-pp-next]');
    var dotsWrap = nav && qs(nav, '[data-pp-dots]');
    var indexEl = nav && qs(nav, '[data-pp-index]');
    var totalEl = nav && qs(nav, '[data-pp-total]');
    if (totalEl) totalEl.textContent = String(total);

    if (dotsWrap && !dotsWrap.childElementCount) {
      cards.forEach(function (_, i) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'pp-nav-dot';
        b.setAttribute('aria-label', 'Go to item ' + (i + 1) + ' of ' + total);
        b.addEventListener('click', function () { go(i); });
        dotsWrap.appendChild(b);
      });
    }

    var ticking = false;

    function indexFromScroll() {
      var x = track.scrollLeft;
      var best = 0, bestDist = Infinity;
      for (var i = 0; i < total; i++) {
        var d = Math.abs(cardLeft(track, cards[i]) - x);
        if (d < bestDist) { bestDist = d; best = i; }
      }
      return best;
    }

    function go(i) {
      i = Math.max(0, Math.min(total - 1, i));
      track.scrollTo({ left: cardLeft(track, cards[i]), behavior: 'smooth' });
    }

    function sync() {
      var i = indexFromScroll();
      if (indexEl) indexEl.textContent = String(i + 1);
      qsa(dotsWrap, '.pp-nav-dot').forEach(function (dot, n) {
        var on = n === i;
        dot.classList.toggle('is-on', on);
        if (on) dot.setAttribute('aria-current', 'true');
        else dot.removeAttribute('aria-current');
      });
      if (prev) prev.disabled = i <= 0;
      if (next) next.disabled = i >= total - 1;
    }

    if (prev) prev.addEventListener('click', function () { go(indexFromScroll() - 1); });
    if (next) next.addEventListener('click', function () { go(indexFromScroll() + 1); });

    track.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () { ticking = false; sync(); });
    }, { passive: true });

    track.addEventListener('keydown', function (e) {
      if (!window.matchMedia(SHELF_MQ).matches) return;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { e.preventDefault(); go(indexFromScroll() + 1); }
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); go(indexFromScroll() - 1); }
      else if (e.key === 'Home') { e.preventDefault(); go(0); }
      else if (e.key === 'End') { e.preventDefault(); go(total - 1); }
    });

    track.addEventListener('wheel', function (e) {
      if (!window.matchMedia(SHELF_MQ).matches) return;
      if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
      var atStart = track.scrollLeft <= 1;
      var atEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - 1;
      if ((e.deltaY < 0 && atStart) || (e.deltaY > 0 && atEnd)) return;
      e.preventDefault();
      track.scrollLeft += e.deltaY;
    }, { passive: false });

    if (!track.hasAttribute('tabindex')) track.setAttribute('tabindex', '0');

    window.addEventListener('resize', sync);
    sync();
  }

  function initModal() {
    var dialog = qs(document, '#pp-catalog-modal');
    if (!dialog || dialog.getAttribute('data-pp-ready') === '1') return;
    dialog.setAttribute('data-pp-ready', '1');
    var body = qs(dialog, '[data-pp-modal-body]');
    var closeBtn = qs(dialog, '[data-pp-close]');

    function unlock() {
      document.documentElement.classList.remove('pp-modal-open');
      if (!modalState) return;
      var s = modalState;
      modalState = null;
      if (s.detail && s.parent) {
        s.detail.hidden = true;
        s.parent.appendChild(s.detail);
      }
      if (s.trigger && typeof s.trigger.focus === 'function') {
        try { s.trigger.focus(); } catch (err) {}
      }
    }

    function openFrom(card, trigger) {
      var detail = qs(card, '.pp-card-detail');
      if (!detail || !body) return;
      if (dialog.open) dialog.close();
      modalState = { detail: detail, parent: detail.parentNode, trigger: trigger || qs(card, '.pp-card-cta') || card };
      detail.hidden = false;
      var title = qs(detail, '.pp-detail-title');
      if (title) {
        if (!title.id) title.id = 'pp-modal-title';
        dialog.setAttribute('aria-labelledby', title.id);
      }
      body.appendChild(detail);
      document.documentElement.classList.add('pp-modal-open');
      if (typeof dialog.showModal === 'function') dialog.showModal();
      else dialog.setAttribute('open', '');
      if (closeBtn) closeBtn.focus();
    }

    function requestClose() {
      if (dialog.open) dialog.close();
      else unlock();
    }

    dialog.addEventListener('close', unlock);

    dialog.addEventListener('click', function (e) {
      if (e.target === dialog) requestClose();
    });

    if (closeBtn) closeBtn.addEventListener('click', requestClose);

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && (dialog.open || modalState)) {
        e.preventDefault();
        requestClose();
      }
    });

    document.addEventListener('click', function (e) {
      var card = e.target.closest && e.target.closest('[data-pp-card]');
      if (!card) return;
      if (e.target.closest('a')) return;
      var trigger = e.target.closest('.pp-card-cta') || qs(card, '.pp-card-cta') || card;
      openFrom(card, trigger);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter' && e.key !== ' ') return;
      var card = e.target.closest && e.target.closest('[data-pp-card]');
      if (!card) return;
      if (e.target.closest('a')) return;
      if (e.target.classList && e.target.classList.contains('pp-card-cta') || e.target === card || e.target.closest('.pp-card-face')) {
        e.preventDefault();
        openFrom(card, e.target.classList.contains('pp-card-cta') ? e.target : qs(card, '.pp-card-cta'));
      }
    });

    global.PPCatalog.openCard = openFrom;
    global.PPCatalog.close = requestClose;
  }

  function init() {
    qsa(document, '[data-pp-catalog]').forEach(initCatalog);
    initModal();
  }

  global.PPCatalog = { init: init };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})(window);
