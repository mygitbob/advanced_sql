"""
Erzeugt die Beispieldatenbank shop_oltp.db der fiktiven Firma
"Nordlicht Versand GmbH" (Onlinehandel für Büro- und Technikbedarf).

Aufruf:  python build_db.py
Die Datei shop_oltp.db wird im selben Ordner neu erzeugt.
Die Daten sind zufällig, aber reproduzierbar (fester Startwert).
"""
import os
import random
import sqlite3
from datetime import date, timedelta

ORDNER = os.path.dirname(os.path.abspath(__file__))
DB_PFAD = os.path.join(ORDNER, "shop_oltp.db")

rnd = random.Random(42)

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE region (
    region_id   INTEGER PRIMARY KEY,
    name        TEXT NOT NULL
);

CREATE TABLE ort (
    ort_id      INTEGER PRIMARY KEY,
    plz         TEXT NOT NULL,
    name        TEXT NOT NULL,
    region_id   INTEGER NOT NULL REFERENCES region(region_id)
);

CREATE TABLE kunde (
    kunde_id        INTEGER PRIMARY KEY,
    vorname         TEXT NOT NULL,
    nachname        TEXT NOT NULL,
    email           TEXT,
    telefon         TEXT,
    ort_id          INTEGER NOT NULL REFERENCES ort(ort_id),
    registriert_am  TEXT NOT NULL
);

CREATE TABLE kategorie (
    kategorie_id    INTEGER PRIMARY KEY,
    name            TEXT NOT NULL
);

CREATE TABLE artikel (
    artikel_id      INTEGER PRIMARY KEY,
    bezeichnung     TEXT NOT NULL,
    kategorie_id    INTEGER REFERENCES kategorie(kategorie_id),
    listenpreis     REAL NOT NULL
);

CREATE TABLE mitarbeiter (
    mitarbeiter_id  INTEGER PRIMARY KEY,
    vorname         TEXT NOT NULL,
    nachname        TEXT NOT NULL,
    abteilung       TEXT NOT NULL,
    vorgesetzter_id INTEGER REFERENCES mitarbeiter(mitarbeiter_id)
);

CREATE TABLE bestellung (
    bestellung_id   INTEGER PRIMARY KEY,
    kunde_id        INTEGER NOT NULL REFERENCES kunde(kunde_id),
    mitarbeiter_id  INTEGER REFERENCES mitarbeiter(mitarbeiter_id),
    bestelldatum    TEXT NOT NULL,
    lieferdatum     TEXT,
    status          TEXT NOT NULL
);

