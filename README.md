# YouTube Video/Music Downloader

Ein einfaches Python-Projekt zum Herunterladen von YouTube Videos und Musik mit `yt-dlp`.

## Features

- ✅ Videos in verschiedenen Qualitäten und Formaten herunterladen
- 🎵 Nur Audio extrahieren (MP3, WAV, M4A, FLAC)
- 📋 Komplette Playlists herunterladen
- ℹ️ Video-Informationen anzeigen
- 🖥️ Interaktiver Modus und Kommandozeilen-Interface
- 📁 Automatische Ordnerstruktur für Downloads

## Installation

### 1. Repository klonen oder Dateien herunterladen

```bash
git clone <repository-url>
cd youtube-downloader
```

### 2. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 3. FFmpeg installieren (für Audio-Konvertierung)

**Windows:**
- Download von https://ffmpeg.org/download.html
- FFmpeg zur PATH-Variable hinzufügen

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

## Verwendung

### Interaktiver Modus (empfohlen für Einsteiger)

```bash
python youtube_downloader.py
```

### Kommandozeile

#### Einzelnes Video herunterladen
```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Nur Audio herunterladen
```bash
python youtube_downloader.py -a "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Playlist herunterladen
```bash
python youtube_downloader.py -p "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

#### Video-Informationen anzeigen
```bash
python youtube_downloader.py -i "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Erweiterte Optionen

```bash
# Bestimmte Qualität wählen
python youtube_downloader.py -q 720p "URL"

# Format festlegen
python youtube_downloader.py -f webm "URL"

# Output-Verzeichnis ändern
python youtube_downloader.py -o /pfad/zu/downloads "URL"

# Playlist mit maximal 10 Videos
python youtube_downloader.py -p --max 10 "PLAYLIST_URL"

# Audio-Format für Playlist
python youtube_downloader.py -p -a -f wav "PLAYLIST_URL"
```

## Kommandozeilen-Optionen

| Option | Beschreibung |
|--------|--------------|
| `-a, --audio-only` | Nur Audio herunterladen |
| `-p, --playlist` | Playlist herunterladen |
| `-q, --quality` | Qualität (best, worst, 720p, 480p, etc.) |
| `-f, --format` | Format (mp4, webm, mp3, wav, etc.) |
| `-o, --output` | Output-Verzeichnis |
| `-i, --info` | Nur Video-Informationen anzeigen |
| `--max` | Maximale Anzahl Downloads für Playlists |

## Beispiele

### Video in 720p als MP4 herunterladen
```bash
python youtube_downloader.py -q 720p -f mp4 "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Musik als MP3 herunterladen
```bash
python youtube_downloader.py -a -f mp3 "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Erste 5 Videos einer Playlist als Audio
```bash
python youtube_downloader.py -p -a --max 5 "https://www.youtube.com/playlist?list=..."
```

## Projektstruktur

```
youtube-downloader/
├── youtube_downloader.py  # Hauptprogramm
├── requirements.txt       # Python-Abhängigkeiten
├── README.md             # Diese Datei
└── downloads/            # Download-Verzeichnis (wird automatisch erstellt)
    ├── video1.mp4
    ├── audio1.mp3
    └── playlist_name/
        ├── song1.mp3
        └── song2.mp3
```

## Unterstützte Seiten

Da das Projekt `yt-dlp` verwendet, werden neben YouTube auch viele andere Video-Plattformen unterstützt:
- YouTube
- YouTube Music
- Vimeo
- Dailymotion
- SoundCloud
- und viele mehr...

## Fehlerbehebung

### "FFmpeg not found"
- Stelle sicher, dass FFmpeg installiert und in der PATH-Variable verfügbar ist
- Teste mit: `ffmpeg -version`

### "No module named 'yt_dlp'"
- Installiere die Abhängigkeiten: `pip install -r requirements.txt`

### Download-Fehler
- Überprüfe die URL
- Manche Videos sind regional gesperrt
- Private Videos können nicht heruntergeladen werden

## Rechtliche Hinweise

⚠️ **Wichtig**: Beachte die Urheberrechte und Nutzungsbedingungen der jeweiligen Plattformen. Dieses Tool ist nur für den persönlichen Gebrauch und für Inhalte gedacht, für die du die entsprechenden Rechte besitzt.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

## Beiträge

Pull Requests und Issues sind willkommen!

## Changelog

### Version 1.0.0
- Grundlegende Download-Funktionen
- Interaktiver und Kommandozeilen-Modus
- Unterstützung für Videos, Audio und Playlists