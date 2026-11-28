/* Pawpartout: the gold rosace, drawn with exact geometry in SVG (no images).
   Flower of Life: 19 circles of radius r, centred on a hexagonal grid
   (the centre, 6 at distance r, 6 at distance 2r, 6 at distance r·√3), inside an outer circle of radius 3r.
   Gold relief is built from stacked strokes (shadow, dark lower edge, pale upper edge, gold body, specular line);
   on wide screens a feSpecularLighting filter adds real lighting on top. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var root = document.documentElement;
  var style = 'mandala';                       /* the only style on Pawpartout */
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var TAU = Math.PI * 2;
  function f(n) { return (Math.round(n * 100) / 100).toString(); }
  function P(r, a) { return [r * Math.cos(a), r * Math.sin(a)]; }
  function circ(cx, cy, r) { return 'M' + f(cx + r) + ' ' + f(cy) + 'A' + f(r) + ' ' + f(r) + ' 0 1 0 ' + f(cx - r) + ' ' + f(cy) + 'A' + f(r) + ' ' + f(r) + ' 0 1 0 ' + f(cx + r) + ' ' + f(cy) + 'Z'; }

  /* the 19 Flower-of-Life centres (pointy-top hexagonal grid, a petal pointing to the top door) */
  function flowerCentres(r) {
    var c = [[0, 0]], k, a;
    for (k = 0; k < 6; k++) { a = -Math.PI / 2 + k * Math.PI / 3; c.push(P(r, a)); }
    for (k = 0; k < 6; k++) { a = -Math.PI / 2 + k * Math.PI / 3; c.push(P(2 * r, a)); }
    for (k = 0; k < 6; k++) { a = -Math.PI / 2 + Math.PI / 6 + k * Math.PI / 3; c.push(P(r * Math.sqrt(3), a)); }
    return c;
  }

  /* ---------- gold material ---------- */
  function defs(sc) {
    return '<defs>' +
      '<linearGradient id="gBody" gradientUnits="userSpaceOnUse" x1="-420" y1="-480" x2="420" y2="480">' +
      '<stop offset="0" stop-color="#7a4f12"/><stop offset=".1" stop-color="#c38f2c"/><stop offset=".2" stop-color="#f7dc8a"/>' +
      '<stop offset=".28" stop-color="#d4a13a"/><stop offset=".42" stop-color="#8f6118"/><stop offset=".52" stop-color="#d7a640"/>' +
      '<stop offset=".6" stop-color="#fff3c0"/><stop offset=".68" stop-color="#e8c05a"/><stop offset=".8" stop-color="#9a6a1c"/>' +
      '<stop offset=".9" stop-color="#cf9d36"/><stop offset="1" stop-color="#f1cf72"/></linearGradient>' +
      '<linearGradient id="gHi" gradientUnits="userSpaceOnUse" x1="-500" y1="-500" x2="500" y2="500">' +
      '<stop offset="0" stop-color="#fffbe8"/><stop offset=".5" stop-color="#ffe9a6"/><stop offset="1" stop-color="#f6d98a"/></linearGradient>' +
      '<radialGradient id="gBead" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#fffbe2"/><stop offset=".25" stop-color="#f6d77e"/>' +
      '<stop offset=".6" stop-color="#c08a26"/><stop offset="1" stop-color="#6e470e"/></radialGradient>' +
      '<radialGradient id="gFill" gradientUnits="userSpaceOnUse" cx="-120" cy="-160" r="620"><stop offset="0" stop-color="#ffeaa8"/>' +
      '<stop offset=".35" stop-color="#e0ae45"/><stop offset=".7" stop-color="#a9761f"/><stop offset="1" stop-color="#6f4710"/></radialGradient>' +
      '<filter id="vShadow" x="-10%" y="-10%" width="120%" height="125%"><feGaussianBlur stdDeviation="' + f(5 * sc) + '"/></filter>' +
      '<filter id="vSpec" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">' +
      '<feGaussianBlur in="SourceAlpha" stdDeviation="' + f(2.2 * sc) + '" result="b"/>' +
      '<feSpecularLighting in="b" surfaceScale="4" specularConstant="1.05" specularExponent="24" lighting-color="#fff6d8" result="s">' +
      '<feDistantLight azimuth="225" elevation="42"/></feSpecularLighting>' +
      '<feComposite in="s" in2="SourceAlpha" operator="in" result="s2"/>' +
      '<feComposite in="SourceGraphic" in2="s2" operator="arithmetic" k1="0" k2="1" k3=".9" k4="0"/></filter>' +
      '<linearGradient id="gSheen" gradientUnits="userSpaceOnUse" x1="-160" y1="0" x2="160" y2="0" gradientTransform="rotate(-32) translate(-1300 0)">' +
      '<stop offset="0" stop-color="#fff8dc" stop-opacity="0"/><stop offset=".5" stop-color="#fffdf0" stop-opacity=".85"/>' +
      '<stop offset="1" stop-color="#fff8dc" stop-opacity="0"/>' +
      (reduce ? '' : '<animateTransform attributeName="gradientTransform" type="translate" additive="sum" values="0 0;0 0;2600 0" keyTimes="0;.45;1" dur="11s" repeatCount="indefinite"/>') +
      '</linearGradient></defs>';
  }

  /* A collection of gold parts. strokes: [d, width]; fills: [d] */
  function Gold() { this.s = []; this.fl = []; }
  Gold.prototype.band = function (d, w) { this.s.push([d, w]); return this; };
  Gold.prototype.fill = function (d) { this.fl.push(d); return this; };
  Gold.prototype.render = function (sc) {
    var o = 1.5 * sc, i, out = [];
    function layer(cls, inner) { out.push('<g class="' + cls + '">' + inner + '</g>'); }
    function S(w, attrs) { var h = ''; for (i = 0; i < this.s.length; i++) h += '<path d="' + this.s[i][0] + '" fill="none" stroke-width="' + f(w(this.s[i][1])) + '"' + (attrs || '') + '/>'; return h; }
    function F(attrs) { var h = ''; for (i = 0; i < this.fl.length; i++) h += '<path d="' + this.fl[i] + '"' + (attrs || '') + '/>'; return h; }
    var me = this, s = function (w, a) { return S.call(me, w, a); }, fl = function (a) { return F.call(me, a); };
    /* 1. cast shadow on the navy */
    layer('g-shadow', '<g transform="translate(' + f(2 * sc) + ' ' + f(7 * sc) + ')" fill="#000" stroke="#000" opacity=".6">' + s(function (w) { return w + 3 * sc; }) + fl() + '</g>');
    /* 2. dark lower edge, 3. pale upper edge (light from the top left) */
    layer('g-dark', '<g transform="translate(' + f(o) + ' ' + f(o * 1.3) + ')" fill="#3a2205" stroke="#3a2205">' + s(function (w) { return w + 1.2 * sc; }) + fl() + '</g>');
    layer('g-light', '<g transform="translate(' + f(-o) + ' ' + f(-o * 1.3) + ')" fill="url(#gHi)" stroke="url(#gHi)">' + s(function (w) { return w + 0.6 * sc; }) + fl() + '</g>');
    /* 4. the gold body (+ specular lighting on wide screens) */
    layer('g-body', '<g stroke="url(#gBody)" fill="url(#gFill)">' + s(function (w) { return Math.max(1, w - 1.4 * sc); }) + fl(' stroke-width="' + f(1.2 * sc) + '"') + '</g>');
    /* 5. a fine polished ridge along each band */
    layer('g-ridge', '<g transform="translate(' + f(-0.5 * sc) + ' ' + f(-0.7 * sc) + ')" stroke="#fff3c0" stroke-opacity=".55" fill="none">' + s(function (w) { return Math.max(.6, w * .16); }) + '</g>');
    return out.join('');
  };
  Gold.prototype.sheen = function (sc) {
    var h = '<g stroke="url(#gSheen)" fill="url(#gSheen)">', i;
    for (i = 0; i < this.s.length; i++) h += '<path d="' + this.s[i][0] + '" fill="none" stroke-width="' + f(this.s[i][1]) + '"/>';
    for (i = 0; i < this.fl.length; i++) h += '<path d="' + this.fl[i] + '" stroke="none"/>';
    return h + '</g>';
  };

  /* ---------- the Flower of Life inside an Art Nouveau mandala ---------- */
  function mandala(sc) {
    var g = new Gold(), r = 80, C = flowerCentres(r), d = '', seed = '', i, k, a;
    for (i = 0; i < C.length; i++) { if (i < 7) seed += circ(C[i][0], C[i][1], r); else d += circ(C[i][0], C[i][1], r); }
    g.band(d, 6 * sc).band(seed, 8 * sc).band(circ(0, 0, 3 * r), 12 * sc);       /* Flower of Life, R = 240 */
    g.band(circ(0, 0, 252), 4 * sc);
    /* petal ring: 20 flame-shaped (ogee) petals between r 256 and 312, each with a carved vein,
       and 20 small buds between them */
    var pet = '', vein = '', small = '';
    for (k = 0; k < 20; k++) {
      a = -Math.PI / 2 + k * TAU / 20;
      var b0 = P(257, a - .088), b1 = P(257, a + .088), t = P(314, a);
      var c0 = P(286, a - .135), c1 = P(300, a - .012), c2 = P(300, a + .012), c3 = P(286, a + .135);
      pet += 'M' + f(b0[0]) + ' ' + f(b0[1]) + 'C' + f(c0[0]) + ' ' + f(c0[1]) + ' ' + f(c1[0]) + ' ' + f(c1[1]) + ' ' + f(t[0]) + ' ' + f(t[1]) +
             'C' + f(c2[0]) + ' ' + f(c2[1]) + ' ' + f(c3[0]) + ' ' + f(c3[1]) + ' ' + f(b1[0]) + ' ' + f(b1[1]) + 'Z';
      var v0 = P(264, a), v1 = P(284, a - .045), v2 = P(296, a);
      vein += 'M' + f(v0[0]) + ' ' + f(v0[1]) + 'Q' + f(v1[0]) + ' ' + f(v1[1]) + ' ' + f(v2[0]) + ' ' + f(v2[1]);
      var a2 = a + TAU / 40, s0 = P(258, a2 - .035), s1 = P(258, a2 + .035), st = P(280, a2), sc0 = P(272, a2 - .05), sc1 = P(272, a2 + .05);
      small += 'M' + f(s0[0]) + ' ' + f(s0[1]) + 'Q' + f(sc0[0]) + ' ' + f(sc0[1]) + ' ' + f(st[0]) + ' ' + f(st[1]) + 'Q' + f(sc1[0]) + ' ' + f(sc1[1]) + ' ' + f(s1[0]) + ' ' + f(s1[1]) + 'Z';
    }
    g.fill(pet).fill(small);
    g.veins = vein;
    /* whiplash ring: 10 lyres of two mirrored coup-de-fouet curves, each ending in a curl */
    var wh = '';
    for (k = 0; k < 10; k++) {
      var cA = -Math.PI / 2 + k * TAU / 10 + TAU / 20;
      [-1, 1].forEach(function (sg) {
        var w0 = P(318, cA), w1 = P(336, cA + sg * .05), w2 = P(318, cA + sg * .17), w3 = P(334, cA + sg * .24);
        var cc = P(326, cA + sg * .26);
        wh += 'M' + f(w0[0]) + ' ' + f(w0[1]) + 'C' + f(w1[0]) + ' ' + f(w1[1]) + ' ' + f(w2[0]) + ' ' + f(w2[1]) + ' ' + f(w3[0]) + ' ' + f(w3[1]) +
              'A6 6 0 1 ' + (sg > 0 ? 1 : 0) + ' ' + f(cc[0]) + ' ' + f(cc[1]);
      });
    }
    g.band(wh, 4 * sc);
    /* beaded border: 60 pearls */
    var beads = [];
    for (k = 0; k < 60; k++) beads.push(P(350, -Math.PI / 2 + k * TAU / 60));
    g.beads = beads;
    g.band(circ(0, 0, 342), 3 * sc).band(circ(0, 0, 362), 9 * sc);
    return g;
  }

  function draw() {
    var svg = document.getElementById('flower'), sh = document.getElementById('sheen');
    if (!svg) return;
    var px = svg.getBoundingClientRect().width || 640;
    var sc = (px < 420 && window.innerWidth <= 640) ? 1.45 : 1;  /* thicker bands on phones so the gold still reads */
    var g = mandala(sc);
    var h = g.render(sc);
    if (g.veins) h += '<path d="' + g.veins + '" fill="none" stroke="#5a3a0b" stroke-width="' + f(2.2 * sc) + '" stroke-linecap="round"/>' +
      '<path d="' + g.veins + '" fill="none" stroke="#fff1bf" stroke-opacity=".7" stroke-width="' + f(.9 * sc) + '" stroke-linecap="round" transform="translate(-1 -1.2)"/>';
    if (g.beads) {
      var bs = '', bb = '', R = 4.8;
      g.beads.forEach(function (q) {
        bs += '<circle cx="' + f(q[0] + 1.5 * sc) + '" cy="' + f(q[1] + 4 * sc) + '" r="' + R + '"/>';
        bb += '<circle cx="' + f(q[0]) + '" cy="' + f(q[1]) + '" r="' + R + '"/>';
      });
      h += '<g class="g-shadow" fill="#000" opacity=".55">' + bs + '</g><g fill="url(#gBead)" stroke="#4a2e08" stroke-width="' + f(.7 * sc) + '">' + bb + '</g>';
    }
    var zoom = .93;
    h = defs(sc) + '<g transform="scale(' + zoom + ')">' + h + '</g>';
    svg.innerHTML = h;
    if (sh) sh.innerHTML = '<defs><linearGradient id="gSheen"' + defs(sc).split('<linearGradient id="gSheen"')[1] + '<g transform="scale(' + zoom + ')">' + g.sheen(sc) + '</g>';
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', draw); else draw();
  var lastBig = null;
  window.addEventListener('resize', function () {
    var w = (document.getElementById('flower') || {}).clientWidth || 0, big = !(w < 420 && window.innerWidth <= 640);
    if (big !== lastBig) { lastBig = big; draw(); }
  });
})();



