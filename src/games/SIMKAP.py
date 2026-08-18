import asyncio
import pygame
import os
import random

from games import ergebnisse
from games.webstil import (WIDTH, HEIGHT, abbrechen_zeichnen, ist_abbruch_event,
                           zurueck_zeichnen, resource_path as _webstil_resource_path)

pygame.mixer.init()

WIN = None  # wird beim Aufruf von run() auf das gemeinsame Fenster gesetzt


def resource_path(relative_path):
    return _webstil_resource_path(relative_path)


UHR_FONT = pygame.font.SysFont('Arial', 80)
BTN_FONT = pygame.font.SysFont('Arial', 30)
AUSWAHLFELD_FOND = pygame.font.SysFont('Arial', 30)
KALENDER_FOND = pygame.font.SysFont('Arial', 22)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (190,190,190)
BEIGE = (255,250,205)
GREEN = (0,100,0)
BLUE = (0,0,255)
FPS = 60
clock = pygame.time.Clock()
# Standarts

# Settings
# Settings

# Variabeln
Gameloop = 0
Delay = 10

DAUER_SEKUNDEN = 1800  # wird vom Hauptmenü gesetzt
DAUER_TEXT = ""


def set_dauer(sekunden):
    """Wird vom Hauptmenü aufgerufen: Übungsdauer in Sekunden."""
    global DAUER_SEKUNDEN, DAUER_TEXT
    DAUER_SEKUNDEN = max(30, int(sekunden))
    DAUER_TEXT = f"{sekunden // 60} Min" if sekunden >= 60 else f"{sekunden} Sek"


# --- Punktezähler für die Auswertung ---
SCORE_RICHTIG_GESTRICHEN = 0   # Treffer im Streichfeld korrekt markiert
SCORE_FALSCH_GESTRICHEN = 0    # Felder markiert, die keine Treffer waren
SCORE_VERPASST = 0             # Treffer, die nicht markiert wurden
BRETTER_GESPIELT = 0

SCORE_FRAGEN_GEFRAGT = 0       # vorgelesene Fragen
SCORE_FRAGEN_RICHTIG = 0       # richtig markierte Antworten
SCORE_FRAGEN_FALSCH = 0        # markierte Antworten zu nie gestellten Fragen


def STREICHFELD_AUSWERTEN():
    """Bewertet das aktuelle Streichfeld-Brett (vor Reset bzw. am Ende).

    Ein 'Treffer' ist ein Eintrag im Aktionsfeld, der auch in der
    zugehörigen Vergleichszeile vorkommt und deshalb gestrichen werden muss.
    """
    global SCORE_RICHTIG_GESTRICHEN, SCORE_FALSCH_GESTRICHEN, SCORE_VERPASST, BRETTER_GESPIELT
    buchstaben = "ABCDEFGHIJ"
    for i in range(1, 11):
        aktion = globals()[f"ZEILE_{i}_AKTION"]
        vergleich = globals()[f"ZEILE_{i}_VERGLEICH"]
        for j in range(5):
            gestrichen = globals()[f"AKT_{buchstaben[i - 1]}{j + 1}_STRICH"]
            ist_treffer = aktion[j] in vergleich
            if gestrichen and ist_treffer:
                SCORE_RICHTIG_GESTRICHEN += 1
            elif gestrichen and not ist_treffer:
                SCORE_FALSCH_GESTRICHEN += 1
            elif ist_treffer:
                SCORE_VERPASST += 1
    BRETTER_GESPIELT += 1


def VORLESEFRAGEN_AUSWERTEN():
    """Bewertet die aktuellen Vorlesefragen (vor Reset bzw. am Ende).

    Antwortfeld k gehört zur k-ten vorgelesenen Frage. Eine Frage gilt als
    gestellt, wenn ihr Zeitstempel erreicht wurde.
    """
    global SCORE_FRAGEN_GEFRAGT, SCORE_FRAGEN_RICHTIG, SCORE_FRAGEN_FALSCH
    reihen = "ABCD"
    for k in range(20):
        zeitstempel = globals()[f"TIMESTAMP_AUFGABE_{k + 1}"]
        markiert = globals()[f"VORLES_{reihen[k // 5]}{k % 5 + 1}_STRICH"]
        if zeitstempel <= GESAMTZEIT:
            SCORE_FRAGEN_GEFRAGT += 1
            if markiert:
                SCORE_FRAGEN_RICHTIG += 1
        elif markiert:
            SCORE_FRAGEN_FALSCH += 1

KALENDER = False
TELEFON_BUCH = False
NAECHSTES = False

SEKUNDE_1 = 0
SEKUNDE_10 = 0
MINUTE_1 = 0
MINUTE_10 = 0
GESAMTZEIT = 0

RANDOMISER_LISTE = []

AUSREDEN = True

KLICK = (0,0,0,0)

ZEILE_1_VERGLEICH = []
ZEILE_2_VERGLEICH = []
ZEILE_3_VERGLEICH = []
ZEILE_4_VERGLEICH = []
ZEILE_5_VERGLEICH = []
ZEILE_6_VERGLEICH = []
ZEILE_7_VERGLEICH = []
ZEILE_8_VERGLEICH = []
ZEILE_9_VERGLEICH = []
ZEILE_10_VERGLEICH = []

ZEILE_1_AKTION = []
ZEILE_2_AKTION = []
ZEILE_3_AKTION = []
ZEILE_4_AKTION = []
ZEILE_5_AKTION = []
ZEILE_6_AKTION = []
ZEILE_7_AKTION = []
ZEILE_8_AKTION = []
ZEILE_9_AKTION = []
ZEILE_10_AKTION = []


ZAHLEN = False
BILDER = False
BUCHSTABEN = True
DOPPELT = True

AKT_A1_STRICH = False
AKT_A2_STRICH = False
AKT_A3_STRICH = False
AKT_A4_STRICH = False
AKT_A5_STRICH = False

AKT_B1_STRICH = False
AKT_B2_STRICH = False
AKT_B3_STRICH = False
AKT_B4_STRICH = False
AKT_B5_STRICH = False

AKT_C1_STRICH = False
AKT_C2_STRICH = False
AKT_C3_STRICH = False
AKT_C4_STRICH = False
AKT_C5_STRICH = False

AKT_D1_STRICH = False
AKT_D2_STRICH = False
AKT_D3_STRICH = False
AKT_D4_STRICH = False
AKT_D5_STRICH = False

AKT_E1_STRICH = False
AKT_E2_STRICH = False
AKT_E3_STRICH = False
AKT_E4_STRICH = False
AKT_E5_STRICH = False

AKT_F1_STRICH = False
AKT_F2_STRICH = False
AKT_F3_STRICH = False
AKT_F4_STRICH = False
AKT_F5_STRICH = False

AKT_G1_STRICH = False
AKT_G2_STRICH = False
AKT_G3_STRICH = False
AKT_G4_STRICH = False
AKT_G5_STRICH = False

AKT_H1_STRICH = False
AKT_H2_STRICH = False
AKT_H3_STRICH = False
AKT_H4_STRICH = False
AKT_H5_STRICH = False

AKT_I1_STRICH = False
AKT_I2_STRICH = False
AKT_I3_STRICH = False
AKT_I4_STRICH = False
AKT_I5_STRICH = False

AKT_J1_STRICH = False
AKT_J2_STRICH = False
AKT_J3_STRICH = False
AKT_J4_STRICH = False
AKT_J5_STRICH = False

VORLES_A1_STRICH = False
VORLES_A2_STRICH = False
VORLES_A3_STRICH = False
VORLES_A4_STRICH = False
VORLES_A5_STRICH = False

VORLES_B1_STRICH = False
VORLES_B2_STRICH = False
VORLES_B3_STRICH = False
VORLES_B4_STRICH = False
VORLES_B5_STRICH = False

VORLES_C1_STRICH = False
VORLES_C2_STRICH = False
VORLES_C3_STRICH = False
VORLES_C4_STRICH = False
VORLES_C5_STRICH = False

VORLES_D1_STRICH = False
VORLES_D2_STRICH = False
VORLES_D3_STRICH = False
VORLES_D4_STRICH = False
VORLES_D5_STRICH = False

ERGEBNISSE = []

KAL_ZEILE_1 = ["Montag", "Morgen"]  # Tag, Tageszeit, Uhrzeit, Taetigkeit, Name
KAL_ZEILE_2 = ["Montag", "Mittag"]
KAL_ZEILE_3 = ["Montag", "Abend"]
KAL_ZEILE_4 = ["Dienstag", "Morgen"]
KAL_ZEILE_5 = ["Dienstag", "Mittag"]
KAL_ZEILE_6 = ["Dienstag", "Abend"]
KAL_ZEILE_7 = ["Mittwoch", "Morgen"]
KAL_ZEILE_8 = ["Mittwoch", "Mittag"]
KAL_ZEILE_9 = ["Mittwoch", "Abend"]
KAL_ZEILE_10 = ["Donnerstag", "Morgen"]
KAL_ZEILE_11 = ["Donnerstag", "Mittag"]
KAL_ZEILE_12 = ["Donnerstag", "Abend"]
KAL_ZEILE_13 = ["Freitag", "Morgen"]
KAL_ZEILE_14 = ["Freitag", "Mittag"]
KAL_ZEILE_15 = ["Freitag", "Abend"]
KAL_ZEILE_16 = ["Samstag", "Morgen"]
KAL_ZEILE_17 = ["Samstag", "Mittag"]
KAL_ZEILE_18 = ["Samstag", "Abend"]
KAL_ZEILE_19 = ["Sonntag", "Morgen"]
KAL_ZEILE_20 = ["Sonntag", "Mittag"]
KAL_ZEILE_21 = ["Sonntag", "Abend"]

KAL_FRAGE_1 = "A"
KAL_FRAGE_2 = "A"
KAL_FRAGE_3 = "A"
KAL_FRAGE_4 = "A"
KAL_FRAGE_5 = "A"
KAL_FRAGE_6 = "A"

KAL_ERGEBNIS_1 = "A"
KAL_ERGEBNIS_2 = "A"
KAL_ERGEBNIS_3 = "A"
KAL_ERGEBNIS_4 = "A"
KAL_ERGEBNIS_5 = "A"
KAL_ERGEBNIS_6 = "A"

TEL_ZEILE_1 = []  # Nachname0, Vorname1, Strasse2 , Hausnummer3, Stadt4, Telefonnummer5
TEL_ZEILE_2 = []
TEL_ZEILE_3 = []
TEL_ZEILE_4 = []
TEL_ZEILE_5 = []
TEL_ZEILE_6 = []
TEL_ZEILE_7 = []
TEL_ZEILE_8 = []
TEL_ZEILE_9 = []
TEL_ZEILE_10 = []
TEL_ZEILE_11 = []
TEL_ZEILE_12 = []
TEL_ZEILE_13 = []
TEL_ZEILE_14 = []
TEL_ZEILE_15 = []
TEL_ZEILE_16 = []

TEL_FRAGE_1 = "A"
TEL_FRAGE_2 = "A"
TEL_FRAGE_3 = "A"
TEL_FRAGE_4 = "A"
TEL_FRAGE_5 = "A"
TEL_FRAGE_6 = "A"
TEL_FRAGE_7 = "A"

TEL_ERGEBNIS_1 = "A"
TEL_ERGEBNIS_2 = "A"
TEL_ERGEBNIS_3 = "A"
TEL_ERGEBNIS_4 = "A"
TEL_ERGEBNIS_5 = "A"
TEL_ERGEBNIS_6 = "A"
TEL_ERGEBNIS_7 = "A"

RECHEN_FRAGE_1 = []  # Zahl1, Zeichen1, Zahl2, Zeichen2, Zahl3
RECHEN_FRAGE_2 = []
RECHEN_FRAGE_3 = []
RECHEN_FRAGE_4 = []
RECHEN_FRAGE_5 = []
RECHEN_FRAGE_6 = []
RECHEN_FRAGE_7 = []

RECHEN_ERGEBNIS_1 = -1
RECHEN_ERGEBNIS_2 = -1
RECHEN_ERGEBNIS_3 = -1
RECHEN_ERGEBNIS_4 = -1
RECHEN_ERGEBNIS_5 = -1
RECHEN_ERGEBNIS_6 = -1
RECHEN_ERGEBNIS_7 = -1

# Variabeln
#Assets
BILD_1 = pygame.transform.scale(pygame.image.load(resource_path('Kreis_Bild_1.PNG')), (50, 50))
BILD_2 = pygame.transform.scale(pygame.image.load(resource_path('Kreis_Bild_2.png')), (50, 50))
BILD_3 = pygame.transform.scale(pygame.image.load(resource_path('Kreis_Bild_3.png')), (50, 50))
BILD_4 = pygame.transform.scale(pygame.image.load(resource_path('Kreis_Bild_4.png')), (50, 50))
BILD_5 = pygame.transform.scale(pygame.image.load(resource_path('Kreis_Bild_5.png')), (50, 50))
BILD_6 = pygame.transform.scale(pygame.image.load(resource_path('Kreis_Bild_6.png')), (50, 50))
BILD_7 = pygame.transform.scale(pygame.image.load(resource_path('Kreis_Bild_7.png')), (50, 50))
BILD_8 = pygame.transform.scale(pygame.image.load(resource_path('Kreis_Bild_8.png')), (50, 50))
BILD_9 = pygame.transform.scale(pygame.image.load(resource_path('Kreis_Bild_9.png')), (50, 50))
BILD_10 = pygame.transform.scale(pygame.image.load(resource_path('Kreis_Bild_10.png')), (50, 50))
BILD_11 = pygame.transform.scale(pygame.image.load(resource_path('Kreis_Bild_11.png')), (50, 50))

STRICH = pygame.image.load(resource_path('STRICH.png'))
#Assets

def OVERLAY():
    pygame.draw.rect(WIN, GREY, pygame.Rect(300, 50, 1100, 750))
    pygame.draw.rect(WIN, WHITE, pygame.Rect(320, 70, 520, 710))
    pygame.draw.rect(WIN, WHITE, pygame.Rect(860, 70, 520, 710))
    pygame.draw.rect(WIN, BEIGE, pygame.Rect(300, 820, 1350, 180))
    pygame.draw.rect(WIN, BLACK, pygame.Rect(1420, 50, 230, 100))


def AUSWAHLFELD_ZAHLEN():
    global ZAHLEN,BILDER,BUCHSTABEN
    global ZEILE_1_VERGLEICH, ZEILE_2_VERGLEICH, ZEILE_3_VERGLEICH, ZEILE_4_VERGLEICH, ZEILE_5_VERGLEICH, ZEILE_6_VERGLEICH, ZEILE_7_VERGLEICH, ZEILE_8_VERGLEICH, ZEILE_9_VERGLEICH, ZEILE_10_VERGLEICH
    global ZEILE_1_AKTION, ZEILE_2_AKTION, ZEILE_3_AKTION, ZEILE_4_AKTION, ZEILE_5_AKTION, ZEILE_6_AKTION, ZEILE_7_AKTION, ZEILE_8_AKTION, ZEILE_9_AKTION, ZEILE_10_AKTION

    if random.randint(1,3) == 1:
        ZAHLEN = True
        BILDER = False
        BUCHSTABEN = False
    elif random.randint(2,3) == 2:
        ZAHLEN = False
        BILDER = True
        BUCHSTABEN = False
    else:
        ZAHLEN = False
        BILDER = False
        BUCHSTABEN = True

    VOR_BUCHSTABEN = ["Q", "W", "E", "R", "T", "Z", "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L",
                      "Y", "X", "C", "V", "B", "N", "M"]
    NACH_BUCHSTABEN = ["q", "w", "e", "r", "t", "z", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l",
                       "y", "x", "c", "v", "b", "n", "m"]


    if ZAHLEN == True:
        ZEILE_1_VORZAHL = random.randint(0,20)
    elif BUCHSTABEN == True:
        ZEILE_1_VORZAHL = random.choice(VOR_BUCHSTABEN)
    elif BILDER == True:
        ZEILE_1_VORZAHL = 0

    ZEILE_1_TARGETS = random.randint(1,3)


    if ZAHLEN == True:
        ZEILE_2_VORZAHL = random.randint(0, 20)
    elif BUCHSTABEN == True:
        ZEILE_2_VORZAHL = random.choice(VOR_BUCHSTABEN)
    elif BILDER == True:
        ZEILE_2_VORZAHL = 0
    ZEILE_2_TARGETS = random.randint(1,3)


    if ZAHLEN == True:
        ZEILE_3_VORZAHL = random.randint(0, 20)
    elif BUCHSTABEN == True:
        ZEILE_3_VORZAHL = random.choice(VOR_BUCHSTABEN)
    elif BILDER == True:
        ZEILE_3_VORZAHL = 0
    ZEILE_3_TARGETS = random.randint(1,3)


    if ZAHLEN == True:
        ZEILE_4_VORZAHL = random.randint(0, 20)
    elif BUCHSTABEN == True:
        ZEILE_4_VORZAHL = random.choice(VOR_BUCHSTABEN)
    elif BILDER == True:
        ZEILE_4_VORZAHL = 0
    ZEILE_4_TARGETS = random.randint(1,3)


    if ZAHLEN == True:
        ZEILE_5_VORZAHL = random.randint(0, 20)
    elif BUCHSTABEN == True:
        ZEILE_5_VORZAHL = random.choice(VOR_BUCHSTABEN)
    elif BILDER == True:
        ZEILE_5_VORZAHL = 0
    ZEILE_5_TARGETS = random.randint(1,3)


    if ZAHLEN == True:
        ZEILE_6_VORZAHL = random.randint(0, 20)
    elif BUCHSTABEN == True:
        ZEILE_6_VORZAHL = random.choice(VOR_BUCHSTABEN)
    elif BILDER == True:
        ZEILE_6_VORZAHL = 0
    ZEILE_6_TARGETS = random.randint(1,3)


    if ZAHLEN == True:
        ZEILE_7_VORZAHL = random.randint(0, 20)
    elif BUCHSTABEN == True:
        ZEILE_7_VORZAHL = random.choice(VOR_BUCHSTABEN)
    elif BILDER == True:
        ZEILE_7_VORZAHL = 0
    ZEILE_7_TARGETS = random.randint(1,3)


    if ZAHLEN == True:
        ZEILE_8_VORZAHL = random.randint(0, 20)
    elif BUCHSTABEN == True:
        ZEILE_8_VORZAHL = random.choice(VOR_BUCHSTABEN)
    elif BILDER == True:
        ZEILE_8_VORZAHL = 0
    ZEILE_8_TARGETS = random.randint(1,3)


    if ZAHLEN == True:
        ZEILE_9_VORZAHL = random.randint(0, 20)
    elif BUCHSTABEN == True:
        ZEILE_9_VORZAHL = random.choice(VOR_BUCHSTABEN)
    elif BILDER == True:
        ZEILE_9_VORZAHL = 0
    ZEILE_9_TARGETS = random.randint(1,3)


    if ZAHLEN == True:
        ZEILE_10_VORZAHL = random.randint(0, 20)
    elif BUCHSTABEN == True:
        ZEILE_10_VORZAHL = random.choice(VOR_BUCHSTABEN)
    elif BILDER == True:
        ZEILE_10_VORZAHL = 0
    ZEILE_10_TARGETS = random.randint(1,3)




    def VERGLEICHSZEILEN_RECHNER(A):
        VERGLEICHSZEILE = []
        while True:
            if len(VERGLEICHSZEILE) < 5:
                if ZAHLEN == True:
                    R = random.randint(1,99) + A * 100
                elif BUCHSTABEN == True:
                    R = (f"" + str(A) + str(random.choice(NACH_BUCHSTABEN)) + str(random.choice(NACH_BUCHSTABEN)))
                elif BILDER == True:
                    R = random.randint(1,11)

                if R in VERGLEICHSZEILE:
                    continue
                else:
                    VERGLEICHSZEILE.append(R)
            else:
                break

        SWITCH_1 = random.choice(VERGLEICHSZEILE)
        VERGLEICHSZEILE.remove(SWITCH_1)
        SWITCH_2 = random.choice(VERGLEICHSZEILE)
        VERGLEICHSZEILE.remove(SWITCH_2)
        SWITCH_3 = random.choice(VERGLEICHSZEILE)
        VERGLEICHSZEILE.remove(SWITCH_3)

        VERGLEICHSZEILE.append(SWITCH_2)
        VERGLEICHSZEILE.append(SWITCH_3)
        VERGLEICHSZEILE.append(SWITCH_1)

        return VERGLEICHSZEILE


    def AKTIONSZEILEN_RECHNER(A,B,C):
        global DOPPELT
        AKTIONSZEILE = []

        while True:
            if len(AKTIONSZEILE) < B:
                R_1 = random.choice(C)
                if R_1 in AKTIONSZEILE:
                    continue
                else:
                    AKTIONSZEILE.append(R_1)



            if len(AKTIONSZEILE) < 5:

                if random.randint(0, 100) < 20 and DOPPELT == True:
                    AKTIONSZEILE.append(random.choice(AKTIONSZEILE))
                    DOPPELT = False
                    continue

                elif ZAHLEN == True:
                    R_2 = random.randint(1, 99) + A * 100
                elif BUCHSTABEN == True:
                    R_2 = (f"" + str(A) + str(random.choice(NACH_BUCHSTABEN)) + str(random.choice(NACH_BUCHSTABEN)))
                elif BILDER == True:
                    R_2 = random.randint(1,11)


                if R_2 in AKTIONSZEILE or R_2 in C:
                    continue
                else:
                    AKTIONSZEILE.append(R_2)

            else:
                break
        DOPPELT = True


        SWITCH_1 = random.choice(AKTIONSZEILE)
        AKTIONSZEILE.remove(SWITCH_1)
        SWITCH_2 = random.choice(AKTIONSZEILE)
        AKTIONSZEILE.remove(SWITCH_2)
        SWITCH_3 = random.choice(AKTIONSZEILE)
        AKTIONSZEILE.remove(SWITCH_3)

        AKTIONSZEILE.append(SWITCH_2)
        AKTIONSZEILE.append(SWITCH_3)
        AKTIONSZEILE.append(SWITCH_1)


        return AKTIONSZEILE


    ZEILE_1_VERGLEICH = VERGLEICHSZEILEN_RECHNER(ZEILE_1_VORZAHL)
    ZEILE_1_AKTION = AKTIONSZEILEN_RECHNER(ZEILE_1_VORZAHL, ZEILE_1_TARGETS, ZEILE_1_VERGLEICH)


    ZEILE_2_VERGLEICH = VERGLEICHSZEILEN_RECHNER(ZEILE_2_VORZAHL)
    ZEILE_2_AKTION = AKTIONSZEILEN_RECHNER(ZEILE_2_VORZAHL, ZEILE_2_TARGETS, ZEILE_2_VERGLEICH)


    ZEILE_3_VERGLEICH = VERGLEICHSZEILEN_RECHNER(ZEILE_3_VORZAHL)
    ZEILE_3_AKTION = AKTIONSZEILEN_RECHNER(ZEILE_3_VORZAHL, ZEILE_3_TARGETS, ZEILE_3_VERGLEICH)


    ZEILE_4_VERGLEICH = VERGLEICHSZEILEN_RECHNER(ZEILE_4_VORZAHL)
    ZEILE_4_AKTION = AKTIONSZEILEN_RECHNER(ZEILE_4_VORZAHL, ZEILE_4_TARGETS, ZEILE_4_VERGLEICH)


    ZEILE_5_VERGLEICH = VERGLEICHSZEILEN_RECHNER(ZEILE_5_VORZAHL)
    ZEILE_5_AKTION = AKTIONSZEILEN_RECHNER(ZEILE_5_VORZAHL, ZEILE_5_TARGETS, ZEILE_5_VERGLEICH)


    ZEILE_6_VERGLEICH = VERGLEICHSZEILEN_RECHNER(ZEILE_6_VORZAHL)
    ZEILE_6_AKTION = AKTIONSZEILEN_RECHNER(ZEILE_6_VORZAHL, ZEILE_6_TARGETS, ZEILE_6_VERGLEICH)


    ZEILE_7_VERGLEICH = VERGLEICHSZEILEN_RECHNER(ZEILE_7_VORZAHL)
    ZEILE_7_AKTION = AKTIONSZEILEN_RECHNER(ZEILE_7_VORZAHL, ZEILE_7_TARGETS, ZEILE_7_VERGLEICH)


    ZEILE_8_VERGLEICH = VERGLEICHSZEILEN_RECHNER(ZEILE_8_VORZAHL)
    ZEILE_8_AKTION = AKTIONSZEILEN_RECHNER(ZEILE_8_VORZAHL, ZEILE_8_TARGETS, ZEILE_8_VERGLEICH)


    ZEILE_9_VERGLEICH = VERGLEICHSZEILEN_RECHNER(ZEILE_9_VORZAHL)
    ZEILE_9_AKTION = AKTIONSZEILEN_RECHNER(ZEILE_9_VORZAHL, ZEILE_9_TARGETS, ZEILE_9_VERGLEICH)


    ZEILE_10_VERGLEICH = VERGLEICHSZEILEN_RECHNER(ZEILE_10_VORZAHL)
    ZEILE_10_AKTION = AKTIONSZEILEN_RECHNER(ZEILE_10_VORZAHL, ZEILE_10_TARGETS, ZEILE_10_VERGLEICH)

