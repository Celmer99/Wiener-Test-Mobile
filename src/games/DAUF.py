# =======================================
# DAUF – Web-Version (Touch-Bedienung, async für den Browser)
# =======================================
import asyncio
import random
import time

import pygame

from games import ergebnisse
from games.webstil import (WIDTH, HEIGHT, FPS, WHITE, BLACK, FONT_MARKANT,
                           abbrechen_zeichnen, ist_abbruch_event,
                           resource_path, ABBRECHEN_RECT, zurueck_zeichnen)

SCORE_FONT = pygame.font.SysFont(FONT_MARKANT, 32)
COUNTDOWN_FONT = pygame.font.SysFont(FONT_MARKANT, 80)
TIMER_FONT = pygame.font.SysFont(FONT_MARKANT, 26)

Wahrscheinlichkeit = 40
BLENDE_DAUER = 0.5  # Sekunden

DREIECK = pygame.image.load(resource_path("Dreieck.PNG"))

TEMPO_SEKUNDEN = {"langsam": 2.0, "normal": 1.5, "schnell": 35 / 60}


async def run(win, dauer_sekunden, tempo="normal"):
    """Führt eine komplette DAUF-Übung aus. Kehrt danach zurück (kein sys.exit)."""
    muster_dauer = TEMPO_SEKUNDEN.get(tempo, 1.5)
    sek_pro_runde = muster_dauer + BLENDE_DAUER
    wiederholungen = max(1, round(dauer_sekunden / sek_pro_runde))
    dauer_text = (f"{dauer_sekunden // 60} Min" if dauer_sekunden >= 60
                  else f"{dauer_sekunden} Sek") + f", Tempo {tempo.capitalize()}"

    clock = pygame.time.Clock()

    # --- Countdown ---
    for c in range(3, -1, -1):
        win.fill(BLACK)
        text = "GO!" if c == 0 else str(c)
        draw = COUNTDOWN_FONT.render(text, True, WHITE)
        win.blit(draw, (WIDTH / 2 - draw.get_width() / 2, HEIGHT / 2 - draw.get_height() / 2))
        pygame.display.flip()
        await asyncio.sleep(1.0)

    start_time = time.time()
    richtig = 0
    fehler = 0
    reaktionszeiten = []

    def timer_zeichnen():
        vergangen = int(time.time() - start_time)
        text = TIMER_FONT.render(f"{vergangen // 60:02d}:{vergangen % 60:02d}", True, WHITE)
        win.blit(text, (30, HEIGHT - 70))

    def neues_muster():
        richtung = 0
        rotationen = []
        for _ in range(7):
            if random.randint(0, 100) < Wahrscheinlichkeit:
                rotationen.append(180)
                richtung += 1
            else:
                rotationen.append(0)
        position = random.choice([-340, 80, 500])
        return rotationen, richtung, position

    runde = 0
    abgebrochen = False

    while runde < wiederholungen:
        rotationen, richtung, position = neues_muster()
        muster_start = time.perf_counter()
        reagiert = False
        muster_ende = muster_start + muster_dauer

        while time.perf_counter() < muster_ende:
            for event in pygame.event.get():
                if ist_abbruch_event(event):
                    abgebrochen = True
                    break
                if not reagiert and (
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN)
                    or (event.type == pygame.MOUSEBUTTONDOWN
                        and not ABBRECHEN_RECT.collidepoint(event.pos))
                ):
                    reagiert = True
                    if richtung == 3:
                        richtig += 1
                        reaktionszeiten.append((time.perf_counter() - muster_start) * 1000)
                    else:
                        fehler += 1
            if abgebrochen:
                break

            win.fill(BLACK)
            x_start, abstand = 430, 150
            for i, r in enumerate(rotationen):
                win.blit(pygame.transform.rotate(DREIECK, r), (x_start + i * abstand, HEIGHT / 2 - position))
            timer_zeichnen()
            abbrechen_zeichnen(win)
            pygame.display.flip()
            clock.tick(FPS)
            await asyncio.sleep(0)

        if abgebrochen:
            break

        if not reagiert and richtung == 3:
            fehler += 1

        # Schwarzblende
        win.fill(BLACK)
        timer_zeichnen()
        pygame.display.flip()
        blende_ende = time.perf_counter() + BLENDE_DAUER
        while time.perf_counter() < blende_ende:
            for event in pygame.event.get():
                if ist_abbruch_event(event):
                    abgebrochen = True
            if abgebrochen:
                break
            await asyncio.sleep(0)

        if abgebrochen:
            break

        runde += 1

    durchschnitt = round(sum(reaktionszeiten) / len(reaktionszeiten)) if reaktionszeiten else 0
    ergebnisse.speichern("DAUF", dauer_text, richtig, fehler, durchschnitt)
    await auswertung_anzeigen(win, richtig, fehler, durchschnitt)


async def auswertung_anzeigen(win, richtig, fehler, durchschnitt):
    lines = [
        f"Richtige Anschläge: {richtig}",
        f"Falsche Anschläge: {fehler}",
        f"Durchschnittliche Reaktionszeit: {durchschnitt} ms",
        "",
        "Tippe, um zum Hauptmenü zurückzukehren...",
    ]
    win.fill(WHITE)
    for i, line in enumerate(lines):
        draw = SCORE_FONT.render(line, True, BLACK)
        win.blit(draw, (WIDTH / 2 - draw.get_width() / 2, HEIGHT / 2 - len(lines) * 30 + i * 50))
    zurueck_zeichnen(win)
    pygame.display.flip()

    warten = True
    while warten:
        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                warten = False
        await asyncio.sleep(0)