/* 8-petal sub-sections: click/tap toggles, keyboard + Escape, one panel at a time.
   Panels that would overflow the viewport are nudged back in. */
(function () {
  'use strict';
  var nodes = document.querySelectorAll('.node.has-sub');
  if (!nodes.length) return;

  function buttonOf(n) { return n.querySelector('.node-hit'); }
  function subOf(n) { return n.querySelector('.sub'); }

  function clearPlace(sub) {
    if (sub) sub.style.transform = '';
  }

  function placePanel(n) {
    var sub = subOf(n);
    if (!sub) return;
    sub.style.transform = '';
    /* wait for CSS display:block to apply */
    requestAnimationFrame(function () {
      if (getComputedStyle(sub).display === 'none') return;
      var q = sub.getBoundingClientRect();
      var pad = 10, dx = 0, dy = 0, vw = window.innerWidth, vh = window.innerHeight;
      if (q.right > vw - pad) dx -= (q.right - (vw - pad));
      if (q.left + dx < pad) dx += (pad - (q.left + dx));
      if (q.bottom > vh - pad) dy -= (q.bottom - (vh - pad));
      if (q.top + dy < pad) dy += (pad - (q.top + dy));
      function box(dx0, dy0) {
        return {left: q.left + dx0, right: q.right + dx0, top: q.top + dy0, bottom: q.bottom + dy0};
      }
      function overlaps(a, b) {
        return a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;
      }
      function inView(r) {
        return r.left >= pad && r.right <= vw - pad && r.top >= pad && r.bottom <= vh - pad;
      }
      var labels = [];
      document.querySelectorAll('.wheel .lbl').forEach(function (el) {
        labels.push(el.getBoundingClientRect());
      });
      var under = document.querySelector('.under');
      if (under) labels.push(under.getBoundingClientRect());
      function hitsLabel(r) {
        for (var i = 0; i < labels.length; i++) if (overlaps(r, labels[i])) return labels[i];
        return null;
      }
      var hit = hitsLabel(box(dx, dy));
      if (hit) {
        var cand = [
          {dx: (hit.right + 8) - q.left, dy: dy},
          {dx: (hit.left - 8 - q.width) - q.left, dy: dy},
          {dx: dx, dy: (hit.top - 8 - q.height) - q.top},
          {dx: dx, dy: (hit.bottom + 8) - q.top}
        ];
        var k, ok = null;
        for (k = 0; k < cand.length; k++) {
          var r = box(cand[k].dx, cand[k].dy);
          if (inView(r) && !hitsLabel(r)) { ok = cand[k]; break; }
        }
        if (ok) { dx = ok.dx; dy = ok.dy; }
      }
      if (q.left + dx < pad) dx = pad - q.left;
      if (q.right + dx > vw - pad) dx = (vw - pad) - q.right;
      if (q.top + dy < pad) dy = pad - q.top;
      if (q.bottom + dy > vh - pad) dy = (vh - pad) - q.bottom;
      if (dx || dy) sub.style.transform = 'translate(' + Math.round(dx) + 'px,' + Math.round(dy) + 'px)';
    });
  }

  function setOpen(n, open) {
    var b = buttonOf(n);
    n.classList.toggle('is-open', open);
    if (b) b.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) placePanel(n);
    else clearPlace(subOf(n));
  }

  function closeAll(except) {
    nodes.forEach(function (n) { if (n !== except) setOpen(n, false); });
  }

  function isFinePointer() {
    return window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches;
  }

  nodes.forEach(function (n) {
    var b = buttonOf(n);
    if (!b) return;
    b.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      var open = !n.classList.contains('is-open');
      closeAll(n);
      setOpen(n, open);
    });
    n.addEventListener('mouseenter', function () {
      if (isFinePointer()) {
        b.setAttribute('aria-expanded', 'true');
        placePanel(n);
      }
    });
    n.addEventListener('mouseleave', function () {
      if (isFinePointer() && !n.classList.contains('is-open') && !n.contains(document.activeElement)) {
        b.setAttribute('aria-expanded', 'false');
        clearPlace(subOf(n));
      }
    });
    n.addEventListener('focusin', function () {
      b.setAttribute('aria-expanded', 'true');
      placePanel(n);
    });
    n.addEventListener('focusout', function (e) {
      if (!n.contains(e.relatedTarget)) setOpen(n, false);
    });
  });

  document.addEventListener('click', function (e) {
    if (!e.target.closest('.node.has-sub')) closeAll();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      var open = document.querySelector('.node.has-sub.is-open') || document.querySelector('.node.has-sub:focus-within');
      closeAll();
      if (open) {
        var b = buttonOf(open);
        if (b) b.focus();
      }
    }
  });
  window.addEventListener('resize', function () {
    var n = document.querySelector('.node.has-sub.is-open') || document.querySelector('.node.has-sub:hover');
    if (n) placePanel(n);
  });
})();