AUSWAHLFELD_ZAHLEN()

def BUTTON(A,B,C,D):
    TARGET = pygame.Rect(A,B,C,D)
    ARROW = pygame.Rect(KLICK[0], KLICK[1],1,1)
    if ARROW.colliderect(TARGET):
        return(1)
    else:
        return(0)

def BUTTON_1(A,B):
    TARGET = pygame.Rect(A)
    ARROW = pygame.Rect(KLICK[0], KLICK[1],1,1)
    if ARROW.colliderect(TARGET) and TELEFON_BUCH == False and KALENDER == False:
        return(True)

    else:
        return(B)


def VERGLEICHSFELD():

    VGL_A1 = pygame.Rect(pygame.Rect(320, 70, 104, 71))
    VGL_A2 = pygame.Rect(pygame.Rect(424, 70, 104, 71))
    VGL_A3 = pygame.Rect(pygame.Rect(528, 70, 104, 71))
    VGL_A4 = pygame.Rect(pygame.Rect(632, 70, 104, 71))
    VGL_A5 = pygame.Rect(pygame.Rect(736, 70, 104, 71))

    VGL_B1 = pygame.Rect(pygame.Rect(320, 141, 104, 71))
    VGL_B2 = pygame.Rect(pygame.Rect(424, 141, 104, 71))
    VGL_B3 = pygame.Rect(pygame.Rect(528, 141, 104, 71))
    VGL_B4 = pygame.Rect(pygame.Rect(632, 141, 104, 71))
    VGL_B5 = pygame.Rect(pygame.Rect(736, 141, 104, 71))

    VGL_C1 = pygame.Rect(pygame.Rect(320, 212, 104, 71))
    VGL_C2 = pygame.Rect(pygame.Rect(424, 212, 104, 71))
    VGL_C3 = pygame.Rect(pygame.Rect(528, 212, 104, 71))
    VGL_C4 = pygame.Rect(pygame.Rect(632, 212, 104, 71))
    VGL_C5 = pygame.Rect(pygame.Rect(736, 212, 104, 71))

    VGL_D1 = pygame.Rect(pygame.Rect(320, 283, 104, 71))
    VGL_D2 = pygame.Rect(pygame.Rect(424, 283, 104, 71))
    VGL_D3 = pygame.Rect(pygame.Rect(528, 283, 104, 71))
    VGL_D4 = pygame.Rect(pygame.Rect(632, 283, 104, 71))
    VGL_D5 = pygame.Rect(pygame.Rect(736, 283, 104, 71))

    VGL_E1 = pygame.Rect(pygame.Rect(320, 354, 104, 71))
    VGL_E2 = pygame.Rect(pygame.Rect(424, 354, 104, 71))
    VGL_E3 = pygame.Rect(pygame.Rect(528, 354, 104, 71))
    VGL_E4 = pygame.Rect(pygame.Rect(632, 354, 104, 71))
    VGL_E5 = pygame.Rect(pygame.Rect(736, 354, 104, 71))

    VGL_F1 = pygame.Rect(pygame.Rect(320, 425, 104, 71))
    VGL_F2 = pygame.Rect(pygame.Rect(424, 425, 104, 71))
    VGL_F3 = pygame.Rect(pygame.Rect(528, 425, 104, 71))
    VGL_F4 = pygame.Rect(pygame.Rect(632, 425, 104, 71))
    VGL_F5 = pygame.Rect(pygame.Rect(736, 425, 104, 71))

    VGL_G1 = pygame.Rect(pygame.Rect(320, 496, 104, 71))
    VGL_G2 = pygame.Rect(pygame.Rect(424, 496, 104, 71))
    VGL_G3 = pygame.Rect(pygame.Rect(528, 496, 104, 71))
    VGL_G4 = pygame.Rect(pygame.Rect(632, 496, 104, 71))
    VGL_G5 = pygame.Rect(pygame.Rect(736, 496, 104, 71))

    VGL_H1 = pygame.Rect(pygame.Rect(320, 567, 104, 71))
    VGL_H2 = pygame.Rect(pygame.Rect(424, 567, 104, 71))
    VGL_H3 = pygame.Rect(pygame.Rect(528, 567, 104, 71))
    VGL_H4 = pygame.Rect(pygame.Rect(632, 567, 104, 71))
    VGL_H5 = pygame.Rect(pygame.Rect(736, 567, 104, 71))

    VGL_I1 = pygame.Rect(pygame.Rect(320, 638, 104, 71))
    VGL_I2 = pygame.Rect(pygame.Rect(424, 638, 104, 71))
    VGL_I3 = pygame.Rect(pygame.Rect(528, 638, 104, 71))
    VGL_I4 = pygame.Rect(pygame.Rect(632, 638, 104, 71))
    VGL_I5 = pygame.Rect(pygame.Rect(736, 638, 104, 71))

    VGL_J1 = pygame.Rect(pygame.Rect(320, 709, 104, 71))
    VGL_J2 = pygame.Rect(pygame.Rect(424, 709, 104, 71))
    VGL_J3 = pygame.Rect(pygame.Rect(528, 709, 104, 71))
    VGL_J4 = pygame.Rect(pygame.Rect(632, 709, 104, 71))
    VGL_J5 = pygame.Rect(pygame.Rect(736, 709, 104, 71))


    def VERGLEICHSFELD_DRAWER(A, B, C):

        if ZAHLEN == True:

            ZERO = False
            DOUBLE_ZERO = False

            if A[B] < 100:  # A = ZEILE_1_AKTION # B = 0
                DOUBLE_ZERO = True
            elif A[B] < 1000:
                ZERO = True
            else:
                ZERO = False
                DOUBLE_ZERO = False

            if ZERO == True:
                AKT_DRAW = AUSWAHLFELD_FOND.render(f"0" + str(A[B]), 1, BLUE)
                WIN.blit(AKT_DRAW, (C[0] + 15, C[1] + 15))  # C = VGL_A1
            elif DOUBLE_ZERO == True:
                AKT_DRAW = AUSWAHLFELD_FOND.render(f"00" + str(A[B]), 1, BLUE)
                WIN.blit(AKT_DRAW, (C[0] + 15, C[1] + 15))
            else:
                AKT_DRAW = AUSWAHLFELD_FOND.render(str(A[B]), 1, BLUE)
                WIN.blit(AKT_DRAW, (C[0] + 15, C[1] + 15))

        elif BUCHSTABEN == True:
            AKT_DRAW = AUSWAHLFELD_FOND.render(str(A[B]), 1, BLUE)
            WIN.blit(AKT_DRAW, (C[0] + 15, C[1] + 15))

        elif BILDER == True:
            if A[B] == 1:
                WIN.blit(BILD_1, (C[0] + 15, C[1] + 5))
            elif A[B] == 2:
                WIN.blit(BILD_2, (C[0] + 15, C[1] + 5))
            elif A[B] == 3:
                WIN.blit(BILD_3, (C[0] + 15, C[1] + 5))
            elif A[B] == 4:
                WIN.blit(BILD_4, (C[0] + 15, C[1] + 5))
            elif A[B] == 5:
                WIN.blit(BILD_5, (C[0] + 15, C[1] + 5))
            elif A[B] == 6:
                WIN.blit(BILD_6, (C[0] + 15, C[1] + 5))
            elif A[B] == 7:
                WIN.blit(BILD_7, (C[0] + 15, C[1] + 5))
            elif A[B] == 8:
                WIN.blit(BILD_8, (C[0] + 15, C[1] + 5))
            elif A[B] == 9:
                WIN.blit(BILD_9, (C[0] + 15, C[1] + 5))
            elif A[B] == 10:
                WIN.blit(BILD_10, (C[0] + 15, C[1] + 5))
            elif A[B] == 11:
                WIN.blit(BILD_11, (C[0] + 15, C[1] + 5))




    VERGLEICHSFELD_DRAWER(ZEILE_1_VERGLEICH, 0, VGL_A1)
    VERGLEICHSFELD_DRAWER(ZEILE_1_VERGLEICH, 1, VGL_A2)
    VERGLEICHSFELD_DRAWER(ZEILE_1_VERGLEICH, 2, VGL_A3)
    VERGLEICHSFELD_DRAWER(ZEILE_1_VERGLEICH, 3, VGL_A4)
    VERGLEICHSFELD_DRAWER(ZEILE_1_VERGLEICH, 4, VGL_A5)

    VERGLEICHSFELD_DRAWER(ZEILE_2_VERGLEICH, 0, VGL_B1)
    VERGLEICHSFELD_DRAWER(ZEILE_2_VERGLEICH, 1, VGL_B2)
    VERGLEICHSFELD_DRAWER(ZEILE_2_VERGLEICH, 2, VGL_B3)
    VERGLEICHSFELD_DRAWER(ZEILE_2_VERGLEICH, 3, VGL_B4)
    VERGLEICHSFELD_DRAWER(ZEILE_2_VERGLEICH, 4, VGL_B5)

    VERGLEICHSFELD_DRAWER(ZEILE_3_VERGLEICH, 0, VGL_C1)
    VERGLEICHSFELD_DRAWER(ZEILE_3_VERGLEICH, 1, VGL_C2)
    VERGLEICHSFELD_DRAWER(ZEILE_3_VERGLEICH, 2, VGL_C3)
    VERGLEICHSFELD_DRAWER(ZEILE_3_VERGLEICH, 3, VGL_C4)
    VERGLEICHSFELD_DRAWER(ZEILE_3_VERGLEICH, 4, VGL_C5)

    VERGLEICHSFELD_DRAWER(ZEILE_4_VERGLEICH, 0, VGL_D1)
    VERGLEICHSFELD_DRAWER(ZEILE_4_VERGLEICH, 1, VGL_D2)
    VERGLEICHSFELD_DRAWER(ZEILE_4_VERGLEICH, 2, VGL_D3)
    VERGLEICHSFELD_DRAWER(ZEILE_4_VERGLEICH, 3, VGL_D4)
    VERGLEICHSFELD_DRAWER(ZEILE_4_VERGLEICH, 4, VGL_D5)

    VERGLEICHSFELD_DRAWER(ZEILE_5_VERGLEICH, 0, VGL_E1)
    VERGLEICHSFELD_DRAWER(ZEILE_5_VERGLEICH, 1, VGL_E2)
    VERGLEICHSFELD_DRAWER(ZEILE_5_VERGLEICH, 2, VGL_E3)
    VERGLEICHSFELD_DRAWER(ZEILE_5_VERGLEICH, 3, VGL_E4)
    VERGLEICHSFELD_DRAWER(ZEILE_5_VERGLEICH, 4, VGL_E5)

    VERGLEICHSFELD_DRAWER(ZEILE_6_VERGLEICH, 0, VGL_F1)
    VERGLEICHSFELD_DRAWER(ZEILE_6_VERGLEICH, 1, VGL_F2)
    VERGLEICHSFELD_DRAWER(ZEILE_6_VERGLEICH, 2, VGL_F3)
    VERGLEICHSFELD_DRAWER(ZEILE_6_VERGLEICH, 3, VGL_F4)
    VERGLEICHSFELD_DRAWER(ZEILE_6_VERGLEICH, 4, VGL_F5)

    VERGLEICHSFELD_DRAWER(ZEILE_7_VERGLEICH, 0, VGL_G1)
    VERGLEICHSFELD_DRAWER(ZEILE_7_VERGLEICH, 1, VGL_G2)
    VERGLEICHSFELD_DRAWER(ZEILE_7_VERGLEICH, 2, VGL_G3)
    VERGLEICHSFELD_DRAWER(ZEILE_7_VERGLEICH, 3, VGL_G4)
    VERGLEICHSFELD_DRAWER(ZEILE_7_VERGLEICH, 4, VGL_G5)

    VERGLEICHSFELD_DRAWER(ZEILE_8_VERGLEICH, 0, VGL_H1)
    VERGLEICHSFELD_DRAWER(ZEILE_8_VERGLEICH, 1, VGL_H2)
    VERGLEICHSFELD_DRAWER(ZEILE_8_VERGLEICH, 2, VGL_H3)
    VERGLEICHSFELD_DRAWER(ZEILE_8_VERGLEICH, 3, VGL_H4)
    VERGLEICHSFELD_DRAWER(ZEILE_8_VERGLEICH, 4, VGL_H5)

    VERGLEICHSFELD_DRAWER(ZEILE_9_VERGLEICH, 0, VGL_I1)
    VERGLEICHSFELD_DRAWER(ZEILE_9_VERGLEICH, 1, VGL_I2)
    VERGLEICHSFELD_DRAWER(ZEILE_9_VERGLEICH, 2, VGL_I3)
    VERGLEICHSFELD_DRAWER(ZEILE_9_VERGLEICH, 3, VGL_I4)
    VERGLEICHSFELD_DRAWER(ZEILE_9_VERGLEICH, 4, VGL_I5)

    VERGLEICHSFELD_DRAWER(ZEILE_10_VERGLEICH, 0, VGL_J1)
    VERGLEICHSFELD_DRAWER(ZEILE_10_VERGLEICH, 1, VGL_J2)
    VERGLEICHSFELD_DRAWER(ZEILE_10_VERGLEICH, 2, VGL_J3)
    VERGLEICHSFELD_DRAWER(ZEILE_10_VERGLEICH, 3, VGL_J4)
    VERGLEICHSFELD_DRAWER(ZEILE_10_VERGLEICH, 4, VGL_J5)

    def STRICH_DRAWER_VGL(A,B,C,D):
        if B[C] in D:
            pygame.draw.line(WIN, BLACK, (A[0] + 30, A[1] + 60), (A[0] + 60, A[1] + 10), 4)

    STRICH_DRAWER_VGL(VGL_A1, ZEILE_1_VERGLEICH, 0, ZEILE_1_AKTION)
    STRICH_DRAWER_VGL(VGL_A2, ZEILE_1_VERGLEICH, 1, ZEILE_1_AKTION)
    STRICH_DRAWER_VGL(VGL_A3, ZEILE_1_VERGLEICH, 2, ZEILE_1_AKTION)
    STRICH_DRAWER_VGL(VGL_A4, ZEILE_1_VERGLEICH, 3, ZEILE_1_AKTION)
    STRICH_DRAWER_VGL(VGL_A5, ZEILE_1_VERGLEICH, 4, ZEILE_1_AKTION)

    STRICH_DRAWER_VGL(VGL_B1, ZEILE_2_VERGLEICH, 0, ZEILE_2_AKTION)
    STRICH_DRAWER_VGL(VGL_B2, ZEILE_2_VERGLEICH, 1, ZEILE_2_AKTION)
    STRICH_DRAWER_VGL(VGL_B3, ZEILE_2_VERGLEICH, 2, ZEILE_2_AKTION)
    STRICH_DRAWER_VGL(VGL_B4, ZEILE_2_VERGLEICH, 3, ZEILE_2_AKTION)
    STRICH_DRAWER_VGL(VGL_B5, ZEILE_2_VERGLEICH, 4, ZEILE_2_AKTION)

    STRICH_DRAWER_VGL(VGL_C1, ZEILE_3_VERGLEICH, 0, ZEILE_3_AKTION)
    STRICH_DRAWER_VGL(VGL_C2, ZEILE_3_VERGLEICH, 1, ZEILE_3_AKTION)
    STRICH_DRAWER_VGL(VGL_C3, ZEILE_3_VERGLEICH, 2, ZEILE_3_AKTION)
    STRICH_DRAWER_VGL(VGL_C4, ZEILE_3_VERGLEICH, 3, ZEILE_3_AKTION)
    STRICH_DRAWER_VGL(VGL_C5, ZEILE_3_VERGLEICH, 4, ZEILE_3_AKTION)

    STRICH_DRAWER_VGL(VGL_D1, ZEILE_4_VERGLEICH, 0, ZEILE_4_AKTION)
    STRICH_DRAWER_VGL(VGL_D2, ZEILE_4_VERGLEICH, 1, ZEILE_4_AKTION)
    STRICH_DRAWER_VGL(VGL_D3, ZEILE_4_VERGLEICH, 2, ZEILE_4_AKTION)
    STRICH_DRAWER_VGL(VGL_D4, ZEILE_4_VERGLEICH, 3, ZEILE_4_AKTION)
    STRICH_DRAWER_VGL(VGL_D5, ZEILE_4_VERGLEICH, 4, ZEILE_4_AKTION)

    STRICH_DRAWER_VGL(VGL_E1, ZEILE_5_VERGLEICH, 0, ZEILE_5_AKTION)
    STRICH_DRAWER_VGL(VGL_E2, ZEILE_5_VERGLEICH, 1, ZEILE_5_AKTION)
    STRICH_DRAWER_VGL(VGL_E3, ZEILE_5_VERGLEICH, 2, ZEILE_5_AKTION)
    STRICH_DRAWER_VGL(VGL_E4, ZEILE_5_VERGLEICH, 3, ZEILE_5_AKTION)
    STRICH_DRAWER_VGL(VGL_E5, ZEILE_5_VERGLEICH, 4, ZEILE_5_AKTION)

    STRICH_DRAWER_VGL(VGL_F1, ZEILE_6_VERGLEICH, 0, ZEILE_6_AKTION)
    STRICH_DRAWER_VGL(VGL_F2, ZEILE_6_VERGLEICH, 1, ZEILE_6_AKTION)
    STRICH_DRAWER_VGL(VGL_F3, ZEILE_6_VERGLEICH, 2, ZEILE_6_AKTION)
    STRICH_DRAWER_VGL(VGL_F4, ZEILE_6_VERGLEICH, 3, ZEILE_6_AKTION)
    STRICH_DRAWER_VGL(VGL_F5, ZEILE_6_VERGLEICH, 4, ZEILE_6_AKTION)

    STRICH_DRAWER_VGL(VGL_G1, ZEILE_7_VERGLEICH, 0, ZEILE_7_AKTION)
    STRICH_DRAWER_VGL(VGL_G2, ZEILE_7_VERGLEICH, 1, ZEILE_7_AKTION)
    STRICH_DRAWER_VGL(VGL_G3, ZEILE_7_VERGLEICH, 2, ZEILE_7_AKTION)
    STRICH_DRAWER_VGL(VGL_G4, ZEILE_7_VERGLEICH, 3, ZEILE_7_AKTION)
    STRICH_DRAWER_VGL(VGL_G5, ZEILE_7_VERGLEICH, 4, ZEILE_7_AKTION)

    STRICH_DRAWER_VGL(VGL_H1, ZEILE_8_VERGLEICH, 0, ZEILE_8_AKTION)
    STRICH_DRAWER_VGL(VGL_H2, ZEILE_8_VERGLEICH, 1, ZEILE_8_AKTION)
    STRICH_DRAWER_VGL(VGL_H3, ZEILE_8_VERGLEICH, 2, ZEILE_8_AKTION)
    STRICH_DRAWER_VGL(VGL_H4, ZEILE_8_VERGLEICH, 3, ZEILE_8_AKTION)
    STRICH_DRAWER_VGL(VGL_H5, ZEILE_8_VERGLEICH, 4, ZEILE_8_AKTION)

    STRICH_DRAWER_VGL(VGL_I1, ZEILE_9_VERGLEICH, 0, ZEILE_9_AKTION)
    STRICH_DRAWER_VGL(VGL_I2, ZEILE_9_VERGLEICH, 1, ZEILE_9_AKTION)
    STRICH_DRAWER_VGL(VGL_I3, ZEILE_9_VERGLEICH, 2, ZEILE_9_AKTION)
    STRICH_DRAWER_VGL(VGL_I4, ZEILE_9_VERGLEICH, 3, ZEILE_9_AKTION)
    STRICH_DRAWER_VGL(VGL_I5, ZEILE_9_VERGLEICH, 4, ZEILE_9_AKTION)

    STRICH_DRAWER_VGL(VGL_J1, ZEILE_10_VERGLEICH, 0, ZEILE_10_AKTION)
    STRICH_DRAWER_VGL(VGL_J2, ZEILE_10_VERGLEICH, 1, ZEILE_10_AKTION)
    STRICH_DRAWER_VGL(VGL_J3, ZEILE_10_VERGLEICH, 2, ZEILE_10_AKTION)
    STRICH_DRAWER_VGL(VGL_J4, ZEILE_10_VERGLEICH, 3, ZEILE_10_AKTION)
    STRICH_DRAWER_VGL(VGL_J5, ZEILE_10_VERGLEICH, 4, ZEILE_10_AKTION)
