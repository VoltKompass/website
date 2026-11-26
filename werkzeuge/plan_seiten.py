"""Erzeugt die Schaltplan-Seiten für Google unter /schaltplan/.

Aufruf (im Ordner website):  python werkzeuge/plan_seiten.py

- 1 Seite je Akku + Wechselrichter (Solar und Ladebooster sind Varianten auf der Seite)
- Übersichtsseiten nach Akku, Wechselrichter, Solar und Ladebooster
- trägt alle Seiten in sitemap.xml ein (Block zwischen PLAN-SEITEN-Kommentaren)

Plandaten (Preis, Kauf-Link, Regler, Seitenzahl) kommen aus plaene-daten.js,
Texte und Planwerte aus werkzeuge/plan_seiten_texte.py.
Nach jeder Änderung an Plänen oder Texten einmal ausführen.
"""
import datetime, html, json, pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SITE / "werkzeuge"))
import plan_seiten_texte as T  # noqa: E402

BASIS = "https://voltkompass.com"
ORDNER = SITE / "schaltplan"
HEUTE = datetime.date.today().isoformat()
STANDARD = (200, 50)                       # vorgewählte Variante: Solar 200 W, Booster 50 A
LADER = {1000: 20, 1500: 30, 2000: 40, 3000: 40}
BILD_V = "2"
e = html.escape


# ---------- Plandaten aus plaene-daten.js ----------
def lade_plaene():
    js = (SITE / "plaene-daten.js").read_text(encoding="utf-8")
    block = js[js.index("let PLAENE = ["):js.index("];")]
    plaene = []
    for m in re.finditer(r"\{([^}]*)\}", block):
        p = {}
        for k, v in re.findall(r'(\w+):\s*("[^"]*"|\d+)', m.group(1)):
            p[k] = v.strip('"') if v.startswith('"') else int(v)
        plaene.append(p)
    return plaene


def slug(p):
    return f"plan-solar{p['solar']}-booster{p['booster']}-akku{p['akku']}" + (f"-{p['inverter']}w" if p["inverter"] else "")


def var_id(p):
    return f"solar{p['solar']}-booster{p['booster']}"


def seite_datei(akku, wr):
    return f"wohnmobil-{akku}ah-lifepo4-" + (f"{wr}w-wechselrichter" if wr else "12v-ohne-wechselrichter") + ".html"


def seite_url(akku, wr):
    return f"/schaltplan/{seite_datei(akku, wr)}"


def preis_zahl(p):
    return re.sub(r"[^\d,]", "", p["preis"]).replace(",", ".") or "0"


def wr_name(wr):
    return f"{wr} W" if wr else "ohne"


