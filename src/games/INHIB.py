# =======================================
# INHIB – Web-Version (Stop-Signal-Paradigma, Touch-Bedienung, async)
# Zeitliche Parameter identisch zur PC-Version.
# =======================================
import array
import asyncio
import math
import random
import time

import pygame

from games import ergebnisse
from games.webstil import (WIDTH, HEIGHT, WHITE, BLACK, FONT_MARKANT,
                           abbrechen_zeichnen, ist_abbruch_event,
                           resource_path, zurueck_zeichnen)

SCORE_FONT = pygame.font.SysFont(FONT_MARKANT, 32)
COUNTDOWN_FONT = pygame.font.SysFont(FONT_MARKANT, 80)

# --- Zeitliche Parameter (Stop-Signal-Paradigma), identisch zur PC-Version ---
PFEIL_MAX_MS = 1000
PAUSE_MS = 1000
STOP_ANTEIL = 25
TON_FREQUENZ = 1000
TON_DAUER_MS = 100
SSD_START = 200
SSD_SCHRITT = 50
SSD_MIN = 50
SSD_MAX = 350

KREUZ = pygame.image.load(resource_path('Kreuz.PNG'))
PFEIL_LINKS = pygame.image.load(resource_path('Pfeil_Links.PNG'))
BUTTON_LINKS = pygame.transform.scale(PFEIL_LINKS, (120, 120))
BUTTON_RECHTS = pygame.transform.rotate(BUTTON_LINKS, 180)

LINKS_RECT = pygame.Rect(80, HEIGHT - 180, 120, 120)
RECHTS_RECT = pygame.Rect(WIDTH - 200, HEIGHT - 180, 120, 120)


def stopton_erzeugen():
    """Erzeugt den Stoppton (1000 Hz, 100 ms) synthetisch."""
    try:
        if pygame.mixer.get_init() is None:
            pygame.mixer.init()
        rate, format_bits, kanaele = pygame.mixer.get_init()
        anzahl = int(rate * TON_DAUER_MS / 1000)
        amplitude = int(32767 * 0.5)
        fade = max(1, int(rate * 0.005))
        samples = array.array('h')
        for i in range(anzahl):
            huellkurve = 1.0
            if i < fade:
                huellkurve = i / fade
            elif i > anzahl - fade:
                huellkurve = max(0.0, (anzahl - i) / fade)
            wert = math.sin(2 * math.pi * TON_FREQUENZ * i / rate)
            s = int(amplitude * wert * huellkurve)
            for _ in range(abs(kanaele)):
                samples.append(s)
        return pygame.mixer.Sound(buffer=samples.tobytes())
    except Exception as e:
        print("Stoppton konnte nicht erzeugt werden:", e)
        return None