def AKTIONSFELD():
    global ZEILE_1_AKTION, ZEILE_2_AKTION, ZEILE_3_AKTION, ZEILE_4_AKTION, ZEILE_5_AKTION, ZEILE_6_AKTION, ZEILE_7_AKTION, ZEILE_8_AKTION, ZEILE_9_AKTION, ZEILE_10_AKTION
    global AKT_A1_STRICH, AKT_A2_STRICH, AKT_A3_STRICH, AKT_A4_STRICH, AKT_A5_STRICH, AKT_B1_STRICH, AKT_B2_STRICH, AKT_B3_STRICH, AKT_B4_STRICH, AKT_B5_STRICH, AKT_C1_STRICH, AKT_C2_STRICH, AKT_C3_STRICH, AKT_C4_STRICH, AKT_C5_STRICH, AKT_D1_STRICH, AKT_D2_STRICH, AKT_D3_STRICH, AKT_D4_STRICH, AKT_D5_STRICH, AKT_E1_STRICH, AKT_E2_STRICH, AKT_E3_STRICH, AKT_E4_STRICH, AKT_E5_STRICH, AKT_F1_STRICH, AKT_F2_STRICH, AKT_F3_STRICH, AKT_F4_STRICH, AKT_F5_STRICH, AKT_G1_STRICH, AKT_G2_STRICH, AKT_G3_STRICH, AKT_G4_STRICH, AKT_G5_STRICH, AKT_H1_STRICH, AKT_H2_STRICH, AKT_H3_STRICH, AKT_H4_STRICH, AKT_H5_STRICH, AKT_I1_STRICH, AKT_I2_STRICH, AKT_I3_STRICH, AKT_I4_STRICH, AKT_I5_STRICH, AKT_J1_STRICH, AKT_J2_STRICH, AKT_J3_STRICH, AKT_J4_STRICH, AKT_J5_STRICH

    AKT_A1 = pygame.Rect(pygame.Rect(860, 70, 104, 71))
    AKT_A2 = pygame.Rect(pygame.Rect(964, 70, 104, 71))
    AKT_A3 = pygame.Rect(pygame.Rect(1068, 70, 104, 71))
    AKT_A4 = pygame.Rect(pygame.Rect(1172, 70, 104, 71))
    AKT_A5 = pygame.Rect(pygame.Rect(1276, 70, 104, 71))

    AKT_B1 = pygame.Rect(pygame.Rect(860, 141, 104, 71))
    AKT_B2 = pygame.Rect(pygame.Rect(964, 141, 104, 71))
    AKT_B3 = pygame.Rect(pygame.Rect(1068, 141, 104, 71))
    AKT_B4 = pygame.Rect(pygame.Rect(1172, 141, 104, 71))
    AKT_B5 = pygame.Rect(pygame.Rect(1276, 141, 104, 71))

    AKT_C1 = pygame.Rect(pygame.Rect(860, 212, 104, 71))
    AKT_C2 = pygame.Rect(pygame.Rect(964, 212, 104, 71))
    AKT_C3 = pygame.Rect(pygame.Rect(1068, 212, 104, 71))
    AKT_C4 = pygame.Rect(pygame.Rect(1172, 212, 104, 71))
    AKT_C5 = pygame.Rect(pygame.Rect(1276, 212, 104, 71))

    AKT_D1 = pygame.Rect(pygame.Rect(860, 283, 104, 71))
    AKT_D2 = pygame.Rect(pygame.Rect(964, 283, 104, 71))
    AKT_D3 = pygame.Rect(pygame.Rect(1068, 283, 104, 71))
    AKT_D4 = pygame.Rect(pygame.Rect(1172, 283, 104, 71))
    AKT_D5 = pygame.Rect(pygame.Rect(1276, 283, 104, 71))

    AKT_E1 = pygame.Rect(pygame.Rect(860, 354, 104, 71))
    AKT_E2 = pygame.Rect(pygame.Rect(964, 354, 104, 71))
    AKT_E3 = pygame.Rect(pygame.Rect(1068, 354, 104, 71))
    AKT_E4 = pygame.Rect(pygame.Rect(1172, 354, 104, 71))
    AKT_E5 = pygame.Rect(pygame.Rect(1276, 354, 104, 71))

    AKT_F1 = pygame.Rect(pygame.Rect(860, 425, 104, 71))
    AKT_F2 = pygame.Rect(pygame.Rect(964, 425, 104, 71))
    AKT_F3 = pygame.Rect(pygame.Rect(1068, 425, 104, 71))
    AKT_F4 = pygame.Rect(pygame.Rect(1172, 425, 104, 71))
    AKT_F5 = pygame.Rect(pygame.Rect(1276, 425, 104, 71))

    AKT_G1 = pygame.Rect(pygame.Rect(860, 496, 104, 71))
    AKT_G2 = pygame.Rect(pygame.Rect(964, 496, 104, 71))
    AKT_G3 = pygame.Rect(pygame.Rect(1068, 496, 104, 71))
    AKT_G4 = pygame.Rect(pygame.Rect(1172, 496, 104, 71))
    AKT_G5 = pygame.Rect(pygame.Rect(1276, 496, 104, 71))

    AKT_H1 = pygame.Rect(pygame.Rect(860, 567, 104, 71))
    AKT_H2 = pygame.Rect(pygame.Rect(964, 567, 104, 71))
    AKT_H3 = pygame.Rect(pygame.Rect(1068, 567, 104, 71))
    AKT_H4 = pygame.Rect(pygame.Rect(1172, 567, 104, 71))
    AKT_H5 = pygame.Rect(pygame.Rect(1276, 567, 104, 71))

    AKT_I1 = pygame.Rect(pygame.Rect(860, 638, 104, 71))
    AKT_I2 = pygame.Rect(pygame.Rect(964, 638, 104, 71))
    AKT_I3 = pygame.Rect(pygame.Rect(1068, 638, 104, 71))
    AKT_I4 = pygame.Rect(pygame.Rect(1172, 638, 104, 71))
    AKT_I5 = pygame.Rect(pygame.Rect(1276, 638, 104, 71))

    AKT_J1 = pygame.Rect(pygame.Rect(860, 709, 104, 71))
    AKT_J2 = pygame.Rect(pygame.Rect(964, 709, 104, 71))
    AKT_J3 = pygame.Rect(pygame.Rect(1068, 709, 104, 71))
    AKT_J4 = pygame.Rect(pygame.Rect(1172, 709, 104, 71))
    AKT_J5 = pygame.Rect(pygame.Rect(1276, 709, 104, 71))


    def AKTIONSFELD_DRAWER(A,B,C):

        if ZAHLEN == True:

            ZERO = False
            DOUBLE_ZERO = False


            if A[B] < 100: # A = ZEILE_1_AKTION # B = 0
                DOUBLE_ZERO = True
            elif A[B] < 1000:
                ZERO = True
            else:
                ZERO = False
                DOUBLE_ZERO = False


            if ZERO == True:
                AKT_DRAW = AUSWAHLFELD_FOND.render(f"0" + str(A[B]), 1, BLUE)
                WIN.blit(AKT_DRAW, (C[0] + 15, C[1] + 15)) # C = AKT_A1
            elif DOUBLE_ZERO == True:
                AKT_DRAW = AUSWAHLFELD_FOND.render(f"00" + str(A[B]), 1, BLUE)
                WIN.blit(AKT_DRAW, (C[0] + 15, C[1] + 15))
            else:
                AKT_DRAW = AUSWAHLFELD_FOND.render(str(A[B]), 1, BLUE)
                WIN.blit(AKT_DRAW, (C[0] + 15, C[1] + 15))

        elif BUCHSTABEN == True:
            AKT_DRAW = AUSWAHLFELD_FOND.render(str(A[B]), 1, BLUE)
            WIN.blit(AKT_DRAW, (C[0] + 15, C[1] + 15))

        elif BILDER == True:
            if A[B] == 1:
                WIN.blit(BILD_1, (C[0] + 15, C[1] + 5))
            elif A[B] == 2:
                WIN.blit(BILD_2, (C[0] + 15, C[1] + 5))
            elif A[B] == 3:
                WIN.blit(BILD_3, (C[0] + 15, C[1] + 5))
            elif A[B] == 4:
                WIN.blit(BILD_4, (C[0] + 15, C[1] + 5))
            elif A[B] == 5:
                WIN.blit(BILD_5, (C[0] + 15, C[1] + 5))
            elif A[B] == 6:
                WIN.blit(BILD_6, (C[0] + 15, C[1] + 5))
            elif A[B] == 7:
                WIN.blit(BILD_7, (C[0] + 15, C[1] + 5))
            elif A[B] == 8:
                WIN.blit(BILD_8, (C[0] + 15, C[1] + 5))
            elif A[B] == 9:
                WIN.blit(BILD_9, (C[0] + 15, C[1] + 5))
            elif A[B] == 10:
                WIN.blit(BILD_10, (C[0] + 15, C[1] + 5))
            elif A[B] == 11:
                WIN.blit(BILD_11, (C[0] + 15, C[1] + 5))

    AKTIONSFELD_DRAWER(ZEILE_1_AKTION, 0, AKT_A1)
    AKTIONSFELD_DRAWER(ZEILE_1_AKTION, 1, AKT_A2)
    AKTIONSFELD_DRAWER(ZEILE_1_AKTION, 2, AKT_A3)
    AKTIONSFELD_DRAWER(ZEILE_1_AKTION, 3, AKT_A4)
    AKTIONSFELD_DRAWER(ZEILE_1_AKTION, 4, AKT_A5)

    AKTIONSFELD_DRAWER(ZEILE_2_AKTION, 0, AKT_B1)
    AKTIONSFELD_DRAWER(ZEILE_2_AKTION, 1, AKT_B2)
    AKTIONSFELD_DRAWER(ZEILE_2_AKTION, 2, AKT_B3)
    AKTIONSFELD_DRAWER(ZEILE_2_AKTION, 3, AKT_B4)
    AKTIONSFELD_DRAWER(ZEILE_2_AKTION, 4, AKT_B5)

    AKTIONSFELD_DRAWER(ZEILE_3_AKTION, 0, AKT_C1)
    AKTIONSFELD_DRAWER(ZEILE_3_AKTION, 1, AKT_C2)
    AKTIONSFELD_DRAWER(ZEILE_3_AKTION, 2, AKT_C3)
    AKTIONSFELD_DRAWER(ZEILE_3_AKTION, 3, AKT_C4)
    AKTIONSFELD_DRAWER(ZEILE_3_AKTION, 4, AKT_C5)

    AKTIONSFELD_DRAWER(ZEILE_4_AKTION, 0, AKT_D1)
    AKTIONSFELD_DRAWER(ZEILE_4_AKTION, 1, AKT_D2)
    AKTIONSFELD_DRAWER(ZEILE_4_AKTION, 2, AKT_D3)
    AKTIONSFELD_DRAWER(ZEILE_4_AKTION, 3, AKT_D4)
    AKTIONSFELD_DRAWER(ZEILE_4_AKTION, 4, AKT_D5)

    AKTIONSFELD_DRAWER(ZEILE_5_AKTION, 0, AKT_E1)
    AKTIONSFELD_DRAWER(ZEILE_5_AKTION, 1, AKT_E2)
    AKTIONSFELD_DRAWER(ZEILE_5_AKTION, 2, AKT_E3)
    AKTIONSFELD_DRAWER(ZEILE_5_AKTION, 3, AKT_E4)
    AKTIONSFELD_DRAWER(ZEILE_5_AKTION, 4, AKT_E5)

    AKTIONSFELD_DRAWER(ZEILE_6_AKTION, 0, AKT_F1)
    AKTIONSFELD_DRAWER(ZEILE_6_AKTION, 1, AKT_F2)
    AKTIONSFELD_DRAWER(ZEILE_6_AKTION, 2, AKT_F3)
    AKTIONSFELD_DRAWER(ZEILE_6_AKTION, 3, AKT_F4)
    AKTIONSFELD_DRAWER(ZEILE_6_AKTION, 4, AKT_F5)

    AKTIONSFELD_DRAWER(ZEILE_7_AKTION, 0, AKT_G1)
    AKTIONSFELD_DRAWER(ZEILE_7_AKTION, 1, AKT_G2)
    AKTIONSFELD_DRAWER(ZEILE_7_AKTION, 2, AKT_G3)
    AKTIONSFELD_DRAWER(ZEILE_7_AKTION, 3, AKT_G4)
    AKTIONSFELD_DRAWER(ZEILE_7_AKTION, 4, AKT_G5)

    AKTIONSFELD_DRAWER(ZEILE_8_AKTION, 0, AKT_H1)
    AKTIONSFELD_DRAWER(ZEILE_8_AKTION, 1, AKT_H2)
    AKTIONSFELD_DRAWER(ZEILE_8_AKTION, 2, AKT_H3)
    AKTIONSFELD_DRAWER(ZEILE_8_AKTION, 3, AKT_H4)
    AKTIONSFELD_DRAWER(ZEILE_8_AKTION, 4, AKT_H5)

    AKTIONSFELD_DRAWER(ZEILE_9_AKTION, 0, AKT_I1)
    AKTIONSFELD_DRAWER(ZEILE_9_AKTION, 1, AKT_I2)
    AKTIONSFELD_DRAWER(ZEILE_9_AKTION, 2, AKT_I3)
    AKTIONSFELD_DRAWER(ZEILE_9_AKTION, 3, AKT_I4)
    AKTIONSFELD_DRAWER(ZEILE_9_AKTION, 4, AKT_I5)

    AKTIONSFELD_DRAWER(ZEILE_10_AKTION, 0, AKT_J1)
    AKTIONSFELD_DRAWER(ZEILE_10_AKTION, 1, AKT_J2)
    AKTIONSFELD_DRAWER(ZEILE_10_AKTION, 2, AKT_J3)
    AKTIONSFELD_DRAWER(ZEILE_10_AKTION, 3, AKT_J4)
    AKTIONSFELD_DRAWER(ZEILE_10_AKTION, 4, AKT_J5)

    def STRICH_DRAWER(A,B):
        if B == True:
            pygame.draw.line(WIN, BLACK, (A[0] + 30, A[1] + 60), (A[0] + 60, A[1] + 10), 4)


    AKT_A1_STRICH = BUTTON_1(AKT_A1, AKT_A1_STRICH)
    AKT_A2_STRICH = BUTTON_1(AKT_A2, AKT_A2_STRICH)
    AKT_A3_STRICH = BUTTON_1(AKT_A3, AKT_A3_STRICH)
    AKT_A4_STRICH = BUTTON_1(AKT_A4, AKT_A4_STRICH)
    AKT_A5_STRICH = BUTTON_1(AKT_A5, AKT_A5_STRICH)

    STRICH_DRAWER(AKT_A1, AKT_A1_STRICH)
    STRICH_DRAWER(AKT_A2, AKT_A2_STRICH)
    STRICH_DRAWER(AKT_A3, AKT_A3_STRICH)
    STRICH_DRAWER(AKT_A4, AKT_A4_STRICH)
    STRICH_DRAWER(AKT_A5, AKT_A5_STRICH)

    AKT_B1_STRICH = BUTTON_1(AKT_B1, AKT_B1_STRICH)
    AKT_B2_STRICH = BUTTON_1(AKT_B2, AKT_B2_STRICH)
    AKT_B3_STRICH = BUTTON_1(AKT_B3, AKT_B3_STRICH)
    AKT_B4_STRICH = BUTTON_1(AKT_B4, AKT_B4_STRICH)
    AKT_B5_STRICH = BUTTON_1(AKT_B5, AKT_B5_STRICH)

    STRICH_DRAWER(AKT_B1, AKT_B1_STRICH)
    STRICH_DRAWER(AKT_B2, AKT_B2_STRICH)
    STRICH_DRAWER(AKT_B3, AKT_B3_STRICH)
    STRICH_DRAWER(AKT_B4, AKT_B4_STRICH)
    STRICH_DRAWER(AKT_B5, AKT_B5_STRICH)

    AKT_C1_STRICH = BUTTON_1(AKT_C1, AKT_C1_STRICH)
    AKT_C2_STRICH = BUTTON_1(AKT_C2, AKT_C2_STRICH)
    AKT_C3_STRICH = BUTTON_1(AKT_C3, AKT_C3_STRICH)
    AKT_C4_STRICH = BUTTON_1(AKT_C4, AKT_C4_STRICH)
    AKT_C5_STRICH = BUTTON_1(AKT_C5, AKT_C5_STRICH)

    STRICH_DRAWER(AKT_C1, AKT_C1_STRICH)
    STRICH_DRAWER(AKT_C2, AKT_C2_STRICH)
    STRICH_DRAWER(AKT_C3, AKT_C3_STRICH)
    STRICH_DRAWER(AKT_C4, AKT_C4_STRICH)
    STRICH_DRAWER(AKT_C5, AKT_C5_STRICH)

    AKT_D1_STRICH = BUTTON_1(AKT_D1, AKT_D1_STRICH)
    AKT_D2_STRICH = BUTTON_1(AKT_D2, AKT_D2_STRICH)
    AKT_D3_STRICH = BUTTON_1(AKT_D3, AKT_D3_STRICH)
    AKT_D4_STRICH = BUTTON_1(AKT_D4, AKT_D4_STRICH)
    AKT_D5_STRICH = BUTTON_1(AKT_D5, AKT_D5_STRICH)

    STRICH_DRAWER(AKT_D1, AKT_D1_STRICH)
    STRICH_DRAWER(AKT_D2, AKT_D2_STRICH)
    STRICH_DRAWER(AKT_D3, AKT_D3_STRICH)
    STRICH_DRAWER(AKT_D4, AKT_D4_STRICH)
    STRICH_DRAWER(AKT_D5, AKT_D5_STRICH)

    AKT_E1_STRICH = BUTTON_1(AKT_E1, AKT_E1_STRICH)
    AKT_E2_STRICH = BUTTON_1(AKT_E2, AKT_E2_STRICH)
    AKT_E3_STRICH = BUTTON_1(AKT_E3, AKT_E3_STRICH)
    AKT_E4_STRICH = BUTTON_1(AKT_E4, AKT_E4_STRICH)
    AKT_E5_STRICH = BUTTON_1(AKT_E5, AKT_E5_STRICH)

    STRICH_DRAWER(AKT_E1, AKT_E1_STRICH)
    STRICH_DRAWER(AKT_E2, AKT_E2_STRICH)
    STRICH_DRAWER(AKT_E3, AKT_E3_STRICH)
    STRICH_DRAWER(AKT_E4, AKT_E4_STRICH)
    STRICH_DRAWER(AKT_E5, AKT_E5_STRICH)

    AKT_F1_STRICH = BUTTON_1(AKT_F1, AKT_F1_STRICH)
    AKT_F2_STRICH = BUTTON_1(AKT_F2, AKT_F2_STRICH)
    AKT_F3_STRICH = BUTTON_1(AKT_F3, AKT_F3_STRICH)
    AKT_F4_STRICH = BUTTON_1(AKT_F4, AKT_F4_STRICH)
    AKT_F5_STRICH = BUTTON_1(AKT_F5, AKT_F5_STRICH)

    STRICH_DRAWER(AKT_F1, AKT_F1_STRICH)
    STRICH_DRAWER(AKT_F2, AKT_F2_STRICH)
    STRICH_DRAWER(AKT_F3, AKT_F3_STRICH)
    STRICH_DRAWER(AKT_F4, AKT_F4_STRICH)
    STRICH_DRAWER(AKT_F5, AKT_F5_STRICH)

    AKT_G1_STRICH = BUTTON_1(AKT_G1, AKT_G1_STRICH)
    AKT_G2_STRICH = BUTTON_1(AKT_G2, AKT_G2_STRICH)
    AKT_G3_STRICH = BUTTON_1(AKT_G3, AKT_G3_STRICH)
    AKT_G4_STRICH = BUTTON_1(AKT_G4, AKT_G4_STRICH)
    AKT_G5_STRICH = BUTTON_1(AKT_G5, AKT_G5_STRICH)

    STRICH_DRAWER(AKT_G1, AKT_G1_STRICH)
    STRICH_DRAWER(AKT_G2, AKT_G2_STRICH)
    STRICH_DRAWER(AKT_G3, AKT_G3_STRICH)
    STRICH_DRAWER(AKT_G4, AKT_G4_STRICH)
    STRICH_DRAWER(AKT_G5, AKT_G5_STRICH)

    AKT_H1_STRICH = BUTTON_1(AKT_H1, AKT_H1_STRICH)
    AKT_H2_STRICH = BUTTON_1(AKT_H2, AKT_H2_STRICH)
    AKT_H3_STRICH = BUTTON_1(AKT_H3, AKT_H3_STRICH)
    AKT_H4_STRICH = BUTTON_1(AKT_H4, AKT_H4_STRICH)
    AKT_H5_STRICH = BUTTON_1(AKT_H5, AKT_H5_STRICH)

    STRICH_DRAWER(AKT_H1, AKT_H1_STRICH)
    STRICH_DRAWER(AKT_H2, AKT_H2_STRICH)
    STRICH_DRAWER(AKT_H3, AKT_H3_STRICH)
    STRICH_DRAWER(AKT_H4, AKT_H4_STRICH)
    STRICH_DRAWER(AKT_H5, AKT_H5_STRICH)

    AKT_I1_STRICH = BUTTON_1(AKT_I1, AKT_I1_STRICH)
    AKT_I2_STRICH = BUTTON_1(AKT_I2, AKT_I2_STRICH)
    AKT_I3_STRICH = BUTTON_1(AKT_I3, AKT_I3_STRICH)
    AKT_I4_STRICH = BUTTON_1(AKT_I4, AKT_I4_STRICH)
    AKT_I5_STRICH = BUTTON_1(AKT_I5, AKT_I5_STRICH)

    STRICH_DRAWER(AKT_I1, AKT_I1_STRICH)
    STRICH_DRAWER(AKT_I2, AKT_I2_STRICH)
    STRICH_DRAWER(AKT_I3, AKT_I3_STRICH)
    STRICH_DRAWER(AKT_I4, AKT_I4_STRICH)
    STRICH_DRAWER(AKT_I5, AKT_I5_STRICH)

    AKT_J1_STRICH = BUTTON_1(AKT_J1, AKT_J1_STRICH)
    AKT_J2_STRICH = BUTTON_1(AKT_J2, AKT_J2_STRICH)
    AKT_J3_STRICH = BUTTON_1(AKT_J3, AKT_J3_STRICH)
    AKT_J4_STRICH = BUTTON_1(AKT_J4, AKT_J4_STRICH)
    AKT_J5_STRICH = BUTTON_1(AKT_J5, AKT_J5_STRICH)

    STRICH_DRAWER(AKT_J1, AKT_J1_STRICH)
    STRICH_DRAWER(AKT_J2, AKT_J2_STRICH)
    STRICH_DRAWER(AKT_J3, AKT_J3_STRICH)
    STRICH_DRAWER(AKT_J4, AKT_J4_STRICH)
    STRICH_DRAWER(AKT_J5, AKT_J5_STRICH)

