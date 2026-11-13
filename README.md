# Fortgeschrittenes SQL & Datenmodellierung – Übungsmaterial

Beispielfirma: **Nordlicht Versand GmbH** (Onlinehandel für Büro- und Technikbedarf)

## Ordner

| Ordner       | Inhalt |
|--------------|--------|
| `daten/`     | `shop_oltp.db` (SQLite-Datenbank) und `build_db.py` zum Neuerzeugen |
| `skript/`    | Skript je Lektion (Word) |
| `notebooks/` | Übungsnotebook je Lektion (Aufgaben mit leeren Zellen) |
| `loesungen/` | Lösungsnotebooks – nur für die Lehrkraft, nicht an Teilnehmende weitergeben |

## Start

1. Ordner komplett entpacken, die Ordnerstruktur nicht verändern.
2. Notebook aus `notebooks/` in Jupyter Lab, Jupyter Notebook oder VS Code öffnen.
3. Erste Codezelle ausführen. Benötigt werden nur Python 3 und `pandas`.

Datenbank kaputt oder verändert? Im Ordner `daten/` ausführen: `python build_db.py`

## Lektionen

0. Arbeitsumgebung und Auffrischung
1. Datenbankzugriff mit Python: Connection, Cursor, Prepared Statements
2. Logische Ausführungsreihenfolge
3. Unterabfragen und CTEs
4. Mengenoperationen
5. Bedingte Logik und NULL-Behandlung
6. Fensterfunktionen
7. OLTP und OLAP, Data Warehouse, Data Lake, ETL
8. Vom relationalen Schema zum Sternschema
9. Abfragen auf ein Sternschema
10. NoSQL-Datenbanken
11. Prüfungstraining
