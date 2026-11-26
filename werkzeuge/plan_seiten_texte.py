"""Texte und Planwerte für die Schaltplan-Seiten (/schaltplan/…).

Wird von werkzeuge/plan_seiten.py gelesen. Hier nur Inhalte pflegen, kein Layout.

WERTE: aus den Materiallisten der PPTX-Pläne (Desktop/claude/Stromlaufplan/Pläne),
Stand 26.11.2026. Innerhalb einer Seite (Akku + Wechselrichter) sind Hauptsicherung,
Hauptleitung und Wechselrichter-Teil in allen 6 Varianten gleich.
Ändert sich ein Plan, hier nachziehen.
"""

# ---------- Planwerte ----------
# Hauptsicherung am Akku + Hauptleitung (Akku → Shunt → Busbar)
HAUPT = {
    (100, 0):    ("150 A MEGA", "35 mm²"),
    (100, 1000): ("150 A MEGA", "35 mm²"),
    (200, 0):    ("150 A MEGA", "35 mm²"),
    (200, 1000): ("150 A MEGA", "35 mm²"),
    (200, 1500): ("225 A MEGA", "70 mm²"),
    (200, 2000): ("250 A MEGA", "70 mm²"),
    (320, 0):    ("150 A MEGA", "35 mm²"),
    (320, 1000): ("150 A MEGA", "35 mm²"),
    (320, 1500): ("225 A MEGA", "70 mm²"),
    (320, 2000): ("250 A MEGA", "70 mm²"),
    (640, 0):    ("150 A Klasse T", "35 mm²"),
    (640, 1000): ("150 A Klasse T", "35 mm²"),
    (640, 1500): ("225 A Klasse T", "70 mm²"),
    (640, 2000): ("250 A Klasse T", "70 mm²"),
    (640, 3000): ("350 A Klasse T", "95 mm² SGX (bis 125 °C)"),
}
# Batteriewächter (Shunt) und Hauptschalter
SHUNT = {(640, 3000): ("500 A", "350 A")}          # sonst:
SHUNT_STANDARD = ("300 A", "275 A")
# Wechselrichter: Sicherung, Leitung, Ladestrom am Landstrom
WR = {
    1000: ("125 A MEGA", "35 mm²", 20),
    1500: ("200 A MEGA", "70 mm²", 30),
    2000: ("225 A MEGA", "70 mm²", 40),
    3000: ("300 A MEGA", "95 mm² SGX", 40),
}
BOOSTER = {
    30: "2 × 60 A MIDI, Leitung 16 mm², D+ 1,5 mm²",
    50: "2 × 80 A MIDI, Leitung 16 mm², D+ 1,5 mm²",
}
SOLAR = {
    100: "1 Modul 100 W, Laderegler MPPT 75/10, 20 A MIDI, 4 mm²",
    200: "2 × 100 W in Reihe (53,9 V Leerlauf), MPPT 75/15, 20 A MIDI, 4 mm²",
    300: "3 × 100 W in Reihe (80,8 V Leerlauf, kalt ca. 93 V), MPPT 100/20, 30 A MIDI, 6 mm² zum Akku",
}