def RECHENAUFGABEN():
    global RECHEN_FRAGE_1, RECHEN_FRAGE_2, RECHEN_FRAGE_3, RECHEN_FRAGE_4, RECHEN_FRAGE_5, RECHEN_FRAGE_6, RECHEN_FRAGE_7
    global RECHEN_ERGEBNIS_1, RECHEN_ERGEBNIS_2, RECHEN_ERGEBNIS_3, RECHEN_ERGEBNIS_4, RECHEN_ERGEBNIS_5, RECHEN_ERGEBNIS_6, RECHEN_ERGEBNIS_7
    global ERGEBNISSE

    RECHENZEICHEN = ["plus", "minus", "mal", "durch"]

    RECHEN_FRAGE_1 = []  # Zahl1, Zeichen1, Zahl2, Zeichen2, Zahl3
    RECHEN_FRAGE_2 = []
    RECHEN_FRAGE_3 = []
    RECHEN_FRAGE_4 = []
    RECHEN_FRAGE_5 = []
    RECHEN_FRAGE_6 = []
    RECHEN_FRAGE_7 = []

    RECHEN_ERGEBNIS_1 = -1
    RECHEN_ERGEBNIS_2 = -1
    RECHEN_ERGEBNIS_3 = -1
    RECHEN_ERGEBNIS_4 = -1
    RECHEN_ERGEBNIS_5 = -1
    RECHEN_ERGEBNIS_6 = -1
    RECHEN_ERGEBNIS_7 = -1

    def ZAHL_GENERATOR():
        ZAHL = random.randint(1, 10)
        return ZAHL
    def ZEICHEN_GENERATOR():
        ZEICHEN = random.choice(RECHENZEICHEN)
        return ZEICHEN
    def RECHENERGEBNIS_GENERATOR(A):
        if A[1] == "plus":
            if A[3] == "mal":
                ERGEBNIS = A[0] + A[2] * A[4]
            elif A[3] == "durch":
                ERGEBNIS = A[0] + A[2] / A[4]
            elif A[3] == "minus":
                ERGEBNIS = A[0] + A[2] - A[4]
            else:
                ERGEBNIS = A[0] + A[2] + A[4]

        elif A[1] == "minus":
            if A[3] == "mal":
                ERGEBNIS = A[0] - A[2] * A[4]
            elif A[3] == "durch":
                ERGEBNIS = A[0] - A[2] / A[4]
            elif A[3] == "minus":
                ERGEBNIS = A[0] - A[2] - A[4]
            else:
                ERGEBNIS = A[0] - A[2] + A[4]

        elif A[1] == "mal":
            if A[3] == "mal":
                ERGEBNIS = A[0] * A[2] * A[4]
            elif A[3] == "durch":
                ERGEBNIS = A[0] * A[2] / A[4]
            elif A[3] == "minus":
                ERGEBNIS = A[0] * A[2] - A[4]
            else:
                ERGEBNIS = A[0] * A[2] + A[4]

        elif A[1] == "durch":
            if A[3] == "mal":
                ERGEBNIS = A[0] / A[2] * A[4]
            elif A[3] == "durch":
                ERGEBNIS = A[0] / A[2] / A[4]
            elif A[3] == "minus":
                ERGEBNIS = A[0] / A[2] - A[4]
            else:
                ERGEBNIS = A[0] / A[2] + A[4]


        if ERGEBNIS > 1 and 2 > ERGEBNIS:
            ERGEBNIS = 0
        elif ERGEBNIS > 2 and 3 > ERGEBNIS:
            ERGEBNIS = 0
        elif ERGEBNIS > 3 and 4 > ERGEBNIS:
            ERGEBNIS = 0
        elif ERGEBNIS > 4 and 5 > ERGEBNIS:
            ERGEBNIS = 0
        elif ERGEBNIS > 5 and 6 > ERGEBNIS:
            ERGEBNIS = 0
        elif ERGEBNIS > 6 and 7 > ERGEBNIS:
            ERGEBNIS = 0
        elif ERGEBNIS > 7 and 8 > ERGEBNIS:
            ERGEBNIS = 0
        elif ERGEBNIS > 8 and 9 > ERGEBNIS:
            ERGEBNIS = 0
        elif ERGEBNIS > 9 and 10 > ERGEBNIS:
            ERGEBNIS = 0
        elif ERGEBNIS > 10 and 11 > ERGEBNIS:
            ERGEBNIS = 0
        elif ERGEBNIS > 11 and 12 > ERGEBNIS:
            ERGEBNIS = 0
        elif ERGEBNIS > 12 and 13 > ERGEBNIS:
            ERGEBNIS = 0
        elif ERGEBNIS > 13 and 14 > ERGEBNIS:
            ERGEBNIS = 0

        return int(ERGEBNIS)

    def RECHENAUFHABEN_GENERATOR_1():
        global RECHEN_FRAGE_1, RECHEN_ERGEBNIS_1, ERGEBNISSE
        while True:
            RECHEN_FRAGE_1.append(ZAHL_GENERATOR())
            RECHEN_FRAGE_1.append(ZEICHEN_GENERATOR())
            RECHEN_FRAGE_1.append(ZAHL_GENERATOR())
            RECHEN_FRAGE_1.append(ZEICHEN_GENERATOR())
            RECHEN_FRAGE_1.append(ZAHL_GENERATOR())
            RECHEN_ERGEBNIS_1 = RECHENERGEBNIS_GENERATOR(RECHEN_FRAGE_1)
            if RECHEN_ERGEBNIS_1 < 1 or RECHEN_ERGEBNIS_1 in ERGEBNISSE:
                RECHEN_FRAGE_1 = []
                RECHEN_ERGEBNIS_1 = []
                continue
            else:
                ERGEBNISSE.append(RECHEN_ERGEBNIS_1)
                break
    def RECHENAUFHABEN_GENERATOR_2():
        global RECHEN_FRAGE_2, RECHEN_ERGEBNIS_2, ERGEBNISSE
        while True:
            RECHEN_FRAGE_2.append(ZAHL_GENERATOR())
            RECHEN_FRAGE_2.append(ZEICHEN_GENERATOR())
            RECHEN_FRAGE_2.append(ZAHL_GENERATOR())
            RECHEN_FRAGE_2.append(ZEICHEN_GENERATOR())
            RECHEN_FRAGE_2.append(ZAHL_GENERATOR())
            RECHEN_ERGEBNIS_2 = RECHENERGEBNIS_GENERATOR(RECHEN_FRAGE_2)
            if RECHEN_ERGEBNIS_2 < 1 or RECHEN_ERGEBNIS_2 in ERGEBNISSE:
                RECHEN_FRAGE_2 = []
                RECHEN_ERGEBNIS_2 = []
                continue
            else:
                ERGEBNISSE.append(RECHEN_ERGEBNIS_2)
                break
    def RECHENAUFHABEN_GENERATOR_3():
        global RECHEN_FRAGE_3, RECHEN_ERGEBNIS_3, ERGEBNISSE
        while True:
            RECHEN_FRAGE_3.append(ZAHL_GENERATOR())
            RECHEN_FRAGE_3.append(ZEICHEN_GENERATOR())
            RECHEN_FRAGE_3.append(ZAHL_GENERATOR())
            RECHEN_FRAGE_3.append(ZEICHEN_GENERATOR())
            RECHEN_FRAGE_3.append(ZAHL_GENERATOR())
            RECHEN_ERGEBNIS_3 = RECHENERGEBNIS_GENERATOR(RECHEN_FRAGE_3)
            if RECHEN_ERGEBNIS_3 < 1 or RECHEN_ERGEBNIS_3 in ERGEBNISSE:
                RECHEN_FRAGE_3 = []
                RECHEN_ERGEBNIS_3 = []
                continue
            else:
                ERGEBNISSE.append(RECHEN_ERGEBNIS_3)
                break
    def RECHENAUFHABEN_GENERATOR_4():
        global RECHEN_FRAGE_4, RECHEN_ERGEBNIS_4, ERGEBNISSE
        while True:
            RECHEN_FRAGE_4.append(ZAHL_GENERATOR())
            RECHEN_FRAGE_4.append(ZEICHEN_GENERATOR())
            RECHEN_FRAGE_4.append(ZAHL_GENERATOR())
            RECHEN_FRAGE_4.append(ZEICHEN_GENERATOR())
            RECHEN_FRAGE_4.append(ZAHL_GENERATOR())
            RECHEN_ERGEBNIS_4 = RECHENERGEBNIS_GENERATOR(RECHEN_FRAGE_4)
            if RECHEN_ERGEBNIS_4 < 1 or RECHEN_ERGEBNIS_4 in ERGEBNISSE:
                RECHEN_FRAGE_4 = []
                RECHEN_ERGEBNIS_4 = []
                continue
            else:
                ERGEBNISSE.append(RECHEN_ERGEBNIS_4)
                break
    def RECHENAUFHABEN_GENERATOR_5():
        global RECHEN_FRAGE_5, RECHEN_ERGEBNIS_5, ERGEBNISSE
        while True:
            RECHEN_FRAGE_5.append(ZAHL_GENERATOR())
            RECHEN_FRAGE_5.append(ZEICHEN_GENERATOR())
            RECHEN_FRAGE_5.append(ZAHL_GENERATOR())
            RECHEN_FRAGE_5.append(ZEICHEN_GENERATOR())
            RECHEN_FRAGE_5.append(ZAHL_GENERATOR())
            RECHEN_ERGEBNIS_5 = RECHENERGEBNIS_GENERATOR(RECHEN_FRAGE_5)
            if RECHEN_ERGEBNIS_5 < 1 or RECHEN_ERGEBNIS_5 in ERGEBNISSE:
                RECHEN_FRAGE_5 = []
                RECHEN_ERGEBNIS_5 = []
                continue
            else:
                ERGEBNISSE.append(RECHEN_ERGEBNIS_5)
                break
    def RECHENAUFHABEN_GENERATOR_6():
        global RECHEN_FRAGE_6, RECHEN_ERGEBNIS_6, ERGEBNISSE
        while True:
            RECHEN_FRAGE_6.append(ZAHL_GENERATOR())
            RECHEN_FRAGE_6.append(ZEICHEN_GENERATOR())
            RECHEN_FRAGE_6.append(ZAHL_GENERATOR())
            RECHEN_FRAGE_6.append(ZEICHEN_GENERATOR())
            RECHEN_FRAGE_6.append(ZAHL_GENERATOR())
            RECHEN_ERGEBNIS_6 = RECHENERGEBNIS_GENERATOR(RECHEN_FRAGE_6)
            if RECHEN_ERGEBNIS_6 < 1 or RECHEN_ERGEBNIS_6 in ERGEBNISSE:
                RECHEN_FRAGE_6 = []
                RECHEN_ERGEBNIS_6 = []
                continue
            else:
                ERGEBNISSE.append(RECHEN_ERGEBNIS_6)
                break
    def RECHENAUFHABEN_GENERATOR_7():
        global RECHEN_FRAGE_7, RECHEN_ERGEBNIS_7, ERGEBNISSE
        while True:
            RECHEN_FRAGE_7.append(ZAHL_GENERATOR())
            RECHEN_FRAGE_7.append(ZEICHEN_GENERATOR())
            RECHEN_FRAGE_7.append(ZAHL_GENERATOR())
            RECHEN_FRAGE_7.append(ZEICHEN_GENERATOR())
            RECHEN_FRAGE_7.append(ZAHL_GENERATOR())
            RECHEN_ERGEBNIS_7 = RECHENERGEBNIS_GENERATOR(RECHEN_FRAGE_7)
            if RECHEN_ERGEBNIS_7 < 1 or RECHEN_ERGEBNIS_7 in ERGEBNISSE:
                RECHEN_FRAGE_7 = []
                RECHEN_ERGEBNIS_7 = []
                continue
            else:
                ERGEBNISSE.append(RECHEN_ERGEBNIS_7)
                break

    RECHENAUFHABEN_GENERATOR_1()
    RECHENAUFHABEN_GENERATOR_2()
    RECHENAUFHABEN_GENERATOR_3()
    RECHENAUFHABEN_GENERATOR_4()
    RECHENAUFHABEN_GENERATOR_5()
    RECHENAUFHABEN_GENERATOR_6()
    RECHENAUFHABEN_GENERATOR_7()