# ---------- Rahmen (Kopf, Navigation, Fuß) ----------
CSS = """
    .sp-hero p.blog-lead{max-width:64ch}
    .sp-top{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:clamp(20px,3vw,40px);align-items:start}
    .sp-panel{padding:clamp(18px,2.4vw,28px);border-radius:20px;border:1px solid var(--line-2);background:linear-gradient(180deg,var(--ink-2),var(--ink-3))}
    .sp-bild{margin:0 0 10px;border-radius:14px;overflow:hidden;border:1px solid var(--line-2);background:#fff;aspect-ratio:2/1}
    .sp-bild img{display:block;width:100%;height:100%;object-fit:cover}
    .sp-thumbs{display:grid;grid-template-columns:repeat(auto-fill,minmax(88px,1fr));gap:8px;margin:0}
    .sp-thumbs button{padding:0;border:1px solid var(--line-2);border-radius:8px;overflow:hidden;background:#fff;cursor:pointer;aspect-ratio:2/1}
    .sp-thumbs button.is-on{border-color:var(--gold);box-shadow:0 0 0 1px var(--gold)}
    .sp-thumbs img{display:block;width:100%;height:100%;object-fit:cover}
    .sp-thumbs-name{margin:8px 0 0;font-size:.85rem !important;color:var(--text-2) !important}
    .sp-wahl{margin:0 0 18px}
    .sp-wahl b{display:block;margin:0 0 8px;font:600 1rem/1.3 var(--font);color:#fff}
    .sp-knoepfe{display:flex;flex-wrap:wrap;gap:8px}
    .sp-knoepfe a{padding:8px 14px;border-radius:999px;border:1px solid var(--line-2);color:var(--text-2);text-decoration:none;font-size:.92rem}
    .sp-knoepfe a:hover{border-color:rgba(230,178,0,.55);color:#fff}
    .sp-knoepfe a.is-on{border-color:var(--gold);background:rgba(230,178,0,.12);color:#fff;font-weight:600}
    .sp-tags{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 14px}
    .sp-tags span{padding:4px 10px;border-radius:999px;border:1px solid var(--line-2);font-size:.8rem;color:var(--text-2)}
    .sp-buy{display:flex;flex-wrap:wrap;align-items:center;gap:12px 18px;padding-top:14px;border-top:1px solid var(--line-2)}
    .sp-price{font:700 1.5rem/1 var(--font);color:#fff}
    .sp-price small{display:block;margin-top:4px;font:500 .75rem/1.2 Inter,sans-serif;color:var(--text-2)}
    .slp-alt{font-weight:500;font-size:.75em;color:var(--text-2);text-decoration-thickness:2px}
    .slp-neu{color:var(--gold)}
    .sp-buy .btn{margin-left:auto}
    .sp-werte{width:100%;border-collapse:collapse;font-size:.95rem}
    .sp-werte th,.sp-werte td{padding:9px 10px;border-bottom:1px solid var(--line-2);text-align:left;vertical-align:top}
    .sp-werte th{color:var(--text-2);font-weight:500;width:38%}
    .sp-werte td{color:#fff}
    .sp-tabelle{overflow-x:auto}
    .sp-varianten{width:100%;border-collapse:collapse;font-size:.93rem;min-width:520px}
    .sp-varianten th,.sp-varianten td{padding:9px 10px;border-bottom:1px solid var(--line-2);text-align:left}
    .sp-varianten th{color:var(--text-2);font-weight:500}
    .sp-varianten tr.is-on td{background:rgba(230,178,0,.08)}
    .sp-varianten a{color:var(--gold)}
    .sp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
    .sp-card{display:flex;flex-direction:column;gap:8px;padding:14px;border-radius:16px;border:1px solid var(--line-2);background:linear-gradient(180deg,var(--ink-2),var(--ink-3));color:inherit;text-decoration:none;transition:border-color .18s,transform .18s}
    .sp-card:hover{border-color:rgba(230,178,0,.55);transform:translateY(-2px)}
    .sp-card img{width:100%;height:auto;aspect-ratio:2/1;object-fit:cover;border-radius:10px;background:#fff}
    .sp-card h3{margin:0;font-size:1rem;color:#fff;line-height:1.35}
    .sp-card span{font-size:.82rem;color:var(--text-2)}
    .sp-links{display:flex;flex-wrap:wrap;gap:8px;margin:0;padding:0;list-style:none}
    .sp-links a{display:inline-block;padding:7px 13px;border-radius:999px;border:1px solid var(--line-2);color:var(--text-2);text-decoration:none;font-size:.9rem}
    .sp-links a:hover{border-color:rgba(230,178,0,.55);color:#fff}
    .sp-text{max-width:72ch}
    @media (max-width:900px){.sp-top{grid-template-columns:1fr}}
    @media (max-width:520px){.sp-buy .btn{margin-left:0;width:100%;text-align:center}}
"""


def kopf(title, desc, url, bild, schema):
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(title)} | VoltKompass</title>
  <meta name="description" content="{e(desc)}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{BASIS}{url}">

  <meta property="og:type" content="website">
  <meta property="og:locale" content="de_DE">
  <meta property="og:site_name" content="VoltKompass">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{BASIS}{url}">
  <meta property="og:image" content="{BASIS}{bild}">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Orbitron:wght@700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css?v=20261028-2">
  <link rel="stylesheet" href="/blog.css?v=20260730-1">
  <link rel="stylesheet" href="/theme.css?v=20261125-1" />
  <link rel="icon" type="image/png" sizes="192x192" href="/favicon-192x192.png">
  <link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">
  <link rel="alternate icon" href="/favicon.ico" sizes="any">
  <script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False, indent=2)}
  </script>
  <style>{CSS}  </style>
