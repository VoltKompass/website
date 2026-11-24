/* ============================================================
   Plan-Kasten für Blogartikel und Rechner.
   Braucht plaene-daten.js davor. Platzhalter im Artikel:
   <div class="planbox" data-plaene="slug1,slug2" data-start="0"
        data-titel="…" data-text="…" data-hinweis="…">Fallback-Link</div>
   Mehrere Slugs = Umschalter (Beschriftung aus dem Wert, der sich unterscheidet).
   ============================================================ */
(function () {
  if (!document.querySelector('link[href^="plan-box.css"]')) {
    const l = document.createElement('link');
    l.rel = 'stylesheet';
    l.href = 'plan-box.css?v=1';
    document.head.appendChild(l);
  }

  const PFEIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  const FORMAT = {solar: v => `${v} W Solar`, booster: v => `${v} A Booster`, akku: v => `${v} Ah`, inverter: v => v ? `${v} W` : 'ohne 230 V'};

  function knopfText(plaene, p) {
    const k = KEYS.filter(k => new Set(plaene.map(x => x[k])).size > 1);
    return k.map(key => FORMAT[key](p[key])).join(' · ');
  }

  function zeichnen(box, plaene, i) {
    const p = plaene[i];
    const link = `stromlaufplaene.html?plan=${slug(p)}`;
    const aktion = aktionAn() ? `<p class="planbox-aktion"><b>${AKTION.name}: −${AKTION.rabatt} %</b> nur bis ${AKTION.bisText}</p>` : '';
    box.querySelector('.planbox-plan').innerHTML = `
      <a class="planbox-bild" href="${link}"><img src="${bild(p)}" width="1200" height="600" loading="lazy" decoding="async" alt="Vorschau Stromlaufplan ${titel(p)}"></a>
      <div class="planbox-daten">
        <h3>${titel(p)}</h3>
        <p class="planbox-meta">PDF · ${p.seiten} Seiten · Laderegler ${p.regler}</p>
        <div class="planbox-preis">${preisHtml(p)}</div>
        ${aktion}
        <div class="planbox-knoepfe">
          <a class="btn btn-primary" href="${link}">Plan ansehen ${PFEIL}</a>
          <a class="planbox-alle" href="stromlaufplaene.html">Alle ${PLAENE.length} Pläne →</a>
        </div>
      </div>`;
    box.querySelectorAll('.planbox-tab').forEach((t, j) => {
      t.classList.toggle('an', j === i);
      t.setAttribute('aria-selected', j === i);
    });
  }

  document.querySelectorAll('.planbox[data-plaene]').forEach(box => {
    const plaene = box.dataset.plaene.split(',').map(s => PLAENE.find(p => slug(p) === s.trim())).filter(Boolean);
    if (!plaene.length) return; // Fallback-Link bleibt stehen
    const start = Math.min(Number(box.dataset.start) || 0, plaene.length - 1);
    const tabs = plaene.length > 1
      ? `<div class="planbox-tabs" role="tablist" aria-label="Variante wählen">${plaene.map((p, j) =>
          `<button type="button" role="tab" class="planbox-tab" data-i="${j}">${knopfText(plaene, p)}</button>`).join('')}</div>`
      : '';
    box.innerHTML = `
      <div class="planbox-kopf">
        <span class="eyebrow">Fertiger Stromlaufplan</span>
        <h2>${box.dataset.titel || 'Diese Anlage als fertiger Plan'}</h2>
        <p>${box.dataset.text || ''}</p>
        ${box.dataset.hinweis ? `<p class="planbox-hinweis">${box.dataset.hinweis}</p>` : ''}
        ${tabs}
      </div>
      <div class="planbox-plan"></div>`;
    box.classList.add('fertig');
    box.addEventListener('click', e => {
      const t = e.target.closest('.planbox-tab');
      if (t) zeichnen(box, plaene, Number(t.dataset.i));
    });
    zeichnen(box, plaene, start);
  });
})();