def TEL_AUFGABEN():
    global TEL_ZEILE_1, TEL_ZEILE_2, TEL_ZEILE_3, TEL_ZEILE_4, TEL_ZEILE_5, TEL_ZEILE_6, TEL_ZEILE_7, TEL_ZEILE_8, TEL_ZEILE_9, TEL_ZEILE_10, TEL_ZEILE_11, TEL_ZEILE_12, TEL_ZEILE_13, TEL_ZEILE_14, TEL_ZEILE_15, TEL_ZEILE_16
    global TEL_ERGEBNIS_1, TEL_ERGEBNIS_2, TEL_ERGEBNIS_3, TEL_ERGEBNIS_4, TEL_ERGEBNIS_5, TEL_ERGEBNIS_6, TEL_ERGEBNIS_7
    global TEL_FRAGE_1, TEL_FRAGE_2, TEL_FRAGE_3, TEL_FRAGE_4, TEL_FRAGE_5, TEL_FRAGE_6, TEL_FRAGE_7
    global ERGEBNISSE

    VORNAMEN = ["Anna", "Marie", "Jessica", "Kerstin", "Mia", "Emma", "Mila", "Emilia", "Lina", "Ella", "Sophie",
                "Amelie", "Lara", "Lena", "Sophia", "Leni", "Leonie", "Nora", "Hannah", "Luisa", "Johannis", "Mike",
                "Maximilian", "Kyle", "Noah", "Lukas", "Felix", "Leon", "Luca", "Leo", "Milan", "Matteo", "Theo",
                "Moritz", "Emil", "Oskar", "Julian", "Anton", "Paul", "Liam"]

    NACHNAMEN = ["Schmidt", "Müller", "Mayer", "Meier", "Kus", "Obama", "Trump", "Brecht", "Schneider", "Fischer",
                 "Weber", "Wagner", "Becker", "Schulz", "Hoffmann", "Schaefer", "Bauer", "Koch", "Richter", "Klein",
                 "Wolf", "Schroeder", "Neumann", "Schwarz", "Braun", "Zimmermann", "Hartmann", "Krueger", "Werner",
                 "Lange", "Schmitz", "Krause", "Lehmann", "Huber", "Herrmann", "Koehler", "Walter", "Koenig",
                 "Schulze",
                 "Fuchs"]

    STRASSEN = ["Erlenweg", "Herner Str.", "Stadtring", "Suedring", "Schulstr.", "Gartenstr.", "Bahnhofstr.",
                "Goethestr.", "Schillerstr.", "Bergstr.", "Jahnstr.", "Mozartstr.", "Oberende", "Unterende",
                "Lindenstr.", "Beethovenstr.", "Lessingstr.", "Hauptstr.", "Feldstr.", "Uhlandstr", "Waldstr.",
                "Kirchenstr.", "Breslauer Str.", "Koenigsberger Str.", "Wiesenstr.", "Friedrichstr.", "Bachstr.",
                "Amselweg", "Postheide", "Haller Weg", "Birkenstr.", "Elbeallee", "Am Stadtholz", "Virchowstr.",
                "Hohe Luft", "In der Wisch", "Hemelinger Str.", "Henriettenstr.", "Rennstieg", "Am Hulsberg",
                "Verdunstr.", "Ruhrstr."]

    STAEDTE = ["Bielefeld", "Hannover", "Bonn", "Köln", "Bremen", "Berlin", "Moskau", "London", "New York",
               "München",
               "Riga", "Oslo", "Paris", "Dortmund", "Tokio", "Buffalo", "Münster", "Aachen", "Dresden", "Madrid",
               "Adyan", "Arizona", "Atlanta", "Lyon", "Mainz", "Neukirchen", "Ottawa", "Rom", "Rotterdam", "Ulm",
               "Wien", "Xanten", "Yokohama", "Zwickau", "Jena", "Leipzig", "Amsterdam", "Bristol", "Augsburg",
               "Eisenstadt"]

    HAUSNUMMERN = []
    TELEFONNUMMERN = []

    TEL_ZEILE_1 = []  # Nachname0, Vorname1, Strasse2 , Hausnummer3, Stadt4, Telefonnummer5
    TEL_ZEILE_2 = []
    TEL_ZEILE_3 = []
    TEL_ZEILE_4 = []
    TEL_ZEILE_5 = []
    TEL_ZEILE_6 = []
    TEL_ZEILE_7 = []
    TEL_ZEILE_8 = []
    TEL_ZEILE_9 = []
    TEL_ZEILE_10 = []
    TEL_ZEILE_11 = []
    TEL_ZEILE_12 = []
    TEL_ZEILE_13 = []
    TEL_ZEILE_14 = []
    TEL_ZEILE_15 = []
    TEL_ZEILE_16 = []

    TEL_ZEILEN_AUSWAHL = [TEL_ZEILE_1, TEL_ZEILE_2, TEL_ZEILE_3, TEL_ZEILE_4, TEL_ZEILE_5, TEL_ZEILE_6, TEL_ZEILE_7, TEL_ZEILE_8, TEL_ZEILE_9, TEL_ZEILE_10, TEL_ZEILE_11, TEL_ZEILE_12, TEL_ZEILE_13, TEL_ZEILE_14, TEL_ZEILE_15, TEL_ZEILE_16]

    TEL_FRAGE_1 = "A"
    TEL_FRAGE_2 = "A"
    TEL_FRAGE_3 = "A"
    TEL_FRAGE_4 = "A"
    TEL_FRAGE_5 = "A"
    TEL_FRAGE_6 = "A"
    TEL_FRAGE_7 = "A"

    TEL_ERGEBNIS_1 = "A"
    TEL_ERGEBNIS_2 = "A"
    TEL_ERGEBNIS_3 = "A"
    TEL_ERGEBNIS_4 = "A"
    TEL_ERGEBNIS_5 = "A"
    TEL_ERGEBNIS_6 = "A"
    TEL_ERGEBNIS_7 = "A"

    def TEL_GENERATOR():



        def NACHNAMEN_AUSWAHL():
            R = random.choice(NACHNAMEN)
            NACHNAMEN.remove(R)
            return R
        def VORNAMEN_AUSWAHL():
            R = random.choice(VORNAMEN)
            VORNAMEN.remove(R)
            return R
        def STRASSEN_AUSWAHL():
            R = random.choice(STRASSEN)
            STRASSEN.remove(R)
            return R
        def HAUSNUMMER_AUSWAHL():
            while True:
                R = random.randint(1, 500)
                if R in HAUSNUMMERN:
                    continue
                else:
                    HAUSNUMMERN.append(R)
                    break
            return R
        def STADT_AUSWAHL():
            R = random.choice(STAEDTE)
            STAEDTE.remove(R)
            return R
        def TELEFONNUMER_AUSWAHL():
            while True:
                R_1 = random.randint(100, 999)
                if R_1 in TELEFONNUMMERN:
                    continue

                else:
                    TELEFONNUMMERN.append(R_1)

                    while True:
                        R_2 = random.randint(1000, 9999)
                        if R_2 in TELEFONNUMMERN:
                            continue

                        else:
                            TELEFONNUMMERN.append(R_2)
                            break

                    break
            return str(R_1) + "-" + str(R_2)

        TEL_ZEILE_1.append(NACHNAMEN_AUSWAHL())
        TEL_ZEILE_1.append(VORNAMEN_AUSWAHL())
        TEL_ZEILE_1.append(STRASSEN_AUSWAHL())
        TEL_ZEILE_1.append(HAUSNUMMER_AUSWAHL())
        TEL_ZEILE_1.append(STADT_AUSWAHL())
        TEL_ZEILE_1.append(TELEFONNUMER_AUSWAHL())

        TEL_ZEILE_2.append(NACHNAMEN_AUSWAHL())
        TEL_ZEILE_2.append(VORNAMEN_AUSWAHL())
        TEL_ZEILE_2.append(STRASSEN_AUSWAHL())
        TEL_ZEILE_2.append(HAUSNUMMER_AUSWAHL())
        TEL_ZEILE_2.append(STADT_AUSWAHL())
        TEL_ZEILE_2.append(TELEFONNUMER_AUSWAHL())

        TEL_ZEILE_3.append(NACHNAMEN_AUSWAHL())
        TEL_ZEILE_3.append(VORNAMEN_AUSWAHL())
        TEL_ZEILE_3.append(STRASSEN_AUSWAHL())
        TEL_ZEILE_3.append(HAUSNUMMER_AUSWAHL())
        TEL_ZEILE_3.append(STADT_AUSWAHL())
        TEL_ZEILE_3.append(TELEFONNUMER_AUSWAHL())

        TEL_ZEILE_4.append(NACHNAMEN_AUSWAHL())
        TEL_ZEILE_4.append(VORNAMEN_AUSWAHL())
        TEL_ZEILE_4.append(STRASSEN_AUSWAHL())
        TEL_ZEILE_4.append(HAUSNUMMER_AUSWAHL())
        TEL_ZEILE_4.append(STADT_AUSWAHL())
        TEL_ZEILE_4.append(TELEFONNUMER_AUSWAHL())

        TEL_ZEILE_5.append(NACHNAMEN_AUSWAHL())
        TEL_ZEILE_5.append(VORNAMEN_AUSWAHL())
        TEL_ZEILE_5.append(STRASSEN_AUSWAHL())
        TEL_ZEILE_5.append(HAUSNUMMER_AUSWAHL())
        TEL_ZEILE_5.append(STADT_AUSWAHL())
        TEL_ZEILE_5.append(TELEFONNUMER_AUSWAHL())

        TEL_ZEILE_6.append(NACHNAMEN_AUSWAHL())
        TEL_ZEILE_6.append(VORNAMEN_AUSWAHL())
        TEL_ZEILE_6.append(STRASSEN_AUSWAHL())
        TEL_ZEILE_6.append(HAUSNUMMER_AUSWAHL())
        TEL_ZEILE_6.append(STADT_AUSWAHL())
        TEL_ZEILE_6.append(TELEFONNUMER_AUSWAHL())

        TEL_ZEILE_7.append(NACHNAMEN_AUSWAHL())
        TEL_ZEILE_7.append(VORNAMEN_AUSWAHL())
        TEL_ZEILE_7.append(STRASSEN_AUSWAHL())
        TEL_ZEILE_7.append(HAUSNUMMER_AUSWAHL())
        TEL_ZEILE_7.append(STADT_AUSWAHL())
        TEL_ZEILE_7.append(TELEFONNUMER_AUSWAHL())

        TEL_ZEILE_8.append(NACHNAMEN_AUSWAHL())
        TEL_ZEILE_8.append(VORNAMEN_AUSWAHL())
        TEL_ZEILE_8.append(STRASSEN_AUSWAHL())
        TEL_ZEILE_8.append(HAUSNUMMER_AUSWAHL())
        TEL_ZEILE_8.append(STADT_AUSWAHL())
        TEL_ZEILE_8.append(TELEFONNUMER_AUSWAHL())

        TEL_ZEILE_9.append(NACHNAMEN_AUSWAHL())
        TEL_ZEILE_9.append(VORNAMEN_AUSWAHL())
        TEL_ZEILE_9.append(STRASSEN_AUSWAHL())
        TEL_ZEILE_9.append(HAUSNUMMER_AUSWAHL())
        TEL_ZEILE_9.append(STADT_AUSWAHL())
        TEL_ZEILE_9.append(TELEFONNUMER_AUSWAHL())

        TEL_ZEILE_10.append(NACHNAMEN_AUSWAHL())
        TEL_ZEILE_10.append(VORNAMEN_AUSWAHL())
        TEL_ZEILE_10.append(STRASSEN_AUSWAHL())
        TEL_ZEILE_10.append(HAUSNUMMER_AUSWAHL())
        TEL_ZEILE_10.append(STADT_AUSWAHL())
        TEL_ZEILE_10.append(TELEFONNUMER_AUSWAHL())

        TEL_ZEILE_11.append(NACHNAMEN_AUSWAHL())
        TEL_ZEILE_11.append(VORNAMEN_AUSWAHL())
        TEL_ZEILE_11.append(STRASSEN_AUSWAHL())
        TEL_ZEILE_11.append(HAUSNUMMER_AUSWAHL())
        TEL_ZEILE_11.append(STADT_AUSWAHL())
        TEL_ZEILE_11.append(TELEFONNUMER_AUSWAHL())

        TEL_ZEILE_12.append(NACHNAMEN_AUSWAHL())
        TEL_ZEILE_12.append(VORNAMEN_AUSWAHL())
        TEL_ZEILE_12.append(STRASSEN_AUSWAHL())
        TEL_ZEILE_12.append(HAUSNUMMER_AUSWAHL())
        TEL_ZEILE_12.append(STADT_AUSWAHL())
        TEL_ZEILE_12.append(TELEFONNUMER_AUSWAHL())

        TEL_ZEILE_13.append(NACHNAMEN_AUSWAHL())
        TEL_ZEILE_13.append(VORNAMEN_AUSWAHL())
        TEL_ZEILE_13.append(STRASSEN_AUSWAHL())
        TEL_ZEILE_13.append(HAUSNUMMER_AUSWAHL())
        TEL_ZEILE_13.append(STADT_AUSWAHL())
        TEL_ZEILE_13.append(TELEFONNUMER_AUSWAHL())

        TEL_ZEILE_14.append(NACHNAMEN_AUSWAHL())
        TEL_ZEILE_14.append(VORNAMEN_AUSWAHL())
        TEL_ZEILE_14.append(STRASSEN_AUSWAHL())
        TEL_ZEILE_14.append(HAUSNUMMER_AUSWAHL())
        TEL_ZEILE_14.append(STADT_AUSWAHL())
        TEL_ZEILE_14.append(TELEFONNUMER_AUSWAHL())

        TEL_ZEILE_15.append(NACHNAMEN_AUSWAHL())
        TEL_ZEILE_15.append(VORNAMEN_AUSWAHL())
        TEL_ZEILE_15.append(STRASSEN_AUSWAHL())
        TEL_ZEILE_15.append(HAUSNUMMER_AUSWAHL())
        TEL_ZEILE_15.append(STADT_AUSWAHL())
        TEL_ZEILE_15.append(TELEFONNUMER_AUSWAHL())

        TEL_ZEILE_16.append(NACHNAMEN_AUSWAHL())
        TEL_ZEILE_16.append(VORNAMEN_AUSWAHL())
        TEL_ZEILE_16.append(STRASSEN_AUSWAHL())
        TEL_ZEILE_16.append(HAUSNUMMER_AUSWAHL())
        TEL_ZEILE_16.append(STADT_AUSWAHL())
        TEL_ZEILE_16.append(TELEFONNUMER_AUSWAHL())

    def TEL_FRAGEN_GENERATOR(A, B): # Nachname 0, Vorname 1, Strasse 2 , Hausnummer 3, Stadt 4, Telefonnummer 5
        if B == 1:
            TEL_FRAGE = ("Wer wohnt in " + str(A[2]) + " " + str(A[3]) + " , " + str(A[4]) + "?")  # lösung A0
        elif B == 2:
            TEL_FRAGE = ("Wie heißt " + str(A[0]) + " mit Vornamen?")  # lösung A1
        elif B == 3:
            TEL_FRAGE = ("In welcher Strasse wohnt " + str(A[1]) + " " + str(A[0]) + "?") # lösung A2
        elif B == 4:
            TEL_FRAGE = ("Welche Hausnummer hat das Zuhause von " + str(A[1]) + " " + str(A[0]) + "?") # lösung A3
        elif B == 5:
            TEL_FRAGE = ("In welcher Stadt liegt " + str(A[2]) + "?") # lösung A4
        elif B == 6:
            TEL_FRAGE = ("Wie lautet die Telefonnummer von " + str(A[1]) + " " + str(A[0]) + "?") # lösung A5


        return TEL_FRAGE
    def TEL_ERGEBNIS_GENERATOR(A, B):
        if B == 1:
            TEL_ERGEBNIS = str(A[0])
        elif B == 2:
            TEL_ERGEBNIS = str(A[1])
        elif B == 3:
            TEL_ERGEBNIS = str(A[2])
        elif B == 4:
            TEL_ERGEBNIS = str(A[3])
        elif B == 5:
            TEL_ERGEBNIS = str(A[4])
        elif B == 6:
            TEL_ERGEBNIS = str(A[5])

        return TEL_ERGEBNIS

    def TEL_AUFGABEN_GENERATOR_1():
        global TEL_ERGEBNIS_1, TEL_FRAGE_1
        while True:
            TEL_ZEILE = random.choice(TEL_ZEILEN_AUSWAHL)
            R_1 = random.randint(1, 6)

            if TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1) in ERGEBNISSE:
                continue
            else:
                ERGEBNISSE.append(TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1))
                TEL_ERGEBNIS_1 = TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1)
                TEL_FRAGE_1 = TEL_FRAGEN_GENERATOR(TEL_ZEILE, R_1)
                break
    def TEL_AUFGABEN_GENERATOR_2():
        global TEL_ERGEBNIS_2, TEL_FRAGE_2
        while True:
            TEL_ZEILE = random.choice(TEL_ZEILEN_AUSWAHL)
            R_1 = random.randint(1, 6)

            if TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1) in ERGEBNISSE:
                continue
            else:
                ERGEBNISSE.append(TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1))
                TEL_ERGEBNIS_2 = TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1)
                TEL_FRAGE_2 = TEL_FRAGEN_GENERATOR(TEL_ZEILE, R_1)
                break
    def TEL_AUFGABEN_GENERATOR_3():
        global TEL_ERGEBNIS_3, TEL_FRAGE_3
        while True:
            TEL_ZEILE = random.choice(TEL_ZEILEN_AUSWAHL)
            R_1 = random.randint(1, 6)

            if TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1) in ERGEBNISSE:
                continue
            else:
                ERGEBNISSE.append(TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1))
                TEL_ERGEBNIS_3 = TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1)
                TEL_FRAGE_3 = TEL_FRAGEN_GENERATOR(TEL_ZEILE, R_1)
                break
    def TEL_AUFGABEN_GENERATOR_4():
        global TEL_ERGEBNIS_4, TEL_FRAGE_4
        while True:
            TEL_ZEILE = random.choice(TEL_ZEILEN_AUSWAHL)
            R_1 = random.randint(1, 6)

            if TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1) in ERGEBNISSE:
                continue
            else:
                ERGEBNISSE.append(TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1))
                TEL_ERGEBNIS_4 = TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1)
                TEL_FRAGE_4 = TEL_FRAGEN_GENERATOR(TEL_ZEILE, R_1)
                break
    def TEL_AUFGABEN_GENERATOR_5():
        global TEL_ERGEBNIS_5, TEL_FRAGE_5
        while True:
            TEL_ZEILE = random.choice(TEL_ZEILEN_AUSWAHL)
            R_1 = random.randint(1, 6)

            if TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1) in ERGEBNISSE:
                continue
            else:
                ERGEBNISSE.append(TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1))
                TEL_ERGEBNIS_5 = TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1)
                TEL_FRAGE_5 = TEL_FRAGEN_GENERATOR(TEL_ZEILE, R_1)
                break
    def TEL_AUFGABEN_GENERATOR_6():
        global TEL_ERGEBNIS_6, TEL_FRAGE_6
        while True:
            TEL_ZEILE = random.choice(TEL_ZEILEN_AUSWAHL)
            R_1 = random.randint(1, 6)

            if TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1) in ERGEBNISSE:
                continue
            else:
                ERGEBNISSE.append(TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1))
                TEL_ERGEBNIS_6 = TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1)
                TEL_FRAGE_6 = TEL_FRAGEN_GENERATOR(TEL_ZEILE, R_1)
                break
    def TEL_AUFGABEN_GENERATOR_7():
        global TEL_ERGEBNIS_7, TEL_FRAGE_7
        while True:
            TEL_ZEILE = random.choice(TEL_ZEILEN_AUSWAHL)
            R_1 = random.randint(1, 6)

            if TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1) in ERGEBNISSE:
                continue
            else:
                ERGEBNISSE.append(TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1))
                TEL_ERGEBNIS_7 = TEL_ERGEBNIS_GENERATOR(TEL_ZEILE, R_1)
                TEL_FRAGE_7 = TEL_FRAGEN_GENERATOR(TEL_ZEILE, R_1)
                break

    TEL_GENERATOR()
    TEL_AUFGABEN_GENERATOR_1()
    TEL_AUFGABEN_GENERATOR_2()
    TEL_AUFGABEN_GENERATOR_3()
    TEL_AUFGABEN_GENERATOR_4()
    TEL_AUFGABEN_GENERATOR_5()
    TEL_AUFGABEN_GENERATOR_6()
    TEL_AUFGABEN_GENERATOR_7()