def _pfeil_anzeigen(win, rotation):
    win.fill(WHITE)
    pfeil = pygame.transform.rotate(PFEIL_LINKS, rotation)
    win.blit(pfeil, (WIDTH // 2 - pfeil.get_width() // 2, HEIGHT // 2 - pfeil.get_height() // 2))
    win.blit(BUTTON_LINKS, LINKS_RECT.topleft)
    win.blit(BUTTON_RECHTS, RECHTS_RECT.topleft)
    abbrechen_zeichnen(win)


def _kreuz_anzeigen(win):
    win.fill(WHITE)
    win.blit(KREUZ, (WIDTH // 2 - KREUZ.get_width() // 2, HEIGHT // 2 - KREUZ.get_height() // 2))
    win.blit(BUTTON_LINKS, LINKS_RECT.topleft)
    win.blit(BUTTON_RECHTS, RECHTS_RECT.topleft)
    abbrechen_zeichnen(win)


async def _pfeilphase(win, rotation, ist_stop, ssd, ton):
    """Rückgabe: (abbruch, antwort, reaktionszeit_ms)."""
    _pfeil_anzeigen(win, rotation)
    pygame.display.flip()
    start = time.perf_counter()
    ton_gespielt = False

    while True:
        verstrichen_ms = (time.perf_counter() - start) * 1000

        if ist_stop and not ton_gespielt and verstrichen_ms >= ssd:
            if ton is not None:
                ton.play()
            ton_gespielt = True

        if verstrichen_ms >= PFEIL_MAX_MS:
            return False, None, None

        for event in pygame.event.get():
            if ist_abbruch_event(event):
                return True, None, None

            antwort = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    antwort = "links"
                elif event.key == pygame.K_RIGHT:
                    antwort = "rechts"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if LINKS_RECT.collidepoint(event.pos):
                    antwort = "links"
                elif RECHTS_RECT.collidepoint(event.pos):
                    antwort = "rechts"

            if antwort:
                return False, antwort, round((time.perf_counter() - start) * 1000)

        await asyncio.sleep(0)


async def _warte_ms(millisekunden):
    """Pause mit Event-Verarbeitung. False = Abbruch."""
    ende = time.perf_counter() + millisekunden / 1000
    while time.perf_counter() < ende:
        for event in pygame.event.get():
            if ist_abbruch_event(event):
                return False
        await asyncio.sleep(0)
    return True


async def run(win, dauer_sekunden, tempo=None):
    dauer_sekunden = max(10, int(dauer_sekunden))
    dauer_text = f"{dauer_sekunden // 60} Min" if dauer_sekunden >= 60 else f"{dauer_sekunden} Sek"

    richtige = fehler = auslassungen = 0
    stop_trials = stop_erfolge = ton_fehler = 0
    reaktionszeiten = []
    ssd_verlauf = []
    ssd = SSD_START
    ton = stopton_erzeugen()

    for i in range(3, 0, -1):
        win.fill(WHITE)
        text = COUNTDOWN_FONT.render(str(i), True, BLACK)
        win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        await asyncio.sleep(1.0)
    win.fill(WHITE)
    text = COUNTDOWN_FONT.render("GO!", True, BLACK)
    win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    await asyncio.sleep(1.0)

    test_start = time.perf_counter()
    while time.perf_counter() - test_start < dauer_sekunden:
        richtung = random.choice(["links", "rechts"])
        rotation = 0 if richtung == "links" else 180
        ist_stop = random.randint(1, 100) <= STOP_ANTEIL

        abbruch, antwort, reaktionszeit = await _pfeilphase(win, rotation, ist_stop, ssd, ton)
        _kreuz_anzeigen(win)
        pygame.display.flip()
        if abbruch:
            break

        if ist_stop:
            stop_trials += 1
            ssd_verlauf.append(ssd)
            if antwort is None:
                stop_erfolge += 1
                ssd = min(SSD_MAX, ssd + SSD_SCHRITT)
            else:
                ton_fehler += 1
                ssd = max(SSD_MIN, ssd - SSD_SCHRITT)
        else:
            if antwort is None:
                auslassungen += 1
            elif antwort == richtung:
                richtige += 1
                reaktionszeiten.append(reaktionszeit)
            else:
                fehler += 1

        if not await _warte_ms(PAUSE_MS):
            break

    rt_mittel = round(sum(reaktionszeiten) / len(reaktionszeiten)) if reaktionszeiten else 0
    ssd_mittel = round(sum(ssd_verlauf) / len(ssd_verlauf)) if ssd_verlauf else 0
    ssrt = rt_mittel - ssd_mittel if (reaktionszeiten and ssd_verlauf) else 0

    ergebnisse.speichern(
        "INHIB", dauer_text, richtige, fehler, rt_mittel,
        details=f"Stopp {stop_erfolge}/{stop_trials}, SSD {ssd_mittel} ms, SSRT {ssrt} ms")

    await auswertung_anzeigen(win, richtige, fehler, auslassungen, stop_erfolge, stop_trials,
                              ton_fehler, rt_mittel, ssd_mittel, ssrt)


async def auswertung_anzeigen(win, richtige, fehler, auslassungen, stop_erfolge, stop_trials,
                              ton_fehler, rt_mittel, ssd_mittel, ssrt):
    win.fill(WHITE)
    ergebnis_text = [
        f"Richtige Antworten: {richtige}",
        f"Falsche Antworten: {fehler}",
        f"Keine Reaktion: {auslassungen}",
        "",
        f"Erfolgreich gestoppt: {stop_erfolge} von {stop_trials}",
        f"Trotz Ton gedrückt: {ton_fehler}",
        "",
        f"Durchschnittliche Reaktionszeit: {rt_mittel} ms",
        f"Mittleres Stopp-Signal-Delay: {ssd_mittel} ms",
        f"Geschätzte Stopp-Reaktionszeit (SSRT): {ssrt} ms",
        "",
        "Tippe, um zum Hauptmenü zurückzukehren...",
    ]
    y_pos = HEIGHT // 2 - (len(ergebnis_text) * 50) // 2
    for line in ergebnis_text:
        if line:
            text = SCORE_FONT.render(line, True, BLACK)
            win.blit(text, (WIDTH // 2 - text.get_width() // 2, y_pos))
        y_pos += 50
    zurueck_zeichnen(win)
    pygame.display.flip()

    warten = True
    while warten:
        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                warten = False
        await asyncio.sleep(0)
