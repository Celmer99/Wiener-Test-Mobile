# Wiener Test SEK – mobile Trainingsversion

Browser-Trainingsprogramm für Smartphones, Tablets und PCs. Die erste mobile
Ausbaustufe konzentriert sich auf **fünf Tests**:

- **DAUF** – Daueraufmerksamkeit
- **SIGNAL** – Quadrate erkennen
- **VIGIL** – Doppelsprünge erkennen
- **INHIB** – Reaktionskontrolle
- **VISGED** – visuelles Gedächtnis

**SIMKAP** ist vorerst nicht im Menü verfügbar. Sein bisheriger Quellcode
bleibt für eine mögliche spätere Erweiterung erhalten.

## Mobile Nutzung

- Das Hauptmenü ist als Raster mit zwei Spalten und drei Reihen aufgebaut
  (fünf Tests und Statistik).
- Für Smartphones ist zunächst die Nutzung **im Querformat** vorgesehen.
- Die Spielmechaniken und Auswertungen wurden in diesem Schritt nicht verändert.
- Die bereits vorhandene Touch-Bedienung muss pro Test auf echten
  Smartphones geprüft werden.

## Entwicklung und Veröffentlichung

Der Python-Quellcode liegt in [`src/`](src/) und verwendet Pygame/Pygbag.
Die Dateien `index.html`, `web.apk` und `web.tar.gz` im Wurzelverzeichnis
bilden die Browser-Veröffentlichung.

**Wichtig:** Änderungen in `src/` erscheinen erst dann in der veröffentlichten
App, wenn die Pygbag-Pakete (`web.apk` und `web.tar.gz`) neu erzeugt
und zusammen mit `index.html` bereitgestellt werden. Die bloße Änderung
des Python-Quellcodes ändert die Website nicht.

## Nächste Schritte

1. Web-Build mit den fünf Tests neu erzeugen.
2. Hauptmenü, Teststart und Abbruch auf Android und/oder iPhone prüfen.
3. DAUF, SIGNAL, VIGIL, INHIB und VISGED einzeln für Touch- und
   Bildschirmgrößen optimieren.
4. Statistik und Offline-Nutzung erweitern.