# ---------- Texte je Seite ----------
# Schlüssel (akku, wechselrichter). Felder:
#   kurz: Kurzname für Karten/Breadcrumb · title/desc: Google · h1 · lead
#   abschnitte: [(Überschrift, HTML)] · variante: HTML für „Welche Variante?“
SEITEN = {

(100, 0): dict(
    kurz="100 Ah · nur 12 V",
    title="Schaltplan Wohnmobil 100 Ah LiFePO4 ohne Wechselrichter (12 V)",
    desc="Fertig verdrahteter Schaltplan fürs Wohnmobil: 100 Ah LiFePO4, Solar 100–300 W und Ladebooster 30 oder 50 A, reine 12-V-Anlage. PDF mit Querschnitten, Sicherungen und Materialliste.",
    h1="Schaltplan Wohnmobil: 100 Ah LiFePO4, reine 12-V-Anlage",
    lead="Der schlanke Einstieg: ein 100-Ah-Akku, Solar und Ladebooster, ganz ohne 230 V. Weniger Geräte, dünnere Leitungen und ein Plan, den du an einem Wochenende verkabeln kannst.",
    abschnitte=[
        ("Für wen passt dieser Plan?",
         "<p>Für Kastenwagen und kleinere Fahrzeuge, die vor allem 12-V-Verbraucher haben: Licht, Wasserpumpe, Kompressorkühlbox, USB-Ladung fürs Handy und ein Laptop über ein 12-V-Netzteil. Der Akku speichert nominal 1280 Wh (100 Ah × 12,8 V).</p>"
         "<p>Ohne Wechselrichter gibt es im Batteriebetrieb keine 230-V-Steckdose. Dafür fällt der größte Verbraucher der Anlage weg, und die Ströme bleiben klein.</p>"),
        ("Was der Plan festlegt",
         "<p>Die Hauptleitung vom Akku über Batteriewächter und Hauptschalter zur Busbar läuft in 35 mm², abgesichert mit einer 150-A-MEGA-Sicherung direkt am Akku. Ladebooster und Laderegler bekommen jeweils eigene Sicherungen an beiden Enden der Leitung.</p>"
         "<p>Ein praktischer Punkt: Der Plan mit 200 Ah nutzt genau dieselben Querschnitte und Sicherungen. Wenn du später einen größeren Akku einbaust, bleibt die Verkabelung gleich.</p>"),
    ],
    variante="<p>Bei 100 Ah reicht der <b>30-A-Ladebooster</b> meist aus. Der 50-A-Booster lohnt sich, wenn du oft nur kurze Strecken fährst und der Akku in wenig Fahrzeit voll werden soll. Prüfe vorher, ob deine Lichtmaschine genug Reserve hat. Beim Solar reichen 100 W für eine kleine Grundlast im Sommer; mit 200 oder 300 W stehst du auch bei wechselhaftem Wetter länger.</p>",
),

(100, 1000): dict(
    kurz="100 Ah · 1000 W",
    title="Schaltplan Wohnmobil 100 Ah LiFePO4 mit 1000 W Wechselrichter",
    desc="Schaltplan fürs Wohnmobil mit 100 Ah LiFePO4, 1000-W-Sinus-Wechselrichter mit 20-A-Ladegerät, Solar und Ladebooster. Mit 230-V-Teilplan, FI/LS, Querschnitten und Materialliste als PDF.",
    h1="Schaltplan Wohnmobil: 100 Ah LiFePO4 und 1000-W-Wechselrichter",
    lead="Die kleine Anlage mit 230 V: Ein 1000-W-Sinus-Wechselrichter versorgt Steckdosen im Fahrzeug und lädt am Landstrom den Akku mit 20 A.",
    abschnitte=[
        ("Für wen passt dieser Plan?",
         "<p>Für alle, die unterwegs ab und zu 230 V brauchen: Laptop-Netzteil, E-Bike-Akku, Akku-Werkzeug oder Kameras laden. Geräte bis 1000 W laufen im Batteriebetrieb. Für Dauerlast ist der 100-Ah-Akku aber knapp: Volle 1000 W würden seine 1280 Wh in gut einer Stunde leeren.</p>"),
        ("Was der Plan festlegt",
         "<p>Am Akku bleibt es bei 35 mm² und einer 150-A-MEGA-Hauptsicherung. Der Wechselrichter hängt mit 35 mm² an der Busbar und ist mit 125 A MEGA abgesichert. Auf der 230-V-Seite sitzen FI/LS-Schutzschalter, 3 × 2,5 mm² Leitung und der Schutzleiter mit 6 mm².</p>"
         "<p>Wichtig für den Campingplatz: Am Landstrom leitet der Wechselrichter die 230 V nur durch. Die Grenze von 1000 W gilt dann trotzdem. Große Verbraucher wie Wasserkocher oder einen Absorberkühlschrank greift der Plan deshalb vor dem Wechselrichter ab; sie haben nur 230 V, wenn Landstrom anliegt.</p>"),
    ],
    variante="<p>Mit Wechselrichter wird der Akku schneller leer. Deshalb passt hier oft der <b>50-A-Ladebooster</b>, wenn du regelmäßig fährst. Wer selten fährt und viel steht, legt den Schwerpunkt besser auf Solar: 200 oder 300 W.</p>",
),

(200, 0): dict(
    kurz="200 Ah · nur 12 V",
    title="Schaltplan Wohnmobil 200 Ah LiFePO4 ohne Wechselrichter (12 V)",
    desc="Schaltplan fürs Wohnmobil mit 200 Ah LiFePO4, Solar 100–300 W und Ladebooster 30 oder 50 A als reine 12-V-Anlage. Fertig verdrahtet mit Querschnitten, Sicherungen, Materialliste und Geräte-Einstellungen.",
    h1="Schaltplan Wohnmobil: 200 Ah LiFePO4, reine 12-V-Anlage",
    lead="Doppelt so viel Energie wie mit 100 Ah, aber dieselbe einfache Verkabelung: Die reine 12-V-Anlage mit 200 Ah ist der Klassiker für längeres Freistehen.",
    abschnitte=[
        ("Für wen passt dieser Plan?",
         "<p>Für Reisende, die mehrere Tage ohne Landstrom stehen und ihre Verbraucher auf 12 V haben: Kompressorkühlschrank, Dieselheizung, Licht, Pumpe und Laptop über ein 12-V-Netzteil. 200 Ah speichern nominal 2560 Wh.</p>"
         "<p>Ohne Wechselrichter gibt es keinen Verbraucher, der im Leerlauf ständig Strom zieht. Die Energie bleibt für das, was du wirklich nutzt.</p>"),
        ("Was der Plan festlegt",
         "<p>Die Hauptleitung läuft in 35 mm² mit einer 150-A-MEGA-Sicherung direkt am Akku, gemessen über einen 300-A-Batteriewächter und schaltbar über einen 275-A-Hauptschalter. Das sind dieselben Werte wie beim 100-Ah-Plan. Der größere Akku braucht also keine dickeren Kabel, weil die Ströme von Ladern und 12-V-Verbrauchern gleich bleiben.</p>"
         "<p>Möchtest du später 230 V nachrüsten, ist der Schritt zum Plan mit 1000-W-Wechselrichter klein: Die Hauptleitung bleibt bei 35 mm².</p>"),
    ],
    variante="<p>Bei 200 Ah spielt der <b>50-A-Ladebooster</b> seine Stärke aus: Er lädt während der Fahrt deutlich mehr nach als 30 A, und der größere Akku kann das auch aufnehmen. Beim Solar sind 200 oder 300 W eine gute Ergänzung zu 200 Ah.</p>",
),

(200, 1000): dict(
    kurz="200 Ah · 1000 W",
    title="Schaltplan Wohnmobil 200 Ah LiFePO4 mit 1000 W Wechselrichter",
    desc="Schaltplan fürs Wohnmobil: 200 Ah LiFePO4, 1000-W-Sinus-Wechselrichter mit 20-A-Landstrom-Ladegerät, Solar und Ladebooster. PDF mit 230-V-Teil, Sicherungen, Querschnitten und Materialliste.",
    h1="Schaltplan Wohnmobil: 200 Ah LiFePO4 und 1000-W-Wechselrichter",
    lead="Viel Kapazität, maßvolle 230 V: Die Anlage für alle, die vor allem 12 V nutzen und für Laptop, Ladegeräte und kleine Küchengeräte eine Steckdose möchten.",
    abschnitte=[
        ("Für wen passt dieser Plan?",
         "<p>Für Paare und Alleinreisende mit Homeoffice im Fahrzeug: Laptop, Monitor, Drohnen- oder Kamera-Akkus, E-Bike-Ladung. Mit 2560 Wh Speicher hält die Anlage auch einen Tag mit mehreren Stunden Laptop-Betrieb gut aus.</p>"),
        ("Was der Plan festlegt",
         "<p>Am Akku: 35 mm² und eine 150-A-MEGA-Hauptsicherung. Der 1000-W-Wechselrichter hängt mit 35 mm² und 125 A MEGA an der Busbar. Auf 230-V-Seite gehören FI/LS-Schutzschalter, 3 × 2,5 mm² und der Schutzleiter mit 6 mm² dazu.</p>"
         "<p>Am Landstrom lädt das eingebaute Ladegerät mit 20 A. Einen leeren 200-Ah-Akku bringt es so in gut zehn Stunden wieder auf voll, also über Nacht. Die 1000-W-Grenze gilt auch am Landstrom; große Verbraucher hängen deshalb vor dem Wechselrichter.</p>"
         "<p>Brauchst du später mehr 230-V-Leistung, steigt die Hauptleitung beim 1500- und 2000-W-Plan auf 70 mm². Wer das schon ahnt, plant besser gleich größer.</p>"),
    ],
    variante="<p>Fährst du regelmäßig, holt der <b>50-A-Booster</b> bei 200 Ah spürbar mehr in den Akku. Stehst du lange an einem Ort, sind 300 W Solar die bessere Investition.</p>",
),

(200, 1500): dict(
    kurz="200 Ah · 1500 W",
    title="Schaltplan Wohnmobil 200 Ah LiFePO4 mit 1500 W Wechselrichter",
    desc="Schaltplan Wohnmobil mit 200 Ah LiFePO4, 1500-W-Sinus-Wechselrichter mit 30-A-Ladegerät, Solar und Ladebooster. Hauptleitung 70 mm², Sicherungen, 230-V-Teil und Materialliste als PDF.",
    h1="Schaltplan Wohnmobil: 200 Ah LiFePO4 und 1500-W-Wechselrichter",
    lead="Ab 1500 W wird die Anlage spürbar kräftiger. Der Plan zeigt, was sich dafür ändert: dickere Hauptleitung, größere Sicherungen und ein Ladegerät mit 30 A.",
    abschnitte=[
        ("Für wen passt dieser Plan?",
         "<p>Für alle, die mehr als Ladegeräte betreiben möchten: eine Kaffeemaschine oder Mikrowelle bis 1500 W, ein Reise-Föhn oder Küchengeräte. Mit 2560 Wh reicht der Akku für viele kurze Einsätze am Tag; Dauerbetrieb mit voller Leistung ist mit 200 Ah nicht das Ziel.</p>"),
        ("Was der Plan festlegt",
         "<p>Hier liegt der große Schritt gegenüber 1000 W: Die Hauptleitung wächst von 35 auf 70 mm², die Hauptsicherung am Akku auf 225 A MEGA. Auch der Wechselrichter hängt mit 70 mm² an der Busbar, abgesichert mit 200 A MEGA.</p>"
         "<p>Das eingebaute Ladegerät lädt am Landstrom mit 30 A, ein leerer 200-Ah-Akku ist damit in rund sieben Stunden wieder voll. Auch am Landstrom dürfen hinter dem Wechselrichter höchstens 1500 W hängen; die Steckdose für Großverbraucher sitzt deshalb davor.</p>"),
    ],
    variante="<p>Mit 1500 W Verbrauch zählt jede Nachladung. Der <b>50-A-Booster</b> ist hier die naheliegende Wahl, dazu 200 oder 300 W Solar. 30 A reichen, wenn deine Lichtmaschine klein ist oder du überwiegend am Landstrom stehst.</p>",
),

(200, 2000): dict(
    kurz="200 Ah · 2000 W",
    title="Schaltplan Wohnmobil 200 Ah LiFePO4 mit 2000 W Wechselrichter",
    desc="Schaltplan fürs Wohnmobil: 200 Ah LiFePO4, 2000-W-Sinus-Wechselrichter mit 40-A-Ladegerät, Solar 100–300 W und Ladebooster. 70 mm², 250-A-Hauptsicherung, 230-V-Teil und Materialliste.",
    h1="Schaltplan Wohnmobil: 200 Ah LiFePO4 und 2000-W-Wechselrichter",
    lead="2000 W am 200-Ah-Akku: genug für Föhn, Induktionsplatte oder Kaffeevollautomat, mit einem Ladegerät, das am Landstrom 40 A in den Akku schiebt.",
    abschnitte=[
        ("Für wen passt dieser Plan?",
         "<p>Für alle, die im Fahrzeug wie zu Hause kochen und Kaffee machen möchten, aber nicht den Platz oder das Budget für einen sehr großen Akku haben. Kurze, kräftige Lasten sind das richtige Einsatzgebiet: 2000 W Dauerlast würden die 2560 Wh in gut einer Stunde leeren.</p>"),
        ("Was der Plan festlegt",
         "<p>Hauptleitung 70 mm² wie beim 1500-W-Plan, aber mit größeren Sicherungen: 250 A MEGA am Akku und 225 A MEGA vor dem Wechselrichter. Die 230-V-Seite bekommt FI/LS, 3 × 2,5 mm² und einen 6-mm²-Schutzleiter.</p>"
         "<p>Mit 40 A Ladestrom am Landstrom ist ein leerer 200-Ah-Akku in rund fünf bis sechs Stunden voll. Auch hier gilt die 2000-W-Grenze am Landstrom, große Verbraucher hängen vor dem Wechselrichter.</p>"),
    ],
    variante="<p>Bei 2000 W und 200 Ah empfehle ich meistens den <b>50-A-Booster</b> und 300 W Solar, damit der Akku nach kräftigen Lasten schnell wieder voll ist. Wer mehr Reserve möchte, schaut sich den gleichen Aufbau mit 320 Ah an.</p>",
),

(320, 0): dict(
    kurz="320 Ah · nur 12 V",
    title="Schaltplan Wohnmobil 320 Ah LiFePO4 ohne Wechselrichter (12 V)",
    desc="Schaltplan fürs Wohnmobil mit 320 Ah LiFePO4 als reine 12-V-Anlage: Solar 100–300 W, Ladebooster 30 oder 50 A, Hauptleitung 35 mm². PDF mit Sicherungen, Materialliste und Einstellungen.",
    h1="Schaltplan Wohnmobil: 320 Ah LiFePO4, reine 12-V-Anlage",
    lead="Viel Speicher, keine 230 V: Mit 320 Ah stehst du lange autark, und die Verkabelung bleibt so einfach wie bei den kleinen Plänen.",
    abschnitte=[
        ("Für wen passt dieser Plan?",
         "<p>Für Langzeitreisende und Wintercamper, deren Verbraucher alle auf 12 V laufen: Kompressorkühlschrank, Dieselheizung, Wasserpumpe, Licht und 12-V-Netzteile. 320 Ah speichern nominal 4096 Wh und überbrücken auch mehrere trübe Tage.</p>"),
        ("Was der Plan festlegt",
         "<p>Die Hauptleitung bleibt bei 35 mm² mit einer 150-A-MEGA-Sicherung am Akku. Der Akku ist zwar groß, aber ohne Wechselrichter fließen nur die Ströme der Lader und 12-V-Verbraucher. Dicke 70-mm²-Leitungen braucht es erst ab 1500 W.</p>"
         "<p>Gerade bei einem großen Akku ist der Batteriewächter (Shunt) wichtig: Er zeigt dir den echten Ladestand, damit du nicht nach Spannung schätzen musst. Die Einstellungen dafür stehen im Plan.</p>"),
    ],
    variante="<p>Ein großer Akku will gefüllt werden. Der <b>50-A-Booster</b> und 300 W Solar passen am besten zu 320 Ah. Mit 30 A und 100 W dauert das Nachladen deutlich länger; das reicht nur, wenn du wenig verbrauchst.</p>",
),

(320, 1000): dict(
    kurz="320 Ah · 1000 W",
    title="Schaltplan Wohnmobil 320 Ah LiFePO4 mit 1000 W Wechselrichter",
    desc="Schaltplan Wohnmobil mit 320 Ah LiFePO4 und 1000-W-Sinus-Wechselrichter (20-A-Ladegerät), Solar und Ladebooster. Fertig verdrahtet mit 230-V-Teil, Querschnitten, Sicherungen und Materialliste.",
    h1="Schaltplan Wohnmobil: 320 Ah LiFePO4 und 1000-W-Wechselrichter",
    lead="Große Reserve, kleine 230-V-Seite: 320 Ah für lange Autarkie und ein 1000-W-Wechselrichter für Laptop, Ladegeräte und kleine Geräte.",
    abschnitte=[
        ("Für wen passt dieser Plan?",
         "<p>Für alle, die viel frei stehen und 230 V nur für kleinere Geräte nutzen. Mit 4096 Wh im Akku kannst du den Wechselrichter für Laptop und Ladegeräte über Tage nutzen, ohne an Landstrom zu müssen.</p>"),
        ("Was der Plan festlegt",
         "<p>Am Akku: 35 mm² und 150 A MEGA. Der Wechselrichter hängt mit 35 mm² und 125 A MEGA an der Busbar, die 230-V-Seite ist mit FI/LS geschützt.</p>"
         "<p>Ein Punkt, den man bei dieser Kombination kennen sollte: Das Ladegerät im 1000-W-Wechselrichter lädt nur mit 20 A. Einen leeren 320-Ah-Akku füllt es erst in rund 16 Stunden. Der Landstrom ist hier eher die Ergänzung; die Hauptarbeit machen Solar und Ladebooster.</p>"),
    ],
    variante="<p>Weil das Landstrom-Ladegerät klein ist, lohnen sich hier der <b>50-A-Booster</b> und möglichst viel Solar besonders. 300 W sind die beste Wahl für 320 Ah.</p>",
),

(320, 1500): dict(
    kurz="320 Ah · 1500 W",
    title="Schaltplan Wohnmobil 320 Ah LiFePO4 mit 1500 W Wechselrichter",
    desc="Schaltplan fürs Wohnmobil: 320 Ah LiFePO4, 1500-W-Sinus-Wechselrichter mit 30-A-Ladegerät, Solar und Ladebooster. Hauptleitung 70 mm², 225-A-Hauptsicherung, 230-V-Teil und Materialliste.",
    h1="Schaltplan Wohnmobil: 320 Ah LiFePO4 und 1500-W-Wechselrichter",
    lead="Ausgewogen für Vielreisende: genug Akku für mehrere Tage und genug 230-V-Leistung für Kaffeemaschine oder Mikrowelle.",
    abschnitte=[
        ("Für wen passt dieser Plan?",
         "<p>Für Reisende, die regelmäßig 230-V-Geräte bis 1500 W nutzen und trotzdem nicht jeden Tag an den Landstrom wollen. Mit 4096 Wh verkraftet der Akku den morgendlichen Kaffee und das Mittagessen aus der Mikrowelle deutlich entspannter als 200 Ah.</p>"),
        ("Was der Plan festlegt",
         "<p>Ab 1500 W steigt die Hauptleitung auf 70 mm² mit 225 A MEGA am Akku. Der Wechselrichter ist mit 70 mm² und 200 A MEGA angebunden. Auf der 230-V-Seite: FI/LS, 3 × 2,5 mm², Schutzleiter 6 mm².</p>"
         "<p>Am Landstrom lädt der Wechselrichter mit 30 A, ein leerer 320-Ah-Akku braucht so rund elf Stunden. Die 1500-W-Grenze gilt auch am Landstrom; der Plan zeigt, wo du Großverbraucher davor abgreifst.</p>"),
    ],
    variante="<p>Zu 320 Ah und 1500 W passen der <b>50-A-Booster</b> und 300 W Solar am besten. Der 30-A-Booster ist die richtige Wahl, wenn deine Lichtmaschine wenig Reserve hat.</p>",
),

(320, 2000): dict(
    kurz="320 Ah · 2000 W",
    title="Schaltplan Wohnmobil 320 Ah LiFePO4 mit 2000 W Wechselrichter",
    desc="Schaltplan Wohnmobil mit 320 Ah LiFePO4, 2000-W-Sinus-Wechselrichter mit 40-A-Ladegerät, Solar 100–300 W und Ladebooster 30/50 A. 70 mm², 250 A Hauptsicherung, FI/LS und Materialliste.",
    h1="Schaltplan Wohnmobil: 320 Ah LiFePO4 und 2000-W-Wechselrichter",
    lead="Die Komplettanlage für den Alltag im Wohnmobil: 320 Ah Speicher, 2000 W an der Steckdose und 40 A Ladestrom am Landstrom.",
    abschnitte=[
        ("Für wen passt dieser Plan?",
         "<p>Für alle, die im Fahrzeug ohne große Einschränkung leben möchten: Induktionsplatte, Föhn, Kaffeevollautomat und dazu der normale 12-V-Bedarf. 4096 Wh lassen Platz für kräftige Lasten, ohne dass der Akku nach einem Abend leer ist.</p>"
         "<p>Eine ähnliche Anlage mit 450 W Solar zeige ich ausführlich im Beitrag <a href=\"/blog-stufe-4.html\">Wohnmobil-Solaranlage Stufe 4</a>.</p>"),
        ("Was der Plan festlegt",
         "<p>Hauptleitung 70 mm² mit 250 A MEGA am Akku, der Wechselrichter mit 70 mm² und 225 A MEGA. Die 230-V-Seite bekommt FI/LS, 3 × 2,5 mm² und den 6-mm²-Schutzleiter.</p>"
         "<p>Das Ladegerät im Wechselrichter lädt am Landstrom mit 40 A, ein leerer 320-Ah-Akku ist damit in rund acht Stunden voll. Am Landstrom gilt die 2000-W-Grenze weiter; große Verbraucher greift der Plan vor dem Wechselrichter ab.</p>"),
    ],
    variante="<p>Für diese Anlage empfehle ich den <b>50-A-Booster</b> und 300 W Solar. So wird der große Akku auch nach Tagen mit viel 230-V-Nutzung wieder voll.</p>",
),

(640, 0): dict(
    kurz="640 Ah · nur 12 V",
    title="Schaltplan Wohnmobil 640 Ah LiFePO4 ohne Wechselrichter (12 V)",
    desc="Schaltplan fürs Wohnmobil mit 640 Ah LiFePO4 als 12-V-Anlage: Klasse-T-Hauptsicherung 150 A, 35 mm², Solar 100–300 W und Ladebooster. Fertig verdrahtet mit Materialliste und Einstellungen.",
    h1="Schaltplan Wohnmobil: 640 Ah LiFePO4, reine 12-V-Anlage",
    lead="Maximale Autarkie ohne 230 V: 640 Ah speichern über 8 kWh. Dafür ändert sich die wichtigste Sicherung im ganzen Plan.",
    abschnitte=[
        ("Für wen passt dieser Plan?",
         "<p>Für Langzeitreisende und Wintercamper mit 12-V-Verbrauchern, die wochenlang ohne Landstrom auskommen wollen: Kompressorkühlschrank, Dieselheizung, Wasser, Licht und Laptop über 12 V. Nominal sind 8192 Wh im Akku.</p>"),
        ("Was der Plan festlegt: Klasse T statt MEGA",
         "<p>Ein so großer LiFePO4-Akku kann bei einem Kurzschluss extrem hohe Ströme liefern. MEGA- oder ANL-Sicherungen haben dafür ein zu geringes Abschaltvermögen. Deshalb sitzt bei 640 Ah eine <b>150-A-Klasse-T-Sicherung</b> direkt am Pluspol des Akkus. Sie schaltet laut Herstellerangabe bis 20.000 A sicher ab.</p>"
         "<p>Die Hauptleitung bleibt bei 35 mm², denn ohne Wechselrichter fließen nur die Ströme der Lader und 12-V-Verbraucher.</p>"),
    ],
    variante="<p>640 Ah wollen gefüllt werden: <b>50-A-Booster</b> und 300 W Solar sind hier fast Pflicht, wenn du den Akku regelmäßig nutzt. Kleinere Lader passen nur, wenn der große Akku vor allem als Reserve dient.</p>",
),

(640, 1000): dict(
    kurz="640 Ah · 1000 W",
    title="Schaltplan Wohnmobil 640 Ah LiFePO4 mit 1000 W Wechselrichter",
    desc="Schaltplan Wohnmobil: 640 Ah LiFePO4 mit Klasse-T-Sicherung, 1000-W-Sinus-Wechselrichter mit 20-A-Ladegerät, Solar und Ladebooster. PDF mit 230-V-Teil, Querschnitten und Materialliste.",
    h1="Schaltplan Wohnmobil: 640 Ah LiFePO4 und 1000-W-Wechselrichter",
    lead="Riesiger Speicher, kleine 230-V-Seite: für alle, die wochenlang autark sein und 230 V nur für Laptop und Ladegeräte nutzen möchten.",
    abschnitte=[
        ("Für wen passt dieser Plan?",
         "<p>Für Langzeitreisende mit Homeoffice oder viel Elektronik, die aber keine Küchengeräte über 230 V betreiben. 8192 Wh im Akku machen den Laptop-Alltag auch bei wenig Sonne unkompliziert.</p>"),
        ("Was der Plan festlegt",
         "<p>Am Akku sitzt eine 150-A-Klasse-T-Sicherung, weil ein 640-Ah-Akku im Kurzschluss mehr Strom liefert, als MEGA-Sicherungen sicher abschalten. Die Hauptleitung bleibt bei 35 mm². Der Wechselrichter hängt mit 35 mm² und 125 A MEGA an der Busbar.</p>"
         "<p>Das Ladegerät im Wechselrichter lädt am Landstrom nur mit 20 A. Einen leeren 640-Ah-Akku würde es erst in rund 32 Stunden füllen. Bei dieser Kombination ist der Landstrom also nur eine Zugabe; Solar und Ladebooster sind die eigentlichen Lader.</p>"),
    ],
    variante="<p>Hier gibt es kaum eine Alternative zum <b>50-A-Booster</b> und 300 W Solar, wenn du den großen Akku auch wirklich nutzen willst.</p>",
),

(640, 1500): dict(
    kurz="640 Ah · 1500 W",
    title="Schaltplan Wohnmobil 640 Ah LiFePO4 mit 1500 W Wechselrichter",
    desc="Schaltplan fürs Wohnmobil: 640 Ah LiFePO4, 225-A-Klasse-T-Hauptsicherung, 70 mm², 1500-W-Sinus-Wechselrichter mit 30-A-Ladegerät, Solar und Ladebooster. Mit FI/LS und Materialliste.",
    h1="Schaltplan Wohnmobil: 640 Ah LiFePO4 und 1500-W-Wechselrichter",
    lead="Großer Akku, solide 230-V-Leistung: Mit 1500 W laufen Kaffeemaschine und Mikrowelle, und der Akku hält trotzdem lange durch.",
    abschnitte=[
        ("Für wen passt dieser Plan?",
         "<p>Für alle, die lange frei stehen und dabei regelmäßig 230-V-Küchengeräte bis 1500 W nutzen. Bei 8192 Wh fällt eine Kaffeemaschine am Morgen kaum ins Gewicht.</p>"),
        ("Was der Plan festlegt",
         "<p>Die Hauptsicherung am Akku ist eine 225-A-Klasse-T-Sicherung, die Hauptleitung läuft ab hier in 70 mm². Der Wechselrichter ist mit 70 mm² und 200 A MEGA angebunden. Auf der 230-V-Seite: FI/LS, 3 × 2,5 mm² und der Schutzleiter mit 6 mm².</p>"
         "<p>Das Ladegerät im Wechselrichter lädt mit 30 A. Einen leeren 640-Ah-Akku bringt es in knapp einem Tag auf voll; für eine Nacht am Campingplatz reicht das zum Auffüllen, nicht zum kompletten Laden.</p>"),
    ],
    variante="<p>Zu 640 Ah gehören der <b>50-A-Booster</b> und 300 W Solar. Mit 30 A oder 100 W wird der große Akku nach einer Phase mit viel Verbrauch nur langsam wieder voll.</p>",
),

(640, 2000): dict(
    kurz="640 Ah · 2000 W",
    title="Schaltplan Wohnmobil 640 Ah LiFePO4 mit 2000 W Wechselrichter",
    desc="Schaltplan Wohnmobil mit 640 Ah LiFePO4, 250-A-Klasse-T-Sicherung, 70 mm², 2000-W-Sinus-Wechselrichter mit 40-A-Ladegerät, Solar und Ladebooster. Fertig verdrahtet als PDF mit Materialliste.",
    h1="Schaltplan Wohnmobil: 640 Ah LiFePO4 und 2000-W-Wechselrichter",
    lead="Für den Alltag im Fahrzeug ohne Verzicht: 2000 W für Induktion, Föhn und Kaffeevollautomat, und genug Akku, um das tagelang durchzuhalten.",
    abschnitte=[
        ("Für wen passt dieser Plan?",
         "<p>Für Vollzeit-Reisende und Familien, die elektrisch kochen und viele 230-V-Geräte nutzen. Mit 8192 Wh im Akku sind auch mehrere kräftige Lasten am Tag kein Problem.</p>"),
        ("Was der Plan festlegt",
         "<p>Am Akku sitzt eine 250-A-Klasse-T-Sicherung, die Hauptleitung ist 70 mm². Der Wechselrichter hängt mit 70 mm² und 225 A MEGA an der Busbar. 230-V-Seite mit FI/LS, 3 × 2,5 mm² und 6-mm²-Schutzleiter.</p>"
         "<p>Am Landstrom lädt der Wechselrichter mit 40 A, ein leerer 640-Ah-Akku braucht damit rund 16 Stunden. Die 2000-W-Grenze gilt auch am Landstrom; große Verbraucher greift der Plan vor dem Wechselrichter ab.</p>"),
    ],
    variante="<p>Für diese Anlage empfehle ich klar den <b>50-A-Booster</b> und 300 W Solar. Wer noch mehr 230-V-Leistung braucht, findet den Plan mit 3000 W.</p>",
),

(640, 3000): dict(
    kurz="640 Ah · 3000 W",
    title="Schaltplan Wohnmobil 640 Ah LiFePO4 mit 3000 W Wechselrichter",
    desc="Schaltplan fürs Wohnmobil: 640 Ah LiFePO4, 3000-W-Sinus-Wechselrichter mit 40-A-Ladegerät, 350-A-Klasse-T-Sicherung, 95 mm² SGX-Kabel, 500-A-Shunt. Mit Solar, Ladebooster und Materialliste.",
    h1="Schaltplan Wohnmobil: 640 Ah LiFePO4 und 3000-W-Wechselrichter",
    lead="Die größte Anlage im Programm: 3000 W an der Steckdose. Damit ändern sich Kabel, Sicherungen, Shunt und Hauptschalter, und der Plan zeigt jedes Detail.",
    abschnitte=[
        ("Für wen passt dieser Plan?",
         "<p>Für alle, die im Fahrzeug fast wie zu Hause leben: Wasserkocher, Induktionskochfeld, Kaffeevollautomat, auch zwei Geräte gleichzeitig bis zusammen 3000 W. Der 640-Ah-Akku mit 8192 Wh sorgt dafür, dass diese Leistung nicht nach einer Stunde vorbei ist.</p>"),
        ("Was der Plan festlegt",
         "<p>Bei 3000 W wird alles eine Nummer größer: <b>350-A-Klasse-T-Sicherung</b> am Akku, 500-A-Batteriewächter und 350-A-Hauptschalter. Hauptleitung und Wechselrichterleitung laufen in <b>95 mm² SGX</b>, einem Batteriekabel mit XLPE-Isolierung, zugelassen bis 125 °C. Der Wechselrichter ist mit 300 A MEGA abgesichert.</p>"
         "<p>Warum SGX? Normales PVC-Kabel (70 °C) verträgt bei 95 mm² nur 292 A und wäre für die 300- und 350-A-Sicherungen zu schwach. Ohne SGX müsstest du 120 mm² verlegen.</p>"
         "<p>Am Landstrom lädt der Wechselrichter mit 40 A. Auch hier gilt die Grenze von 3000 W am Landstrom; große Verbraucher greift der Plan vor dem Wechselrichter ab.</p>"),
    ],
    variante="<p>Bei 3000 W ist der <b>50-A-Booster</b> zusammen mit 300 W Solar die sinnvolle Wahl. Der 30-A-Booster passt nur, wenn deine Lichtmaschine keine Reserve für 50 A hat.</p>",
),
}

