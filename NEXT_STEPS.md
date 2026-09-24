
# Zwischenstand Python-Modell v2

## Korrigierte Startannahmen
Die physisch installierten Leistungen wurden nicht verändert. Reduziert wurden
nur Betriebs-/Lastfaktoren und Gleichzeitigkeiten.

Wesentliche Änderungen:
- Gastronomie: Standard-Gleichzeitigkeit 0,45 statt 0,70
- Kombidämpfer: Lastfaktor 0,30
- Induktion: 0,30
- Spülmaschine: 0,35
- Rührtechnik: 0,20
- Kühlung Lebensmittel: 0,25
- Tiefkühlung: 0,32
- Warmhaltetechnik: ca. 0,35–0,40
- Wellness moderat reduziert
- Kirchberghütte: Gleichzeitigkeitsfaktor 0,45
- Ladestation: 8 kWh je Ladevorgang statt 20 kWh
- Zeitumstellung: alle 35.040 Messintervalle bleiben erhalten

## Ergebnis v2
Messung Netzbezug:
- ca. 252,5 MWh/a
- Peak 75,9 kW

Modell v2:
- Bruttoverbrauch ca. 305,3 MWh/a
- modellierter Netzbezug ca. 284,3 MWh/a
- Peak ca. 85,4 kW

Damit liegt der Jahres-Netzbezug des Modells nur noch ca. 12,6 % über der Messung.

## Verbrauchergruppen v2
- Gastronomie: ca. 79,3 MWh/a
- Wellness: ca. 49,9 MWh/a
- Chalets: ca. 46,1 MWh/a
- Haustechnik: ca. 37,7 MWh/a
- Wäscherei: ca. 28,2 MWh/a
- Ladestation: ca. 22,5 MWh/a
- Zimmer: ca. 20,5 MWh/a
- Kirchberghütte: ca. 12,2 MWh/a

## Nächste fachliche Schritte
Weitere Reduktionen sollten nicht pauschal erfolgen. Als nächstes:
1. reale Außentemperatur einlesen,
2. PV-Profil über PVGIS oder Messwerte ersetzen,
3. Kühlleistungen der Gastronomie klären (elektrisch vs. thermisch),
4. reale Ladedaten prüfen,
5. Betriebszyklen von Sauna, Wäscherei und Gastro weiter schärfen.
