#!/usr/bin/env python3
"""
YouTube Video/Music Downloader
Ein einfaches Python-Projekt zum Herunterladen von YouTube Videos und Musik
"""

import os
import sys
import argparse
from pathlib import Path
import yt_dlp


class YouTubeDownloader:
    def __init__(self, output_dir="downloads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def download_video(self, url, quality="best", format_type="mp4", include_audio=True):
        """
        Lädt ein YouTube Video herunter

        Args:
            url (str): YouTube URL
            quality (str): Videoqualität ('best', 'worst', '4k', '1440p', '1080p', '720p', '480p', etc.)
            format_type (str): Ausgabeformat ('mp4', 'webm', 'mkv')
            include_audio (bool): Audio mit herunterladen (benötigt FFmpeg)
        """
        output_template = str(self.output_dir / "%(title)s.%(ext)s")

        # Format-String für verschiedene Qualitäten
        if quality == "4k":
            if include_audio:
                format_str = f'bestvideo[height<=2160][ext={format_type}]+bestaudio[ext=m4a]/bestvideo[height<=2160]+bestaudio/best'
            else:
                format_str = f'bestvideo[height<=2160][ext={format_type}]/bestvideo[height<=2160]/best'
        elif quality == "1440p":
            if include_audio:
                format_str = f'bestvideo[height<=1440][ext={format_type}]+bestaudio[ext=m4a]/bestvideo[height<=1440]+bestaudio/best'
            else:
                format_str = f'bestvideo[height<=1440][ext={format_type}]/bestvideo[height<=1440]/best'
        elif quality == "1080p":
            if include_audio:
                format_str = f'bestvideo[height<=1080][ext={format_type}]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best'
            else:
                format_str = f'bestvideo[height<=1080][ext={format_type}]/bestvideo[height<=1080]/best'
        elif quality == "720p":
            if include_audio:
                format_str = f'bestvideo[height<=720][ext={format_type}]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best'
            else:
                format_str = f'bestvideo[height<=720][ext={format_type}]/bestvideo[height<=720]/best'
        elif quality == "480p":
            if include_audio:
                format_str = f'bestvideo[height<=480][ext={format_type}]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio/best'
            else:
                format_str = f'bestvideo[height<=480][ext={format_type}]/bestvideo[height<=480]/best'
        elif quality == "best":
            if include_audio:
                # Für beste Qualität: Video und Audio separat laden und zusammenfügen
                format_str = f'bestvideo[ext={format_type}]+bestaudio[ext=m4a]/bestvideo+bestaudio/best'
            else:
                format_str = f'bestvideo[ext={format_type}]/bestvideo/best'
        else:
            format_str = f'{quality}[ext={format_type}]/best[ext={format_type}]/best'

        ydl_opts = {
            'format': format_str,
            'outtmpl': output_template,
            'noplaylist': True,
        }

        # Nur merge_output_format hinzufügen wenn Audio dabei ist
        if include_audio and ('+' in format_str):
            ydl_opts['merge_output_format'] = format_type

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Lade Video herunter: {url}")
                if not include_audio:
                    print("⚠️  Hinweis: Nur Video ohne Audio wird heruntergeladen")
                ydl.download([url])
                print("Video erfolgreich heruntergeladen!")

        except Exception as e:
            if "ffmpeg is not installed" in str(e):
                print("❌ FFmpeg ist nicht installiert!")
                print("💡 Tipp: Lade das Video ohne Audio herunter oder installiere FFmpeg.")
                retry = input("Möchtest du das Video ohne Audio herunterladen? (j/n): ").strip().lower()
                if retry == 'j':
                    self.download_video(url, quality, format_type, include_audio=False)
            else:
                print(f"Fehler beim Herunterladen des Videos: {e}")

    def download_audio(self, url, quality="best", format_type="mp3"):
        """
        Lädt nur den Ton eines YouTube Videos herunter

        Args:
            url (str): YouTube URL
            quality (str): Audioqualität ('best', 'worst')
            format_type (str): Ausgabeformat ('mp3', 'wav', 'm4a', 'flac')
        """
        output_template = str(self.output_dir / "%(title)s.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format_type,
                'preferredquality': '192' if format_type == 'mp3' else None,
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Lade Audio herunter: {url}")
                ydl.download([url])
                print("Audio erfolgreich heruntergeladen!")

        except Exception as e:
            print(f"Fehler beim Herunterladen des Audios: {e}")

    def download_playlist(self, url, audio_only=False, max_downloads=None):
        """
        Lädt eine komplette Playlist herunter

        Args:
            url (str): YouTube Playlist URL
            audio_only (bool): Nur Audio herunterladen
            max_downloads (int): Maximale Anzahl Downloads (None für alle)
        """
        output_template = str(self.output_dir / "%(playlist)s/%(title)s.%(ext)s")

        ydl_opts = {
            'outtmpl': output_template,
            'noplaylist': False,
        }

        if max_downloads:
            ydl_opts['playlistend'] = max_downloads

        if audio_only:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            ydl_opts['format'] = 'best[ext=mp4]/best'

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Lade Playlist herunter: {url}")
                ydl.download([url])
                print("Playlist erfolgreich heruntergeladen!")

        except Exception as e:
            print(f"Fehler beim Herunterladen der Playlist: {e}")

    def get_video_info(self, url):
        """
        Holt Informationen über ein YouTube Video

        Args:
            url (str): YouTube URL

        Returns:
            dict: Video Informationen
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'N/A'),
                    'duration': info.get('duration', 'N/A'),
                    'uploader': info.get('uploader', 'N/A'),
                    'view_count': info.get('view_count', 'N/A'),
                    'upload_date': info.get('upload_date', 'N/A'),
                    'description': info.get('description', 'N/A')[:200] + '...' if info.get('description') else 'N/A'
                }
        except Exception as e:
            print(f"Fehler beim Abrufen der Video-Informationen: {e}")
            return None


def check_available_formats(url):
    """Zeigt alle verfügbaren Formate für ein Video an"""
    ydl_opts = {
        'listformats': True,
        'quiet': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Fehler beim Abrufen der Formate: {e}")


def main():
    parser = argparse.ArgumentParser(description='YouTube Video/Music Downloader')
    parser.add_argument('url', help='YouTube URL')
    parser.add_argument('-o', '--output', default='downloads', help='Output Verzeichnis')
    parser.add_argument('-a', '--audio-only', action='store_true', help='Nur Audio herunterladen')
    parser.add_argument('-p', '--playlist', action='store_true', help='Playlist herunterladen')
    parser.add_argument('-q', '--quality', default='best', help='Qualität (best, 4k, 1440p, 1080p, 720p, 480p)')
    parser.add_argument('-f', '--format', default='mp4', help='Format (mp4, webm, mp3, wav, etc.)')
    parser.add_argument('-i', '--info', action='store_true', help='Nur Video-Informationen anzeigen')
    parser.add_argument('--max', type=int, help='Maximale Anzahl Downloads für Playlists')
    parser.add_argument('--list-formats', action='store_true', help='Alle verfügbaren Formate anzeigen')

    args = parser.parse_args()

    # Downloader initialisieren
    downloader = YouTubeDownloader(args.output)

    # Verfügbare Formate anzeigen
    if args.list_formats:
        check_available_formats(args.url)
        return

    # Nur Informationen anzeigen
    if args.info:
        info = downloader.get_video_info(args.url)
        if info:
            print("\n=== Video Informationen ===")
            for key, value in info.items():
                print(f"{key.capitalize()}: {value}")
        return

    # Playlist herunterladen
    if args.playlist:
        downloader.download_playlist(args.url, args.audio_only, args.max)
    # Nur Audio herunterladen
    elif args.audio_only:
        downloader.download_audio(args.url, args.quality, args.format)
    # Video herunterladen
    else:
        downloader.download_video(args.url, args.quality, args.format)


def interactive_mode():
    """Interaktiver Modus für benutzerfreundliche Bedienung"""
    print("=== YouTube Downloader ===")
    print("1. Video herunterladen")
    print("2. Audio herunterladen")
    print("3. Playlist herunterladen")
    print("4. Video-Informationen anzeigen")
    print("5. Verfügbare Formate anzeigen")
    print("6. Beenden")

    downloader = YouTubeDownloader()

    while True:
        try:
            choice = input("\nWähle eine Option (1-6): ").strip()

            if choice == '6':
                print("Auf Wiedersehen!")
                break

            if choice not in ['1', '2', '3', '4', '5']:
                print("Ungültige Auswahl. Bitte wähle 1-6.")
                continue

            url = input("YouTube URL eingeben: ").strip()
            if not url:
                print("Keine URL eingegeben.")
                continue

            if choice == '1':
                quality = input("Qualität (best/4k/1440p/1080p/720p/480p, Enter für 'best'): ").strip() or 'best'
                format_type = input("Format (mp4/webm/mkv, Enter für 'mp4'): ").strip() or 'mp4'

                # Bei hohen Qualitäten nach Audio fragen
                include_audio = True
                if quality in ['4k', '1440p', '1080p', 'best']:
                    print(f"\n⚠️  Hinweis: Für '{quality}' wird FFmpeg benötigt, um Video und Audio zusammenzufügen.")
                    audio_choice = input("Audio mit herunterladen? (j/n, Enter für 'j'): ").strip().lower()
                    include_audio = audio_choice != 'n'

                    if not include_audio:
                        print("📹 Nur Video wird heruntergeladen (ohne Audio)")
                    else:
                        print("🎵 Video mit Audio wird heruntergeladen")

                downloader.download_video(url, quality, format_type, include_audio)

            elif choice == '2':
                quality = input("Qualität (best/worst, Enter für 'best'): ").strip() or 'best'
                format_type = input("Format (mp3/wav/m4a/flac, Enter für 'mp3'): ").strip() or 'mp3'
                downloader.download_audio(url, quality, format_type)

            elif choice == '3':
                audio_only = input("Nur Audio? (j/n, Enter für 'n'): ").strip().lower() == 'j'
                max_str = input("Max. Downloads (Enter für alle): ").strip()
                max_downloads = int(max_str) if max_str.isdigit() else None
                downloader.download_playlist(url, audio_only, max_downloads)

            elif choice == '4':
                info = downloader.get_video_info(url)
                if info:
                    print("\n=== Video Informationen ===")
                    for key, value in info.items():
                        print(f"{key.capitalize()}: {value}")

            elif choice == '5':
                check_available_formats(url)

        except KeyboardInterrupt:
            print("\n\nProgramm beendet.")
            break
        except Exception as e:
            print(f"Fehler: {e}")


if __name__ == "__main__":
    # Wenn keine Argumente übergeben wurden, starte interaktiven Modus
    if len(sys.argv) == 1:
        interactive_mode()
    else:
        main()