# ---------- Übersichtsseiten ----------
# Schlüssel: (art, wert) mit art = akku | wr | solar | booster
UEBERSICHT = {
    ("akku", 100): dict(
        datei="akku-100ah",
        title="Schaltpläne Wohnmobil mit 100 Ah LiFePO4",
        h1="Schaltpläne mit 100 Ah LiFePO4",
        desc="Fertig verdrahtete Wohnmobil-Schaltpläne mit 100 Ah LiFePO4: reine 12-V-Anlage oder mit 1000-W-Wechselrichter, jeweils mit Solar 100–300 W und Ladebooster 30 oder 50 A.",
        text="<p>100 Ah sind der Einstieg in die Lithium-Welt: nominal 1280 Wh, leicht und kompakt. Die Pläne gibt es als reine 12-V-Anlage und mit 1000-W-Wechselrichter. Beide nutzen eine 35-mm²-Hauptleitung mit 150-A-MEGA-Sicherung.</p>"),
    ("akku", 200): dict(
        datei="akku-200ah",
        title="Schaltpläne Wohnmobil mit 200 Ah LiFePO4",
        h1="Schaltpläne mit 200 Ah LiFePO4",
        desc="Wohnmobil-Schaltpläne mit 200 Ah LiFePO4: ohne Wechselrichter oder mit 1000, 1500 und 2000 W, jeweils mit Solar und Ladebooster. Fertig verdrahtet mit Querschnitten und Materialliste.",
        text="<p>200 Ah (2560 Wh) sind die beliebteste Größe für Wohnmobile. Bis 1000 W Wechselrichter reicht eine 35-mm²-Hauptleitung, ab 1500 W wird auf 70 mm² verkabelt. Wähle aus, wie viel 230 V du brauchst.</p>"),
    ("akku", 320): dict(
        datei="akku-320ah",
        title="Schaltpläne Wohnmobil mit 320 Ah LiFePO4",
        h1="Schaltpläne mit 320 Ah LiFePO4",
        desc="Wohnmobil-Schaltpläne mit 320 Ah LiFePO4 für lange Autarkie: ohne Wechselrichter oder mit 1000, 1500 und 2000 W, mit Solar und Ladebooster als fertig verdrahtetes PDF.",
        text="<p>320 Ah speichern rund 4 kWh und sind ideal für längeres Freistehen. Die Verkabelung richtet sich nach dem Wechselrichter: bis 1000 W in 35 mm², ab 1500 W in 70 mm².</p>"),
    ("akku", 640): dict(
        datei="akku-640ah",
        title="Schaltpläne Wohnmobil mit 640 Ah LiFePO4 und Klasse-T-Sicherung",
        h1="Schaltpläne mit 640 Ah LiFePO4",
        desc="Wohnmobil-Schaltpläne mit 640 Ah LiFePO4 und Klasse-T-Hauptsicherung: ohne Wechselrichter oder mit 1000 bis 3000 W, mit Solar und Ladebooster. Fertig verdrahtet mit Materialliste.",
        text="<p>640 Ah (über 8 kWh) für maximale Autarkie. Alle Pläne mit diesem Akku nutzen eine Klasse-T-Sicherung direkt am Pluspol, weil ein so großer Akku im Kurzschluss mehr Strom liefert, als MEGA-Sicherungen sicher abschalten. Bei 3000 W kommen 95-mm²-SGX-Kabel und ein 500-A-Shunt dazu.</p>"),
    ("wr", 0): dict(
        datei="ohne-wechselrichter",
        title="Schaltpläne Wohnmobil ohne Wechselrichter: reine 12-V-Anlage",
        h1="Schaltpläne ohne Wechselrichter (nur 12 V)",
        desc="Wohnmobil-Schaltpläne als reine 12-V-Anlage ohne Wechselrichter: LiFePO4 100 bis 640 Ah, Solar 100–300 W und Ladebooster 30 oder 50 A. Fertig verdrahtet mit Materialliste.",
        text="<p>Ohne Wechselrichter bleibt die Anlage einfach: keine 230-V-Seite, kein Leerlaufverbrauch und eine Hauptleitung mit 35 mm², egal wie groß der Akku ist. Ideal, wenn Kühlschrank, Heizung und Laptop auf 12 V laufen.</p>"),
    ("wr", 1000): dict(
        datei="wechselrichter-1000w",
        title="Schaltpläne Wohnmobil mit 1000 W Wechselrichter",
        h1="Schaltpläne mit 1000-W-Wechselrichter",
        desc="Wohnmobil-Schaltpläne mit 1000-W-Sinus-Wechselrichter und 20-A-Ladegerät: LiFePO4 100 bis 640 Ah, Solar und Ladebooster, mit 230-V-Teilplan und FI/LS.",
        text="<p>1000 W reichen für Laptop, Ladegeräte und kleine Geräte. Der Wechselrichter hängt mit 35 mm² und 125 A MEGA an der Busbar und lädt am Landstrom mit 20 A. Je größer der Akku, desto mehr übernehmen Solar und Ladebooster das Laden.</p>"),
    ("wr", 1500): dict(
        datei="wechselrichter-1500w",
        title="Schaltpläne Wohnmobil mit 1500 W Wechselrichter",
        h1="Schaltpläne mit 1500-W-Wechselrichter",
        desc="Wohnmobil-Schaltpläne mit 1500-W-Sinus-Wechselrichter und 30-A-Ladegerät: LiFePO4 200, 320 oder 640 Ah, Hauptleitung 70 mm², mit Solar, Ladebooster und Materialliste.",
        text="<p>Ab 1500 W wird die Anlage kräftiger: Hauptleitung 70 mm², Wechselrichter mit 200 A MEGA, Ladegerät mit 30 A. Genug für Kaffeemaschine und Mikrowelle.</p>"),
    ("wr", 2000): dict(
        datei="wechselrichter-2000w",
        title="Schaltpläne Wohnmobil mit 2000 W Wechselrichter",
        h1="Schaltpläne mit 2000-W-Wechselrichter",
        desc="Wohnmobil-Schaltpläne mit 2000-W-Sinus-Wechselrichter und 40-A-Ladegerät: LiFePO4 200, 320 oder 640 Ah, 70 mm² und 250-A-Hauptsicherung, mit Solar und Ladebooster.",
        text="<p>2000 W für Föhn, Induktionsplatte und Kaffeevollautomat. Die Pläne nutzen 70 mm², eine 250-A-Hauptsicherung und 225 A MEGA vor dem Wechselrichter. Am Landstrom lädt er mit 40 A.</p>"),
    ("wr", 3000): dict(
        datei="wechselrichter-3000w",
        title="Schaltplan Wohnmobil mit 3000 W Wechselrichter",
        h1="Schaltplan mit 3000-W-Wechselrichter",
        desc="Wohnmobil-Schaltplan mit 3000-W-Sinus-Wechselrichter, 640 Ah LiFePO4, 350-A-Klasse-T-Sicherung und 95 mm² SGX-Kabel, mit Solar, Ladebooster und Materialliste.",
        text="<p>3000 W sind die Oberklasse: 95 mm² SGX-Kabel, 350-A-Klasse-T-Sicherung, 500-A-Shunt und 350-A-Hauptschalter. Diesen Wechselrichter gibt es deshalb nur mit dem 640-Ah-Akku.</p>"),
    ("solar", 100): dict(
        datei="solar-100w",
        title="Schaltpläne Wohnmobil mit 100 W Solar",
        h1="Schaltpläne mit 100 W Solar",
        desc="Wohnmobil-Schaltpläne mit 100-W-Solarmodul und MPPT 75/10: mit LiFePO4 100 bis 640 Ah, Ladebooster und optional Wechselrichter. Fertig verdrahtet mit Materialliste.",
        text="<p>Ein 100-W-Modul am Laderegler MPPT 75/10, abgesichert mit 20 A MIDI und angeschlossen mit 4 mm². Die kleine Solaranlage für Grundlast und Erhaltung. 100 W gibt es in jedem Plan als Variante.</p>"),
    ("solar", 200): dict(
        datei="solar-200w",
        title="Schaltpläne Wohnmobil mit 200 W Solar",
        h1="Schaltpläne mit 200 W Solar",
        desc="Wohnmobil-Schaltpläne mit 200 W Solar (2 × 100 W in Reihe) und MPPT 75/15, mit LiFePO4 100 bis 640 Ah, Ladebooster und optional Wechselrichter.",
        text="<p>Zwei 100-W-Module in Reihe (53,9 V Leerlaufspannung) an einem MPPT 75/15. Absicherung 20 A MIDI, Leitung 4 mm². 200 W gibt es in jedem Plan als Variante.</p>"),
    ("solar", 300): dict(
        datei="solar-300w",
        title="Schaltpläne Wohnmobil mit 300 W Solar",
        h1="Schaltpläne mit 300 W Solar",
        desc="Wohnmobil-Schaltpläne mit 300 W Solar (3 × 100 W in Reihe) und MPPT 100/20, mit LiFePO4 100 bis 640 Ah, Ladebooster und optional Wechselrichter bis 3000 W.",
        text="<p>Drei 100-W-Module in Reihe: 80,8 V Leerlauf, bei Kälte rund 93 V. Darum sitzt hier ein MPPT 100/20, abgesichert mit 30 A MIDI und mit 6 mm² zum Akku. 300 W gibt es in jedem Plan als Variante.</p>"),
    ("booster", 30): dict(
        datei="ladebooster-30a",
        title="Schaltpläne Wohnmobil mit 30 A Ladebooster",
        h1="Schaltpläne mit 30-A-Ladebooster",
        desc="Wohnmobil-Schaltpläne mit 30-A-Ladebooster: zwei 60-A-MIDI-Sicherungen, 16 mm² und D+-Leitung, mit LiFePO4 100 bis 640 Ah, Solar und optional Wechselrichter.",
        text="<p>Der 30-A-Ladebooster passt zu kleineren Lichtmaschinen und kleineren Akkus. Im Plan ist er mit zwei 60-A-MIDI-Sicherungen und 16 mm² angeschlossen. Welche Größe zu deinem Fahrzeug passt, erkläre ich im Beitrag <a href=\"/ladebooster-30a-oder-50a-wirkungsgrad.html\">30 A oder 50 A Ladebooster</a>.</p>"),
    ("booster", 50): dict(
        datei="ladebooster-50a",
        title="Schaltpläne Wohnmobil mit 50 A Ladebooster",
        h1="Schaltpläne mit 50-A-Ladebooster",
        desc="Wohnmobil-Schaltpläne mit 50-A-Ladebooster: zwei 80-A-MIDI-Sicherungen, 16 mm² und D+-Leitung, mit LiFePO4 100 bis 640 Ah, Solar und optional Wechselrichter.",
        text="<p>Der 50-A-Ladebooster lädt während der Fahrt deutlich mehr nach und passt besonders zu großen Akkus. Im Plan ist er mit zwei 80-A-MIDI-Sicherungen und 16 mm² angeschlossen; ist der Weg von der Starterbatterie länger als 3 m, zeigt der Plan die Lösung mit 25 mm². Ob deine Lichtmaschine das schafft, steht im Beitrag <a href=\"/ladebooster-lichtmaschine.html\">Ladebooster und Lichtmaschine</a>.</p>"),
}
