# =======================================
# Wiener Test SEK – Web-Version für unterwegs (Handy/Tablet, Touch-Bedienung)
# Enthält DAUF, SIGNAL, INHIB, VIGIL, VISGED. SIMKAP bleibt der PC-Version
# vorbehalten (Sprachausgabe, viele kleine Felder – am Handy nicht sinnvoll).
# =======================================
import asyncio
import importlib

import pygame

from games import ergebnisse
from games.webstil import (WIDTH, HEIGHT, FPS, WHITE, BLACK, STEEL, BTN_FILL,
                           FONT_MARKANT, hintergrund_zeichnen, titel_zeichnen,
                           button_zeichnen, zurueck_zeichnen, ist_abbruch_event)

SPIELE = [
    ("DAUF", "games.DAUF"),
    ("SIGNAL", "games.SIGNAL"),
    ("INHIB", "games.INHIB"),
    ("VISGED", "games.VISGED"),
    ("VIGIL", "games.VIGIL"),
]

TEMPO_STUFEN = [("Langsam", "langsam"), ("Normal", "normal"), ("Schnell", "schnell")]
EINPRAEG_STUFEN = [("Lang", "langsam"), ("Normal", "normal"), ("Kurz", "schnell")]
SYMBOLE_VISGED = [(str(n), n) for n in (4, 5, 6, 7, 8, 9)]
RUNDEN_VISGED = [(str(n), n) for n in (1, 5, 10, 20, 35, 50)]
DAUERN_KACHELN = [
    ("Testlauf", 30), ("5 Min", 300), ("10 Min", 600), ("15 Min", 900),
    ("20 Min", 1200), ("25 Min", 1500), ("30 Min", 1800), ("45 Min", 2700), ("60 Min", 3600),
]

INSTRUKTIONEN = {
    "DAUF": [
        "Dir werden fortlaufend 7 Dreiecke angezeigt.",
        "Tippe, sobald genau 3 Dreiecke",
        "mit der Spitze nach unten zeigen.",
    ],
    "SIGNAL": [
        "Auf dem Punktefeld erscheinen und verschwinden laufend Punkte.",
        "Tippe, sobald 4 Punkte",
        "zusammen ein Quadrat bilden.",
    ],
    "INHIB": [
        "In der Mitte erscheint ein Pfeil nach links oder rechts.",
        "Tippe schnellstmöglich auf den passenden Pfeil-Button unten –",
        "aber NICHT, wenn kurz darauf ein Ton erklingt!",
        "Der Ton kommt mit der Zeit immer später: Je besser du stoppst,",
        "desto schwerer wird es.",
    ],
    "VISGED": [
        "Präge dir die Position der Symbole auf der Karte ein.",
        "Danach wird jedes Symbol einzeln angezeigt.",
        "Tippe auf die Stelle der Karte, an der es sich befand.",
    ],
    "VIGIL": [
        "Ein Punkt wandert Sprung für Sprung im Kreis.",
        "Tippe, wenn der Punkt einen Doppelsprung macht.",
    ],
}


async def fenster_oeffnen():
    pygame.init()
    pygame.font.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Wiener Test SEK')
    pygame.event.clear()
    return win


def kachel_reihe(eintraege, kachel_w, kachel_h, gap, start_y, spalten):
    rects = []
    zeilen = [eintraege[i:i + spalten] for i in range(0, len(eintraege), spalten)]
    for z, zeile in enumerate(zeilen):
        zeilen_breite = len(zeile) * kachel_w + (len(zeile) - 1) * gap
        x0 = WIDTH // 2 - zeilen_breite // 2
        y = start_y + z * (kachel_h + gap)
        for s, (label, wert) in enumerate(zeile):
            rects.append((pygame.Rect(x0 + s * (kachel_w + gap), y, kachel_w, kachel_h), label, wert))
    return rects


async def button_menue(win, titel, eintraege, button_height=70, gap=18, start_y=260):
    """Einfache Buttonliste. Rückgabe: gewählter Wert oder None."""
    button_font = pygame.font.SysFont(FONT_MARKANT, 30)
    clock = pygame.time.Clock()
    button_width = 700

    while True:
        hintergrund_zeichnen(win)
        titel_zeichnen(win, titel)
        rects = []
        for i, (label, wert) in enumerate(eintraege):
            rect = pygame.Rect(WIDTH // 2 - button_width // 2,
                               start_y + i * (button_height + gap),
                               button_width, button_height)
            rects.append((rect, wert))
            button_zeichnen(win, rect, label, button_font, False, rot=(wert is None))

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, wert in rects:
                    if rect.collidepoint(event.pos):
                        return wert