def KAL_AUFGABEN():
    global KAL_ZEILE_1, KAL_ZEILE_2, KAL_ZEILE_3, KAL_ZEILE_4, KAL_ZEILE_5, KAL_ZEILE_6, KAL_ZEILE_7, KAL_ZEILE_8, KAL_ZEILE_9, KAL_ZEILE_10, KAL_ZEILE_11, KAL_ZEILE_12, KAL_ZEILE_13, KAL_ZEILE_14, KAL_ZEILE_15, KAL_ZEILE_16, KAL_ZEILE_17, KAL_ZEILE_18, KAL_ZEILE_19, KAL_ZEILE_20, KAL_ZEILE_21
    global KAL_FRAGE_1, KAL_FRAGE_2, KAL_FRAGE_3, KAL_FRAGE_4, KAL_FRAGE_5, KAL_FRAGE_6
    global KAL_ERGEBNIS_1, KAL_ERGEBNIS_2, KAL_ERGEBNIS_3, KAL_ERGEBNIS_4, KAL_ERGEBNIS_5, KAL_ERGEBNIS_6
    global ERGEBNISSE

    Taetigkeiten = [" telefonieren", " treffen", " spatzieren", " verabreden", " trainieren", " Einkaufen gehen",
                    " Laufen gehen", " einen Termin ausmachen", " unterhalten", " ins Kino gehen", " Essen gehen", " spielen",
                    " kämpfen", " Angeln gehen", " Bowlen gehen", " musizieren", " kochen", " Springseil springen",
                    " Ideen sammeln", " Urlaub planen"]
    Personen = [" mit deinem Hausarzt", " mit deinem Zahnarzt", " mit deiner Mutter", " mit deinem Vater",
                " mit deinem besten Freund", " mit Maria", " mit deinem Chef", " mit Benni",
                " mit deinem Physiotherapeuten", " mit deinem Steuerberater", " mit Angelika", " mit Nick",
                " mit Richard", " mit Julia", " mit deinem Mechaniker", " mit deinem Trainer", " mit Fredi",
                " mit Vivian", " mit Sandra", " mit Florian"]

    MINUTENZEITEN = ["00", "15", "30", "45"]


    KAL_ZEILE_1 = ["Montag", "Morgen"]  # Tag, Tageszeit, Uhrzeit, Taetigkeit, Name
    KAL_ZEILE_2 = ["Montag", "Mittag"]
    KAL_ZEILE_3 = ["Montag", "Abend"]
    KAL_ZEILE_4 = ["Dienstag", "Morgen"]
    KAL_ZEILE_5 = ["Dienstag", "Mittag"]
    KAL_ZEILE_6 = ["Dienstag", "Abend"]
    KAL_ZEILE_7 = ["Mittwoch", "Morgen"]
    KAL_ZEILE_8 = ["Mittwoch", "Mittag"]
    KAL_ZEILE_9 = ["Mittwoch", "Abend"]
    KAL_ZEILE_10 = ["Donnerstag", "Morgen"]
    KAL_ZEILE_11 = ["Donnerstag", "Mittag"]
    KAL_ZEILE_12 = ["Donnerstag", "Abend"]
    KAL_ZEILE_13 = ["Freitag", "Morgen"]
    KAL_ZEILE_14 = ["Freitag", "Mittag"]
    KAL_ZEILE_15 = ["Freitag", "Abend"]
    KAL_ZEILE_16 = ["Samstag", "Morgen"]
    KAL_ZEILE_17 = ["Samstag", "Mittag"]
    KAL_ZEILE_18 = ["Samstag", "Abend"]
    KAL_ZEILE_19 = ["Sonntag", "Morgen"]
    KAL_ZEILE_20 = ["Sonntag", "Mittag"]
    KAL_ZEILE_21 = ["Sonntag", "Abend"]

    KAL_ZEILEN_AUSWAHL = [KAL_ZEILE_1, KAL_ZEILE_2, KAL_ZEILE_3, KAL_ZEILE_4, KAL_ZEILE_5, KAL_ZEILE_6, KAL_ZEILE_7,
                          KAL_ZEILE_8, KAL_ZEILE_9, KAL_ZEILE_10, KAL_ZEILE_11, KAL_ZEILE_12, KAL_ZEILE_13,
                          KAL_ZEILE_14, KAL_ZEILE_15, KAL_ZEILE_16, KAL_ZEILE_17, KAL_ZEILE_18, KAL_ZEILE_19,
                          KAL_ZEILE_20, KAL_ZEILE_21]

    KAL_FRAGE_1 = "A"
    KAL_FRAGE_2 = "A"
    KAL_FRAGE_3 = "A"
    KAL_FRAGE_4 = "A"
    KAL_FRAGE_5 = "A"
    KAL_FRAGE_6 = "A"

    KAL_ERGEBNIS_1 = "A"
    KAL_ERGEBNIS_2 = "A"
    KAL_ERGEBNIS_3 = "A"
    KAL_ERGEBNIS_4 = "A"
    KAL_ERGEBNIS_5 = "A"
    KAL_ERGEBNIS_6 = "A"

    def KAL_GENERATOR():

        def UHRZEIT_GENERATOR(A):
            if A[1] == "Morgen":
                R_1 = random.randint(6, 11)
                if R_1 < 10:
                    UHRZEIT = ("Um " + "0" + str(R_1) + ":" + str(random.choice(MINUTENZEITEN)) + " Uhr")
                else:
                    UHRZEIT = ("Um " + str(R_1) + ":" + str(random.choice(MINUTENZEITEN)) + " Uhr")

            elif A[1] == "Mittag":
                UHRZEIT = ("Um " + str(random.randint(12, 17)) + ":" + str(random.choice(MINUTENZEITEN)) + " Uhr")
            else:
                UHRZEIT = ("Um " + str(random.randint(18, 23)) + ":" + str(random.choice(MINUTENZEITEN)) + " Uhr")

            return UHRZEIT

        KAL_ZEILE_1.append(UHRZEIT_GENERATOR(KAL_ZEILE_1))
        KAL_ZEILE_1.append(random.choice(Taetigkeiten))
        KAL_ZEILE_1.append(random.choice(Personen))

        KAL_ZEILE_2.append(UHRZEIT_GENERATOR(KAL_ZEILE_2))
        KAL_ZEILE_2.append(random.choice(Taetigkeiten))
        KAL_ZEILE_2.append(random.choice(Personen))

        KAL_ZEILE_3.append(UHRZEIT_GENERATOR(KAL_ZEILE_3))
        KAL_ZEILE_3.append(random.choice(Taetigkeiten))
        KAL_ZEILE_3.append(random.choice(Personen))

        KAL_ZEILE_4.append(UHRZEIT_GENERATOR(KAL_ZEILE_4))
        KAL_ZEILE_4.append(random.choice(Taetigkeiten))
        KAL_ZEILE_4.append(random.choice(Personen))

        KAL_ZEILE_5.append(UHRZEIT_GENERATOR(KAL_ZEILE_5))
        KAL_ZEILE_5.append(random.choice(Taetigkeiten))
        KAL_ZEILE_5.append(random.choice(Personen))

        KAL_ZEILE_6.append(UHRZEIT_GENERATOR(KAL_ZEILE_6))
        KAL_ZEILE_6.append(random.choice(Taetigkeiten))
        KAL_ZEILE_6.append(random.choice(Personen))

        KAL_ZEILE_7.append(UHRZEIT_GENERATOR(KAL_ZEILE_7))
        KAL_ZEILE_7.append(random.choice(Taetigkeiten))
        KAL_ZEILE_7.append(random.choice(Personen))

        KAL_ZEILE_8.append(UHRZEIT_GENERATOR(KAL_ZEILE_8))
        KAL_ZEILE_8.append(random.choice(Taetigkeiten))
        KAL_ZEILE_8.append(random.choice(Personen))

        KAL_ZEILE_9.append(UHRZEIT_GENERATOR(KAL_ZEILE_9))
        KAL_ZEILE_9.append(random.choice(Taetigkeiten))
        KAL_ZEILE_9.append(random.choice(Personen))

        KAL_ZEILE_10.append(UHRZEIT_GENERATOR(KAL_ZEILE_10))
        KAL_ZEILE_10.append(random.choice(Taetigkeiten))
        KAL_ZEILE_10.append(random.choice(Personen))

        KAL_ZEILE_11.append(UHRZEIT_GENERATOR(KAL_ZEILE_11))
        KAL_ZEILE_11.append(random.choice(Taetigkeiten))
        KAL_ZEILE_11.append(random.choice(Personen))

        KAL_ZEILE_12.append(UHRZEIT_GENERATOR(KAL_ZEILE_12))
        KAL_ZEILE_12.append(random.choice(Taetigkeiten))
        KAL_ZEILE_12.append(random.choice(Personen))

        KAL_ZEILE_13.append(UHRZEIT_GENERATOR(KAL_ZEILE_13))
        KAL_ZEILE_13.append(random.choice(Taetigkeiten))
        KAL_ZEILE_13.append(random.choice(Personen))

        KAL_ZEILE_14.append(UHRZEIT_GENERATOR(KAL_ZEILE_14))
        KAL_ZEILE_14.append(random.choice(Taetigkeiten))
        KAL_ZEILE_14.append(random.choice(Personen))

        KAL_ZEILE_15.append(UHRZEIT_GENERATOR(KAL_ZEILE_15))
        KAL_ZEILE_15.append(random.choice(Taetigkeiten))
        KAL_ZEILE_15.append(random.choice(Personen))

        KAL_ZEILE_16.append(UHRZEIT_GENERATOR(KAL_ZEILE_16))
        KAL_ZEILE_16.append(random.choice(Taetigkeiten))
        KAL_ZEILE_16.append(random.choice(Personen))

        KAL_ZEILE_17.append(UHRZEIT_GENERATOR(KAL_ZEILE_17))
        KAL_ZEILE_17.append(random.choice(Taetigkeiten))
        KAL_ZEILE_17.append(random.choice(Personen))

        KAL_ZEILE_18.append(UHRZEIT_GENERATOR(KAL_ZEILE_18))
        KAL_ZEILE_18.append(random.choice(Taetigkeiten))
        KAL_ZEILE_18.append(random.choice(Personen))

        KAL_ZEILE_19.append(UHRZEIT_GENERATOR(KAL_ZEILE_19))
        KAL_ZEILE_19.append(random.choice(Taetigkeiten))
        KAL_ZEILE_19.append(random.choice(Personen))

        KAL_ZEILE_20.append(UHRZEIT_GENERATOR(KAL_ZEILE_20))
        KAL_ZEILE_20.append(random.choice(Taetigkeiten))
        KAL_ZEILE_20.append(random.choice(Personen))

        KAL_ZEILE_21.append(UHRZEIT_GENERATOR(KAL_ZEILE_21))
        KAL_ZEILE_21.append(random.choice(Taetigkeiten))
        KAL_ZEILE_21.append(random.choice(Personen))

    def KAL_FRAGEN_GENERATOR(A, B):
        if B == 1:
            KAL_FRAGE = ("Um wiviel Uhr sollst du " + str(A[3]) + str(A[4]) + " am " + str(A[0]) + " " + str(A[1]))
        elif B == 2:
            KAL_FRAGE = ("Was machst du " + str(A[2]) + str(A[4]) + " am " + str(A[0]) + " " + str(A[1]))
        elif B == 3:
            KAL_FRAGE = ("Mit wem sollst du " + str(A[2]) + str(A[3]) + " am " + str(A[0]) + " " + str(A[1]))
        return KAL_FRAGE
    def KAL_ERGEBNIS_GENERATOR(A, B):
        if B == 1:
            KAL_ERGEBNIS = str(A[2])
        elif B == 2:
            KAL_ERGEBNIS = str(A[3])
        elif B == 3:
            KAL_ERGEBNIS = str(A[4])
        return KAL_ERGEBNIS

    def KAL_AUFGABEN_GENERATOR_1():
        global KAL_ERGEBNIS_1, KAL_FRAGE_1
        while True:
            KAL_ZEILE = random.choice(KAL_ZEILEN_AUSWAHL)
            R_1 = random.randint(1, 3)

            if KAL_ERGEBNIS_GENERATOR(KAL_ZEILE, R_1) in ERGEBNISSE:
                continue
            else:
                ERGEBNISSE.append(KAL_ERGEBNIS_GENERATOR(KAL_ZEILE, R_1))
                KAL_ERGEBNIS_1 = KAL_ERGEBNIS_GENERATOR(KAL_ZEILE, R_1)
                KAL_FRAGE_1 = KAL_FRAGEN_GENERATOR(KAL_ZEILE, R_1)
                break
    def KAL_AUFGABEN_GENERATOR_2():
        global KAL_ERGEBNIS_2, KAL_FRAGE_2
        while True:
            KAL_ZEILE = random.choice(KAL_ZEILEN_AUSWAHL)
            R_1 = random.randint(1, 3)

            if KAL_ERGEBNIS_GENERATOR(KAL_ZEILE, R_1) in ERGEBNISSE:
                continue
            else:
                ERGEBNISSE.append(KAL_ERGEBNIS_GENERATOR(KAL_ZEILE, R_1))
                KAL_ERGEBNIS_2 = KAL_ERGEBNIS_GENERATOR(KAL_ZEILE, R_1)
                KAL_FRAGE_2 = KAL_FRAGEN_GENERATOR(KAL_ZEILE, R_1)
                break
    def KAL_AUFGABEN_GENERATOR_3():
        global KAL_ERGEBNIS_3, KAL_FRAGE_3
        while True:
            KAL_ZEILE = random.choice(KAL_ZEILEN_AUSWAHL)
            R_1 = random.randint(1, 3)

            if KAL_ERGEBNIS_GENERATOR(KAL_ZEILE, R_1) in ERGEBNISSE:
                continue
            else:
                ERGEBNISSE.append(KAL_ERGEBNIS_GENERATOR(KAL_ZEILE, R_1))
                KAL_ERGEBNIS_3 = KAL_ERGEBNIS_GENERATOR(KAL_ZEILE, R_1)
                KAL_FRAGE_3 = KAL_FRAGEN_GENERATOR(KAL_ZEILE, R_1)
                break
    def KAL_AUFGABEN_GENERATOR_4():
        global KAL_ERGEBNIS_4, KAL_FRAGE_4
        while True:
            KAL_ZEILE = random.choice(KAL_ZEILEN_AUSWAHL)
            R_1 = random.randint(1, 3)

            if KAL_ERGEBNIS_GENERATOR(KAL_ZEILE, R_1) in ERGEBNISSE:
                continue
            else:
                ERGEBNISSE.append(KAL_ERGEBNIS_GENERATOR(KAL_ZEILE, R_1))
                KAL_ERGEBNIS_4 = KAL_ERGEBNIS_GENERATOR(KAL_ZEILE, R_1)
                KAL_FRAGE_4 = KAL_FRAGEN_GENERATOR(KAL_ZEILE, R_1)
                break
    def KAL_AUFGABEN_GENERATOR_5():
        global KAL_ERGEBNIS_5, KAL_FRAGE_5
        while True:
            KAL_ZEILE = random.choice(KAL_ZEILEN_AUSWAHL)
            R_1 = random.randint(1, 3)

            if KAL_ERGEBNIS_GENERATOR(KAL_ZEILE, R_1) in ERGEBNISSE:
                continue
            else:
                ERGEBNISSE.append(KAL_ERGEBNIS_GENERATOR(KAL_ZEILE, R_1))
                KAL_ERGEBNIS_5 = KAL_ERGEBNIS_GENERATOR(KAL_ZEILE, R_1)
                KAL_FRAGE_5 = KAL_FRAGEN_GENERATOR(KAL_ZEILE, R_1)
                break
    def KAL_AUFGABEN_GENERATOR_6():
        global KAL_ERGEBNIS_6, KAL_FRAGE_6
        while True:
            KAL_ZEILE = random.choice(KAL_ZEILEN_AUSWAHL)
            R_1 = random.randint(1, 3)

            if KAL_ERGEBNIS_GENERATOR(KAL_ZEILE, R_1) in ERGEBNISSE:
                continue
            else:
                ERGEBNISSE.append(KAL_ERGEBNIS_GENERATOR(KAL_ZEILE, R_1))
                KAL_ERGEBNIS_6 = KAL_ERGEBNIS_GENERATOR(KAL_ZEILE, R_1)
                KAL_FRAGE_6 = KAL_FRAGEN_GENERATOR(KAL_ZEILE, R_1)
                break

    KAL_GENERATOR()
    KAL_AUFGABEN_GENERATOR_1()
    KAL_AUFGABEN_GENERATOR_2()
    KAL_AUFGABEN_GENERATOR_3()
    KAL_AUFGABEN_GENERATOR_4()
    KAL_AUFGABEN_GENERATOR_5()
    KAL_AUFGABEN_GENERATOR_6()
def VORLESEFRAGEN_RANDOMISER():
    global RANDOMISER_LISTE

    while len(RANDOMISER_LISTE) < 20:
        R = random.randint(0, 19)
        if R not in RANDOMISER_LISTE:
            RANDOMISER_LISTE.append(R)
        else:
            continue

RECHENAUFGABEN()
TEL_AUFGABEN()
KAL_AUFGABEN()
VORLESEFRAGEN_RANDOMISER()

def UHR():
    global SEKUNDE_1, SEKUNDE_10, MINUTE_1, MINUTE_10, GESAMTZEIT

    if Gameloop == 60:
        SEKUNDE_1 = SEKUNDE_1 + 1
        GESAMTZEIT = GESAMTZEIT + 1
    if SEKUNDE_1 == 10:
        SEKUNDE_1 = 0
        SEKUNDE_10 = SEKUNDE_10 + 1
    if SEKUNDE_10 == 6:
        SEKUNDE_10 = 0
        MINUTE_1 = MINUTE_1 + 1
    if MINUTE_1 == 10:
        MINUTE_1 = 0
        MINUTE_10 = MINUTE_10 + 1
    if MINUTE_10 == 10:
        SEKUNDE_1 = 0
        SEKUNDE_10 = 0
        MINUTE_1 = 0
        MINUTE_10 = 0

    draw_SEKUNDE_1 = UHR_FONT.render(str(SEKUNDE_1), 1, GREEN)
    WIN.blit(draw_SEKUNDE_1, (1600, 50))

    draw_SEKUNDE_10 = UHR_FONT.render(f" : " + str(SEKUNDE_10), 1, GREEN)
    WIN.blit(draw_SEKUNDE_10, (1510, 50))

    draw_MINUTE_1 = UHR_FONT.render(str(MINUTE_1), 1, GREEN)
    WIN.blit(draw_MINUTE_1, (1475, 50))

    draw_MINUTE_10 = UHR_FONT.render(str(MINUTE_10), 1, GREEN)
    WIN.blit(draw_MINUTE_10, (1435, 50))

