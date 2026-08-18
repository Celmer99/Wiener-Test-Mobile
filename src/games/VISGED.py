# =======================================
# VISGED – Web-Version (Touch-Bedienung, async für den Browser)
# Zustandslogik (EINGABE/ANZEIGEN/RESET) 1:1 aus der PC-Version übernommen.
# =======================================
import asyncio
import random

import pygame

from games import ergebnisse
from games.webstil import (WIDTH, HEIGHT, FPS, WHITE, BLACK, FONT_MARKANT,
                           abbrechen_zeichnen, ist_abbruch_event,
                           resource_path, ABBRECHEN_RECT, zurueck_zeichnen)

RED = (255, 0, 0)
SCORE_FONT = pygame.font.SysFont(FONT_MARKANT, 32)
COUNTDOWN_FONT = pygame.font.SysFont(FONT_MARKANT, 80)

KARTEN_WIDHT = [400, 1433]
KARTEN_HIGHT = [120, 849]


def _lade_bild(dateiname):
    return pygame.image.load(resource_path(dateiname))


KARTEN = [_lade_bild(f'Karte{i}.PNG') for i in range(1, 5)]
ICON_DATEIEN = ['Bahnhof.png', 'Bar.PNG', 'Bibliothek.PNG', 'Bushaltestelle.PNG',
                'Cafe.PNG', 'Campingplatz.PNG', 'Flughafen.PNG', 'Information.PNG',
                'Kirche.PNG', 'Krankenhaus.PNG', 'Poststelle.PNG', 'Tankstelle.PNG',
                'Taxi_Stand.PNG', 'Telefon.PNG', 'WC.PNG']
ICONS = [_lade_bild(name) for name in ICON_DATEIEN]

FRAMES_PRO_SYMBOL = 240
PUNKTE_PRO_SYMBOL = 130
_EINPRAEG_STUFEN = {"langsam": 600, "normal": 420, "schnell": 300}
_EINPRAEG_NAMEN = {"langsam": "Lang", "normal": "Normal", "schnell": "Kurz"}


def _layout(anzahl_symbole):
    karte = random.choice(KARTEN)
    gezogene_icons = random.sample(ICONS, anzahl_symbole)

    def random_pos(prev_rects):
        while True:
            x = random.randint(*KARTEN_WIDHT)
            y = random.randint(*KARTEN_HIGHT)
            rect = pygame.Rect(x, y, 65, 61)
            if all(not rect.colliderect(r) for r in prev_rects):
                return x, y, rect

    uebungs_icons = []
    belegte_rects = []
    for icon in gezogene_icons:
        x, y, rect = random_pos(belegte_rects)
        belegte_rects.append(rect)
        uebungs_icons.append((icon, x, y))
    return karte, uebungs_icons


async def run(win, symbole, runden, tempo="normal"):
    anzeige_frames = _EINPRAEG_STUFEN.get(tempo, 420)
    tempo_name = _EINPRAEG_NAMEN.get(tempo, "Normal")
    runden_frames = anzeige_frames + symbole * FRAMES_PRO_SYMBOL

    clock = pygame.time.Clock()
    genauigkeit = []

    karte, uebungs_icons = _layout(symbole)
    gameloop = 0
    runde = 0
    eingabe = False
    anzeigen = False
    reset = True
    treffer = (0, 0)
    abgebrochen = False

    while runde < runden:
        for event in pygame.event.get():
            if ist_abbruch_event(event):
                abgebrochen = True
                break
            if (event.type == pygame.MOUSEBUTTONDOWN and eingabe and not anzeigen
                    and not ABBRECHEN_RECT.collidepoint(event.pos)):
                treffer = event.pos
                anzeigen = True
        if abgebrochen:
            break

        gameloop += 1

        win.fill(WHITE)
        if gameloop < anzeige_frames and not eingabe:
            win.blit(karte, (400, 120))
            for icon, x, y in uebungs_icons:
                win.blit(icon, (x, y))
        elif gameloop >= anzeige_frames:
            index = (gameloop - anzeige_frames) // FRAMES_PRO_SYMBOL
            phase = (gameloop - anzeige_frames) % FRAMES_PRO_SYMBOL
            if index < len(uebungs_icons):
                icon, x, y = uebungs_icons[index]
                if phase < FRAMES_PRO_SYMBOL // 2:
                    anzeigen = False
                    reset = True
                    win.fill(WHITE)
                    win.blit(icon, (WIDTH / 2 - 32, HEIGHT / 2 - 30))
                else:
                    win.fill(WHITE)
                    win.blit(karte, (400, 120))
                    eingabe = True
                    if not anzeigen:
                        rect = pygame.Rect(0, 0, 65, 61)
                        rect.center = pygame.mouse.get_pos()
                        win.blit(icon, rect)
                    if anzeigen:
                        pygame.draw.circle(win, RED, (x + 32, y + 30), 130, 5)
                        win.blit(icon, (x, y))
                        win.blit(icon, (int(treffer[0]) - 32, int(treffer[1]) - 30))
                        if reset:
                            wert_w = abs(treffer[0] - x - 32)
                            wert_h = abs(treffer[1] - y - 30)
                            genauigkeit.append(max(0, 130 - max(wert_w, wert_h)))
                            reset = False
                        eingabe = False

        abbrechen_zeichnen(win)
        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)

        if gameloop > runden_frames:
            runde += 1
            if runde < runden:
                gameloop = 0
                eingabe = False
                anzeigen = False
                reset = True
                karte, uebungs_icons = _layout(symbole)

    max_punkte = PUNKTE_PRO_SYMBOL * symbole * runden
    prozent = round(sum(genauigkeit) / max_punkte * 100, 2) if genauigkeit else 0

    ergebnisse.speichern(
        "VISGED", f"{symbole} Symbole, {runden} Runden, Einprägzeit {tempo_name}",
        f"{sum(genauigkeit)} Pkt", f"{max_punkte - sum(genauigkeit)} Pkt",
        None, details=f"{prozent}% Genauigkeit")

    await auswertung_anzeigen(win, sum(genauigkeit), max_punkte, prozent)


async def auswertung_anzeigen(win, punkte, max_punkte, prozent):
    win.fill(BLACK)
    ergebnis = f"Score: {punkte} Pkt. von {max_punkte} Pkt. ({prozent}%) richtig."
    draw = SCORE_FONT.render(ergebnis, True, WHITE)
    win.blit(draw, (WIDTH / 2 - draw.get_width() / 2, HEIGHT / 2 - 60))
    hinweis = SCORE_FONT.render("Tippe, um zum Hauptmenü zurückzukehren...", True, WHITE)
    win.blit(hinweis, (WIDTH / 2 - hinweis.get_width() / 2, HEIGHT / 2 + 40))
    zurueck_zeichnen(win)
    pygame.display.flip()

    warten = True
    while warten:
        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                warten = False
        await asyncio.sleep(0)
