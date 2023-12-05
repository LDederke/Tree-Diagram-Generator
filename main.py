# -- coding: UTF-8 -*-

import geopandas as gpd
from shapely.geometry import LineString, Polygon
import os



#Projektname an Variable übergeben

#Arbeits ordner erstellen
Home = r'C:\Users\Stefan\Documents\Temp'



Wertetabelle = r'C:\Users\Stefan\Documents\Decissiontree\Eingabemappe.txt'
Datentabelle = r'C:\Users\Stefan\Documents\Decissiontree\Datentabelle.txt'

#Variablen:
Kastenhoehe = 2
Kastenbreite = 4
Abstandhorizontal = 2
Abstandvertikal = 20
    #Rasterhorizontal = Kastenbreite + Abstandhorizontal
    #Rastervertikal = Kastenhöhe + Abstandvertikal
    #Fixpunkt = X=0; Y=0
    #DockUnten = X=Fixpunkt; Y= Fixpunkt + (Kastenbreite/2)
    #Dockoben = X=Fixpunkt + Kastenhöhe; Y= Fixpunkt + (Kastenbreit/2)

# Alle möglichen Parameter und Werte
ListeParameterWerte = []

with open(Wertetabelle) as f:   #Parameter einlesen aus Datei
    for line in f:
        inner_list = [elt.strip() for elt in line.split('\t')]
        inner_list = [feld for feld in inner_list if feld != '']
        ListeParameterWerte.append(inner_list)

AnzahlParameter = len(ListeParameterWerte) #Anzahl der Parameter ermiteln

ListeParameter = [] #Liste Aller Parameter mit [Nummer, Name, Anzahl der Werte]
m=0
for i in range(1, AnzahlParameter+1):
    j = 'Parameter' + str(i)
    k = ListeParameterWerte[m][0]
    l = len(ListeParameterWerte[m])-1
    ListeParameter.append([j,k,l])
    m += 1

ListeWerte = [] #Liste der Werte
m=0
for i in range(1, AnzahlParameter+1):
    j = ListeParameterWerte[m][1:ListeParameter[m][2]+1]
    ListeWerte.append(j)
    m += 1

AnzahlKlassen = 1 #Anzahl der Klassen
m = 0
for i in ListeParameter:
    j = ListeParameter[m][2]
    AnzahlKlassen= AnzahlKlassen*j
    m += 1

ListeWirklichAllerKlassen =[] #Alle Klassen ermiteln

for i in range(0, AnzahlKlassen):
    j = []
    ListeWirklichAllerKlassen.append(j)

m = 0
NrParameter = 0
NrWert = 0
AnzahlKlassenDato = 1
for i in range(0, AnzahlParameter):                        #Durchlauf der Parameterebenen
    AnzahlWerte = ListeParameter[NrParameter][2]
    AnzahlKlassenDato *= AnzahlWerte
    for j in range(0, AnzahlKlassenDato):                         #Durchlauf der Werte
        for k in range(0, int(AnzahlKlassen/AnzahlKlassenDato)): #Durchlauf der Wertwiederholung
            l = ListeWirklichAllerKlassen[m]                      #Definition der Liste in die geschrieben werden soll
            l.append(ListeWerte[NrParameter][NrWert])             #Hizufügen des Werts zur Liste
            m += 1
        NrWert += 1
        if NrWert == AnzahlWerte:                                   #Wenn der Wert die MxiZahl erreicht hat wird er Resetet
            NrWert = 0
        else:
            pass
    m = 0
    NrParameter +=1

#Geometrien schreiben
Gesamtbreite = (Kastenbreite + Abstandhorizontal) * AnzahlKlassen
Gesamthoehe = (Kastenhoehe + Abstandvertikal) * AnzahlParameter
feature_info = []


m = 1 #Anzahl der Blöcke
for i in range(0, AnzahlParameter):
    b = Gesamthoehe - (i * (Kastenhoehe + Abstandvertikal))
    n = 1                                               # Nummer des zu schreibenden Blocks
    for o in range(0, m):
        a = Gesamtbreite / m                            #Breite eines Blocks
        k = ListeParameter[i][2]                        #aktuelle Anzahl der Klassen
        c = Gesamtbreite / m / k                        #Breite einer Klasse
        for j in range(0, k):
            x = a*n + c*(j+1) - c/2 - a                 #X/Y-Koordinate untere Kastenmitte
            y = b
            feature_info.append([[x - Kastenbreite/2, y], [x + Kastenbreite/2, y], [x + Kastenbreite/2, y + Kastenhoehe], [x - Kastenbreite/2, y + Kastenhoehe]])
        n += 1
    m = m*ListeParameter[i][2]

# A list that will hold each of the Polyline objects
features = []

for feature in feature_info:
    # Create a Polyline object based on the array of points
    # Append to the list of Polyline objects
    features.append(
        arcpy.Polygon(
            arcpy.Array([arcpy.Point(*coords) for coords in feature])))

# Persist a copy of the Polyline objects using CopyFeatures
arcpy.CopyFeatures_management(features, os.path.join(Home, 'Klassen_P.shp'))



print(ListeParameterWerte)
print(AnzahlParameter)
print(ListeParameter)
print(ListeWerte)
print(AnzahlKlassen)
print(ListeWirklichAllerKlassen)
print(Gesamtbreite)
print(feature_info)
