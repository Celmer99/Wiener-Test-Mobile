# Wiener Test SEK – Web-Version

Trainingsprogramm für die Testverfahren des Wiener Testsystems, direkt im
Browser spielbar (Handy, Tablet, PC). Touch-Bedienung, keine Installation
nötig.

Enthält: DAUF, SIGNAL, INHIB, VIGIL, VISGED.

## Nutzung

Einfach die veröffentlichte Seite öffnen (siehe GitHub Pages-Link im
Repository) – funktioniert direkt im Browser, ohne Installation.

## Quellcode

Der Python-Quellcode liegt im Ordner [`src/`](src/) (gebaut mit
[pygbag](https://github.com/pygame-web/pygbag)). Die Dateien `index.html`,
`web.apk`, `web.tar.gz` und `favicon.png` im Hauptverzeichnis sind der
fertige Build, den GitHub Pages ausliefert – diese Dateien müssen nach
Änderungen am Quellcode neu gebaut werden:

```bash
python -m pygbag --build web
```
