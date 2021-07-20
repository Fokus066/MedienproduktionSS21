# MedienproduktionSS21
Thema: Straße mit Häußer und Natur generieren

## Abstract
Das Blender-Python Addon generiert eine ländliche Nachbarschaft mit verschiedenen Objekten wie Bäumen, Steinen, Wiesen und vielen mehreren. 
Der User hat die Möglichkeit mithilfe eines UI Details in der Umgebung zu verändern:
- Tageszeit
- Szenengröße
- Baumart
- Anzahl der Bäume
- Anzahl der Steine
- Maximale Astlänge
- Blattform
- Darstellung der Blätter (on/off)
- Objekte innerhalb einer Collection (on/off)

## Repository Struktur
### Environment
Das Addon muss aus der environment.py gestartet werden: 
1. Öffnen des Files innerhalb des Blender-Scripting-Reiters
2. Ausführen des Codes
3. Environment Operator unter Create öffnen und ggf. Werte im UI ändern
4. Auf 'OK' klicken

### Prototypen
Die meisten Objekte sind separat in files untergliedert und liegen im /prototypes Verzeichnis. 

### Texturen
Texturen sind Bilddateien im .jpg- oder .png-Format und liegen im /materials Verzeichnis.

