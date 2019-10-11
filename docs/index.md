---
layout: default
title: Starkniederschlag in Berlin
---

# Übersicht

Diese Seite stellt ausgewählte Analysen von Starkniederschlagereignissen im Stadtgebiet Berlins dar.
Zu diesem Zweck werden Radardaten (DX, RW) des Deutschen Wetterdienstes (DWD)
sowie Messungen mit Regenschreibern (BWB, DWD) genutzt. Die Verarbeitung der Daten erfolgt
mit der Softwarebibliothek [wradlib](https://wradlib.org).

### Ereignisse

Die folgende Abbildung stellt die kumulative Niederschlagshöhe an den Niederschlagsschreibern
der BWB für sechs Ereignisse im Sommer 2019 dar.

![overview](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/events_gauges.png "BWB-Schreiber")

### Produkte

Für jede Analyse werden vier Produktvarianten untersucht:

**DX**: Niederschlagsschätzung aus "rohen" Reflektivitätsmessungen des Radarstandorts Prötzel (polares DX-Produkt des DWD).
Die zeitliche Auflösung beträgt 5 Minuten. Die Umrechnung von Reflektivität in Niederschlagsintensität
erfolgt nach [Marshall und Palmer](https://docs.wradlib.org/en/stable/generated/wradlib.zr.r_to_z.html#wradlib.zr.r_to_z).

**DX korrigiert**: Bei intensiven Niederschlägen wird das Radarsignal entlang des Ausbreitungspfades gedämpft.
Dies kann zu einer Unterschätzung des Niederschlags führen. Daher wird diese Dämpfung zunächst korrigiert (nach [Jacobi & Heistermann 2016](https://www.tandfonline.com/doi/full/10.1080/19475705.2016.1155080)); ansonsten wie `DX`.

**RW**: Beim [RW-Produkt](https://www.dwd.de/DE/leistungen/radolan/produktuebersicht/radolan_produktuebersicht_pdf.pdf?__blob=publicationFile&v=7)
des DWD handelt es sich um ein deutschlandweites Komposit mit einer zeitlichen
Auflösung von 60 Minuten. Die auf einem 1x1 km Gitter kompositierten Daten werden
auf Grundlage von Niederschlagsschreibern des DWD korrigiert ("angeeicht").

**Interpolation**: Zu Vergleichszwecken werden die Beobachtungen der Niederschlagsschreiber der BWB
im Raum interpoliert (Inverse Distance Weighting). Entsprechend beträgt die zeitliche Auflösung
ebenfalls 5 Minuten.

### Räumliche Konfiguration

Die folgende Karte stellt die Lage des DWD C-Band Radars in Prötzel (Brandenburg) sowie
die Positionen der Niederschlagsschreiber der BWB und des DWD im Stadtgebiet Berlin und Umgebung dar.

![setup](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/setup.png "Uebersichtskarte")

(click [here](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/setup.png) to enlarge)

### Verifikation
Zur Überprüfung der Produkte werden die geschätzten Ereignissummen mit den Beobachtungen der Niederschlagsschreiber
verglichen. Ferner erfolgt eine Darstellung der kumulierten Niederschlagssummen in einer zeitlichen Auflösung von
5 Minuten. In dieser Darstellung lassen sich auch defekte Niederschlagsschreiber identifizieren, die mutmaßlich von Staueffekten
betroffen sind (verzögerte Reaktion). Ein Vegetationseinfluss lässt sich auf diese Weise nicht zuverlässig feststellen.

Die radargestützte Niederschlagsschätzung an einem Regenschreiberstandort wird ermittelt, indem in einer Nachbarschaft
von 1,5 Kilometern jenes Radarbin ermittelt wird, dessen Ereignissumme dem Niederschlagsschreiber am Nächsten kommt. Dieses
Verfahren trägt der Unsicherheit in der räumlichen Verortung der radargestützten Niederschlagsschätzung am Boden Rechnung
(u.a. durch Winddrifteffekte, Öffnungswinkel des Radars, Refraktionsindex der Atmosphäre usw.).

Das Produkt `Ìnterpolation` wird mittels n-facher Kreuzvalidierung geprüft (X-Valid.).

# 2. August 2019

#### 13:00-16:00, UTC

### Ereignissummen (Kartendarstellung)
![rain map](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-08-02.png "Rainmap 2019-08-02 13:00-16:00 UTC")

(click [here](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-08-02.png) to enlarge)

#### Ereignissummen (Verifikation)
![verfication](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/scatter_2019-08-02.png "Verification 2019-08-02 13:00-16:00 UTC")

#### Zeitreihen
![timeseries](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/cumsumproducts_2019-08-02.png "Timeseries 2019-08-02 13:00-16:00 UTC")


# 31. Juli 2019

### 16:00-20:00, UTC

#### Ereignissummen (Kartendarstellung)
![rain map](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-07-31.png "Rainmap 2019-07-31 16:00-20:00 UTC")

(click [here](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-07-31.png) to enlarge)

#### Ereignissummen (Verifikation)
![verfication](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/scatter_2019-07-31.png "Verification 2019-07-31 16:00-20:00 UTC")

#### Zeitreihen
![timeseries](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/cumsumproducts_2019-07-31.png "Timeseries 2019-07-31 16:00-20:00 UTC")


# 29. Juli 2019

### 14:00-17:00, UTC

#### Ereignissummen (Kartendarstellung)
![rain map](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-07-29.png "Rainmap 2019-07-29 14:00-17:00 UTC")

(click [here](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-07-29.png) to enlarge)

#### Ereignissummen (Verifikation)
![verfication](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/scatter_2019-07-29.png "Verification 2019-07-29 14:00-17:00 UTC")

#### Zeitreihen
![timeseries](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/cumsumproducts_2019-07-29.png "Timeseries 2019-07-29 14:00-17:00 UTC")



# 20. Juli 2019

### 20:00-23:00, UTC

#### Ereignissummen (Kartendarstellung)
![rain map](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-07-20.png "Rainmap 2019-07-20 20:00-23:00 UTC")

(click [here](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-07-20.png) to enlarge)

#### Ereignissummen (Verifikation)
![verfication](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/scatter_2019-07-20.png "Verification 2019-07-20 20:00-23:00 UTC")

#### Zeitreihen
![timeseries](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/cumsumproducts_2019-07-20.png "Timeseries 2019-07-20 20:00-23:00 UTC")


# 11. Juni 2019

### 19:00-2:00, UTC

#### Ereignissummen (Kartendarstellung)
![rain map](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-06-11.png "Rainmap 2019-06-11 19:00-2:00 UTC")

(click [here](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-06-11.png) to enlarge)

#### Ereignissummen (Verifikation)
![verfication](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/scatter_2019-06-11.png "Verification 2019-06-11 19:00-2:00 UTC")

#### Zeitreihen
![timeseries](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/cumsumproducts_2019-06-11.png "Timeseries 2019-06-11 19:00-2:00 UTC")


# 6. Juni 2019

### 12:00-21:00, UTC

#### Ereignissummen (Kartendarstellung)
![rain map](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap_2019-06-06.png "Rainmap 2019-06-06 12:00-21:00 UTC")

(click [here](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/rainmap2019-06-06.png) to enlarge)

#### Ereignissummen (Verifikation)
![verfication](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/scatter_2019-06-06.png "Verification 2019-06-06 12:00-21:00 UTC")

#### Zeitreihen
![timeseries](https://github.com/heistermann/rain-in-berlin/raw/master/docs/events/cumsumproducts_2019-06-06.png "Timeseries 2019-06-06 12:00-21:00 UTC")
