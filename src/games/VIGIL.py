# =======================================
# VIGIL – Web-Version (Touch-Bedienung, async für den Browser)
# =======================================
import asyncio
import random
import time

import pygame

from games import ergebnisse
from games.webstil import (WIDTH, HEIGHT, FPS, WHITE, BLACK, FONT_MARKANT,
                           abbrechen_zeichnen, ist_abbruch_event, ABBRECHEN_RECT,
                           resource_path, zurueck_zeichnen)

SCORE_FONT = pygame.font.SysFont(FONT_MARKANT, 32)
COUNTDOWN_FONT = pygame.font.SysFont(FONT_MARKANT, 80)

PUNKT = pygame.image.load(resource_path('Punkt.png'))

TEMPO_SEKUNDEN = {"langsam": 2.0, "normal": 1.5, "schnell": 1.2}

_KREIS_POSITIONEN = [
    (921, 263), (972, 269), (1019, 284), (1064, 309), (1103, 340),
    (1137, 379), (1162, 424), (1176, 474), (1180, 524), (1176, 574),
    (1164, 624), (1137, 667), (1105, 706), (1065, 740), (1020, 765),
    (972, 779), (921, 785), (869, 780), (820, 765), (775, 740),
    (736, 707), (704, 667), (679, 624), (665, 574), (660, 524),
    (665, 474), (679, 424), (704, 379), (736, 340), (776, 307),
    (820, 284), (869, 269),
]


def _ist_reaktion(event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        return True
    if event.type == pygame.MOUSEBUTTONDOWN and not ABBRECHEN_RECT.collidepoint(event.pos):
        return True
    return False


async def run(win, dauer_sekunden, tempo="normal"):
    schritt_sekunden = TEMPO_SEKUNDEN.get(tempo, 1.5)
    wiederholungen = max(1, round(dauer_sekunden / schritt_sekunden))
    dauer_text = (f"{dauer_sekunden // 60} Min" if dauer_sekunden >= 60
                  else f"{dauer_sekunden} Sek") + f", Tempo {tempo.capitalize()}"

    clock = pygame.time.Clock()

    for c in range(4, 0, -1):
        win.fill(BLACK)
        text = "GO!" if c == 1 else str(c - 1)
        draw = COUNTDOWN_FONT.render(text, True, WHITE)
        win.blit(draw, (WIDTH / 2 - draw.get_width() / 2, HEIGHT / 2 - draw.get_height() / 2))
        pygame.display.flip()
        await asyncio.sleep(1.0)

    position = 1
    richtig = 0
    fehler = 0
    reaktionszeiten = []
    runde = 0
    abgebrochen = False

    while runde < wiederholungen:
        doppelsprung = random.randint(1, 100) < 20
        position += 2 if doppelsprung else 1
        if position > 32:
            position = ((position - 1) % 32) + 1

        reagiert = False
        reaktions_start = time.perf_counter() if doppelsprung else None
        schritt_ende = time.perf_counter() + schritt_sekunden

        while time.perf_counter() < schritt_ende:
            for event in pygame.event.get():
                if ist_abbruch_event(event):
                    abgebrochen = True
                    break
                if not reagiert and _ist_reaktion(event):
                    reagiert = True
                    if doppelsprung:
                        richtig += 1
                        if reaktions_start is not None:
                            reaktionszeiten.append((time.perf_counter() - reaktions_start) * 1000)
                    else:
                        fehler += 1
            if abgebrochen:
                break

            win.fill(BLACK)
            win.blit(PUNKT, _KREIS_POSITIONEN[position - 1])
            abbrechen_zeichnen(win)
            pygame.display.flip()
            clock.tick(FPS)
            await asyncio.sleep(0)

        if abgebrochen:
            break

        if not reagiert and doppelsprung:
            fehler += 1

        runde += 1

    durchschnitt = round(sum(reaktionszeiten) / len(reaktionszeiten)) if reaktionszeiten else 0
    ergebnisse.speichern("VIGIL", dauer_text, richtig, fehler, durchschnitt)
    await auswertung_anzeigen(win, richtig, fehler, durchschnitt)


async def auswertung_anzeigen(win, richtig, fehler, durchschnitt):
    lines = [
        f"Richtige Reaktionen: {richtig}",
        f"Falsche Reaktionen: {fehler}",
        f"Durchschnittliche Reaktionszeit: {durchschnitt} ms",
        "",
        "Tippe, um zum Hauptmenü zurückzukehren...",
    ]
    win.fill(WHITE)
    y = HEIGHT / 2 - len(lines) * 20
    for line in lines:
        draw = SCORE_FONT.render(line, True, BLACK)
        win.blit(draw, (WIDTH / 2 - draw.get_width() / 2, y))
        y += 40
    zurueck_zeichnen(win)
    pygame.display.flip()

    warten = True
    while warten:
        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                warten = False
        await asyncio.sleep(0)