</head>
<body class="blog-page">
<header class="nav">
  <div class="wrap nav-inner">
    <a href="/index.html#top" class="brand"><img class="brand-mark" src="/compass.svg" alt="" width="28" height="28" /><span><span class="v">Volt</span><span class="k">Kompass</span></span></a>
    <ul>
      <li><a href="/index.html#planfinder">Plan finden</a></li>
      <li><a href="/index.html#inhalt">Was drin ist</a></li>
      <li><a href="/index.html#solaranlage-beratung">Rechner</a></li>
      <li><a href="/blog.html">Blog</a></li>
      <li><a href="/index.html#ueber">Über mich</a></li>
      <li><a href="/einkaufsliste.html">Einkaufsliste</a></li>
      <li><a href="/index.html#beratung">Beratung</a></li>
    </ul>
    <div class="nav-actions">
      <a href="/einkaufsliste.html" class="nav-blog-mobile nav-einkauf" aria-label="Einkaufsliste" title="Einkaufsliste"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2.5 3h2.6l2.4 11.2a2 2 0 0 0 2 1.6h8.1a2 2 0 0 0 2-1.5L21.5 7H6"/></svg></a>
      <a href="/blog.html" class="nav-blog-mobile">Blog</a>
      <a href="/index.html#beratung" class="nav-blog-mobile">Beratung</a>
      <a href="/stromlaufplaene.html" class="cta">Stromlaufpläne →</a>
    </div>
  </div>
</header>
"""


FUSS = """
<footer>
  <div class="wrap foot">
    <div class="foot-brand">
      <a href="/index.html#top" class="brand"><img class="brand-mark" src="/compass.svg" alt="" width="28" height="28" /><span><span class="v">Volt</span><span class="k">Kompass</span></span></a>
      <p>© 2026 VoltKompass — Wohnmobil-Beratung für Strom &amp; Autarkie</p>
    </div>
    <nav>
      <a href="/index.html#top">Startseite</a>
      <a href="/blog.html">Blog</a>
      <a href="/stromlaufplaene.html">Stromlaufpläne</a>
      <a href="/impressum.html">Impressum</a>
      <a href="/datenschutz.html">Datenschutz</a>
      <a href="/index.html#kontakt">Kontakt</a>
      <button type="button" class="cookie-settings-link" data-cookie-settings>Cookie-Einstellungen</button>
    </nav>
  </div>
