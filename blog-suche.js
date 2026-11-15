/* VoltKompass Blog-Suche: durchsucht suchindex.json (erzeugt mit werkzeuge/suchindex.py) */
(function () {
  var root = document.getElementById('blogSuche');
  if (!root) return;
  var input = document.getElementById('blogSucheInput');
  var box = document.getElementById('blogSucheErgebnisse');
  var clearBtn = document.getElementById('blogSucheLeeren');
  var DATA = null, loading = null, VOCAB = null;

  /* ---------- Normalisieren ---------- */
  var UNIT_WORDS = [
    [/\bkilowattstunden?\b/g, 'kwh'], [/\bwattstunden?\b/g, 'wh'], [/\bamperestunden?\b/g, 'ah'],
    [/\bampere\b/g, 'a'], [/\bamp\b/g, 'a'], [/\bkilowatt\b/g, 'kw'], [/\bwatt\b/g, 'w'], [/\bvolt\b/g, 'v'],
    [/\bquadratmillimeter\b/g, 'mm2'], [/\bquadrat\b/g, 'mm2'], [/\bqmm\b/g, 'mm2'], [/\bmilliohm\b/g, 'mohm'],
    [/\bgrad\b/g, 'c']
  ];
  function base(s) {
    return String(s).toLowerCase()
      .replace(/­/g, '')
      .replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue').replace(/ß/g, 'ss')
      .replace(/[éè]/g, 'e').replace(/²/g, '2').replace(/°\s*c\b/g, ' c').replace(/°/g, ' ')
      .replace(/(\d)\.(\d)/g, '$1,$2');
  }
  function norm(s) {
    s = base(s);
    UNIT_WORDS.forEach(function (r) { s = s.replace(r[0], r[1]); });
    // Zahl + Einheit zusammenziehen: "100 ah", "100-ah", "100ah" -> "100ah"
    s = s.replace(/(\d+(?:,\d+)?)\s*-?\s*(kwh|wh|ah|mm2|mohm|kw|wp|a|w|v|c)\b/g, '$1$2');
    return s;
  }
  function tokens(s) {
    return norm(s).split(/[^a-z0-9,]+/).map(function (t) { return t.replace(/^,+|,+$/g, ''); }).filter(Boolean);
  }

  var STOP = ('ich du er sie es wir ihr man mein meine meinen meinem mir mich dein deine mit fuer wie was welche welcher welches ' +
    'wieviel der die das den dem des ein eine einen einem einer und oder im in am an zu bei von vom zum zur ist sind sein ' +
    'brauche braucht brauchen soll sollte kann koennen muss viel viele auf aus als dass wenn nicht kein keine wird werden gibt ' +
    'auch noch so nur habe hat haben mehr sich ob bis um wo wann warum gut am beste besten richtig richtige richtigen ' +
    'meinem unser unsere hier da dann denn doch aber gegen ueber unter ohne').split(' ');
  var STOPSET = {}; STOP.forEach(function (w) { STOPSET[w] = 1; });

  var SYN = [
    ['akku', 'akkus', 'batterie', 'batterien', 'aufbaubatterie', 'versorgerbatterie', 'bordbatterie', 'lifepo4', 'lithium', 'lithiumbatterie'],
    ['wechselrichter', 'inverter', 'spannungswandler'],
    ['solarmodul', 'solarmodule', 'solarpanel', 'solarpanels', 'panel', 'panele', 'modul', 'module', 'solarplatte', 'photovoltaik', 'pv', 'solarzelle'],
    ['solaranlage', 'solar', 'photovoltaikanlage', 'pvanlage'],
    ['lichtmaschine', 'lima', 'generator'],
    ['ladebooster', 'booster', 'dcdc', 'ladewandler', 'b2b'],
    ['laderegler', 'mppt', 'solarregler', 'solarladeregler', 'regler'],
    ['sicherung', 'sicherungen', 'absicherung', 'absichern', 'fuse', 'hauptsicherung'],
    ['kabel', 'leitung', 'leitungen', 'kabelquerschnitt', 'querschnitt', 'batteriekabel'],
    ['wohnmobil', 'camper', 'kastenwagen', 'womo', 'reisemobil', 'van'],
    ['starterbatterie', 'starterakku', 'fahrzeugbatterie', 'startbatterie'],
    ['landstrom', 'ladegeraet', 'netzladegeraet', 'landstromladegeraet'],
    ['schatten', 'verschattung', 'teilschatten', 'beschattung'],
    ['kosten', 'preis', 'preise', 'teuer', 'guenstig', 'billig', 'euro'],
    ['laden', 'laedt', 'ladung', 'aufladen', 'ladestrom', 'lade'],
    ['gel', 'agm', 'blei', 'bleiakku', 'bleibatterie'],
    ['kuehlschrank', 'kuehlbox', 'kompressorkuehlbox'],
    ['schaltplan', 'stromlaufplan', 'verkabelung', 'anschlussplan', 'plan'],
    ['spannungsabfall', 'spannungsverlust', 'spannungsfall'],
    ['heiss', 'warm', 'waerme', 'hitze', 'temperatur'],
    ['wirkungsgrad', 'effizienz', 'verlust', 'verluste']
  ];
  var SYNMAP = {};
  SYN.forEach(function (g) { g.forEach(function (w) { SYNMAP[w] = (SYNMAP[w] || []).concat(g); }); });

  /* ---------- Index vorbereiten ---------- */
  function prep(d) {
    VOCAB = {};
    d.posts.forEach(function (p, pi) {
      p._t = countWords(p.t + ' ' + (p.tags || []).join(' '));
      p._m = countWords(p.d + ' ' + p.m);
      p.c.forEach(function (c) {
        c._h = countWords(c.h);
        c._x = countWords(c.x);
      });
    });
    return d;
  }
  function countWords(s) {
    var m = {};
    tokens(s).forEach(function (t) { m[t] = (m[t] || 0) + 1; VOCAB[t] = 1; });
    return m;
  }

  function lev1(a, b, max) {
    // Levenshtein mit Abbruch
    var la = a.length, lb = b.length;
    if (Math.abs(la - lb) > max) return max + 1;
    var prev = [], cur, i, j;
    for (j = 0; j <= lb; j++) prev[j] = j;
    for (i = 1; i <= la; i++) {
      cur = [i]; var rowMin = i;
      for (j = 1; j <= lb; j++) {
        cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
        if (cur[j] < rowMin) rowMin = cur[j];
      }
      if (rowMin > max) return max + 1;
      prev = cur;
    }
    return prev[lb];
  }

  // Für ein Suchwort: welche Index-Wörter passen, mit welcher Stärke?
  function expand(q) {
    var out = {};
    function add(w, s) { if (!out[w] || out[w] < s) out[w] = s; }
    var isNum = /^\d/.test(q);
    Object.keys(VOCAB).forEach(function (w) {
      if (w === q) return add(w, 1);
      if (isNum) {
        // "100" findet auch "100ah", "100w"; "100ah" findet nur genau das
        if (/^\d+(,\d+)?$/.test(q) && w.indexOf(q) === 0 && /^[a-z]/.test(w.slice(q.length))) add(w, 0.9);
        return;
      }
      if (q.length >= 4 && w.indexOf(q) === 0) return add(w, 0.85);
      if (w.length >= 5 && q.indexOf(w) === 0 && q.length - w.length <= 3) return add(w, 0.8);
      if (q.length >= 5 && !/\d/.test(w)) {
        var d = lev1(q, w, q.length >= 8 ? 2 : 1);
        if (d <= (q.length >= 8 ? 2 : 1)) add(w, 0.6);
      }
    });
    (SYNMAP[q] || []).forEach(function (s) {
      if (s === q) return;
      Object.keys(VOCAB).forEach(function (w) {
        if (w === s) add(w, 0.7);
        else if (s.length >= 5 && w.indexOf(s) === 0) add(w, 0.6);
      });
    });
    return out;
  }

  function strength(map, ex) {
    // beste Stärke und Anzahl der Treffer in einer Wortzählung
    var best = 0, n = 0;
    for (var w in ex) if (map[w]) { n += map[w]; if (ex[w] > best) best = ex[w]; }
    return { s: best, n: n };
  }

  function search(q) {
    var qt = tokens(q).filter(function (t) { return !STOPSET[t] && (t.length > 1 || /\d/.test(t)); });
    var seen = {}; qt = qt.filter(function (t) { return seen[t] ? false : (seen[t] = 1); });
    if (!qt.length) return { terms: [], res: [] };
    var groups = qt.map(function (t) { return { t: t, ex: expand(t) }; }).filter(function (g) { return Object.keys(g.ex).length; });
    var missing = qt.length - groups.length;
    var res = [];
    DATA.posts.forEach(function (p) {
      var cover = 0, titleScore = 0;
      var chunkScores = p.c.map(function (c) {
        var sc = 0, cov = 0;
        groups.forEach(function (g) {
          var h = strength(c._h, g.ex), x = strength(c._x, g.ex);
          var s = Math.max(h.s, x.s);
          if (!s) return;
          cov++;
          sc += s * ((h.s ? (c.k === 'faq' ? 7 : 6) : 0) + Math.min(3, Math.log(1 + x.n) / Math.LN2));
        });
        if (c.a === 'quellen') sc *= 0.4;
        return { c: c, sc: sc, cov: cov };
      });
      groups.forEach(function (g) {
        var t = strength(p._t, g.ex), m = strength(p._m, g.ex);
        var inDoc = t.s || m.s || chunkScores.some(function (cs) { return strength(cs.c._h, g.ex).s || strength(cs.c._x, g.ex).s; });
        if (inDoc) cover++;
        titleScore += t.s * 10 + m.s * 3;
      });
      if (!cover) return;
      chunkScores.sort(function (a, b) { return (b.cov - a.cov) || (b.sc - a.sc); });
      var best = chunkScores[0];
      var rest = chunkScores.slice(1, 8).reduce(function (s, x) { return s + x.sc; }, 0);
      var score = cover * 100 + titleScore + best.cov * 25 + best.sc + Math.min(40, rest * 0.25);
      var more = chunkScores.slice(1).filter(function (x) { return x.sc > 0 && x.cov === best.cov && x.c.h && x.c.k !== 'intro'; }).slice(0, 2);
      res.push({ p: p, score: score, cover: cover, best: best.sc > 0 ? best.c : null, more: more.map(function (x) { return x.c; }) });
    });
    res.sort(function (a, b) { return b.score - a.score; });
    var top = res.length ? res[0].cover : 0;
    res.forEach(function (r) { r.partial = r.cover < groups.length || missing > 0; });
    return { terms: groups, res: res.slice(0, 8), full: top === groups.length && !missing };
  }

  /* ---------- Ausgabe ---------- */
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function isHit(word, terms) {
    var t = tokens(word);
    return t.some(function (w) { return terms.some(function (g) { return g.ex[w]; }); });
  }
  function highlight(text, terms) {
    // Wörter (und Zahl+Einheit-Paare) einzeln prüfen
    var parts = text.split(/(\s+)/), out = '';
    for (var i = 0; i < parts.length; i++) {
      var w = parts[i];
      if (/^\s+$/.test(w) || !w) { out += esc(w); continue; }
      var pair = parts[i + 2];
      if (/\d[.,]?$/.test(w) && pair && /^[A-Za-zµ°²]/.test(pair) && isHit(w + ' ' + pair, terms) && !isHit(w, terms)) {
        out += '<mark>' + esc(w + parts[i + 1] + pair) + '</mark>'; i += 2; continue;
      }
      out += isHit(w, terms) ? '<mark>' + esc(w) + '</mark>' : esc(w);
    }
    return out;
  }
  function snippet(text, terms) {
    var words = text.split(/\s+/), pos = -1;
    for (var i = 0; i < words.length && pos < 0; i++) {
      if (isHit(words[i], terms) || (words[i + 1] && isHit(words[i] + ' ' + words[i + 1], terms))) pos = i;
    }
    if (pos < 0) pos = 0;
    var from = Math.max(0, pos - 10), to = Math.min(words.length, pos + 24);
    return (from > 0 ? '… ' : '') + highlight(words.slice(from, to).join(' '), terms) + (to < words.length ? ' …' : '');
  }
  function link(p, c) { return p.u + (c && c.a ? '#' + c.a : ''); }
  function label(c) { return c.k === 'faq' ? 'Häufige Frage' : 'Abschnitt'; }

  function render(q) {
    if (!DATA) return;
    q = q.trim();
    clearBtn.hidden = !q;
    if (q.length < 2) { box.innerHTML = ''; box.hidden = true; return; }
    var r = search(q);
    box.hidden = false;
    if (!r.res.length) {
      box.innerHTML = '<div class="bs-empty"><strong>Dazu gibt es noch keinen Beitrag.</strong> ' +
        'Versuch es mit einem anderen Begriff, z. B. „Ladebooster“, „Sicherung“ oder „100 Ah“. ' +
        'Oder frag mich direkt: <a href="index.html#kontakt">1:1-Beratung per WhatsApp, Telegram oder Signal</a>.</div>';
      return;
    }
    var html = '<p class="bs-count">' + r.res.length + (r.res.length === 1 ? ' Beitrag' : ' Beiträge') + ' zu „' + esc(q) + '“</p><ol class="bs-list">';
    r.res.forEach(function (x, i) {
      var c = x.best;
      html += '<li class="bs-item' + (x.partial ? ' is-partial' : '') + '">' +
        '<a class="bs-title" href="' + esc(link(x.p, c && c.k !== 'intro' ? c : null)) + '">' + highlight(x.p.t, r.terms) + '</a>' +
        (x.partial && r.full ? '<span class="bs-part">passt teilweise</span>' : '');
      if (c && c.h && c.k !== 'intro') {
        html += '<a class="bs-sec" href="' + esc(link(x.p, c)) + '"><span>' + label(c) + ':</span> ' + highlight(c.h, r.terms) + '</a>';
      }
      html += '<p class="bs-snip">' + snippet(c ? c.x : x.p.d, r.terms) + '</p>';
      if (x.more.length) {
        html += '<div class="bs-more">' + x.more.map(function (m) {
          return '<a href="' + esc(link(x.p, m)) + '">' + (m.k === 'faq' ? 'Frage: ' : '') + esc(m.h) + '</a>';
        }).join('') + '</div>';
      }
      html += '</li>';
    });
    box.innerHTML = html + '</ol>';
  }

  function load() {
    if (DATA || loading) return loading;
    loading = fetch('suchindex.json', { cache: 'no-cache' })
      .then(function (r) { return r.json(); })
      .then(function (d) { DATA = prep(d); render(input.value); })
      .catch(function () { box.hidden = false; box.innerHTML = '<div class="bs-empty">Die Suche konnte nicht geladen werden. Bitte lade die Seite neu.</div>'; });
    return loading;
  }

  var timer = null;
  function update() {
    clearTimeout(timer);
    timer = setTimeout(function () {
      render(input.value);
      try {
        var u = new URL(location.href);
        if (input.value.trim()) u.searchParams.set('q', input.value.trim()); else u.searchParams.delete('q');
        history.replaceState(null, '', u.pathname + u.search + u.hash);
      } catch (e) {}
    }, 120);
  }
  input.addEventListener('focus', load);
  input.addEventListener('input', function () { load(); update(); });
  root.addEventListener('submit', function (e) {
    e.preventDefault();
    var first = box.querySelector('.bs-sec, .bs-title');
    if (first) location.href = first.getAttribute('href');
  });
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { input.value = ''; update(); }
  });
  clearBtn.addEventListener('click', function () { input.value = ''; update(); input.focus(); });
  document.querySelectorAll('[data-suche]').forEach(function (b) {
    b.addEventListener('click', function () { input.value = b.getAttribute('data-suche'); load(); update(); input.focus(); });
  });

  try {
    var q0 = new URL(location.href).searchParams.get('q');
    if (q0) { input.value = q0; load(); }
  } catch (e) {}
})();
