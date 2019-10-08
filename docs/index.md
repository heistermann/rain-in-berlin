---
layout: default
title: Starkniederschlag in Berlin
---

# Übersicht

Diese Seite stellt ausgewählte Analysen von Starkniederschlagereignissen im Stadtgebiet Berlins dar.
Zu diesem Zweck werden Radardaten (DX, RW) des Deutschen Wetterdienstes (DWD)
sowie Messungen mit Regenschreibern der Berliner Wasserbetriebe genutzt. Die
Verarbeitung der Daten erfolgt mit der Softwarebibliothek [wradlib](https://wradlib.org).

### Produkte

Für jede Analyse werden vier Produktvarianten untersucht:

**DX**: Niederschlagsschätzung aus "rohen" Reflektivitätsmessungen des Radarstandorts Prötzel (polares DX-Produkt des DWD).
Die zeitliche Auflösung beträgt 5 Minuten.

**DX korrigiert**: Bei intensiven Niederschlägen wird das Radarsignal entlang des Ausbreitungspfades gedämpft.
Dies kann zu einer Unterschätzung des Niederschlags führen. Daher wird diese Dämpfung zunächst korrigiert (nach [Jacobi & Heistermann 2016](https://www.tandfonline.com/doi/full/10.1080/19475705.2016.1155080)).

**RW**: Bei dem RW-Produkt des DWD handelt es sich um ein deutschlandweites Komposit mit einer zeitlichen
Auflösung von 60 Minuten. Die auf einem 1x1 km Gitter kompositierten Daten werden
auf Grundlage von Niederschlagsschreibern des DWD korrigiert ("angeeicht").

**Interpolation**: Zu Vergleichszwecken werden die Beobachtungen der Niederschlagsschreiber (BWB)
im Raum interpoliert (Inverse Distance Weighting). Entsprechend beträgt die zeitliche Auflösung
ebenfalls 5 Minuten.

### Räumliche Konfiguration

![setup](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/setup.png "Uebersichtskarte")

(click [here](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/setup.png) to enlarge)

### Verifikation
Zur Überprüfung der Produkte werden die geschätzten Ereignissummen mit den Beobachtungen der Niederschlagsschreiber
verglichen. Ferner erfolgte eine Darstellung der kumulierten Niederschlagssummen in einer zeitlichen Auflösung von
5 Minuten. In dieser Darstellung lassen sich defekte Niederschlagsschreiber identifizieren, die mutmaßlich von Staueffekten
betroffen sind. Ein Vegetationseinfluss lässt sich auf diese Weise nicht unmittelbar feststellen.

# 2. August 2

### Kartendarstellung
![rain map](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-08-02.png "Rainmap 2019-08-02")

(click [here](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-08-02.png) to enlarge)

### Ereignissummen
![verfication](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/scatter_2019-08-02.png "Verification 2019-08-02")

### Zeitreihen
![timeseries](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/cumsumproducts_2019-08-02.png "Timeseries 2019-08-02")


# 31. Juli 2019

### Kartendarstellung
![rain map](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-07-31.png "Rainmap 2019-07-31")

(click [here](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-07-31.png) to enlarge)

### Ereignissummen
![verfication](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/scatter_2019-07-31.png "Verification 2019-07-31")

### Zeitreihen
![timeseries](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/cumsumproducts_2019-07-31.png "Timeseries 2019-07-31")


# 20. Juli 2019

### Kartendarstellung
![rain map](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-07-20.png "Rainmap 2019-07-20")

(click [here](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-07-20.png) to enlarge)

### Ereignissummen
![verfication](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/scatter_2019-07-20.png "Verification 2019-07-20")

### Zeitreihen
![timeseries](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/cumsumproducts_2019-07-20.png "Timeseries 2019-07-20")


# 11. Juni 2019

### Kartendarstellung
![rain map](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-06-11.png "Rainmap 2019-06-11")

(click [here](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-06-11.png) to enlarge)

### Ereignissummen
![verfication](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/scatter_2019-06-11.png "Verification 2019-06-11")

### Zeitreihen
![timeseries](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/cumsumproducts_2019-06-11.png "Timeseries 2019-06-11")


# 6. Juni 2019

### Kartendarstellung
![rain map](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-06-06.png "Rainmap 2019-06-06")

(click [here](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-06-11.png) to enlarge)

### Ereignissummen
![verfication](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/scatter_2019-06-11.png "Verification 2019-06-11")

### Zeitreihen
![timeseries](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/cumsumproducts_2019-06-11.png "Timeseries 2019-06-11")