</footer>
"""

HINWEIS = ('<p class="blog-disclaimer"><strong>Sicherheitshinweis:</strong> Die Pläne sind Beispielpläne nach bestem Wissen '
           'und ersetzen keine Fachberatung. Herstellerangaben haben Vorrang. Lass die Anlage vor der Inbetriebnahme von einer '
           'Elektrofachkraft prüfen. Die PDFs sind nur für die private Nutzung bestimmt.</p>')


def breadcrumb_schema(teile):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASIS + u} for i, (n, u) in enumerate(teile)]}


def breadcrumb_html(teile):
    out = []
    for i, (n, u) in enumerate(teile):
        out.append(f'<span>{e(n)}</span>' if i == len(teile) - 1 else f'<a href="{u}">{e(n)}</a>')
    return '<nav class="blog-breadcrumb" aria-label="Breadcrumb">' + "<span>/</span>".join(out) + "</nav>"


def karte(p_bild, titel, unter, url):
    return (f'<a class="sp-card" href="{url}"><img src="/assets/stromlaufplaene/{slug(p_bild)}.webp?v={BILD_V}" '
            f'width="1200" height="600" alt="Vorschau Schaltplan {e(titel)}" loading="lazy"><h3>{e(titel)}</h3><span>{unter}</span></a>')


# ---------- Plan-Seite ----------
def plan_seite(akku, wr, gruppe, alle_gruppen):
    t = T.SEITEN[(akku, wr)]
    url = seite_url(akku, wr)
    gruppe.sort(key=lambda p: (p["solar"], p["booster"]))
    std = next(p for p in gruppe if (p["solar"], p["booster"]) == STANDARD)
    haupt, leitung = T.HAUPT[(akku, wr)]
    shunt, schalter = T.SHUNT.get((akku, wr), T.SHUNT_STANDARD)
    preis = std["preis"]
    seiten = std["seiten"]

    # Planwerte-Tabelle
    zeilen = [
        ("Akku", f"LiFePO4 12,8 V · {akku} Ah (nominal " + f"{akku * 128 // 10:,}".replace(",", ".") + " Wh)"),
        ("Hauptsicherung am Akku", haupt),
        ("Hauptleitung Akku → Busbar", leitung),
        ("Batteriewächter / Hauptschalter", f"Shunt {shunt} · Hauptschalter {schalter}"),
    ]
    if wr:
        wsich, wleit, wlad = T.WR[wr]
        zeilen += [
            ("Wechselrichter", f"{wr} W Sinus, Ladegerät {wlad} A am Landstrom"),
            ("Absicherung / Leitung Wechselrichter", f"{wsich} · {wleit}"),
            ("230-V-Seite", "FI/LS-Schutzschalter, 3 × 2,5 mm², Schutzleiter 6 mm²"),
        ]
    else:
        zeilen.append(("Wechselrichter", "keiner – reine 12-V-Anlage"))
    zeilen += [
        ("Ladebooster 30 A", T.BOOSTER[30]),
        ("Ladebooster 50 A", T.BOOSTER[50]),
        ("Solar 100 W", T.SOLAR[100]),
        ("Solar 200 W", T.SOLAR[200]),
        ("Solar 300 W", T.SOLAR[300]),
    ]
    werte = "".join(f"<tr><th>{e(a)}</th><td>{e(b)}</td></tr>" for a, b in zeilen)

    # Varianten
    var_json = [{"id": var_id(p), "slug": slug(p), "solar": p["solar"], "booster": p["booster"],
                 "regler": p["regler"], "preis": p["preis"], "kauf": p["digistore"]} for p in gruppe]
    var_rows = "".join(
        f'<tr data-v="{var_id(p)}"{" class=\"is-on\"" if p is std else ""}><td>{p["solar"]} W</td><td>{p["booster"]} A</td>'
        f'<td>{e(p["regler"])}</td><td class="sp-preis" data-slug="{slug(p)}">{e(p["preis"])}</td>'
        f'<td><a href="{e(p["digistore"])}" class="sp-kauf" data-slug="{slug(p)}" target="_blank" rel="noopener">Kaufen →</a> · '
        f'<a href="#{var_id(p)}" class="sp-zeig">ansehen</a></td></tr>' for p in gruppe)
    knopf_solar = "".join(f'<a href="#solar{s}-booster{STANDARD[1]}" data-k="solar" data-w="{s}"{" class=\"is-on\"" if s == STANDARD[0] else ""}>{s} W</a>' for s in (100, 200, 300))
    knopf_boost = "".join(f'<a href="#solar{STANDARD[0]}-booster{b}" data-k="booster" data-w="{b}"{" class=\"is-on\"" if b == STANDARD[1] else ""}>{b} A</a>' for b in (30, 50))

    vorschau = [(2, "Gesamtplan"), (3, "Teilplan Batterie"), (4, "Teilplan Ladebooster"), (5, "Teilplan Solar")]
    vorschau += [(6, "Teilplan 230 V"), (7, "Materialliste")] if seiten == 7 else [(6, "Materialliste")]
    thumbs = "".join(f'<button type="button" data-s="{s}" data-n="{n}"{" class=\"is-on\"" if i == 0 else ""} aria-label="{n} ansehen">'
                     f'<img src="/assets/stromlaufplaene/{slug(std)}/{s}.webp?v={BILD_V}" width="1200" height="600" alt="" loading="lazy"></button>'
                     for i, (s, n) in enumerate(vorschau))

    abschnitte = "".join(f'<section class="blog-section{" blog-section-alt" if i % 2 else ""}"><div class="wrap sp-text"><h2>{e(h)}</h2>{body}</div></section>'
                         for i, (h, body) in enumerate(t["abschnitte"]))

    # Nachbarn
    akkus = sorted({a for a, _ in alle_gruppen})
    wrs_hier = sorted(w for a, w in alle_gruppen if a == akku)
    nachbarn = [(f"{a} Ah mit {wr_name(wr) if wr else 'nur 12 V'}", seite_url(a, wr)) for a in akkus if a != akku and (a, wr) in alle_gruppen]
    nachbarn += [(f"{akku} Ah · {'nur 12 V' if not w else str(w) + ' W'}", seite_url(akku, w)) for w in wrs_hier if w != wr]
    nachbar_html = "".join(f'<li><a href="{u}">{e(n)}</a></li>' for n, u in nachbarn)
    ueber = [T.UEBERSICHT[("akku", akku)], T.UEBERSICHT[("wr", wr)]]
    ueber_html = "".join(f'<li><a href="/schaltplan/{u["datei"]}.html">{e(u["h1"])}</a></li>' for u in ueber)

    bild = f"/assets/stromlaufplaene/{slug(std)}.webp"
    teile = [("Startseite", "/"), ("Stromlaufpläne", "/stromlaufplaene.html"), (t["kurz"], url)]
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Product", "@id": f"{BASIS}{url}#plan", "name": t["h1"].replace("Schaltplan Wohnmobil: ", "Schaltplan Wohnmobil – "),
         "description": t["desc"], "image": [f"{BASIS}/assets/stromlaufplaene/{slug(p)}.webp" for p in gruppe],
         "brand": {"@type": "Brand", "name": "VoltKompass"}, "category": "Stromlaufplan Wohnmobil (PDF)",
         "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": preis_zahl(std), "highPrice": preis_zahl(std),
                    "offerCount": len(gruppe), "availability": "https://schema.org/InStock", "url": f"{BASIS}{url}"}},
        breadcrumb_schema(teile)]}

    body = f"""
  <main>
    <article>
      <section class="blog-hero sp-hero">
        <div class="wrap">
          {breadcrumb_html(teile)}
          <span class="eyebrow">Fertig verdrahtet · PDF · {seiten} Seiten · 6 Varianten</span>
          <h1>{e(t["h1"])}</h1>
          <p class="blog-lead">{e(t["lead"])}</p>
        </div>
      </section>

      <section class="blog-section" id="plan" style="padding-top:8px">
        <div class="wrap sp-top">
          <div>
            <figure class="sp-bild"><img id="spBild" src="/assets/stromlaufplaene/{slug(std)}/2.webp?v={BILD_V}" width="1200" height="600" alt="Gesamtplan {e(t["kurz"])}"></figure>
            <div class="sp-thumbs" id="spThumbs">{thumbs}</div>
            <p class="sp-thumbs-name" id="spThumbName">Gesamtplan</p>
          </div>
          <div class="sp-panel">
            <div class="sp-wahl"><b>Solarleistung</b><div class="sp-knoepfe" id="spSolar">{knopf_solar}</div></div>
            <div class="sp-wahl"><b>Ladebooster</b><div class="sp-knoepfe" id="spBooster">{knopf_boost}</div></div>
            <h2 id="spTitel" style="font-size:1.2rem;margin:0 0 8px">Solar {std["solar"]} W · Ladebooster {std["booster"]} A · {akku} Ah{f" · {wr} W" if wr else ""}</h2>
            <div class="sp-tags"><span>PDF · {seiten} Seiten</span><span id="spRegler">Laderegler {e(std["regler"])}</span>{f"<span>{LADER[wr]} A Landstrom-Ladegerät</span>" if wr else "<span>nur 12 V</span>"}</div>
            <div class="sp-buy">
              <div class="sp-price" id="spPreis">{e(preis)}<small>Sofort-Download über Digistore24</small></div>
              <a class="btn btn-primary" id="spKauf" href="{e(std["digistore"])}" target="_blank" rel="noopener">Plan kaufen →</a>
            </div>
          </div>
        </div>
      </section>

      {abschnitte}

      <section class="blog-section{" blog-section-alt" if len(t["abschnitte"]) % 2 else ""}" id="variante">
        <div class="wrap sp-text">
          <h2>Welche Variante passt?</h2>
          {t["variante"]}
          <p>Mehr dazu: <a href="/ladebooster-30a-oder-50a-wirkungsgrad.html">30 A oder 50 A Ladebooster</a> · <a href="/ladebooster-lichtmaschine.html">Ladebooster und Lichtmaschine</a> · <a href="/mppt-laderegler-wohnmobil.html">MPPT-Laderegler</a></p>
          <div class="sp-tabelle"><table class="sp-varianten">
            <thead><tr><th>Solar</th><th>Ladebooster</th><th>Laderegler</th><th>Preis</th><th></th></tr></thead>
            <tbody id="spVarianten">{var_rows}</tbody>
          </table></div>
        </div>
      </section>

      <section class="blog-section{"" if len(t["abschnitte"]) % 2 else " blog-section-alt"}" id="werte">
        <div class="wrap sp-text">
          <h2>Die wichtigsten Werte im Plan</h2>
          <p>Querschnitte und Sicherungen aus der Materialliste des Plans. Im PDF steht jede Leitung mit Länge, jeder Kabelschuh und jede Sicherung einzeln, dazu die Einstellungen für Laderegler, Ladebooster, Batteriewächter{" und Wechselrichter" if wr else ""}.</p>
          <div class="sp-tabelle"><table class="sp-werte"><tbody>{werte}</tbody></table></div>
          <p style="margin-top:14px">Hintergrund: <a href="/kabelquerschnitt-wohnmobil-kabelrechner.html">Kabelquerschnitt im Wohnmobil</a> · <a href="/sicherung-kabel-wohnmobil-sicherungsrechner.html">Welche Sicherung für welches Kabel</a></p>
        </div>
      </section>

      <section class="blog-section{" blog-section-alt" if len(t["abschnitte"]) % 2 else ""}">
        <div class="wrap">
          <h2>Ähnliche Schaltpläne</h2>
          <ul class="sp-links">{nachbar_html}</ul>
          <h3 style="margin-top:22px">Übersichten</h3>
          <ul class="sp-links">{ueber_html}<li><a href="/stromlaufplaene.html">Alle Pläne im Planfinder</a></li></ul>
        </div>
      </section>

      <section class="blog-section blog-section-final">
        <div class="blog-wrap">
          <p class="blog-eyebrow">Deine Kombination ist nicht dabei?</p>
          <h2>Ich plane dein System individuell</h2>
          <p>Andere Akkugröße, mehr Solar oder ein anderer Wechselrichter: Dann plane ich die Anlage für dein Fahrzeug mit dir zusammen.</p>
          <div class="blog-actions"><a href="/index.html#kontakt" class="btn btn-primary">Beratung buchen</a></div>
          {HINWEIS}
        </div>
      </section>
    </article>
  </main>