/* Centre the rosace in the viewport for #wheel / #rosace and the back-to-rosace button. */
(function () {
  'use strict';

  var HASH = { wheel: 1, rosace: 1 };

  function reduceMotion() {
    return window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function headerHeight() {
    var bars = document.querySelectorAll('.vbar, .pp-head, header');
    var h = 0, i, el, cs, r;
    for (i = 0; i < bars.length; i++) {
      el = bars[i];
      cs = getComputedStyle(el);
      if (cs.position !== 'sticky' && cs.position !== 'fixed') continue;
      if (cs.display === 'none' || cs.visibility === 'hidden') continue;
      r = el.getBoundingClientRect();
      if (r.bottom > 0 && r.top < 8) h = Math.max(h, Math.round(r.bottom));
    }
    return h;
  }

  function rosaceBox() {
    var wheel = document.getElementById('wheel');
    if (!wheel) return null;
    var top = Infinity, bottom = -Infinity, left = Infinity, right = -Infinity;
    function inc(el) {
      var r = el.getBoundingClientRect();
      if (!r.width && !r.height) return;
      if (r.top < top) top = r.top;
      if (r.bottom > bottom) bottom = r.bottom;
      if (r.left < left) left = r.left;
      if (r.right > right) right = r.right;
    }
    inc(wheel);
    wheel.querySelectorAll('.node, .lbl, .core, .flower').forEach(inc);
    if (top === Infinity) return null;
    return { top: top, bottom: bottom, height: bottom - top, mid: (top + bottom) / 2, left: left, right: right };
  }

  function targetY() {
    var b = rosaceBox();
    if (!b) return 0;
    var hh = headerHeight();
    var avail = Math.max(0, window.innerHeight - hh);
    var y;
    var max = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
    if (b.height <= avail - 4) {
      y = (b.mid + window.scrollY) - hh - avail / 2;
    } else {
      y = (b.top + window.scrollY) - hh - 8;
    }
    if (y < 0) y = 0;
    if (y > max) y = max;
    return Math.round(y);
  }

  function isRosaceHash(hash) {
    return HASH[(hash || location.hash || '').replace(/^#/, '')] === 1;
  }

  var scrolling = false;
  var scrollTimer = 0;

  function go(smooth) {
    if (!document.getElementById('wheel')) return;
    var y = targetY();
    var useSmooth = !!(smooth && !reduceMotion());
    scrolling = true;
    window.scrollTo({ top: y, behavior: useSmooth ? 'smooth' : 'auto' });
    clearTimeout(scrollTimer);
    scrollTimer = setTimeout(function () { scrolling = false; syncButton(); }, useSmooth ? 700 : 50);
    if (!useSmooth) {
      /* one more pass after layout/fonts */
      requestAnimationFrame(function () {
        var y2 = targetY();
        if (Math.abs(y2 - window.scrollY) > 1) window.scrollTo({ top: y2, behavior: 'auto' });
      });
    }
  }

  function reveal() {
    document.documentElement.classList.remove('pp-rosace-pending');
  }

  function restoreHash() {
    var h = window.__ppRosaceHash;
    if (!h) return;
    window.__ppRosaceHash = null;
    if (location.hash !== h) history.replaceState(null, '', location.pathname + location.search + h);
  }

  function onLanding() {
    if (!(window.__ppRosaceHash || isRosaceHash())) { reveal(); return; }
    restoreHash();
    go(false);
    reveal();
  }

  function samePage(url) {
    var here = location.pathname;
    var there = url.pathname;
    function norm(p) {
      if (!p || p === '/') return '/';
      return p.replace(/\/index\.html$/, '/').replace(/\/+$/, '/') || '/';
    }
    return url.origin === location.origin && norm(here) === norm(there);
  }

  function syncButton() {
    var btn = document.querySelector('a.rosace-back');
    if (!btn) return;
    var b = rosaceBox();
    var hh = headerHeight();
    var vh = window.innerHeight;
    var show = !!(b && (b.bottom < hh + 48 || b.top > vh - 48));
    var foot = document.querySelector('footer');
    var base = window.matchMedia('(max-width:640px)').matches ? 12 : 16;
    var bottom = base;
    if (show && foot) {
      var fr = foot.getBoundingClientRect();
      if (fr.top < vh) {
        bottom = Math.max(base, Math.ceil(vh - fr.top + 12));
      }
    }
    btn.style.setProperty('--rb-bottom', bottom + 'px');
    btn.classList.toggle('is-on', show);
    btn.setAttribute('aria-hidden', show ? 'false' : 'true');
    btn.setAttribute('tabindex', show ? '0' : '-1');
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var url;
    try { url = new URL(a.getAttribute('href'), location.href); } catch (err) { return; }
    if (!samePage(url) || !isRosaceHash(url.hash)) return;
    e.preventDefault();
    if (location.hash !== url.hash) history.pushState(null, '', url.hash);
    go(true);
  });

  window.addEventListener('hashchange', function () {
    if (isRosaceHash()) go(true);
  });
  window.addEventListener('popstate', function () {
    if (isRosaceHash()) go(false);
  });
  window.addEventListener('resize', function () {
    if (isRosaceHash()) go(false);
    syncButton();
  });
  window.addEventListener('scroll', function () {
    if (!scrolling) syncButton();
  }, { passive: true });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      onLanding();
      syncButton();
    });
  } else {
    onLanding();
    syncButton();
  }
  window.addEventListener('load', function () {
    if (isRosaceHash()) go(false);
    reveal();
    syncButton();
  });
})();