def TIMESTAMP_GENERATOR():

    global TIMESTAMP_AUFGABE_1, TIMESTAMP_AUFGABE_2, TIMESTAMP_AUFGABE_3, TIMESTAMP_AUFGABE_4, TIMESTAMP_AUFGABE_5, TIMESTAMP_AUFGABE_6, TIMESTAMP_AUFGABE_7, TIMESTAMP_AUFGABE_8, TIMESTAMP_AUFGABE_9, TIMESTAMP_AUFGABE_10, TIMESTAMP_AUFGABE_11, TIMESTAMP_AUFGABE_12, TIMESTAMP_AUFGABE_13, TIMESTAMP_AUFGABE_14, TIMESTAMP_AUFGABE_15, TIMESTAMP_AUFGABE_16, TIMESTAMP_AUFGABE_17, TIMESTAMP_AUFGABE_18, TIMESTAMP_AUFGABE_19, TIMESTAMP_AUFGABE_20

    MIN_ZEIT = 20
    MAX_ZEIT = 35
    TIMESTAMP_AUFGABE_1 = random.randint(GESAMTZEIT + MIN_ZEIT, GESAMTZEIT + MAX_ZEIT)
    TIMESTAMP_AUFGABE_2 = random.randint(TIMESTAMP_AUFGABE_1 + MIN_ZEIT, TIMESTAMP_AUFGABE_1 + MAX_ZEIT)
    TIMESTAMP_AUFGABE_3 = random.randint(TIMESTAMP_AUFGABE_2 + MIN_ZEIT, TIMESTAMP_AUFGABE_2 + MAX_ZEIT)
    TIMESTAMP_AUFGABE_4 = random.randint(TIMESTAMP_AUFGABE_3 + MIN_ZEIT, TIMESTAMP_AUFGABE_3 + MAX_ZEIT)
    TIMESTAMP_AUFGABE_5 = random.randint(TIMESTAMP_AUFGABE_4 + MIN_ZEIT, TIMESTAMP_AUFGABE_4 + MAX_ZEIT)
    TIMESTAMP_AUFGABE_6 = random.randint(TIMESTAMP_AUFGABE_5 + MIN_ZEIT, TIMESTAMP_AUFGABE_5 + MAX_ZEIT)
    TIMESTAMP_AUFGABE_7 = random.randint(TIMESTAMP_AUFGABE_6 + MIN_ZEIT, TIMESTAMP_AUFGABE_6 + MAX_ZEIT)
    TIMESTAMP_AUFGABE_8 = random.randint(TIMESTAMP_AUFGABE_7 + MIN_ZEIT, TIMESTAMP_AUFGABE_7 + MAX_ZEIT)
    TIMESTAMP_AUFGABE_9 = random.randint(TIMESTAMP_AUFGABE_8 + MIN_ZEIT, TIMESTAMP_AUFGABE_8 + MAX_ZEIT)
    TIMESTAMP_AUFGABE_10 = random.randint(TIMESTAMP_AUFGABE_9 + MIN_ZEIT, TIMESTAMP_AUFGABE_9 + MAX_ZEIT)
    TIMESTAMP_AUFGABE_11 = random.randint(TIMESTAMP_AUFGABE_10 + MIN_ZEIT, TIMESTAMP_AUFGABE_10 + MAX_ZEIT)
    TIMESTAMP_AUFGABE_12 = random.randint(TIMESTAMP_AUFGABE_11 + MIN_ZEIT, TIMESTAMP_AUFGABE_11 + MAX_ZEIT)
    TIMESTAMP_AUFGABE_13 = random.randint(TIMESTAMP_AUFGABE_12 + MIN_ZEIT, TIMESTAMP_AUFGABE_12 + MAX_ZEIT)
    TIMESTAMP_AUFGABE_14 = random.randint(TIMESTAMP_AUFGABE_13 + MIN_ZEIT, TIMESTAMP_AUFGABE_13 + MAX_ZEIT)
    TIMESTAMP_AUFGABE_15 = random.randint(TIMESTAMP_AUFGABE_14 + MIN_ZEIT, TIMESTAMP_AUFGABE_14 + MAX_ZEIT)
    TIMESTAMP_AUFGABE_16 = random.randint(TIMESTAMP_AUFGABE_15 + MIN_ZEIT, TIMESTAMP_AUFGABE_15 + MAX_ZEIT)
    TIMESTAMP_AUFGABE_17 = random.randint(TIMESTAMP_AUFGABE_16 + MIN_ZEIT, TIMESTAMP_AUFGABE_16 + MAX_ZEIT)
    TIMESTAMP_AUFGABE_18 = random.randint(TIMESTAMP_AUFGABE_17 + MIN_ZEIT, TIMESTAMP_AUFGABE_17 + MAX_ZEIT)
    TIMESTAMP_AUFGABE_19 = random.randint(TIMESTAMP_AUFGABE_18 + MIN_ZEIT, TIMESTAMP_AUFGABE_18 + MAX_ZEIT)
    TIMESTAMP_AUFGABE_20 = random.randint(TIMESTAMP_AUFGABE_19 + MIN_ZEIT, TIMESTAMP_AUFGABE_19 + MAX_ZEIT)

TIMESTAMP_GENERATOR()
def AUSWAHLFELD_VORLESEFRAGEN():
    global VORLES_A1_STRICH, VORLES_A2_STRICH, VORLES_A3_STRICH, VORLES_A4_STRICH, VORLES_A5_STRICH, VORLES_B1_STRICH, VORLES_B2_STRICH, VORLES_B3_STRICH, VORLES_B4_STRICH, VORLES_B5_STRICH, VORLES_C1_STRICH, VORLES_C2_STRICH, VORLES_C3_STRICH, VORLES_C4_STRICH, VORLES_C5_STRICH, VORLES_D1_STRICH, VORLES_D2_STRICH, VORLES_D3_STRICH, VORLES_D4_STRICH, VORLES_D5_STRICH

    def AUSWAHL_AUS_ERGEBNISLISTE(A,B):
        VORLES_DRAW = AUSWAHLFELD_FOND.render(str(ERGEBNISSE[B]), 1, BLUE)
        WIN.blit(VORLES_DRAW, (A[0] + 10, A[1] + 10))

    VORLES_A1 = pygame.Rect(pygame.Rect(300, 820, 270, 45))
    VORLES_A2 = pygame.Rect(pygame.Rect(570, 820, 270, 45))
    VORLES_A3 = pygame.Rect(pygame.Rect(840, 820, 270, 45))
    VORLES_A4 = pygame.Rect(pygame.Rect(1110, 820, 270, 45))
    VORLES_A5 = pygame.Rect(pygame.Rect(1380, 820, 270, 45))

    VORLES_B1 = pygame.Rect(pygame.Rect(300, 865, 270, 45))
    VORLES_B2 = pygame.Rect(pygame.Rect(570, 865, 270, 45))
    VORLES_B3 = pygame.Rect(pygame.Rect(840, 865, 270, 45))
    VORLES_B4 = pygame.Rect(pygame.Rect(1110, 865, 270, 45))
    VORLES_B5 = pygame.Rect(pygame.Rect(1380, 865, 270, 45))

    VORLES_C1 = pygame.Rect(pygame.Rect(300, 910, 270, 45))
    VORLES_C2 = pygame.Rect(pygame.Rect(570, 910, 270, 45))
    VORLES_C3 = pygame.Rect(pygame.Rect(840, 910, 270, 45))
    VORLES_C4 = pygame.Rect(pygame.Rect(1110, 910, 270, 45))
    VORLES_C5 = pygame.Rect(pygame.Rect(1380, 910, 270, 45))

    VORLES_D1 = pygame.Rect(pygame.Rect(300, 955, 270, 45))
    VORLES_D2 = pygame.Rect(pygame.Rect(570, 955, 270, 45))
    VORLES_D3 = pygame.Rect(pygame.Rect(840, 955, 270, 45))
    VORLES_D4 = pygame.Rect(pygame.Rect(1110, 955, 270, 45))
    VORLES_D5 = pygame.Rect(pygame.Rect(1380, 955, 270, 45))

    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_A1,RANDOMISER_LISTE[0])
    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_A2,RANDOMISER_LISTE[1])
    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_A3,RANDOMISER_LISTE[2])
    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_A4,RANDOMISER_LISTE[3])
    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_A5,RANDOMISER_LISTE[4])

    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_B1,RANDOMISER_LISTE[5])
    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_B2,RANDOMISER_LISTE[6])
    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_B3,RANDOMISER_LISTE[7])
    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_B4,RANDOMISER_LISTE[8])
    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_B5,RANDOMISER_LISTE[9])

    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_C1,RANDOMISER_LISTE[10])
    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_C2,RANDOMISER_LISTE[11])
    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_C3,RANDOMISER_LISTE[12])
    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_C4,RANDOMISER_LISTE[13])
    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_C5,RANDOMISER_LISTE[14])

    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_D1,RANDOMISER_LISTE[15])
    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_D2,RANDOMISER_LISTE[16])
    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_D3,RANDOMISER_LISTE[17])
    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_D4,RANDOMISER_LISTE[18])
    AUSWAHL_AUS_ERGEBNISLISTE(VORLES_D5,RANDOMISER_LISTE[19])

    def UNTERSTRICH_DRAWER(A,B):
        if B == True:
            pygame.draw.line(WIN, BLACK, (A[0]+ 10, A[1] + 45), (A[0] + 260, A[1] + 45), 4)

    VORLES_A1_STRICH = BUTTON_1(VORLES_A1, VORLES_A1_STRICH)
    VORLES_A2_STRICH = BUTTON_1(VORLES_A2, VORLES_A2_STRICH)
    VORLES_A3_STRICH = BUTTON_1(VORLES_A3, VORLES_A3_STRICH)
    VORLES_A4_STRICH = BUTTON_1(VORLES_A4, VORLES_A4_STRICH)
    VORLES_A5_STRICH = BUTTON_1(VORLES_A5, VORLES_A5_STRICH)

    UNTERSTRICH_DRAWER(VORLES_A1, VORLES_A1_STRICH)
    UNTERSTRICH_DRAWER(VORLES_A2, VORLES_A2_STRICH)
    UNTERSTRICH_DRAWER(VORLES_A3, VORLES_A3_STRICH)
    UNTERSTRICH_DRAWER(VORLES_A4, VORLES_A4_STRICH)
    UNTERSTRICH_DRAWER(VORLES_A5, VORLES_A5_STRICH)

    VORLES_B1_STRICH = BUTTON_1(VORLES_B1, VORLES_B1_STRICH)
    VORLES_B2_STRICH = BUTTON_1(VORLES_B2, VORLES_B2_STRICH)
    VORLES_B3_STRICH = BUTTON_1(VORLES_B3, VORLES_B3_STRICH)
    VORLES_B4_STRICH = BUTTON_1(VORLES_B4, VORLES_B4_STRICH)
    VORLES_B5_STRICH = BUTTON_1(VORLES_B5, VORLES_B5_STRICH)

    UNTERSTRICH_DRAWER(VORLES_B1, VORLES_B1_STRICH)
    UNTERSTRICH_DRAWER(VORLES_B2, VORLES_B2_STRICH)
    UNTERSTRICH_DRAWER(VORLES_B3, VORLES_B3_STRICH)
    UNTERSTRICH_DRAWER(VORLES_B4, VORLES_B4_STRICH)
    UNTERSTRICH_DRAWER(VORLES_B5, VORLES_B5_STRICH)

    VORLES_C1_STRICH = BUTTON_1(VORLES_C1, VORLES_C1_STRICH)
    VORLES_C2_STRICH = BUTTON_1(VORLES_C2, VORLES_C2_STRICH)
    VORLES_C3_STRICH = BUTTON_1(VORLES_C3, VORLES_C3_STRICH)
    VORLES_C4_STRICH = BUTTON_1(VORLES_C4, VORLES_C4_STRICH)
    VORLES_C5_STRICH = BUTTON_1(VORLES_C5, VORLES_C5_STRICH)

    UNTERSTRICH_DRAWER(VORLES_C1, VORLES_C1_STRICH)
    UNTERSTRICH_DRAWER(VORLES_C2, VORLES_C2_STRICH)
    UNTERSTRICH_DRAWER(VORLES_C3, VORLES_C3_STRICH)
    UNTERSTRICH_DRAWER(VORLES_C4, VORLES_C4_STRICH)
    UNTERSTRICH_DRAWER(VORLES_C5, VORLES_C5_STRICH)

    VORLES_D1_STRICH = BUTTON_1(VORLES_D1, VORLES_D1_STRICH)
    VORLES_D2_STRICH = BUTTON_1(VORLES_D2, VORLES_D2_STRICH)
    VORLES_D3_STRICH = BUTTON_1(VORLES_D3, VORLES_D3_STRICH)
    VORLES_D4_STRICH = BUTTON_1(VORLES_D4, VORLES_D4_STRICH)
    VORLES_D5_STRICH = BUTTON_1(VORLES_D5, VORLES_D5_STRICH)

    UNTERSTRICH_DRAWER(VORLES_D1, VORLES_D1_STRICH)
    UNTERSTRICH_DRAWER(VORLES_D2, VORLES_D2_STRICH)
    UNTERSTRICH_DRAWER(VORLES_D3, VORLES_D3_STRICH)
    UNTERSTRICH_DRAWER(VORLES_D4, VORLES_D4_STRICH)
    UNTERSTRICH_DRAWER(VORLES_D5, VORLES_D5_STRICH)
def VORLESER():

    global TIMESTAMP_AUFGABE_1, TIMESTAMP_AUFGABE_2, TIMESTAMP_AUFGABE_3, TIMESTAMP_AUFGABE_4, TIMESTAMP_AUFGABE_5, TIMESTAMP_AUFGABE_6, TIMESTAMP_AUFGABE_7, TIMESTAMP_AUFGABE_8, TIMESTAMP_AUFGABE_9, TIMESTAMP_AUFGABE_10, TIMESTAMP_AUFGABE_11, TIMESTAMP_AUFGABE_12, TIMESTAMP_AUFGABE_13, TIMESTAMP_AUFGABE_14, TIMESTAMP_AUFGABE_15, TIMESTAMP_AUFGABE_16, TIMESTAMP_AUFGABE_17, TIMESTAMP_AUFGABE_18, TIMESTAMP_AUFGABE_19, TIMESTAMP_AUFGABE_20
    global AUSREDEN

    def SPEAK(TEXT):
        # Sprachausgabe über die im Browser eingebaute Web Speech API
        # (window.speechSynthesis) – funktioniert ohne Server/Internet,
        # nutzt die vom Betriebssystem/Browser bereitgestellten Stimmen.
        # Als rohes JS ausgeführt (statt über die Python-JS-Bridge-Proxys),
        # da das zuverlässiger ist als der Konstruktor-Aufruf über .new().
        try:
            import platform
            escaped = (str(TEXT).replace("\\", "\\\\")
                                  .replace('"', '\\"')
                                  .replace("\n", " "))
            js_code = (
                '(function(){'
                'try{'
                'var u=new SpeechSynthesisUtterance("' + escaped + '");'
                'var stimmen=window.speechSynthesis.getVoices();'
                'for(var i=0;i<stimmen.length;i++){'
                'if(stimmen[i].lang&&stimmen[i].lang.toLowerCase().indexOf("de")===0){'
                'u.voice=stimmen[i];break;}}'
                'u.lang="de-DE";u.rate=1.0;'
                'window.speechSynthesis.speak(u);'
                '}catch(e){console.error("SIMKAP SPEAK Fehler:",e);}'
                '})();'
            )
            platform.window.eval(js_code)
        except Exception as e:
            print("Sprachausgabe nicht möglich:", e)

    def MELDEZEITGENERATOR(A):
        MELDEZEITEN = [30, 45, 60, 75, 90, 105, 120, 135, 150]
        R = random.choice(MELDEZEITEN)
        R_1 = (R + A) / 60
        R_2 = int(R_1)
        R_3 = int((R_1 - R_2) * 60)
        return str(f"Bei " + str(R_2) + " Minute und " + str(R_3) + " Sekunden beantworte ")

    FRAGEN_LISTE = [RECHEN_FRAGE_1, TEL_FRAGE_1, KAL_FRAGE_1, RECHEN_FRAGE_2, TEL_FRAGE_2, KAL_FRAGE_2, RECHEN_FRAGE_3, TEL_FRAGE_3, KAL_FRAGE_3, RECHEN_FRAGE_4,TEL_FRAGE_4, KAL_FRAGE_4, RECHEN_FRAGE_5, TEL_FRAGE_5, KAL_FRAGE_5, RECHEN_FRAGE_6, TEL_FRAGE_6, KAL_FRAGE_6, RECHEN_FRAGE_7, TEL_FRAGE_7]

    def VORLESE_REIHENFOLGE(A,B):
        global AUSREDEN

        if GESAMTZEIT == A + 15:
            AUSREDEN = True

        if A == GESAMTZEIT and AUSREDEN == True:
            if random.randint(0,100) < 15:
                SPEAK(str(MELDEZEITGENERATOR(A)) + str(FRAGEN_LISTE[RANDOMISER_LISTE[B]]))
                AUSREDEN = False

            else:
                SPEAK(str(FRAGEN_LISTE[RANDOMISER_LISTE[B]]))
                AUSREDEN = False

    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_1, 0)
    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_2, 1)
    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_3, 2)
    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_4, 3)
    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_5, 4)
    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_6, 5)
    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_7, 6)
    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_8, 7)
    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_9, 8)
    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_10, 9)
    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_11, 10)
    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_12, 11)
    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_13, 12)
    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_14, 13)
    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_15, 14)
    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_16, 15)
    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_17, 16)
    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_18, 17)
    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_19, 18)
    VORLESE_REIHENFOLGE(TIMESTAMP_AUFGABE_20, 19)