"""
    skript = f"""
<script src="/plaene-daten.js?v=2"></script>
<script>
// Varianten umschalten (Solar/Booster), Bild, Preis und Kauf-Link anpassen. Ohne JS bleibt die Standardvariante.
(() => {{
  const V = {json.dumps(var_json, ensure_ascii=False)};
  const AKKU = {akku}, WR = {wr};
  let akt = V.find(v => v.id === "{var_id(std)}"), seite = 2;
  const P = s => (typeof PLAENE !== "undefined" ? PLAENE.find(p => slug(p) === s) : null);
  const preisZeigen = (el, v, klein) => {{
    const p = P(v.slug);
    if (p && typeof aktionAn === "function" && aktionAn()) el.innerHTML = preisHtml(p) + (klein ? `<small>${{AKTION.name}} −${{AKTION.rabatt}} % · nur bis ${{AKTION.bisText}}</small>` : "");
    else el.innerHTML = v.preis + (klein ? "<small>Sofort-Download über Digistore24</small>" : "");
  }};
  const link = v => {{ const p = P(v.slug); return p && typeof kaufLink === "function" ? kaufLink(p) : v.kauf; }};
  function zeige() {{
    document.getElementById("spBild").src = `/assets/stromlaufplaene/${{akt.slug}}/${{seite}}.webp?v={BILD_V}`;
    document.querySelectorAll("#spThumbs button").forEach(b => {{
      b.querySelector("img").src = `/assets/stromlaufplaene/${{akt.slug}}/${{b.dataset.s}}.webp?v={BILD_V}`;
      b.classList.toggle("is-on", +b.dataset.s === seite);
    }});
    document.getElementById("spTitel").textContent = `Solar ${{akt.solar}} W · Ladebooster ${{akt.booster}} A · ${{AKKU}} Ah` + (WR ? ` · ${{WR}} W` : "");
    document.getElementById("spRegler").textContent = "Laderegler " + akt.regler;
    preisZeigen(document.getElementById("spPreis"), akt, true);
    document.getElementById("spKauf").href = link(akt);
    for (const [id, k] of [["spSolar", "solar"], ["spBooster", "booster"]])
      document.querySelectorAll(`#${{id}} a`).forEach(a => {{
        a.classList.toggle("is-on", +a.dataset.w === akt[k]);
        const z = V.find(v => v[k] === +a.dataset.w && v[k === "solar" ? "booster" : "solar"] === akt[k === "solar" ? "booster" : "solar"]);
        a.href = "#" + z.id;
      }});
    document.querySelectorAll("#spVarianten tr").forEach(tr => tr.classList.toggle("is-on", tr.dataset.v === akt.id));
  }}
  function ausHash() {{ const v = V.find(x => x.id === location.hash.slice(1)); if (v) {{ akt = v; zeige(); document.getElementById("plan").scrollIntoView({{behavior: "smooth"}}); }} }}
  document.getElementById("spThumbs").addEventListener("click", ev => {{
    const b = ev.target.closest("button"); if (!b) return;
    seite = +b.dataset.s; document.getElementById("spThumbName").textContent = b.dataset.n; zeige();
  }});
  document.querySelectorAll("#spVarianten tr").forEach(tr => {{
    const v = V.find(x => x.id === tr.dataset.v);
    preisZeigen(tr.querySelector(".sp-preis"), v, false);
    tr.querySelector(".sp-kauf").href = link(v);
  }});
  addEventListener("hashchange", ausHash);
  if (location.hash) ausHash(); else zeige();
}})();
</script>
<script src="/cookie-consent.js"></script>
<script src="/site.js"></script>
</body>
</html>
"""
    bild_og = bild
    return kopf(t["title"], t["desc"], url, bild_og, schema) + body + FUSS + skript


# ---------- Übersichtsseite ----------
def uebersicht_seite(art, wert, gruppen):
    u = T.UEBERSICHT[(art, wert)]
    url = f"/schaltplan/{u['datei']}.html"
    if art == "akku":
        treffer = [(a, w) for a, w in gruppen if a == wert]
        hash_ = ""
    elif art == "wr":
        treffer = [(a, w) for a, w in gruppen if w == wert]
        hash_ = ""
    else:
        treffer = sorted(gruppen)
        hash_ = f"#solar{wert}-booster{STANDARD[1]}" if art == "solar" else f"#solar{STANDARD[0]}-booster{wert}"
    karten = []
    for a, w in sorted(treffer):
        g = gruppen[(a, w)]
        if art == "solar":
            p = next(x for x in g if x["solar"] == wert and x["booster"] == STANDARD[1])
        elif art == "booster":
            p = next(x for x in g if x["booster"] == wert and x["solar"] == STANDARD[0])
        else:
            p = next(x for x in g if (x["solar"], x["booster"]) == STANDARD)
        titel = T.SEITEN[(a, w)]["h1"].replace("Schaltplan Wohnmobil: ", "")
        karten.append(karte(p, titel, f"{p['preis']} · {p['seiten']} Seiten · 6 Varianten", seite_url(a, w) + hash_))

    andere = [v for (k, _), v in T.UEBERSICHT.items() if v is not u]
    andere_html = "".join(f'<li><a href="/schaltplan/{v["datei"]}.html">{e(v["h1"].replace("Schaltpläne mit ", "").replace("Schaltplan mit ", ""))}</a></li>' for v in andere)
    teile = [("Startseite", "/"), ("Stromlaufpläne", "/stromlaufplaene.html"), (u["h1"], url)]
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": f"{BASIS}{url}", "name": u["title"], "description": u["desc"], "inLanguage": "de-DE",
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "url": BASIS + seite_url(a, w)} for i, (a, w) in enumerate(sorted(treffer))]}},
        breadcrumb_schema(teile)]}
    erstes = gruppen[sorted(treffer)[0]][0]
    body = f"""
  <main>
    <article>
      <section class="blog-hero sp-hero">
        <div class="wrap">
          {breadcrumb_html(teile)}
          <span class="eyebrow">Fertig verdrahtet · PDF mit Materialliste</span>
          <h1>{e(u["h1"])}</h1>
          <div class="blog-lead sp-text">{u["text"]}</div>
        </div>
      </section>
      <section class="blog-section" style="padding-top:8px">
        <div class="wrap">
          <div class="sp-grid">{"".join(karten)}</div>
        </div>
      </section>
      <section class="blog-section blog-section-alt">
        <div class="wrap">
          <h2>Weitere Übersichten</h2>
          <ul class="sp-links">{andere_html}<li><a href="/stromlaufplaene.html">Alle Pläne im Planfinder</a></li></ul>
        </div>
      </section>
      <section class="blog-section blog-section-final">
        <div class="blog-wrap">
          <p class="blog-eyebrow">Deine Kombination ist nicht dabei?</p>
          <h2>Ich plane dein System individuell</h2>
          <div class="blog-actions"><a href="/index.html#kontakt" class="btn btn-primary">Beratung buchen</a></div>
          {HINWEIS}
        </div>
      </section>
    </article>
  </main>
