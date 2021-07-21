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
- Wolken generieren (on/off)
- Zufällige Höhe der Häuser (on/off)

## Repository Struktur
### Environment
Das Addon muss aus der environment.py gestartet werden: 
1. Baum Addon aktivieren in Blender: Edit -> Preferences -> Addons -> checkbox Sapling Tree Gen aktivieren
2. Öffnen des environment.py Files innerhalb des Blender-Scripting-Reiters
3. Absoluten Pfad für Straßen Textur "street.png" aus dem Verzeichnis /materials in Zeile 199 zu filepath einfügen (Relativer Pfad haben wir leider nicht implementieren können :( )
4. Ausführen des Codes
5. Environment Operator unter Create öffnen und ggf. Werte im UI ändern
6. Auf 'OK' klicken

### Prototypen
Die meisten Objekte sind separat in files untergliedert und liegen im /prototypes Verzeichnis. 

### Texturen
Texturen sind Bilddateien im .jpg- oder .png-Format und liegen im /materials Verzeichnis.

