(function () {
  'use strict';

  var MAPS = 'https://www.google.com/maps/search/?api=1&query=';
  var STORE = 'pawpartout-vet-card-v1';

  var PHRASES = {
    en: {
      hint: 'English — show these lines at a clinic desk',
      items: [
        'My pet is having trouble breathing.',
        'I think my pet swallowed something toxic.',
        'My pet has been vomiting / has diarrhea.',
        'My pet is bleeding / is injured.',
        'My pet had a seizure / is having a seizure.',
        'My pet’s belly is swollen and hard (possible bloat).',
        'My pet is taking these medications: …',
        'My pet is allergic to: …'
      ]
    },
    fr: {
      hint: 'Français (Canada / Québec) — à montrer à l’accueil de la clinique',
      items: [
        'Mon animal a de la difficulté à respirer.',
        'Je crois que mon animal a avalé quelque chose de toxique.',
        'Mon animal vomit / a de la diarrhée.',
        'Mon animal saigne / est blessé.',
        'Mon animal a fait une crise convulsive / est en train d’en faire une.',
        'Le ventre de mon animal est gonflé et dur (possible dilatation-torsion).',
        'Mon animal prend ces médicaments : …',
        'Mon animal est allergique à : …'
      ]
    },
    es: {
      hint: 'Español (EE. UU.) — para mostrar en la recepción de la clínica',
      items: [
        'Mi mascota tiene dificultad para respirar.',
        'Creo que mi mascota tragó algo tóxico.',
        'Mi mascota está vomitando / tiene diarrea.',
        'Mi mascota está sangrando / está herida.',
        'Mi mascota tuvo una convulsión / está convulsionando.',
        'El abdomen de mi mascota está hinchado y duro (posible dilatación gástrica).',
        'Mi mascota toma estos medicamentos: …',
        'Mi mascota es alérgica a: …'
      ]
    }
  };

  function mapsUrl(place) {
    var q = place && String(place).replace(/\s+/g, ' ').trim();
    if (!q) return MAPS + encodeURIComponent('24 hour emergency vet near me');
    return MAPS + encodeURIComponent('24 hour emergency vet near ' + q);
  }


  var form = document.getElementById('vet-place');
  var place = document.getElementById('place');
  var hidden = document.getElementById('vet-query');
  var globeBtn = document.getElementById('vet-globe-btn');
  var azLive = document.getElementById('az-live');
  var lastAction = null;

  function pingMap() {
    if (!globeBtn) return;
    globeBtn.classList.remove('is-ping');
    void globeBtn.offsetWidth;
    globeBtn.classList.add('is-ping');
    window.setTimeout(function () { globeBtn.classList.remove('is-ping'); }, 2000);
  }

  function openMaps(query, type) {
    var url = mapsUrl(query);
    lastAction = { type: type, url: url, query: query || 'me' };
    if (hidden) hidden.value = query ? ('24 hour emergency vet near ' + query) : '24 hour emergency vet near me';
    pingMap();
    window.open(url, '_blank', 'noopener');
    return url;
  }

  function searchOrLocate() {
    var v = place ? place.value.replace(/\s+/g, ' ').trim() : '';
    if (v) {
      if (azLive) azLive.textContent = 'Opening Google Maps for ' + v;
      return openMaps(v, 'query');
    }
    if (!navigator.geolocation) {
      if (azLive) azLive.textContent = 'Location unavailable. Opening a nearby search.';
      return openMaps('', 'fallback');
    }
    if (azLive) azLive.textContent = 'Finding your location…';
    var settled = false;
    function fail() {
      if (settled) return;
      settled = true;
      if (azLive) azLive.textContent = 'Location unavailable. Opening a nearby search.';
      openMaps('', 'fallback');
    }
    try {
      navigator.geolocation.getCurrentPosition(
        function (pos) {
          if (settled) return;
          settled = true;
          var q = pos.coords.latitude.toFixed(5) + ',' + pos.coords.longitude.toFixed(5);
          if (azLive) azLive.textContent = 'Opening Google Maps near your location.';
          openMaps(q, 'geo');
        },
        function () { fail(); },
        { enableHighAccuracy: false, timeout: 5000, maximumAge: 60000 }
      );
    } catch (err) {
      fail();
    }
    return lastAction;
  }

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      searchOrLocate();
    });
  }

  var list = document.getElementById('phrase-list');
  var hint = document.getElementById('lang-hint');
  var buttons = document.querySelectorAll('.lang-btn');

  function setLang(code) {
    var pack = PHRASES[code] || PHRASES.en;
    if (list) {
      list.lang = code;
      list.innerHTML = pack.items.map(function (t) { return '<li>' + t + '</li>'; }).join('');
    }
    if (hint) hint.textContent = pack.hint;
    buttons.forEach(function (b) {
      var on = b.getAttribute('data-lang') === code;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-selected', on ? 'true' : 'false');
    });
    try { localStorage.setItem(STORE + ':lang', code); } catch (err) {}
  }

  buttons.forEach(function (b) {
    b.addEventListener('click', function () { setLang(b.getAttribute('data-lang')); });
  });

  var card = document.getElementById('e-card');
  var fields = ['petName', 'species', 'breed', 'weight', 'chip', 'allergies', 'meds', 'vetName', 'vetPhone'];

  function readCard() {
    if (!card) return {};
    var data = {};
    fields.forEach(function (name) {
      var el = card.elements[name];
      if (el) data[name] = el.value;
    });
    var unit = card.querySelector('input[name="unit"]:checked');
    data.unit = unit ? unit.value : 'lb';
    return data;
  }

  function writeCard(data) {
    if (!card || !data) return;
    fields.forEach(function (name) {
      var el = card.elements[name];
      if (el && data[name] != null) el.value = data[name];
    });
    if (data.unit) {
      var u = card.querySelector('input[name="unit"][value="' + data.unit + '"]');
      if (u) u.checked = true;
    }
  }

  function saveCard() {
    try { localStorage.setItem(STORE, JSON.stringify(readCard())); } catch (err) {}
  }

  function loadCard() {
    try {
      var raw = localStorage.getItem(STORE);
      if (raw) writeCard(JSON.parse(raw));
      var lang = localStorage.getItem(STORE + ':lang');
      setLang(lang && PHRASES[lang] ? lang : 'en');
    } catch (err) {
      setLang('en');
    }
  }

  if (card) {
    card.addEventListener('input', saveCard);
    card.addEventListener('change', saveCard);
  }

  var resetBtn = document.getElementById('card-reset');
  if (resetBtn) {
    resetBtn.addEventListener('click', function () {
      if (card) card.reset();
      try {
        localStorage.removeItem(STORE);
      } catch (err) {}
    });
  }

  var printBtn = document.getElementById('card-print');
  if (printBtn) {
    printBtn.addEventListener('click', function () { window.print(); });
  }

  loadCard();

  window.__ppVet = {
    mapsUrl: mapsUrl,
    readCard: readCard,
    setLang: setLang,
    store: STORE,
    searchOrLocate: searchOrLocate,
    lastAction: function () { return lastAction; }
  };
})();
