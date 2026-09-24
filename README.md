
# Adaptives Energiesystemmodell – MVP v1

## Zweck
Erste lauffähige Python-Version des elektrischen Energiesystemmodells.

Die Version:
1. liest den gemessenen 15-Minuten-Netzbezug 2025 ein,
2. liest die aktuelle Excel-Modellkonfiguration ein,
3. erzeugt einen synthetischen 20-kWp-PV-Lastgang,
4. berechnet Verbraucher- und Gruppenlastgänge,
5. aggregiert diese zum modellierten Bruttoverbrauch,
6. zieht PV ab und bildet einen modellierten Netzbezug,
7. exportiert Zeitreihen, KPIs und Diagramme.

## Methodik
Jeder Verbraucher folgt grundsätzlich:

P_i(t) = n_i · P_N,i · f_B,i(t) · f_T,i(t) · f_L,i · g_i

Verwendete generische Lastmodelle:
- FIXED
- LINEAR
- STEP
- EVENT
- MEASURED (Schnittstelle vorbereitet)

Die Tagesformen sind bewusst als kleine Standardprofil-Bibliothek aufgebaut.
Das folgt der Idee standardisierter Lastprofile: wenige wiederverwendbare
Profiltypen + betriebliche Treiber statt gerätespezifischer Sonderfunktionen.

## Wichtige Grenzen von v1
Noch keine Kalibrierung. Einige Werte sind explizite Fallback-Annahmen:
- Referenzzimmer
- Chalet-Allgemeinverbrauch
- elektrische Aufnahme der Chalet-Splitgeräte
- Grundlast Kirchberghütte
- Außentemperatur ist noch synthetisch
- PV ist synthetisch und auf 20 kWp / 21.000 kWh/a normiert
- bei gemessenem Netzbezug = 0 ist der reale PV-Eigenverbrauch nicht rekonstruierbar

Alle provisorischen Werte stehen zentral in `src/assumptions.py`.

## Start
```bash
pip install -r requirements.txt
python main.py
```

## Ergebnisse
Im Ordner `results/`:
- `timeseries_15min.csv`
- `kpis.csv`
- `group_energy_kwh.csv`
- `01_beispielwoche_januar.png`
- `02_gruppen_beispieltag.png`
- `03_jahresdauerlinie.png`

## Nächste technische Schritte
- echte Außentemperatur 2025 einlesen
- PV-Profil später durch Messung/PVGIS ersetzen
- fehlende elektrische Anschlusswerte durch Typenschilder ersetzen
- Profilparameter aus realem Lastgang plausibilisieren
- Erzeuger, Speicher und Lastmanagement als Szenarien ergänzen
