# Kamera-Erweiterung · 27. Oktober 2026

## Verwendung

1. Portrait Studio öffnen und anmelden.
2. In der Kachel „Fotos aufnehmen“ zum Kamerabereich springen.
3. „Kamerabereich öffnen“ einschalten und die Hinweise lesen.
4. Kameranutzung bestätigen, „Kamera starten“ wählen und die Browserfreigabe erteilen.
5. Frontal, leicht nach links oder leicht nach rechts auswählen. Kopf ins Oval,
   Augen an die Linie und Kamera auf Augenhöhe. Weiches Licht von vorn verwenden.
6. Ein Foto aufnehmen; optional den Drei-Sekunden-Selbstauslöser nutzen.
7. Bis zu fünf Fotos prüfen, einzeln als JPG oder gemeinsam als ZIP herunterladen.
8. ZIP entpacken. JPG-Dateien im gewählten KI-Chat selbst hochladen, den separat
   exportierten Bildprompt ergänzen und erst dort die Bilderzeugung freigeben.

## Datenschutz und Grenzen

Die Kamera ist standardmäßig aus. Es wird kein Ton angefordert. Die neue
Kamerafunktion arbeitet vollständig im Browser: keine Fotoübertragung an Python,
Streamlit oder einen KI-Anbieter; keine eigene Speicherung im Browser dauerhaft.
Fotos werden im Arbeitsspeicher und als temporäre Blob-URLs gehalten. Eine
gespiegelte Vorschau ändert nicht die gespeicherten ungespiegelten JPG-Dateien.
Rahmen und Texte sind nur Vorschauhilfen und werden nicht in die Fotos gezeichnet.

Kamera aus: beendet die Kameraspur, behält aufgenommene Bilder für den Download.
Alle Aufnahmen löschen: entfernt diese Bilder aus der Kameraansicht, aber keine
bereits heruntergeladenen Dateien. Beim Verlassen des Tabs oder nach zehn Minuten
wird die Kamera gestoppt. Schließen des Bereichs, Abmelden, App-Updates oder
Neuladen können die Bilder verwerfen; deshalb vorher herunterladen.

Die Auflösung wird bis 1920 × 1080 angefragt, hängt aber von Gerät und Browser ab.
Längste Exportkante maximal 2560 Pixel. Kleine Kamerabilder werden nicht künstlich
vergrößert. Keine Gesichtserkennung, keine automatische Licht-/Identitätsprüfung,
keine KI-Verschönerung und keine Bilderzeugung. Nicht jeder externe KI-Dienst
unterstützt eigene Referenzfotos; dessen Datenschutz- und Nutzungsregeln gelten
beim späteren Upload separat.

## Technische Integration

Neue Dateien im Projektstamm:

- `camera_section.py`: Streamlit-Schalter und Einbettung der statischen Kameraansicht.
- `camera_ui.html`: Browserkamera, Gesichtsrahmen, Anleitung und Galerie.
- `camera_utils.js`: ZIP-Export, Dateinamen und Größenbegrenzung ohne Fremdbibliothek.

`streamlit_app.py` bindet den Bereich ein. Passwortprüfung, elf Fragen und
Exportfreigabe bleiben erhalten. Keine neuen Python-Abhängigkeiten und kein
API-Schlüssel nötig. Die Kamera benötigt HTTPS oder localhost und eine Freigabe
im Browser. Bei eingebetteten In-App-Browsern kann der Kamerazugriff eingeschränkt
sein; dann die App direkt in Chrome, Edge oder Safari öffnen. Die Rückkamera ist
eine Präferenz, keine Garantie auf jedem Gerät.

## Prüfung

- 10 Streamlit-AppTests erfolgreich: bestehender Zugang und Promptablauf,
  Kamera standardmäßig aus, lokale Einbettung und Export bei geöffnetem Bereich.
- 9 JavaScript-Tests erfolgreich: Einwilligung, erlaubte/verweigerte Kamera,
  Abbruch während Browserfreigabe, Aufnahmenlimit, Galerie, Löschen, Stoppen beim
  Tabwechsel, Freigabewiderruf sowie ZIP-CRC und Dateinamen.
- Browser-ZIP mit synthetischen Testbytes zusätzlich mit Python `zipfile` gelesen.
- Kameraansicht und wechselnde Ausrichtungshinweise lokal in Chrome geprüft,
  einschließlich Smartphone-Breite. Die echte Kamera wurde dabei nicht aktiviert.
- Ein echter Hardwaretest von Aufnahmequalität und gerätespezifischer Kameraauswahl
  bleibt vom Nutzer auf dem gewünschten Gerät auszuführen.

Für spätere automatisierte Wiederholung: `python -m pytest tests -q` und
`node --test tests/test_camera.js`. Die JavaScript-Tests simulieren Kamera und
Canvas im Speicher; sie erzeugen keine Personenfotos und nutzen keine KI.
