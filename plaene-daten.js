/* ============================================================
   Gemeinsame Plan-Daten für stromlaufplaene.html UND index.html
   (Schnellfinder auf der Startseite). Neue Pläne NUR hier eintragen.
   Nach Änderungen in beiden Seiten ?v= bei plaene-daten.js erhöhen.
   ============================================================ */
/* ============================================================
   PLÄNE – hier pflegen.
   Nur Pläne in dieser Liste erscheinen auf der Seite.
   digistore: Kauf-Link von Digistore24 (leer = "bald verfügbar")
   preis:     z. B. "19,90 €" (leer = "Preis folgt")
   ============================================================ */
let PLAENE = [
  {solar:100, booster:30, akku:100, inverter:0,    regler:"MPPT 75/10",  seiten:6, preis:"15 €", digistore:"https://www.checkout-ds24.com/product/770782"},
  {solar:100, booster:30, akku:100, inverter:1000, regler:"MPPT 75/10",  seiten:7, preis:"17 €", digistore:"https://www.checkout-ds24.com/product/770921"},
  {solar:100, booster:50, akku:100, inverter:0,    regler:"MPPT 75/10",  seiten:6, preis:"15 €", digistore:"https://www.checkout-ds24.com/product/771188"},
  {solar:100, booster:50, akku:100, inverter:1000, regler:"MPPT 75/10",  seiten:7, preis:"17 €", digistore:"https://www.checkout-ds24.com/product/770931"},
  {solar:200, booster:30, akku:100, inverter:0,    regler:"MPPT 75/15",  seiten:6, preis:"15 €", digistore:"https://www.checkout-ds24.com/product/770897"},
  {solar:200, booster:30, akku:100, inverter:1000, regler:"MPPT 75/15",  seiten:7, preis:"17 €", digistore:"https://www.checkout-ds24.com/product/770929"},
  {solar:200, booster:50, akku:100, inverter:0,    regler:"MPPT 75/15",  seiten:6, preis:"15 €", digistore:"https://www.checkout-ds24.com/product/771194"},
  {solar:200, booster:50, akku:100, inverter:1000, regler:"MPPT 75/15",  seiten:7, preis:"17 €", digistore:"https://www.checkout-ds24.com/product/770932"},
  {solar:300, booster:30, akku:100, inverter:0,    regler:"MPPT 100/20", seiten:6, preis:"15 €", digistore:"https://www.checkout-ds24.com/product/770911"},
  {solar:300, booster:30, akku:100, inverter:1000, regler:"MPPT 100/20", seiten:7, preis:"17 €", digistore:"https://www.checkout-ds24.com/product/770930"},
  {solar:300, booster:50, akku:100, inverter:0,    regler:"MPPT 100/20", seiten:6, preis:"15 €", digistore:"https://www.checkout-ds24.com/product/771195"},
  {solar:300, booster:50, akku:100, inverter:1000, regler:"MPPT 100/20", seiten:7, preis:"17 €", digistore:"https://www.checkout-ds24.com/product/770933"},
  {solar:100, booster:50, akku:200, inverter:0,    regler:"MPPT 75/10",  seiten:6, preis:"15 €", digistore:"https://www.checkout-ds24.com/product/771324"},
  {solar:200, booster:50, akku:200, inverter:0,    regler:"MPPT 75/15",  seiten:6, preis:"15 €", digistore:"https://www.checkout-ds24.com/product/771323"},
  {solar:300, booster:50, akku:200, inverter:0,    regler:"MPPT 100/20", seiten:6, preis:"15 €", digistore:"https://www.checkout-ds24.com/product/771322"},
  {solar:100, booster:50, akku:200, inverter:1500, regler:"MPPT 75/10",  seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/771326"},
  {solar:200, booster:50, akku:200, inverter:1500, regler:"MPPT 75/15",  seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/771325"},
  {solar:300, booster:50, akku:200, inverter:1500, regler:"MPPT 100/20", seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/771197"},
  {solar:100, booster:50, akku:200, inverter:1000, regler:"MPPT 75/10",  seiten:7, preis:"17 €", digistore:"https://www.checkout-ds24.com/product/771740"},
  {solar:200, booster:50, akku:200, inverter:1000, regler:"MPPT 75/15",  seiten:7, preis:"17 €", digistore:"https://www.checkout-ds24.com/product/771741"},
  {solar:300, booster:50, akku:200, inverter:1000, regler:"MPPT 100/20", seiten:7, preis:"17 €", digistore:"https://www.checkout-ds24.com/product/771742"},
  {solar:100, booster:30, akku:200, inverter:0,    regler:"MPPT 75/10",  seiten:6, preis:"15 €", digistore:"https://www.checkout-ds24.com/product/771743"},
  {solar:100, booster:30, akku:200, inverter:1000, regler:"MPPT 75/10",  seiten:7, preis:"17 €", digistore:"https://www.checkout-ds24.com/product/771744"},
  {solar:100, booster:30, akku:200, inverter:1500, regler:"MPPT 75/10",  seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/771745"},
  {solar:200, booster:30, akku:200, inverter:0,    regler:"MPPT 75/15",  seiten:6, preis:"15 €", digistore:"https://www.checkout-ds24.com/product/771746"},
  {solar:200, booster:30, akku:200, inverter:1000, regler:"MPPT 75/15",  seiten:7, preis:"17 €", digistore:"https://www.checkout-ds24.com/product/771747"},
  {solar:200, booster:30, akku:200, inverter:1500, regler:"MPPT 75/15",  seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/771748"},
  {solar:300, booster:30, akku:200, inverter:0,    regler:"MPPT 100/20", seiten:6, preis:"15 €", digistore:"https://www.checkout-ds24.com/product/771749"},
  {solar:300, booster:30, akku:200, inverter:1000, regler:"MPPT 100/20", seiten:7, preis:"17 €", digistore:"https://www.checkout-ds24.com/product/771751"},
  {solar:300, booster:30, akku:200, inverter:1500, regler:"MPPT 100/20", seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/771752"},
  {solar:100, booster:30, akku:200, inverter:2000, regler:"MPPT 75/10",  seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/771949"},
  {solar:100, booster:50, akku:200, inverter:2000, regler:"MPPT 75/10",  seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/771950"},
  {solar:200, booster:30, akku:200, inverter:2000, regler:"MPPT 75/15",  seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/771951"},
  {solar:200, booster:50, akku:200, inverter:2000, regler:"MPPT 75/15",  seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/771952"},
  {solar:300, booster:30, akku:200, inverter:2000, regler:"MPPT 100/20", seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/771954"},
  {solar:300, booster:50, akku:200, inverter:2000, regler:"MPPT 100/20", seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/771948"},
  {solar:100, booster:30, akku:320, inverter:0,    regler:"MPPT 75/10",  seiten:6, preis:"15 €", digistore:"https://www.checkout-ds24.com/product/772057"},
  {solar:200, booster:30, akku:320, inverter:0,    regler:"MPPT 75/15",  seiten:6, preis:"15 €", digistore:"https://www.checkout-ds24.com/product/772060"},
  {solar:300, booster:30, akku:320, inverter:0,    regler:"MPPT 100/20", seiten:6, preis:"15 €", digistore:"https://www.checkout-ds24.com/product/772064"},
  {solar:100, booster:50, akku:320, inverter:0,    regler:"MPPT 75/10",  seiten:6, preis:"15 €", digistore:"https://www.checkout-ds24.com/product/772048"},
  {solar:200, booster:50, akku:320, inverter:0,    regler:"MPPT 75/15",  seiten:6, preis:"15 €", digistore:"https://www.checkout-ds24.com/product/772049"},
  {solar:300, booster:50, akku:320, inverter:0,    regler:"MPPT 100/20", seiten:6, preis:"15 €", digistore:"https://www.checkout-ds24.com/product/772050"},
  {solar:100, booster:30, akku:320, inverter:1000, regler:"MPPT 75/10",  seiten:7, preis:"17 €", digistore:"https://www.checkout-ds24.com/product/772058"},
  {solar:200, booster:30, akku:320, inverter:1000, regler:"MPPT 75/15",  seiten:7, preis:"17 €", digistore:"https://www.checkout-ds24.com/product/772061"},
  {solar:300, booster:30, akku:320, inverter:1000, regler:"MPPT 100/20", seiten:7, preis:"17 €", digistore:"https://www.checkout-ds24.com/product/772065"},
  {solar:100, booster:50, akku:320, inverter:1000, regler:"MPPT 75/10",  seiten:7, preis:"17 €", digistore:"https://www.checkout-ds24.com/product/772054"},
  {solar:200, booster:50, akku:320, inverter:1000, regler:"MPPT 75/15",  seiten:7, preis:"17 €", digistore:"https://www.checkout-ds24.com/product/772055"},
  {solar:300, booster:50, akku:320, inverter:1000, regler:"MPPT 100/20", seiten:7, preis:"17 €", digistore:"https://www.checkout-ds24.com/product/772056"},
  {solar:100, booster:30, akku:320, inverter:1500, regler:"MPPT 75/10",  seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/772059"},
  {solar:200, booster:30, akku:320, inverter:1500, regler:"MPPT 75/15",  seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/772063"},
  {solar:300, booster:30, akku:320, inverter:1500, regler:"MPPT 100/20", seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/772066"},
  {solar:100, booster:50, akku:320, inverter:1500, regler:"MPPT 75/10",  seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/772051"},
  {solar:200, booster:50, akku:320, inverter:1500, regler:"MPPT 75/15",  seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/772052"},
  {solar:300, booster:50, akku:320, inverter:1500, regler:"MPPT 100/20", seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/772053"},
  {solar:100, booster:30, akku:320, inverter:2000, regler:"MPPT 75/10",  seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/772067"},
  {solar:200, booster:30, akku:320, inverter:2000, regler:"MPPT 75/15",  seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/772070"},
  {solar:300, booster:30, akku:320, inverter:2000, regler:"MPPT 100/20", seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/772075"},
  {solar:100, booster:50, akku:320, inverter:2000, regler:"MPPT 75/10",  seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/772068"},
  {solar:200, booster:50, akku:320, inverter:2000, regler:"MPPT 75/15",  seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/772074"},
  {solar:300, booster:50, akku:320, inverter:2000, regler:"MPPT 100/20", seiten:7, preis:"18 €", digistore:"https://www.checkout-ds24.com/product/772076"},
];

// Rabatt-Aktion: Streichpreis + Aktionspreis bis zum Ende-Zeitpunkt, danach automatisch wieder Normalpreis.
// Rabatt über Digistore24-Rabattcode (code, gleiches Ablaufdatum wie bis); der Kauf-Link bekommt ?voucher=<code>.
const AKTION = {name: "Black Week", rabatt: 30, code: "BLACKWEEK", bis: "2026-11-29T23:59:59+01:00", bisText: "Sonntag, 29.11., 23:59 Uhr"};
const aktionAn = () => Date.now() <= Date.parse(AKTION.bis);
const kaufLink = p => aktionAn() ? `${p.digistore}?voucher=${AKTION.code}` : p.digistore;
const euro = n => (Number.isInteger(n) ? String(n) : n.toFixed(2).replace(".", ",")) + " €";
const aktionsPreis = p => euro(Math.round(parseFloat(p.preis.replace(",", ".")) * (100 - AKTION.rabatt)) / 100);
const preisHtml = p => !p.preis ? "Preis folgt"
  : aktionAn() ? `<s class="slp-alt">${p.preis}</s> <span class="slp-neu">${aktionsPreis(p)}</span>` : p.preis;

// Seiten im 3D-Karussell (Bild = PDF-Seite, Ordner assets/stromlaufplaene/<plan>/)
const VORSCHAU = {
  6: [[2,"Gesamtplan"],[3,"Teilplan Batterie"],[4,"Teilplan Ladebooster"],[5,"Teilplan Solar"],[6,"Materialliste"],[1,"Hinweise"]],
  7: [[2,"Gesamtplan"],[3,"Teilplan Batterie"],[4,"Teilplan Ladebooster"],[5,"Teilplan Solar"],[6,"Teilplan 230 V"],[7,"Materialliste"],[1,"Hinweise"]],
};
PLAENE.forEach(p => p.vorschau ||= VORSCHAU[p.seiten]);

// Ladestrom des Wechselrichters am Landstrom, in A (Ective 1000 W: 20 A, Ective CSI 15 PRO 1500 W: 30 A, Ective CSI 20 PRO Gen2 2000 W: 40 A)
const LADER = {1000: 20, 1500: 30, 2000: 40};
const KEYS = ["solar","booster","akku","inverter"];
const NAME = {solar:"Solarleistung", booster:"Ladebooster", akku:"Akku", inverter:"Spannungswandler"};
const LABEL = {
  solar: v => v + " W",
  booster: v => v + " A",
  akku: v => v + " Ah",
  inverter: v => v ? v + " W" : "ohne",
};
const SUB = {
  solar: () => "Modulleistung gesamt",
  booster: () => "Ladestrom während der Fahrt",
  akku: () => "12,8 V LiFePO4",
  inverter: v => v ? `Sinus 230 V · ${LADER[v]} A Ladegerät` : "nur 12 V",
};
const slug = p => `plan-solar${p.solar}-booster${p.booster}-akku${p.akku}${p.inverter ? "-" + p.inverter + "w" : ""}`;
// Bilder unter /assets/ sind ein Jahr im Browser gespeichert: nach neuen Vorschaubildern BILD_V erhöhen
const BILD_V = "2";
const bild = p => `assets/stromlaufplaene/${slug(p)}.webp?v=${BILD_V}`;
const titel = p => `Solar ${p.solar} W · Ladebooster ${p.booster} A · Akku ${p.akku} Ah` + (p.inverter ? ` · Wechselrichter ${p.inverter} W mit ${LADER[p.inverter]} A Ladegerät` : "");
