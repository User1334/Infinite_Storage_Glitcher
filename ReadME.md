# Infinite_Storage_Glitcher

Ein Python-basiertes Tool zur Konvertierung von Dateien in Videos und zurück. Dieses Programm nutzt GPU-Beschleunigung und bewahrt Metadaten wie Erstellungs- und Änderungsdatum der Dateien.

---

## 📜 Beschreibung

## Dieses Programm ist aktuell nur unter macOS mit AppleM1/M2 lauffähig.

`Infinite_Storage_Glitcher` ermöglicht:
- **Datei in Video konvertieren:** 
  - Dateien werden in ein Schwarz-Weiß-Video umgewandelt.
  - Die Binärdaten der Datei werden in Frames eines Videos gespeichert.
  - Metadaten wie Erstellungs- und Änderungsdatum werden im Video eingebettet.

- **Video in Datei rekonstruieren:**
  - Das Programm liest die Frames aus dem Video aus und rekonstruiert daraus die ursprüngliche Datei.
  - Metadaten werden aus dem Video extrahiert und auf die Datei angewendet.

---

## 🛠️ Abhängigkeiten

### **Systemanforderungen**
- **Python**: Version 3.10 (GPU-Unterstützung erfordert diese Version).
- **MacOS**: Mit Apple Silicon (M1/M2) für GPU-Beschleunigung.
- **FFmpeg**: Für Videoverarbeitung erforderlich.
- **Homebrew**: Paketmanager für macOS

### **Python-Bibliotheken**
Die erforderlichen Bibliotheken können mit folgendem Befehl installiert werden:

```bash
pip install numpy torch tqdm opencv-python
```
Installiere FFmpeg über Homebrew:
```bash
brew install ffmpeg
```

---

## 🚀 Installation & Ausführung
1.	Repository klonen:

```bash
git clone https://github.com/username/Datei2Videoundzurueck.git
cd Infinite_Storage_Glitcher
```
2.	Programm starten:

```bash
python3 converter.py
```

3.	Option auswählen:
  - 1: Datei in ein Video konvertieren.
  - 2: Video in eine Datei rekonstruieren.

4.	Eingabeaufforderungen folgen:
	
  - Option 1 (Datei → Video):
  - Eingabe: Pfad zur Datei.
  - Ausgabe: Pfad zum Zielvideo.
  - Option 2 (Video → Datei):
  - Eingabe: Pfad zum Video.
  - Ausgabe: Pfad zur Zieldatei.

## 📋 Beispiele

Datei in Video konvertieren:

```bash
python3 converter.py
Gib 1 oder 2 ein: 1
Gib den Pfad zur gewünschten Datei ein: /Pfad/zur/Datei.txt
Gib den Pfad zum Ausgabevideo ein (ohne .mov): /Pfad/zum/Video
```

Video in Datei rekonstruieren:

```bash
python3 converter.py
Gib 1 oder 2 ein: 2
Gib den Pfad zum Video ein: /Pfad/zum/Video.mov
Gib den Pfad zur Ausgabedatei ein: /Pfad/zur/rekonstruierten/Datei.txt
```

## ✨ Features
  - GPU-Beschleunigung: Nutzung der Metal-API auf macOS für schnelle Verarbeitung.
  - Metadaten-Speicherung: Erhalt von Erstellungs- und Änderungsdatum zwischen Datei und Video.
  - Effiziente Verarbeitung: Unterstützt große Dateien mit optimierter Speicherverwaltung.
  - Fortschrittsanzeige: Zeigt Fortschritt bei der Video- und Dateiverarbeitung.

## 🧪 Zukünftige Verbesserungen
  - Unterstützung weiterer Plattformen und GPUs.
  - Verbesserte Geschwindigkeit für die Dateirekonstruktion.
  - Hinzufügen von Tests zur Validierung der Metadatenübertragung.