"""
    ende = '\n<script src="/cookie-consent.js"></script>\n<script src="/site.js"></script>\n</body>\n</html>\n'
    return kopf(u["title"], u["desc"], url, f"/assets/stromlaufplaene/{slug(erstes)}.webp", schema) + body + FUSS + ende


# ---------- Sitemap ----------
def sitemap(urls):
    pfad = SITE / "sitemap.xml"
    xml = pfad.read_text(encoding="utf-8")
    xml = re.sub(r"\s*<!-- PLAN-SEITEN START -->.*?<!-- PLAN-SEITEN ENDE -->", "", xml, flags=re.S)
    block = "\n  <!-- PLAN-SEITEN START -->" + "".join(
        f"\n  <url>\n    <loc>{BASIS}{u}</loc>\n    <lastmod>{HEUTE}</lastmod>\n  </url>" for u in urls) + "\n  <!-- PLAN-SEITEN ENDE -->"
    xml = xml.replace("\n</urlset>", block + "\n</urlset>")
    pfad.write_text(xml, encoding="utf-8")


def links_im_planfinder(gruppen):
    """Feste Links zu allen Plan- und Übersichtsseiten in stromlaufplaene.html (für Google ohne JavaScript)."""
    pfad = SITE / "stromlaufplaene.html"
    s = pfad.read_text(encoding="utf-8")
    a, z = "<!-- PLAN-SEITEN-LINKS START -->", "<!-- PLAN-SEITEN-LINKS ENDE -->"
    if a not in s:
        sys.exit("Markierung PLAN-SEITEN-LINKS fehlt in stromlaufplaene.html")
    zeilen = []
    for akku in sorted({k[0] for k in gruppen}):
        li = "".join(f'<li><a href="{seite_url(akku, w)}">{e(T.SEITEN[(akku, w)]["kurz"])}</a></li>'
                     for w in sorted(w for k, w in gruppen if k == akku))
        zeilen.append(f'<h3 style="margin:18px 0 8px;font-size:1rem">{akku} Ah LiFePO4</h3><ul class="sp-links">{li}</ul>')
    ueb = "".join(f'<li><a href="/schaltplan/{u["datei"]}.html">{e(u["h1"])}</a></li>' for u in T.UEBERSICHT.values())
    block = f"""{a}
      <section class="blog-section" id="nach-akku">
        <style>.sp-links{{display:flex;flex-wrap:wrap;gap:8px;margin:0;padding:0;list-style:none}}.sp-links a{{display:inline-block;padding:7px 13px;border-radius:999px;border:1px solid var(--line-2);color:var(--text-2);text-decoration:none;font-size:.9rem}}.sp-links a:hover{{border-color:rgba(230,178,0,.55);color:#fff}}</style>
        <div class="wrap">
          <p class="blog-eyebrow">Nach Akku und Wechselrichter</p>
          <h2>Alle Schaltpläne mit Details</h2>
          <p style="max-width:62ch">Jede Seite zeigt Querschnitte, Sicherungen und alle Varianten mit Solar und Ladebooster.</p>
          {"".join(zeilen)}
          <h3 style="margin:22px 0 8px;font-size:1rem">Übersichten</h3>
          <ul class="sp-links">{ueb}</ul>
        </div>
      </section>
      {z}"""
    s = re.sub(re.escape(a) + r".*?" + re.escape(z), lambda m: block, s, flags=re.S)
    pfad.write_text(s, encoding="utf-8")


def main():
    plaene = lade_plaene()
    gruppen = {}
    for p in plaene:
        gruppen.setdefault((p["akku"], p["inverter"]), []).append(p)
    fehlt = [k for k in gruppen if k not in T.SEITEN or k not in T.HAUPT]
    if fehlt:
        sys.exit(f"Texte/Werte fehlen für: {fehlt} – in plan_seiten_texte.py ergänzen")
    for k, g in gruppen.items():
        if len(g) != 6 or not any((p["solar"], p["booster"]) == STANDARD for p in g):
            sys.exit(f"Gruppe {k} hat nicht die 6 erwarteten Varianten")

    ORDNER.mkdir(exist_ok=True)
    urls = []
    for (a, w) in sorted(gruppen):
        (ORDNER / seite_datei(a, w)).write_text(plan_seite(a, w, gruppen[(a, w)], gruppen), encoding="utf-8")
        urls.append(seite_url(a, w))
    for (art, wert) in T.UEBERSICHT:
        u = T.UEBERSICHT[(art, wert)]
        (ORDNER / f"{u['datei']}.html").write_text(uebersicht_seite(art, wert, gruppen), encoding="utf-8")
        urls.append(f"/schaltplan/{u['datei']}.html")
    sitemap(urls)
    links_im_planfinder(gruppen)
    print(f"{len(gruppen)} Plan-Seiten + {len(T.UEBERSICHT)} Übersichten in /schaltplan/ erzeugt, Sitemap: {len(urls)} Einträge")


if __name__ == "__main__":
    main()