async def kombi_menue(win, titel, gruppen, spalten=3):
    """Mehrere Kachel-Gruppen auf einer Seite (z. B. Tempo + Dauer).

    Rückgabe: Tupel der gewählten Werte, oder None bei Zurück."""
    label_font = pygame.font.SysFont(FONT_MARKANT, 28)
    kachel_font = pygame.font.SysFont(FONT_MARKANT, 36)
    button_font = pygame.font.SysFont(FONT_MARKANT, 30)
    clock = pygame.time.Clock()

    gesamt_zeilen = sum((len(e) + spalten - 1) // spalten for _, e, _ in gruppen)
    kompakt = gesamt_zeilen > 4
    kachel_w = 200
    kachel_h = 80 if kompakt else 100
    gap = 18 if kompakt else 24
    label_h = 42 if kompakt else 47
    gruppen_abstand = 28 if kompakt else 40

    gruppen_layout = []
    y = 212 if kompakt else 218
    for label, eintraege, _ in gruppen:
        label_y = y
        y += label_h
        rects = kachel_reihe(eintraege, kachel_w, kachel_h, gap, y, spalten)
        zeilen = (len(eintraege) + spalten - 1) // spalten
        y += zeilen * (kachel_h + gap) - gap + gruppen_abstand
        gruppen_layout.append((label, label_y, rects))

    start_rect = pygame.Rect(WIDTH // 2 - 360, y + 12, 720, 70)

    wahlen = [vorauswahl for _, _, vorauswahl in gruppen]

    while True:
        hintergrund_zeichnen(win)
        titel_zeichnen(win, titel)
        zurueck_zeichnen(win)

        for i, (label, label_y, rects) in enumerate(gruppen_layout):
            draw = label_font.render(label.upper(), True, STEEL)
            win.blit(draw, (WIDTH // 2 - draw.get_width() // 2, label_y))
            for rect, kachel_label, wert in rects:
                button_zeichnen(win, rect, kachel_label, kachel_font, wert == wahlen[i])

        bereit = all(w is not None for w in wahlen)
        if bereit:
            button_zeichnen(win, start_rect, "Start", button_font, False, gruen=True)
        else:
            pygame.draw.rect(win, BTN_FILL, start_rect)
            pygame.draw.rect(win, STEEL, start_rect, 2)
            text = button_font.render("START", True, STEEL)
            win.blit(text, (start_rect.centerx - text.get_width() // 2,
                            start_rect.centery - text.get_height() // 2))

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)

        for event in pygame.event.get():
            if ist_abbruch_event(event):
                return None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, (_, _, rects) in enumerate(gruppen_layout):
                    for rect, _, wert in rects:
                        if rect.collidepoint(event.pos):
                            wahlen[i] = wert
                if bereit and start_rect.collidepoint(event.pos):
                    return tuple(wahlen)


async def instruktion_anzeigen(win, spiel_name):
    """Rückgabe: True = Test starten, False = zurück zum Hauptmenü."""
    text_font = pygame.font.SysFont(FONT_MARKANT, 34)
    hinweis_font = pygame.font.SysFont(FONT_MARKANT, 28)
    clock = pygame.time.Clock()
    zeilen = INSTRUKTIONEN.get(spiel_name, [])

    while True:
        hintergrund_zeichnen(win)
        titel_zeichnen(win, spiel_name)
        zurueck_zeichnen(win)

        zeilen_hoehe = 56
        y = HEIGHT // 2 - (len(zeilen) * zeilen_hoehe) // 2
        for zeile in zeilen:
            draw = text_font.render(zeile, True, WHITE)
            win.blit(draw, (WIDTH // 2 - draw.get_width() // 2, y))
            y += zeilen_hoehe

        hinweis = hinweis_font.render("TIPPEN, UM ZU STARTEN...", True, STEEL)
        win.blit(hinweis, (WIDTH // 2 - hinweis.get_width() // 2, 900))

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)

        for event in pygame.event.get():
            if ist_abbruch_event(event):
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True


async def statistik_anzeigen(win):
    kopf_font = pygame.font.SysFont(FONT_MARKANT, 24)
    zeilen_font = pygame.font.SysFont(FONT_MARKANT, 22)
    hinweis_font = pygame.font.SysFont(FONT_MARKANT, 28)
    button_font = pygame.font.SysFont(FONT_MARKANT, 30)
    clock = pygame.time.Clock()

    eintraege = ergebnisse.laden()
    eintraege.reverse()
    eintraege = eintraege[:14]

    spalten = [("Datum", 140), ("Zeit", 280), ("Test", 380), ("Einstellung", 520),
               ("Richtig", 900), ("Falsch", 1050), ("RT", 1200), ("Details", 1330)]

    reset_rect = pygame.Rect(WIDTH // 2 - 570, 960, 560, 60)
    zurueck_rect = pygame.Rect(WIDTH // 2 + 10, 960, 560, 60)
    ja_rect = pygame.Rect(WIDTH // 2 - 570, 620, 560, 60)
    nein_rect = pygame.Rect(WIDTH // 2 + 10, 620, 560, 60)
    bestaetigen = False

    while True:
        hintergrund_zeichnen(win)
        titel_zeichnen(win, "Statistik")

        if bestaetigen:
            frage = hinweis_font.render("WIRKLICH ALLE ERGEBNISSE LÖSCHEN?", True, WHITE)
            win.blit(frage, (WIDTH // 2 - frage.get_width() // 2, 480))
            button_zeichnen(win, ja_rect, "Ja, löschen", button_font, False, rot=True)
            button_zeichnen(win, nein_rect, "Abbrechen", button_font, False)
        elif not eintraege:
            leer = hinweis_font.render("NOCH KEINE ERGEBNISSE VORHANDEN", True, STEEL)
            win.blit(leer, (WIDTH // 2 - leer.get_width() // 2, 450))
        else:
            for name, x in spalten:
                draw = kopf_font.render(name.upper(), True, STEEL)
                win.blit(draw, (x, 250))
            pygame.draw.rect(win, STEEL, (140, 290, 1600, 2))
            y = 310
            for e in eintraege:
                werte = [e.get("Datum", ""), e.get("Uhrzeit", ""), e.get("Test", ""),
                         str(e.get("Einstellung", ""))[:26], e.get("Richtig", ""),
                         e.get("Falsch", ""), e.get("Reaktionszeit_ms", ""),
                         str(e.get("Details", ""))[:20]]
                for (name, x), wert in zip(spalten, werte):
                    draw = zeilen_font.render(str(wert), True, WHITE)
                    win.blit(draw, (x, y))
                y += 42

        if not bestaetigen:
            button_zeichnen(win, reset_rect, "Zurücksetzen", button_font, False)
            button_zeichnen(win, zurueck_rect, "Zurück", button_font, False, rot=True)

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if bestaetigen:
                    if ja_rect.collidepoint(event.pos):
                        ergebnisse.loeschen()
                        eintraege = []
                        bestaetigen = False
                    elif nein_rect.collidepoint(event.pos):
                        bestaetigen = False
                else:
                    if reset_rect.collidepoint(event.pos) and eintraege:
                        bestaetigen = True
                    elif zurueck_rect.collidepoint(event.pos):
                        return


async def spiel_starten(win, modulname, spiel_name, wert=None, tempo=None,
                        symbole=None, runden=None):
    modul = importlib.import_module(modulname)
    if modulname == "games.VISGED":
        await modul.run(win, symbole=symbole, runden=runden, tempo=tempo)
    else:
        await modul.run(win, dauer_sekunden=wert, tempo=tempo)


async def main():
    win = await fenster_oeffnen()

    while True:
        eintraege = [(name, modul) for name, modul in SPIELE]
        eintraege.append(("Statistik", "STATISTIK"))

        modulname = await button_menue(win, "Wiener Test SEK", eintraege,
                                       button_height=90, gap=22, start_y=230)

        if modulname == "STATISTIK":
            await statistik_anzeigen(win)
            continue

        spiel_name = modulname.split(".")[-1]

        if modulname == "games.VISGED":
            auswahl = await kombi_menue(win, spiel_name, [
                ("Einprägzeit", EINPRAEG_STUFEN, "normal"),
                ("Anzahl der Symbole", SYMBOLE_VISGED, None),
                ("Anzahl der Runden", RUNDEN_VISGED, None),
            ])
            if auswahl is None:
                win = await fenster_oeffnen()
                continue
            tempo, symbole, runden = auswahl
            if not await instruktion_anzeigen(win, spiel_name):
                win = await fenster_oeffnen()
                continue
            await spiel_starten(win, modulname, spiel_name, tempo=tempo,
                                symbole=symbole, runden=runden)
        else:
            auswahl = await kombi_menue(win, spiel_name, [
                ("Geschwindigkeit", TEMPO_STUFEN, "normal"),
                ("Übungsdauer", DAUERN_KACHELN, None),
            ])
            if auswahl is None:
                win = await fenster_oeffnen()
                continue
            tempo, wert = auswahl
            if not await instruktion_anzeigen(win, spiel_name):
                win = await fenster_oeffnen()
                continue
            await spiel_starten(win, modulname, spiel_name, wert=wert, tempo=tempo)

        win = await fenster_oeffnen()


asyncio.run(main())
