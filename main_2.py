# -- coding: UTF-8 -*-

import geopandas as gpd
from shapely.geometry import LineString, Polygon
import os
from datetime import datetime
import pandas as pd

# Aktuelles Datum und Uhrzeit abrufen
now = datetime.now()

# Benutzer nach dem Projektnamen fragen
project_name = input("Geben Sie den Projektnamen ein: ")

# Format für Datum und Uhrzeit festlegen (z.B., YYYYMMDD_HHMMSS)
date_time_format = now.strftime("%Y%m%d_%H%M%S")

# Projektordner erstellen
folder_name = f"{date_time_format}_{project_name}"
folder_path = os.path.join(r'C:\Users\Stefan\Documents\Decissintrees', folder_name)                  

# Verwenden Sie den Dateipfad nach Bedarf
print(folder_path)

# Passe den Dateipfad entsprechend an
excel_dateipfad = r'C:\Users\Stefan\Documents\Decissiontree\Test-Daten.xlsx'

# Lese die Excel-Tabelle ein
daten = pd.read_excel(excel_dateipfad)

# Zeige die ersten Zeilen der Tabelle an
#print(daten.head())

ueberschriften_liste = daten.columns.tolist()

# Zeige die Überschriften an
print("Verfügbare Überschriften:")
for i, ueberschrift in enumerate(ueberschriften_liste):
    print(f"{i}: {ueberschrift}")

# Lass den Benutzer die Indizes der gewünschten Spalten eingeben
benutzer_eingabe = input("Geben Sie die Indizes der gewünschten Spalten in der Reihenfolge ein (getrennt durch Kommas): ")
ausgewaehlte_spalten_indizes = [int(index) for index in benutzer_eingabe.split(',')]
print(ausgewaehlte_spalten_indizes)
# Wähle nur die ausgewählten Spalten aus dem Datenrahmen aus
ausgewaehlte_daten = daten.iloc[:, ausgewaehlte_spalten_indizes]

# Zeige die ausgewählten Daten an
#print(ausgewaehlte_daten)

# Erstelle eine Liste mit vollständigen Spaltenbezeichnungen
ausgewaehlte_spalten = [ueberschriften_liste[index] for index in ausgewaehlte_spalten_indizes]
print(ausgewaehlte_spalten)

# Gruppiere den DataFrame nach den ausgewählten Spalten
grouped_data = ausgewaehlte_daten.groupby(ausgewaehlte_spalten)

# Erstelle eine Liste mit Unterlisten für jeden Wert in den ausgewählten Spalten
ergebnisse = []
for name, group in grouped_data:
    einzigartige_werte = {spalte: group[spalte].unique().tolist() for spalte in ausgewaehlte_spalten}
    ergebnisse.append(einzigartige_werte)

# Zeige die Ergebnisse an
print("\nAusgewählte Spalten und ihre einzigartigen Werte:")
for ergebnis in ergebnisse:
    print(ergebnis)