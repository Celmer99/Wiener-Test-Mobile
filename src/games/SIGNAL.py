# =======================================
# SIGNAL – Web-Version (Touch-Bedienung, async für den Browser)
# =======================================
import asyncio
import random
import time

import pygame

from games import ergebnisse
from games.webstil import (WIDTH, HEIGHT, FPS, WHITE, BLACK, FONT_MARKANT,
                           abbrechen_zeichnen, ist_abbruch_event, ABBRECHEN_RECT,
                           zurueck_zeichnen)

SCORE_FONT = pygame.font.SysFont(FONT_MARKANT, 32)
COUNTDOWN_FONT = pygame.font.SysFont(FONT_MARKANT, 80)

TEMPO_SEKUNDEN = {"langsam": 0.90, "normal": 0.75, "schnell": 0.60}

# --- Punkte-Grid (10x6) ---
_SPALTEN_X = [250, 400, 550, 700, 850, 1000, 1150, 1300, 1450, 1600]
_ZEILEN_Y = [150, 300, 450, 600, 750, 900]
_BUCHSTABEN = "ABCDEFGHIJ"


def _grid_aufbauen():
    punkte = {}
    for spalte_idx, buchstabe in enumerate(_BUCHSTABEN):
        for zeile_idx in range(6):
            punkte[f"{buchstabe}{zeile_idx + 1}"] = (
                _SPALTEN_X[spalte_idx], _ZEILEN_Y[zeile_idx], 10, 10)
    return punkte


_PUNKTE = _grid_aufbauen()
DOT_LISTE = list(_PUNKTE.values())

VECKS = []
for L in "ABCDEFGHI":
    nextL = chr(ord(L) + 1)
    for n in range(1, 6):
        VECKS.append([_PUNKTE[f"{L}{n}"], _PUNKTE[f"{L}{n + 1}"],
                     _PUNKTE[f"{nextL}{n}"], _PUNKTE[f"{nextL}{n + 1}"]])

_START_AKTIV = ["B6", "C2", "C4", "D1", "D3", "D4", "D6", "E2", "E4", "E5",
                "F6", "G2", "G4", "H4", "H5", "I2", "J1", "J2", "J3", "J6"]


def _ist_reaktion(event):
    """Enter-Taste oder Klick/Tipp außerhalb des Abbrechen-Buttons."""
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        return True
    if event.type == pygame.MOUSEBUTTONDOWN and not ABBRECHEN_RECT.collidepoint(event.pos):
        return True
    return False


async def run(win, dauer_sekunden, tempo="normal"):
    tempo_sek = TEMPO_SEKUNDEN.get(tempo, 0.75)
    wiederholungen = max(1, round(dauer_sekunden / tempo_sek))
    dauer_text = (f"{dauer_sekunden // 60} Min" if dauer_sekunden >= 60
                  else f"{dauer_sekunden} Sek") + f", Tempo {tempo.capitalize()}"

    aktiv = [_PUNKTE[k] for k in _START_AKTIV]
    moeglich = [d for d in DOT_LISTE if d not in aktiv]
    gesperrt = set()
    erscheinungszeit = {}

    clock = pygame.time.Clock()

    for i in range(3, -1, -1):
        win.fill(BLACK)
        text = "GO!" if i == 0 else str(i)
        draw = COUNTDOWN_FONT.render(text, True, WHITE)
        win.blit(draw, (WIDTH / 2 - draw.get_width() / 2, HEIGHT / 2 - draw.get_height() / 2))
        pygame.display.flip()
        await asyncio.sleep(1.0)

    erkannte_quadrate = 0
    falsche_tasten = 0
    reaktionszeiten = []
    delay_active = True
    neue_quads = []
    runde = 0
    abgebrochen = False

    def reaktion_verarbeiten():
        nonlocal delay_active, neue_quads, erkannte_quadrate, falsche_tasten
        if not delay_active:
            return
        delay_active = False
        if neue_quads:
            for qkey in neue_quads:
                start_t = erscheinungszeit.get(qkey)
                if start_t is not None:
                    reaktionszeiten.append(time.time() - start_t)
                    erkannte_quadrate += 1
                    gesperrt.add(qkey)
                    erscheinungszeit.pop(qkey, None)
            neue_quads = []
        else:
            falsche_tasten += 1

    while runde < wiederholungen:
        naechster_wechsel = time.perf_counter() + tempo_sek
        while time.perf_counter() < naechster_wechsel:
            for event in pygame.event.get():
                if ist_abbruch_event(event):
                    abgebrochen = True
                    break
                if _ist_reaktion(event):
                    reaktion_verarbeiten()
            if abgebrochen:
                break

            win.fill(BLACK)
            for dot in aktiv:
                pygame.draw.rect(win, WHITE, pygame.Rect(dot))
            abbrechen_zeichnen(win)
            pygame.display.flip()
            clock.tick(FPS)
            await asyncio.sleep(0)

        if abgebrochen:
            break

        runde += 1
        delay_active = True
        for key in list(erscheinungszeit.keys()):
            if key not in gesperrt:
                gesperrt.add(key)
                erscheinungszeit.pop(key, None)

        if aktiv and moeglich:
            entf = random.choice(aktiv)
            einf = random.choice(moeglich)
            aktiv.remove(entf)
            moeglich.remove(einf)
            aktiv.append(einf)
            moeglich.append(entf)

        for q in VECKS:
            if all(p in aktiv for p in q):
                key = tuple(q)
                if key not in gesperrt and key not in erscheinungszeit:
                    erscheinungszeit[key] = time.time()
                    if key not in neue_quads:
                        neue_quads.append(key)

    avg_ms = round((sum(reaktionszeiten) / len(reaktionszeiten)) * 1000) if reaktionszeiten else 0
    ergebnisse.speichern("SIGNAL", dauer_text, erkannte_quadrate, falsche_tasten, avg_ms)
    await auswertung_anzeigen(win, erkannte_quadrate, falsche_tasten, avg_ms)


async def auswertung_anzeigen(win, erkannte_quadrate, falsche_tasten, avg_ms):
    win.fill(WHITE)
    text = f"Richtig: {erkannte_quadrate}   Falsch: {falsche_tasten}   Ø-Reaktionszeit: {avg_ms} ms"
    draw = SCORE_FONT.render(text, True, BLACK)
    win.blit(draw, (WIDTH / 2 - draw.get_width() / 2, HEIGHT / 2 - draw.get_height() / 2))
    hinweis = SCORE_FONT.render("Tippe, um zum Hauptmenü zurückzukehren...", True, BLACK)
    win.blit(hinweis, (WIDTH / 2 - hinweis.get_width() / 2, HEIGHT / 2 + 80))
    zurueck_zeichnen(win)
    pygame.display.flip()

    warten = True
    while warten:
        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                warten = False
        await asyncio.sleep(0)
