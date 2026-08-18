# =======================================
# Ergebnis-Historie für die Web-Version: speichert im Browser (localStorage),
# da eine Datei-CSV auf dem Handy nicht sinnvoll erreichbar wäre.
# =======================================
import json
from datetime import datetime

SCHLUESSEL = "wienertest_ergebnisse"


def _window():
    """Zugriff auf das Browser-window-Objekt (nur im Browser vorhanden)."""
    try:
        import platform
        return getattr(platform, "window", None)
    except Exception:
        return None


def speichern(test, einstellung, richtig, falsch, reaktionszeit_ms, details=""):
    """Hängt ein Ergebnis an die im Browser gespeicherte Liste an."""
    win = _window()
    if win is None:
        return
    try:
        jetzt = datetime.now()
        eintrag = {
            "Datum": jetzt.strftime("%d.%m.%Y"),
            "Uhrzeit": jetzt.strftime("%H:%M"),
            "Test": test,
            "Einstellung": einstellung,
            "Richtig": richtig,
            "Falsch": falsch,
            "Reaktionszeit_ms": reaktionszeit_ms if reaktionszeit_ms is not None else "",
            "Details": details,
        }
        vorhanden = win.localStorage.getItem(SCHLUESSEL)
        liste = json.loads(vorhanden) if vorhanden else []
        liste.append(eintrag)
        win.localStorage.setItem(SCHLUESSEL, json.dumps(liste))
    except Exception as e:
        print("Ergebnis konnte nicht gespeichert werden:", e)


def laden():
    """Liest alle gespeicherten Ergebnisse (älteste zuerst)."""
    win = _window()
    if win is None:
        return []
    try:
        vorhanden = win.localStorage.getItem(SCHLUESSEL)
        return json.loads(vorhanden) if vorhanden else []
    except Exception as e:
        print("Ergebnisse konnten nicht geladen werden:", e)
        return []


def loeschen():
    """Löscht die komplette Ergebnis-Historie. True = erfolgreich."""
    win = _window()
    if win is None:
        return False
    try:
        win.localStorage.removeItem(SCHLUESSEL)
        return True
    except Exception as e:
        print("Ergebnisse konnten nicht gelöscht werden:", e)
        return False
