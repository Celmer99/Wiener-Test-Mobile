# =======================================
# Gemeinsamer Stil für die Web-Version (Wiener Test SEK)
# Angelehnt an das Design der PC-Version (main.py), fürs Handy per
# Touch bedienbar.
# =======================================
import os
import pygame

WIDTH, HEIGHT = 1920, 1080
FPS = 60

WHITE = (235, 235, 230)
BLACK = (12, 12, 12)
STEEL = (150, 155, 150)
BTN_FILL = (30, 33, 30)
BTN_HOVER = (58, 68, 48)
RED_FILL = (85, 18, 18)
RED_HOVER = (130, 30, 30)
RED_BORDER = (170, 70, 70)
GREEN_FILL = (35, 70, 35)
GREEN_HOVER = (55, 105, 55)

FONT_MARKANT = 'impact,arialblack,arial'

_logo_cache = None


def resource_path(relative_path):
    return os.path.join('Assets', relative_path)


def logo_laden():
    """Lädt das Hintergrundbild einmalig; None, falls nicht vorhanden."""
    global _logo_cache
    if _logo_cache is not None:
        return _logo_cache
    pfad = resource_path('Logo.png')
    if not os.path.exists(pfad):
        _logo_cache = False
        return None
    try:
        logo = pygame.image.load(pfad).convert()
        weisser_fluegel_y = 534
        streifen_ratio = 0.4364
        hoehe = round(weisser_fluegel_y / streifen_ratio)
        breite = round(logo.get_width() * hoehe / logo.get_height())
        logo = pygame.transform.smoothscale(logo, (breite, hoehe))
        logo.set_alpha(110)
        pos = ((WIDTH - breite) // 2, 0)
        _logo_cache = (logo, pos)
        return _logo_cache
    except Exception as e:
        print("Logo konnte nicht geladen werden:", e)
        _logo_cache = False
        return None


def hintergrund_zeichnen(win):
    win.fill(BLACK)
    logo = logo_laden()
    if logo:
        bild, pos = logo
        win.blit(bild, pos)


def titel_zeichnen(win, titel):
    font = pygame.font.SysFont(FONT_MARKANT, 84)
    draw = font.render(titel.upper(), True, WHITE)
    win.blit(draw, (WIDTH // 2 - draw.get_width() // 2, 70))
    linie_y = 70 + draw.get_height() + 12
    halbbreite = max(draw.get_width() // 2 + 60, 420)
    pygame.draw.rect(win, STEEL, (WIDTH // 2 - halbbreite, linie_y, halbbreite * 2, 4))
    pygame.draw.rect(win, STEEL, (WIDTH // 2 - halbbreite + 40, linie_y + 10,
                                  (halbbreite - 40) * 2, 2))


def button_zeichnen(win, rect, label, font, hover, rot=False, gruen=False):
    if rot:
        fill = RED_HOVER if hover else RED_FILL
        border = RED_BORDER
    elif gruen:
        fill = GREEN_HOVER if hover else GREEN_FILL
        border = WHITE if hover else STEEL
    else:
        fill = BTN_HOVER if hover else BTN_FILL
        border = WHITE if hover else STEEL

    pygame.draw.rect(win, fill, rect)
    pygame.draw.rect(win, border, rect, 2)
    for cx, cy, dx, dy in ((rect.left, rect.top, 1, 1),
                           (rect.right - 1, rect.top, -1, 1),
                           (rect.left, rect.bottom - 1, 1, -1),
                           (rect.right - 1, rect.bottom - 1, -1, -1)):
        pygame.draw.line(win, border, (cx, cy), (cx + dx * 14, cy), 4)
        pygame.draw.line(win, border, (cx, cy), (cx, cy + dy * 14), 4)

    text = font.render(label.upper(), True, WHITE)
    win.blit(text, (rect.centerx - text.get_width() // 2,
                    rect.centery - text.get_height() // 2))


# --- Abbrechen-Button: fester Platz oben links, während einer Übung sichtbar.
# Touch-Geräte haben keine ESC-Taste, deshalb übernimmt dieser Button die
# Abbruch-Funktion (ESC funktioniert am PC-Browser zusätzlich weiterhin). ---
ABBRECHEN_RECT = pygame.Rect(30, 30, 220, 70)


def abbrechen_zeichnen(win, label="ABBRECHEN"):
    font = pygame.font.SysFont(FONT_MARKANT, 26)
    pygame.draw.rect(win, RED_FILL, ABBRECHEN_RECT)
    pygame.draw.rect(win, RED_BORDER, ABBRECHEN_RECT, 2)
    text = font.render(label, True, WHITE)
    win.blit(text, (ABBRECHEN_RECT.centerx - text.get_width() // 2,
                    ABBRECHEN_RECT.centery - text.get_height() // 2))


def zurueck_zeichnen(win):
    """Roter Zurück-Button, gleiche Position/Optik wie ABBRECHEN (Menüs statt Tests)."""
    abbrechen_zeichnen(win, label="ZURÜCK")


def ist_abbruch_event(event):
    """True, wenn das Event den Test abbrechen soll (Touch-Button, ESC-Taste)."""
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return True
    if event.type == pygame.MOUSEBUTTONDOWN and ABBRECHEN_RECT.collidepoint(event.pos):
        return True
    return False