def KALENDER_TELEFON_BUCH_OVERLAY():
    global KAL_ZEILE_1, KAL_ZEILE_2, KAL_ZEILE_3, KAL_ZEILE_4, KAL_ZEILE_5, KAL_ZEILE_6, KAL_ZEILE_7, KAL_ZEILE_8, KAL_ZEILE_9, KAL_ZEILE_10, KAL_ZEILE_11, KAL_ZEILE_12, KAL_ZEILE_13, KAL_ZEILE_14, KAL_ZEILE_15, KAL_ZEILE_16, KAL_ZEILE_17, KAL_ZEILE_18, KAL_ZEILE_19, KAL_ZEILE_20, KAL_ZEILE_21
    global TEL_ZEILE_1, TEL_ZEILE_2, TEL_ZEILE_3, TEL_ZEILE_4, TEL_ZEILE_5, TEL_ZEILE_6, TEL_ZEILE_7, TEL_ZEILE_8, TEL_ZEILE_9, TEL_ZEILE_10, TEL_ZEILE_11, TEL_ZEILE_12, TEL_ZEILE_13, TEL_ZEILE_14, TEL_ZEILE_15, TEL_ZEILE_16

    def SCHREIBER(A,B,C):
        DRAW = KALENDER_FOND.render(A, 1, BLACK)
        WIN.blit(DRAW, (B, C))


    pygame.draw.rect(WIN, GREY, pygame.Rect(1420, 250, 230, 100))
    CALENDER_DRAW = BTN_FONT.render("KALENDER", 1, BLACK)
    WIN.blit(CALENDER_DRAW, (1470, 280))
    if KALENDER == True:
        pygame.draw.rect(WIN, GREY, pygame.Rect(450, 50, 880, 940))
        pygame.draw.rect(WIN, WHITE, pygame.Rect(790, 930, 200, 50))
        SCHREIBER("SCHLIESSEN", 833, 942)
        SCHREIBER("KALENDER", 840, 60)
        SCHREIBER("MONTAG", 500, 150)
        SCHREIBER("DIENSTAG", 500, 270)
        SCHREIBER("MITTWOCH", 500, 390)
        SCHREIBER("DONNERSTAG", 500, 510)
        SCHREIBER("FREITAG", 500, 630)
        SCHREIBER("SAMSTAG", 500, 750)
        SCHREIBER("SONNTAG", 500, 870)

        SCHREIBER((KAL_ZEILE_1[1] + "s    " + KAL_ZEILE_1[2] + KAL_ZEILE_1[3] + KAL_ZEILE_1[4]), 700, 120)
        SCHREIBER((KAL_ZEILE_2[1] + "s      " + KAL_ZEILE_2[2] + KAL_ZEILE_2[3] + KAL_ZEILE_2[4]), 700, 150)
        SCHREIBER((KAL_ZEILE_3[1] + "s     " + KAL_ZEILE_3[2] + KAL_ZEILE_3[3] + KAL_ZEILE_3[4]), 700, 180)

        SCHREIBER((KAL_ZEILE_4[1] + "s    " + KAL_ZEILE_4[2] + KAL_ZEILE_4[3] + KAL_ZEILE_4[4]), 700, 240)
        SCHREIBER((KAL_ZEILE_5[1] + "s      " + KAL_ZEILE_5[2] + KAL_ZEILE_5[3] + KAL_ZEILE_5[4]), 700, 270)
        SCHREIBER((KAL_ZEILE_6[1] + "s     " + KAL_ZEILE_6[2] + KAL_ZEILE_6[3] + KAL_ZEILE_6[4]), 700, 300)

        SCHREIBER((KAL_ZEILE_7[1] + "s    " + KAL_ZEILE_7[2] + KAL_ZEILE_7[3] + KAL_ZEILE_7[4]), 700, 360)
        SCHREIBER((KAL_ZEILE_8[1] + "s      " + KAL_ZEILE_8[2] + KAL_ZEILE_8[3] + KAL_ZEILE_8[4]), 700, 390)
        SCHREIBER((KAL_ZEILE_9[1] + "s     " + KAL_ZEILE_9[2] + KAL_ZEILE_9[3] + KAL_ZEILE_9[4]), 700, 420)

        SCHREIBER((KAL_ZEILE_10[1] + "s    " + KAL_ZEILE_10[2] + KAL_ZEILE_10[3] + KAL_ZEILE_10[4]), 700, 480)
        SCHREIBER((KAL_ZEILE_11[1] + "s      " + KAL_ZEILE_11[2] + KAL_ZEILE_11[3] + KAL_ZEILE_11[4]), 700, 510)
        SCHREIBER((KAL_ZEILE_12[1] + "s     " + KAL_ZEILE_12[2] + KAL_ZEILE_12[3] + KAL_ZEILE_12[4]), 700, 540)

        SCHREIBER((KAL_ZEILE_13[1] + "s    " + KAL_ZEILE_13[2] + KAL_ZEILE_13[3] + KAL_ZEILE_13[4]), 700, 600)
        SCHREIBER((KAL_ZEILE_14[1] + "s      " + KAL_ZEILE_14[2] + KAL_ZEILE_14[3] + KAL_ZEILE_14[4]), 700, 630)
        SCHREIBER((KAL_ZEILE_15[1] + "s     " + KAL_ZEILE_15[2] + KAL_ZEILE_15[3] + KAL_ZEILE_15[4]), 700, 660)

        SCHREIBER((KAL_ZEILE_16[1] + "s    " +  KAL_ZEILE_16[2] + KAL_ZEILE_16[3] + KAL_ZEILE_16[4]), 700, 720)
        SCHREIBER((KAL_ZEILE_17[1] + "s      " +  KAL_ZEILE_17[2] + KAL_ZEILE_17[3] + KAL_ZEILE_17[4]), 700, 750)
        SCHREIBER((KAL_ZEILE_18[1] + "s     " +  KAL_ZEILE_18[2] + KAL_ZEILE_18[3] + KAL_ZEILE_18[4]), 700, 780)

        SCHREIBER((KAL_ZEILE_19[1] + "s    " +  KAL_ZEILE_19[2] + KAL_ZEILE_19[3] + KAL_ZEILE_19[4]), 700, 840)
        SCHREIBER((KAL_ZEILE_20[1] + "s      " +  KAL_ZEILE_20[2] + KAL_ZEILE_20[3] + KAL_ZEILE_20[4]), 700, 870)
        SCHREIBER((KAL_ZEILE_21[1] + "s     " +  KAL_ZEILE_21[2] + KAL_ZEILE_21[3] + KAL_ZEILE_21[4]), 700, 900)




    pygame.draw.rect(WIN, GREY, pygame.Rect(1420, 400, 230, 100))
    TELEFON_BUCH_DRAW = BTN_FONT.render("TELEFON_BUCH", 1, BLACK)
    WIN.blit(TELEFON_BUCH_DRAW, (1435, 430))
    if TELEFON_BUCH == True:
        pygame.draw.rect(WIN, GREY, pygame.Rect(450, 50, 880, 940))
        pygame.draw.rect(WIN, WHITE, pygame.Rect(790, 930, 200, 50))
        SCHREIBER("SCHLIESSEN", 833, 942)
        SCHREIBER("TELEFONBUCH", 840, 60)

        SCHREIBER("NAME", 550, 100)
        SCHREIBER("ADRESSE", 840, 100)
        SCHREIBER("TELEFON", 1150, 100)

        SCHREIBER(str(TEL_ZEILE_1[0]) + ",  " + str(TEL_ZEILE_1[1]), 550, 150)
        SCHREIBER(str(TEL_ZEILE_1[2]) + "  " + str(TEL_ZEILE_1[3]) + ",  " + str(TEL_ZEILE_1[4]),840, 150)
        SCHREIBER(str(TEL_ZEILE_1[5]), 1150, 150)

        SCHREIBER(str(TEL_ZEILE_2[0]) + ",  " + str(TEL_ZEILE_2[1]), 550, 200)
        SCHREIBER(str(TEL_ZEILE_2[2]) + "  " + str(TEL_ZEILE_2[3]) + ",  " + str(TEL_ZEILE_2[4]), 840, 200)
        SCHREIBER(str(TEL_ZEILE_2[5]), 1150, 200)

        SCHREIBER(str(TEL_ZEILE_3[0]) + ",  " + str(TEL_ZEILE_3[1]), 550, 250)
        SCHREIBER(str(TEL_ZEILE_3[2]) + "  " + str(TEL_ZEILE_3[3]) + ",  " + str(TEL_ZEILE_3[4]), 840, 250)
        SCHREIBER(str(TEL_ZEILE_3[5]), 1150, 250)

        SCHREIBER(str(TEL_ZEILE_4[0]) + ",  " + str(TEL_ZEILE_4[1]), 550, 300)
        SCHREIBER(str(TEL_ZEILE_4[2]) + "  " + str(TEL_ZEILE_4[3]) + ",  " + str(TEL_ZEILE_4[4]), 840, 300)
        SCHREIBER(str(TEL_ZEILE_4[5]), 1150, 300)

        SCHREIBER(str(TEL_ZEILE_5[0]) + ",  " + str(TEL_ZEILE_5[1]), 550, 350)
        SCHREIBER(str(TEL_ZEILE_5[2]) + "  " + str(TEL_ZEILE_5[3]) + ",  " + str(TEL_ZEILE_5[4]), 840, 350)
        SCHREIBER(str(TEL_ZEILE_5[5]), 1150, 350)

        SCHREIBER(str(TEL_ZEILE_6[0]) + ",  " + str(TEL_ZEILE_6[1]), 550, 400)
        SCHREIBER(str(TEL_ZEILE_6[2]) + "  " + str(TEL_ZEILE_6[3]) + ",  " + str(TEL_ZEILE_6[4]), 840, 400)
        SCHREIBER(str(TEL_ZEILE_6[5]), 1150, 400)

        SCHREIBER(str(TEL_ZEILE_7[0]) + ",  " + str(TEL_ZEILE_7[1]), 550, 450)
        SCHREIBER(str(TEL_ZEILE_7[2]) + "  " + str(TEL_ZEILE_7[3]) + ",  " + str(TEL_ZEILE_7[4]), 840, 450)
        SCHREIBER(str(TEL_ZEILE_7[5]), 1150, 450)

        SCHREIBER(str(TEL_ZEILE_8[0]) + ",  " + str(TEL_ZEILE_8[1]), 550, 500)
        SCHREIBER(str(TEL_ZEILE_8[2]) + "  " + str(TEL_ZEILE_8[3]) + ",  " + str(TEL_ZEILE_8[4]), 840, 500)
        SCHREIBER(str(TEL_ZEILE_8[5]), 1150, 500)

        SCHREIBER(str(TEL_ZEILE_9[0]) + ",  " + str(TEL_ZEILE_9[1]), 550, 550)
        SCHREIBER(str(TEL_ZEILE_9[2]) + "  " + str(TEL_ZEILE_9[3]) + ",  " + str(TEL_ZEILE_9[4]), 840, 550)
        SCHREIBER(str(TEL_ZEILE_9[5]), 1150, 550)

        SCHREIBER(str(TEL_ZEILE_10[0]) + ",  " + str(TEL_ZEILE_10[1]), 550, 600)
        SCHREIBER(str(TEL_ZEILE_10[2]) + "  " + str(TEL_ZEILE_10[3]) + ",  " + str(TEL_ZEILE_10[4]), 840, 600)
        SCHREIBER(str(TEL_ZEILE_10[5]), 1150, 600)

        SCHREIBER(str(TEL_ZEILE_11[0]) + ",  " + str(TEL_ZEILE_11[1]), 550, 650)
        SCHREIBER(str(TEL_ZEILE_11[2]) + "  " + str(TEL_ZEILE_11[3]) + ",  " + str(TEL_ZEILE_11[4]), 840, 650)
        SCHREIBER(str(TEL_ZEILE_11[5]), 1150, 650)

        SCHREIBER(str(TEL_ZEILE_12[0]) + ",  " + str(TEL_ZEILE_12[1]), 550, 700)
        SCHREIBER(str(TEL_ZEILE_12[2]) + "  " + str(TEL_ZEILE_12[3]) + ",  " + str(TEL_ZEILE_12[4]), 840, 700)
        SCHREIBER(str(TEL_ZEILE_12[5]), 1150, 700)

        SCHREIBER(str(TEL_ZEILE_13[0]) + ",  " + str(TEL_ZEILE_13[1]), 550, 750)
        SCHREIBER(str(TEL_ZEILE_13[2]) + "  " + str(TEL_ZEILE_13[3]) + ",  " + str(TEL_ZEILE_13[4]), 840, 750)
        SCHREIBER(str(TEL_ZEILE_13[5]), 1150, 750)

        SCHREIBER(str(TEL_ZEILE_14[0]) + ",  " + str(TEL_ZEILE_14[1]), 550, 800)
        SCHREIBER(str(TEL_ZEILE_14[2]) + "  " + str(TEL_ZEILE_14[3]) + ",  " + str(TEL_ZEILE_14[4]), 840, 800)
        SCHREIBER(str(TEL_ZEILE_14[5]), 1150, 800)

        SCHREIBER(str(TEL_ZEILE_15[0]) + ",  " + str(TEL_ZEILE_15[1]), 550, 850)
        SCHREIBER(str(TEL_ZEILE_15[2]) + "  " + str(TEL_ZEILE_15[3]) + ",  " + str(TEL_ZEILE_15[4]), 840, 850)
        SCHREIBER(str(TEL_ZEILE_15[5]), 1150, 850)

        SCHREIBER(str(TEL_ZEILE_16[0]) + ",  " + str(TEL_ZEILE_16[1]), 550, 900)
        SCHREIBER(str(TEL_ZEILE_16[2]) + "  " + str(TEL_ZEILE_16[3]) + ",  " + str(TEL_ZEILE_16[4]), 840, 900)
        SCHREIBER(str(TEL_ZEILE_16[5]), 1150, 900)



    pygame.draw.rect(WIN, GREY, pygame.Rect(1420, 700, 230, 100))
    NEXT_DRAW = BTN_FONT.render("NÄCHSTES", 1, BLACK)
    WIN.blit(NEXT_DRAW, (1470, 730))


def BTN_LAYOUT():
    global KALENDER, TELEFON_BUCH, ERGEBNISSE, RANDOMISER_LISTE
    global AKT_A1_STRICH, AKT_A2_STRICH, AKT_A3_STRICH, AKT_A4_STRICH, AKT_A5_STRICH, AKT_B1_STRICH, AKT_B2_STRICH, AKT_B3_STRICH, AKT_B4_STRICH, AKT_B5_STRICH, AKT_C1_STRICH, AKT_C2_STRICH, AKT_C3_STRICH, AKT_C4_STRICH, AKT_C5_STRICH, AKT_D1_STRICH, AKT_D2_STRICH, AKT_D3_STRICH, AKT_D4_STRICH, AKT_D5_STRICH, AKT_E1_STRICH, AKT_E2_STRICH, AKT_E3_STRICH, AKT_E4_STRICH, AKT_E5_STRICH, AKT_F1_STRICH, AKT_F2_STRICH, AKT_F3_STRICH, AKT_F4_STRICH, AKT_F5_STRICH, AKT_G1_STRICH, AKT_G2_STRICH, AKT_G3_STRICH, AKT_G4_STRICH, AKT_G5_STRICH, AKT_H1_STRICH, AKT_H2_STRICH, AKT_H3_STRICH, AKT_H4_STRICH, AKT_H5_STRICH, AKT_I1_STRICH, AKT_I2_STRICH, AKT_I3_STRICH, AKT_I4_STRICH, AKT_I5_STRICH, AKT_J1_STRICH, AKT_J2_STRICH, AKT_J3_STRICH, AKT_J4_STRICH, AKT_J5_STRICH
    global VORLES_A1_STRICH, VORLES_A2_STRICH, VORLES_A3_STRICH, VORLES_A4_STRICH, VORLES_A5_STRICH, VORLES_B1_STRICH, VORLES_B2_STRICH, VORLES_B3_STRICH, VORLES_B4_STRICH, VORLES_B5_STRICH, VORLES_C1_STRICH, VORLES_C2_STRICH, VORLES_C3_STRICH, VORLES_C4_STRICH, VORLES_C5_STRICH, VORLES_D1_STRICH, VORLES_D2_STRICH, VORLES_D3_STRICH, VORLES_D4_STRICH, VORLES_D5_STRICH


    #KALENDER
    if BUTTON(1420, 250, 230, 100) == 1:
        if KALENDER == False and TELEFON_BUCH == False:
            KALENDER = True
        else:
            KALENDER = KALENDER

    # TELEFON_BUCH
    if BUTTON(1420, 400, 230, 100) == 1:
        if TELEFON_BUCH == False and KALENDER == False:
            TELEFON_BUCH = True
        else:
            TELEFON_BUCH = TELEFON_BUCH

    if BUTTON(790, 930, 200, 50) == 1:
        if TELEFON_BUCH == True or KALENDER == True:
            KALENDER = False
            TELEFON_BUCH = False
        else:
            TELEFON_BUCH = TELEFON_BUCH
            KALENDER = KALENDER
    # NEXT_BUTTON
    if BUTTON(1420, 700, 230, 100) == 1:
        if TELEFON_BUCH == False and KALENDER == False:
            STREICHFELD_AUSWERTEN()  # aktuelles Brett bewerten, bevor es ersetzt wird
            AKT_A1_STRICH = False
            AKT_A2_STRICH = False
            AKT_A3_STRICH = False
            AKT_A4_STRICH = False
            AKT_A5_STRICH = False

            AKT_B1_STRICH = False
            AKT_B2_STRICH = False
            AKT_B3_STRICH = False
            AKT_B4_STRICH = False
            AKT_B5_STRICH = False

            AKT_C1_STRICH = False
            AKT_C2_STRICH = False
            AKT_C3_STRICH = False
            AKT_C4_STRICH = False
            AKT_C5_STRICH = False

            AKT_D1_STRICH = False
            AKT_D2_STRICH = False
            AKT_D3_STRICH = False
            AKT_D4_STRICH = False
            AKT_D5_STRICH = False

            AKT_E1_STRICH = False
            AKT_E2_STRICH = False
            AKT_E3_STRICH = False
            AKT_E4_STRICH = False
            AKT_E5_STRICH = False

            AKT_F1_STRICH = False
            AKT_F2_STRICH = False
            AKT_F3_STRICH = False
            AKT_F4_STRICH = False
            AKT_F5_STRICH = False

            AKT_G1_STRICH = False
            AKT_G2_STRICH = False
            AKT_G3_STRICH = False
            AKT_G4_STRICH = False
            AKT_G5_STRICH = False

            AKT_H1_STRICH = False
            AKT_H2_STRICH = False
            AKT_H3_STRICH = False
            AKT_H4_STRICH = False
            AKT_H5_STRICH = False

            AKT_I1_STRICH = False
            AKT_I2_STRICH = False
            AKT_I3_STRICH = False
            AKT_I4_STRICH = False
            AKT_I5_STRICH = False

            AKT_J1_STRICH = False
            AKT_J2_STRICH = False
            AKT_J3_STRICH = False
            AKT_J4_STRICH = False
            AKT_J5_STRICH = False
            AUSWAHLFELD_ZAHLEN()

            if VORLES_A1_STRICH == True and VORLES_A2_STRICH == True and VORLES_A3_STRICH == True and VORLES_A4_STRICH == True and VORLES_A5_STRICH == True and VORLES_B1_STRICH == True and VORLES_B2_STRICH == True and VORLES_B3_STRICH == True and VORLES_B4_STRICH == True and VORLES_B5_STRICH == True and VORLES_C1_STRICH == True and VORLES_C2_STRICH == True and VORLES_C3_STRICH == True and VORLES_C4_STRICH == True and VORLES_C5_STRICH == True and VORLES_D1_STRICH == True and VORLES_D2_STRICH == True and VORLES_D3_STRICH == True and VORLES_D4_STRICH == True and VORLES_D5_STRICH == True:
                VORLESEFRAGEN_AUSWERTEN()  # alte Fragen bewerten, bevor neue erzeugt werden
                ERGEBNISSE = []
                RANDOMISER_LISTE = []
                VORLES_A1_STRICH = False
                VORLES_A2_STRICH = False
                VORLES_A3_STRICH = False
                VORLES_A4_STRICH = False
                VORLES_A5_STRICH = False

                VORLES_B1_STRICH = False
                VORLES_B2_STRICH = False
                VORLES_B3_STRICH = False
                VORLES_B4_STRICH = False
                VORLES_B5_STRICH = False

                VORLES_C1_STRICH = False
                VORLES_C2_STRICH = False
                VORLES_C3_STRICH = False
                VORLES_C4_STRICH = False
                VORLES_C5_STRICH = False

                VORLES_D1_STRICH = False
                VORLES_D2_STRICH = False
                VORLES_D3_STRICH = False
                VORLES_D4_STRICH = False
                VORLES_D5_STRICH = False

                VORLESEFRAGEN_RANDOMISER()
                TIMESTAMP_GENERATOR()
                RECHENAUFGABEN()
                TEL_AUFGABEN()
                KAL_AUFGABEN()

        else:
            TELEFON_BUCH = TELEFON_BUCH
            KALENDER = KALENDER



# Hauptfenster
def draw_window():
    WIN.fill(WHITE)

    OVERLAY()
    UHR()
    VERGLEICHSFELD()
    AKTIONSFELD()
    AUSWAHLFELD_VORLESEFRAGEN()
    BTN_LAYOUT()
    KALENDER_TELEFON_BUCH_OVERLAY()
    VORLESER()
    abbrechen_zeichnen(WIN)
    pygame.display.update()


# Hauptfenster


# Ende-Bildschirm mit Auswertung (einheitliche markante Schrift wie im
# Hauptmenü; die Schriften im Testverfahren selbst bleiben unverändert)
async def ende_anzeigen():
    FONT_MARKANT = 'impact,arialblack,arial'
    ende_font_gross = pygame.font.SysFont(FONT_MARKANT, 80)
    ende_font_klein = pygame.font.SysFont(FONT_MARKANT, 32)

    pygame.mixer.music.stop()

    # Aktuellen Stand bewerten (Brett + Fragen)
    STREICHFELD_AUSWERTEN()
    VORLESEFRAGEN_AUSWERTEN()

    ergebnisse.speichern(
        "SIMKAP", DAUER_TEXT,
        SCORE_RICHTIG_GESTRICHEN + SCORE_FRAGEN_RICHTIG,
        SCORE_FALSCH_GESTRICHEN + SCORE_FRAGEN_FALSCH,
        None,
        details=(f"Verpasste Treffer: {SCORE_VERPASST}, "
                 f"Fragen richtig: {SCORE_FRAGEN_RICHTIG}/{SCORE_FRAGEN_GEFRAGT}"))

    WIN.fill(WHITE)
    zeit_text = ende_font_gross.render("Zeit abgelaufen!", 1, BLACK)
    WIN.blit(zeit_text, (WIDTH / 2 - zeit_text.get_width() / 2, 180))

    zeilen = [
        "Streichfeld:",
        f"Richtig gestrichen: {SCORE_RICHTIG_GESTRICHEN}",
        f"Falsch gestrichen: {SCORE_FALSCH_GESTRICHEN}",
        f"Verpasste Treffer: {SCORE_VERPASST}",
        "",
        "Vorlesefragen:",
        f"Gestellte Fragen: {SCORE_FRAGEN_GEFRAGT}",
        f"Richtig beantwortet: {SCORE_FRAGEN_RICHTIG}",
        f"Falsch markiert: {SCORE_FRAGEN_FALSCH}",
        "",
        "Tippe, um zum Hauptmenü zurückzukehren..."
    ]
    y = 340
    for zeile in zeilen:
        if zeile:
            draw = ende_font_klein.render(zeile, 1, BLACK)
            WIN.blit(draw, (WIDTH / 2 - draw.get_width() / 2, y))
        y += 48

    zurueck_zeichnen(WIN)
    pygame.display.update()

    waiting = True
    while waiting:
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN or ev.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        await asyncio.sleep(0)


# Hauptcode
async def run(win, dauer_sekunden=None, tempo=None):
    # tempo wird von SIMKAP nicht genutzt (keine Geschwindigkeitsstufen,
    # wie auch in der PC-Version) – Parameter nur der einheitlichen
    # Aufrufschnittstelle wegen vorhanden.
    global WIN, Gameloop, KLICK, Delay
    WIN = win

    if dauer_sekunden is not None:
        set_dauer(dauer_sekunden)

    run_flag = True
    while run_flag:

        clock.tick(FPS)

        KLICK = (0, 0)

        for event in pygame.event.get():
            if ist_abbruch_event(event):
                await ende_anzeigen()
                return

            if event.type == pygame.MOUSEBUTTONDOWN and Delay == 10:
                KLICK = pygame.mouse.get_pos()
                Delay = 0

        if Delay < 10:
            Delay = Delay + 1

        if Gameloop == 60:
            Gameloop = 0
        else:
            Gameloop = Gameloop + 1

        # Übungsdauer erreicht?
        if GESAMTZEIT >= DAUER_SEKUNDEN:
            await ende_anzeigen()
            return

        draw_window()
        await asyncio.sleep(0)