CREATE TABLE bestellposition (
    bestellung_id   INTEGER NOT NULL REFERENCES bestellung(bestellung_id),
    position_nr     INTEGER NOT NULL,
    artikel_id      INTEGER NOT NULL REFERENCES artikel(artikel_id),
    menge           INTEGER NOT NULL,
    einzelpreis     REAL NOT NULL,
    rabatt          REAL,
    PRIMARY KEY (bestellung_id, position_nr)
);
"""

REGIONEN = [(1, "Nord"), (2, "Ost"), (3, "Süd"), (4, "West")]

ORTE = [
    (1, "20095", "Hamburg", 1), (2, "28195", "Bremen", 1), (3, "24103", "Kiel", 1),
    (4, "10115", "Berlin", 2), (5, "01067", "Dresden", 2), (6, "04109", "Leipzig", 2),
    (7, "80331", "München", 3), (8, "70173", "Stuttgart", 3), (9, "90402", "Nürnberg", 3),
    (10, "50667", "Köln", 4), (11, "40213", "Düsseldorf", 4), (12, "44135", "Dortmund", 4),
]

KATEGORIEN = [
    (1, "Notebooks"), (2, "Monitore"), (3, "Zubehör"),
    (4, "Bürobedarf"), (5, "Möbel"), (6, "Software"),
]

ARTIKEL = [
    (1, "Notebook ProBook 14", 1, 899.00), (2, "Notebook Air 13", 1, 1199.00),
    (3, "Notebook Basic 15", 1, 549.00), (4, "Monitor 24 Zoll", 2, 159.00),
    (5, "Monitor 27 Zoll", 2, 249.00), (6, "Monitor 32 Zoll 4K", 2, 429.00),
    (7, "Maus kabellos", 3, 24.90), (8, "Tastatur ergonomisch", 3, 69.00),
    (9, "Headset USB", 3, 49.00), (10, "Dockingstation USB-C", 3, 179.00),
    (11, "Webcam HD", 3, 59.00), (12, "Kopierpapier A4 (500 Bl.)", 4, 5.49),
    (13, "Kugelschreiber (10 Stk.)", 4, 3.99), (14, "Ordner breit", 4, 2.79),
    (15, "Haftnotizen (12 Blöcke)", 4, 7.49), (16, "Bürostuhl Comfort", 5, 289.00),
    (17, "Schreibtisch höhenverstellbar", 5, 549.00), (18, "Rollcontainer", 5, 179.00),
    (19, "Office-Paket Jahreslizenz", 6, 99.00), (20, "Antivirus 3 Geräte", 6, 39.90),
    (21, "Projektsoftware Lizenz", 6, 249.00),
    # nie verkauft (für NOT EXISTS / LEFT JOIN-Übungen)
    (22, "Monitorarm doppelt", 3, 89.00), (23, "Whiteboard 120x90", 5, 119.00),
    # ohne Kategorie (für NULL- und LEFT JOIN-Übungen)
    (24, "Restposten Kabelset", None, 9.99),
]

MITARBEITER = [
    (1, "Sabine", "Krüger", "Geschäftsführung", None),
    (2, "Thomas", "Wolf", "Vertrieb", 1),
    (3, "Aylin", "Demir", "Vertrieb", 2),
    (4, "Jonas", "Becker", "Vertrieb", 2),
    (5, "Lea", "Hoffmann", "Kundenservice", 1),
    (6, "Marco", "Schulz", "Kundenservice", 5),
]

VORNAMEN = ["Anna", "Ben", "Clara", "David", "Elif", "Felix", "Greta", "Hannes",
            "Ida", "Jan", "Katrin", "Lukas", "Mia", "Noah", "Olga", "Paul",
            "Rana", "Simon", "Tina", "Uwe"]
NACHNAMEN = ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer",
             "Wagner", "Becker", "Schäfer", "Koch", "Richter", "Klein",
             "Neumann", "Schwarz", "Zimmermann", "Braun", "Yilmaz", "Kowalski"]


def zufallsdatum(von: date, bis: date) -> date:
    return von + timedelta(days=rnd.randint(0, (bis - von).days))


def kunden_erzeugen(anzahl=40):
    kunden = []
    for kid in range(1, anzahl + 1):
        vn, nn = rnd.choice(VORNAMEN), rnd.choice(NACHNAMEN)
        email = f"{vn.lower()}.{nn.lower()}{kid}@example.org"
        email = email.replace("ü", "ue").replace("ä", "ae").replace("ö", "oe")
        if kid % 13 == 0:
            email = None                              # fehlende E-Mail
        telefon = None if kid % 3 == 0 else f"0{rnd.randint(150, 179)} {rnd.randint(1000000, 9999999)}"
        ort_id = rnd.randint(1, len(ORTE))
        reg = zufallsdatum(date(2022, 1, 1), date(2024, 6, 30)).isoformat()
        kunden.append((kid, vn, nn, email, telefon, ort_id, reg))
    return kunden


def bestellungen_erzeugen(kunden, anzahl=320):
    # Kunden 39 und 40 bestellen nie (für NOT EXISTS / LEFT JOIN-Übungen)
    aktive = [k[0] for k in kunden if k[0] not in (39, 40)]
    verkaufbar = [a for a in ARTIKEL if a[0] not in (22, 23)]
    bestellungen, positionen = [], []
    for bid in range(1, anzahl + 1):
        kid = rnd.choice(aktive)
        ma = rnd.choice([3, 4, 3, 4, 6, None])        # gelegentlich ohne Bearbeiter
        bdat = zufallsdatum(date(2024, 1, 1), date(2025, 12, 31))
        status = rnd.choices(["geliefert", "versendet", "offen", "storniert"],
                             weights=[80, 8, 6, 6])[0]
        if bdat > date(2025, 12, 20) and status == "geliefert":
            status = "versendet"
        ldat = (bdat + timedelta(days=rnd.randint(1, 6))).isoformat() \
            if status == "geliefert" else None
        bestellungen.append((bid, kid, ma, bdat.isoformat(), ldat, status))

        for pos in range(1, rnd.choice([1, 1, 2, 2, 3, 4]) + 1):
            art = rnd.choice(verkaufbar)
            menge = rnd.choice([1, 1, 1, 2, 3]) if art[3] > 50 else rnd.choice([1, 2, 5, 10, 20])
            rabatt = rnd.choice([None, None, None, 0.05, 0.10]) if art[3] > 100 else None
            positionen.append((bid, pos, art[0], menge, art[3], rabatt))
    return bestellungen, positionen


def main():
    if os.path.exists(DB_PFAD):
        os.remove(DB_PFAD)
    con = sqlite3.connect(DB_PFAD)
    con.executescript(SCHEMA)

    kunden = kunden_erzeugen()
    bestellungen, positionen = bestellungen_erzeugen(kunden)

    con.executemany("INSERT INTO region VALUES (?,?)", REGIONEN)
    con.executemany("INSERT INTO ort VALUES (?,?,?,?)", ORTE)
    con.executemany("INSERT INTO kunde VALUES (?,?,?,?,?,?,?)", kunden)
    con.executemany("INSERT INTO kategorie VALUES (?,?)", KATEGORIEN)
    con.executemany("INSERT INTO artikel VALUES (?,?,?,?)", ARTIKEL)
    con.executemany("INSERT INTO mitarbeiter VALUES (?,?,?,?,?)", MITARBEITER)
    con.executemany("INSERT INTO bestellung VALUES (?,?,?,?,?,?)", bestellungen)
    con.executemany("INSERT INTO bestellposition VALUES (?,?,?,?,?,?)", positionen)
    con.commit()

    for t in ["region", "ort", "kunde", "kategorie", "artikel",
              "mitarbeiter", "bestellung", "bestellposition"]:
        n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"{t:<16} {n:>5} Zeilen")
    con.close()
    print(f"\nDatenbank erzeugt: {DB_PFAD}")


if __name__ == "__main__":
    main()
