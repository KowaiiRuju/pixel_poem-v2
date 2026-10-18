#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Top 10 (up to 2026) - YouTube & YouTube Music Audio Downloader
Pixel Poem v2 Music Library Suite

Downloads the user's top-ranked tracks with high-quality MP3 conversion,
embedded metadata (Title, Artist, Album, Year, Cover Art), and seamless
integration with the Pixel Poem web music player.
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path

# Force UTF-8 encoding on Windows standard streams to handle Japanese, Tagalog, and special characters
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    import yt_dlp
except ImportError:
    print("[ERROR] yt-dlp is not installed in this Python environment.")
    print("Please install it using: pip install yt-dlp")
    sys.exit(1)


# ==============================================================================
# DATASET: Top 10 Tracks (Up to 2026)
# ==============================================================================

TOP_10_OVERALL = [
    {
        "id": "overall_1",
        "rank": 1,
        "rank_display": "1",
        "title": "Deslocado",
        "artist": "NAPA",
        "total_plays": 53,
        "default_url": "https://www.youtube.com/watch?v=EPn9pzrx2Ec",
        "versions": {
            "topic": {"name": "Topic Audio (33 plays)", "url": "https://www.youtube.com/watch?v=EPn9pzrx2Ec"},
            "mv": {"name": "Official MV (12 plays)", "url": "https://www.youtube.com/watch?v=pNstFdk-hnY"},
            "eurovision": {"name": "Eurovision 2025 (8 plays)", "url": "https://www.youtube.com/watch?v=-s1Cc2uEj3U"},
        },
        "channel": "https://www.youtube.com/channel/UCEsDcAiBwLjrq2DVLtJxs1w",
        "notes": "33 Topic audio, 12 Official MV, 8 Eurovision 2025",
    },
    {
        "id": "overall_2",
        "rank": 2,
        "rank_display": "2",
        "title": "Multo",
        "artist": "Cup of Joe",
        "total_plays": 48,
        "default_url": "https://www.youtube.com/watch?v=5kGb5mayIzI",
        "versions": {
            "cozy_cove": {"name": "Extended Cozy Cove / Live (33 plays)", "url": "https://www.youtube.com/watch?v=5kGb5mayIzI"},
            "wish1075": {"name": "Wish 107.5 Bus (4 plays)", "url": "https://www.youtube.com/watch?v=YGNOrGlYSmk"},
        },
        "channel": "https://www.youtube.com/channel/UCPq0kgKjpNzryoNbRp5eUyQ",
        "notes": "21 Extended Cozy Cove, 12 Cozy Cove Live/Stripped, 4 Wish 107.5, 4 Topic, 7 Lyric/Covers",
    },
    {
        "id": "overall_3",
        "rank": 3,
        "rank_display": "3",
        "title": "Tipsy (寄り酔い)",
        "artist": "Wanuka (和ぬか)",
        "total_plays": 39,
        "default_url": "https://www.youtube.com/watch?v=Rq0NjgXSj0s",
        "versions": {
            "mv": {"name": "Official MV (21 plays)", "url": "https://www.youtube.com/watch?v=Rq0NjgXSj0s"},
            "topic": {"name": "Topic audio (13 plays)", "url": "https://www.youtube.com/watch?v=o1HxeJYKwlQ"},
        },
        "channel": "https://www.youtube.com/channel/UCm7rYZ6xOw3m5GaTMuUJjVw",
        "notes": "21 Official MV, 13 Topic audio, 5 Cover versions",
    },
    {
        "id": "overall_4",
        "rank": 4,
        "rank_display": "4",
        "title": "Fallen",
        "artist": "Lola Amour",
        "total_plays": 38,
        "default_url": "https://www.youtube.com/watch?v=7h-ygnzJek0",
        "versions": {
            "cozy_cove": {"name": "Live at Cozy Cove (19 plays)", "url": "https://www.youtube.com/watch?v=7h-ygnzJek0"},
            "topic": {"name": "Topic audio (13 plays)", "url": "https://www.youtube.com/watch?v=AaC4SOe1rQ4"},
            "lyric": {"name": "Lyric Video (4 plays)", "url": "https://www.youtube.com/watch?v=S3wytd6ZbXc"},
        },
        "channel": "https://www.youtube.com/channel/UC7YhcSdz6o3L_BJDiqisF-g",
        "notes": "19 Live at Cozy Cove, 13 Topic audio, 4 Lyric Video, 2 Extended",
    },
    {
        "id": "overall_5",
        "rank": 5,
        "rank_display": "5",
        "title": "back to friends",
        "artist": "sombr",
        "total_plays": 33,
        "default_url": "https://www.youtube.com/watch?v=c-8abSPAPOU",
        "versions": {
            "topic": {"name": "Topic audio (24 plays)", "url": "https://www.youtube.com/watch?v=c-8abSPAPOU"},
            "mv": {"name": "Official Video (2 plays)", "url": "https://www.youtube.com/watch?v=c8zq4kAn_O0"},
        },
        "channel": "https://www.youtube.com/channel/UCyI0V6RmULLsRxegMTCmkWQ",
        "notes": "24 Topic audio, 2 Official Video, 1 Radio 1 Piano, 6 Cover",
    },
    {
        "id": "overall_6",
        "rank": 6,
        "rank_display": "6",
        "title": "Kalapastangan",
        "artist": "fitterkarma",
        "total_plays": 32,
        "default_url": "https://www.youtube.com/watch?v=YRqz58yOCLc",
        "versions": {
            "cozy_cove": {"name": "Live at Cozy Cove (23 plays)", "url": "https://www.youtube.com/watch?v=YRqz58yOCLc"},
            "topic": {"name": "Topic audio (7 plays)", "url": "https://www.youtube.com/watch?v=FpJxPzveHzA"},
        },
        "channel": "https://www.youtube.com/channel/UCVZoM1H-jFwni_C4nogarjw",
        "notes": "23 Live at Cozy Cove, 7 Topic audio, 2 Lyrics/Karaoke",
    },
    {
        "id": "overall_7",
        "rank": 7,
        "rank_display": "7",
        "title": "Sunny (晴る / Haru)",
        "artist": "Yorushika (ヨルシカ)",
        "total_plays": 32,
        "default_url": "https://www.youtube.com/watch?v=mUSVav9pKO4",
        "versions": {
            "topic": {"name": "Topic audio (12 plays)", "url": "https://www.youtube.com/watch?v=mUSVav9pKO4"},
            "mv": {"name": "Official MV (11 plays)", "url": "https://www.youtube.com/watch?v=CkvWJNt77mU"},
            "live": {"name": "Official Live (5 plays)", "url": "https://www.youtube.com/watch?v=YmvAXVmfK0A"},
        },
        "channel": "https://www.youtube.com/channel/UCRIgIJQWuBJ0Cv_VlU3USNA",
        "notes": "12 Topic audio, 11 Official MV, 5 Official Live, 4 Lyrics/Tabs",
    },
    {
        "id": "overall_8",
        "rank": 8,
        "rank_display": "8",
        "title": "tindahan ng mga alaala",
        "artist": "Ian Quiruz",
        "total_plays": 25,
        "default_url": "https://www.youtube.com/watch?v=MZSql0fzQrA",
        "versions": {
            "topic": {"name": "Topic audio (24 plays)", "url": "https://www.youtube.com/watch?v=MZSql0fzQrA"},
            "artist_upload": {"name": "Artist upload (1 play)", "url": "https://www.youtube.com/watch?v=pGN9UmEoIrE"},
        },
        "channel": "https://www.youtube.com/channel/UCpT4pF0w1UGWrTgtwYLSbOg",
        "notes": "24 Topic audio (19 on YouTube, 5 on YT Music), 1 Artist upload",
    },
    {
        "id": "overall_9",
        "rank": 9,
        "rank_display": "9",
        "title": "Good Goodbye",
        "artist": "HWASA",
        "total_plays": 25,
        "default_url": "https://www.youtube.com/watch?v=QxGt54-oh1A",
        "versions": {
            "topic": {"name": "Topic audio (19 plays)", "url": "https://www.youtube.com/watch?v=QxGt54-oh1A"},
            "mv": {"name": "Official MV (3 plays)", "url": "https://www.youtube.com/watch?v=Qe8fa4b5xNU"},
        },
        "channel": "https://www.youtube.com/channel/UCiM8arBZ-GyuBFG3wy6fEgw",
        "notes": "19 Topic audio, 3 Official MV, 3 Live/Stage performances",
    },
    {
        "id": "overall_10a",
        "rank": 10,
        "rank_display": "10 (Tie)",
        "title": "Padaba Taka",
        "artist": "dwta",
        "total_plays": 25,
        "default_url": "https://www.youtube.com/watch?v=iiyrcma7OTs",
        "versions": {
            "topic": {"name": "Topic audio (15 plays)", "url": "https://www.youtube.com/watch?v=iiyrcma7OTs"},
            "cozy_cove": {"name": "Live at Cozy Cove (6 plays)", "url": "https://www.youtube.com/watch?v=jJiqbBNITo0"},
        },
        "channel": "https://www.youtube.com/channel/UC4u8HuyLlY2k5jgrt-ZTYpw",
        "notes": "15 Topic audio, 6 Live at Cozy Cove, 3 Lyric Video, 1 MV",
    },
    {
        "id": "overall_10b",
        "rank": 10,
        "rank_display": "10 (Tie)",
        "title": "Everything Goes On",
        "artist": "Porter Robinson",
        "total_plays": 25,
        "default_url": "https://www.youtube.com/watch?v=eEFVxI9lqjU",
        "versions": {
            "mv": {"name": "Official MV (16 plays)", "url": "https://www.youtube.com/watch?v=eEFVxI9lqjU"},
            "lyric": {"name": "Lyric Videos (6 plays)", "url": "https://www.youtube.com/watch?v=izHyKdrSKvo"},
        },
        "channel": "https://www.youtube.com/channel/UCKKKYE55BVswHgKihx5YXew",
        "notes": "16 Official MV, 6 Lyric Videos, 1 Topic audio, 2 Covers",
    },
]

TOP_10_YT_MUSIC = [
    {
        "id": "ytm_1",
        "rank": 1,
        "rank_display": "1",
        "title": "Deslocado",
        "artist": "NAPA",
        "yt_music_plays": 30,
        "default_url": "https://www.youtube.com/watch?v=EPn9pzrx2Ec",
        "channel": "https://www.youtube.com/channel/UCEsDcAiBwLjrq2DVLtJxs1w",
    },
    {
        "id": "ytm_2",
        "rank": 2,
        "rank_display": "2",
        "title": "back to friends",
        "artist": "sombr",
        "yt_music_plays": 23,
        "default_url": "https://www.youtube.com/watch?v=c-8abSPAPOU",
        "channel": "https://www.youtube.com/channel/UCyI0V6RmULLsRxegMTCmkWQ",
    },
    {
        "id": "ytm_3a",
        "rank": 3,
        "rank_display": "3 (Tie)",
        "title": "Best Friend",
        "artist": "Rex Orange County",
        "yt_music_plays": 18,
        "default_url": "https://www.youtube.com/watch?v=MMvlxSupSVE",
        "channel": "https://www.youtube.com/channel/UC7Yqsq07_fdXg23hLRODh-w",
    },
    {
        "id": "ytm_3b",
        "rank": 3,
        "rank_display": "3 (Tie)",
        "title": "I Thought I Saw Your Face Today",
        "artist": "She & Him",
        "yt_music_plays": 18,
        "default_url": "https://www.youtube.com/watch?v=HJstyRBLqBQ",
        "channel": "https://www.youtube.com/channel/UC8CvgMoefY0bNy52qs0cPPg",
    },
    {
        "id": "ytm_5a",
        "rank": 5,
        "rank_display": "5 (Tie)",
        "title": "Pag-Ibig ay Kanibalismo II",
        "artist": "fitterkarma",
        "yt_music_plays": 17,
        "default_url": "https://www.youtube.com/watch?v=cb9gPI11ZL0",
        "channel": "https://www.youtube.com/channel/UCVZoM1H-jFwni_C4nogarjw",
    },
    {
        "id": "ytm_5b",
        "rank": 5,
        "rank_display": "5 (Tie)",
        "title": "Good Goodbye",
        "artist": "HWASA",
        "yt_music_plays": 17,
        "default_url": "https://www.youtube.com/watch?v=QxGt54-oh1A",
        "channel": "https://www.youtube.com/channel/UCiM8arBZ-GyuBFG3wy6fEgw",
    },
    {
        "id": "ytm_7a",
        "rank": 7,
        "rank_display": "7 (Tie)",
        "title": "Sailor Song",
        "artist": "Gigi Perez",
        "yt_music_plays": 15,
        "default_url": "https://www.youtube.com/watch?v=wPY6dOC-MDA",
        "channel": "https://www.youtube.com/channel/UCobE63bvA-2tK_HZ2LbP8cQ",
    },
    {
        "id": "ytm_7b",
        "rank": 7,
        "rank_display": "7 (Tie)",
        "title": "Super Shy",
        "artist": "NewJeans",
        "yt_music_plays": 15,
        "default_url": "https://www.youtube.com/watch?v=0c7zGU2C2mM",
        "channel": "https://www.youtube.com/channel/UCxOqS3cYg4FaHbobICo7nFQ",
    },
    {
        "id": "ytm_9a",
        "rank": 9,
        "rank_display": "9 (Tie)",
        "title": "Padaba Taka",
        "artist": "dwta",
        "yt_music_plays": 14,
        "default_url": "https://www.youtube.com/watch?v=iiyrcma7OTs",
        "channel": "https://www.youtube.com/channel/UC4u8HuyLlY2k5jgrt-ZTYpw",
    },
    {
        "id": "ytm_9b",
        "rank": 9,
        "rank_display": "9 (Tie)",
        "title": "Thunder (Album Version)",
        "artist": "BOYS LIKE GIRLS",
        "yt_music_plays": 14,
        "default_url": "https://www.youtube.com/watch?v=RaJYMfuR7Zs",
        "channel": "https://www.youtube.com/channel/UCUMVaSA7G1VLTnYhivV3hmw",
    },
    {
        "id": "ytm_9c",
        "rank": 9,
        "rank_display": "9 (Tie)",
        "title": "I Love You So",
        "artist": "The Walters",
        "yt_music_plays": 14,
        "default_url": "https://www.youtube.com/watch?v=k7kzc3Nof08",
        "channel": "https://www.youtube.com/channel/UCWXnGZRSAZJQ7JV7id5fufg",
    },
]

NEW_SCREENSHOT_SONGS = [
    {
        "id": "new_1",
        "rank": 3,
        "rank_display": "3 (Tie)",
        "title": "Same Ground",
        "artist": "Kitchie Nadal",
        "plays": 7,
        "default_url": "https://www.youtube.com/watch?v=DBCV7rfGiUY",
        "notes": "Live at The Cozy Cove",
    },
    {
        "id": "new_2",
        "rank": 3,
        "rank_display": "3 (Tie)",
        "title": "平行線 (Heikousen)",
        "artist": "Eve × suis from Yorushika",
        "plays": 7,
        "default_url": "https://www.youtube.com/watch?v=lxw4Y8qzq4w",
        "notes": "Official Music Video",
    },
    {
        "id": "new_3",
        "rank": 3,
        "rank_display": "3 (Tie)",
        "title": "たぶん (Tabun)",
        "artist": "YOASOBI",
        "plays": 7,
        "default_url": "https://www.youtube.com/watch?v=8iuLXODzL04",
        "notes": "Official Music Video",
    },
    {
        "id": "new_4",
        "rank": 7,
        "rank_display": "7 (Tie)",
        "title": "Fallen",
        "artist": "Lola Amour",
        "plays": 6,
        "default_url": "https://www.youtube.com/watch?v=7h-ygnzJek0",
        "notes": "Live at The Cozy Cove",
    },
    {
        "id": "new_5",
        "rank": 7,
        "rank_display": "7 (Tie)",
        "title": "Sunny (晴る / Haru)",
        "artist": "Yorushika (ヨルシカ)",
        "plays": 6,
        "default_url": "https://www.youtube.com/watch?v=YmvAXVmfK0A",
        "notes": "2 on YouTube Music, 4 on Official Live",
    },
    {
        "id": "new_6",
        "rank": 9,
        "rank_display": "9 (Tie)",
        "title": "What if I miss you for the rest of my life?",
        "artist": "Janine Berdin",
        "plays": 5,
        "default_url": "https://www.youtube.com/watch?v=3ku3TxWAo1A",
        "notes": "2 Studio Live on YTM, 3 at 39th Awit Awards",
    },
    {
        "id": "new_7",
        "rank": 9,
        "rank_display": "9 (Tie)",
        "title": "Na Para Bang",
        "artist": "Mariah Deborah",
        "plays": 5,
        "default_url": "https://www.youtube.com/watch?v=Y5z_4utl678",
        "notes": "1 on YouTube Music, 4 on Wish 107.5 Bus",
    },
]


def purge_old_songs(playlist_dir: Path):
    """Removes obsolete tracks from the playlist folder (e.g. Taylor Swift, Ado, Vaundy)."""
    old_keywords = ["Taylor Swift", "Ado", "Vaundy", "Cruel Summer", "Paper Rings", "The Alchemy", "Anti-Hero", "Vivarium", "Odoriko"]
    removed = []
    if not playlist_dir.exists():
        return removed
    for f in list(playlist_dir.glob("*.mp3")) + list(playlist_dir.glob("*.m4a")):
        if any(kw.lower() in f.name.lower() for kw in old_keywords):
            try:
                f.unlink()
                removed.append(f.name)
                print(f" [PURGE] Removed old track: {f.name}")
            except Exception as e:
                print(f" [WARN] Failed to delete {f.name}: {e}")
    return removed


def get_all_unique_tracks():
    """Returns a list of all unique tracks combining Top Overall, YT Music, and New Screenshot lists."""
    seen_urls = set()
    unique_tracks = []
    
    # Add New Screenshot tracks first
    for track in NEW_SCREENSHOT_SONGS:
        url = track["default_url"]
        if url not in seen_urls:
            seen_urls.add(url)
            t = dict(track)
            t["category"] = "New Screenshot Songs"
            unique_tracks.append(t)

    # Add Top Overall
    for track in TOP_10_OVERALL:
        url = track["default_url"]
        if url not in seen_urls:
            seen_urls.add(url)
            t = dict(track)
            t["category"] = "Top Overall"
            unique_tracks.append(t)
            
    # Add remaining from YT Music
    for track in TOP_10_YT_MUSIC:
        url = track["default_url"]
        if url not in seen_urls:
            seen_urls.add(url)
            t = dict(track)
            t["category"] = "YouTube Music Only"
            unique_tracks.append(t)
            
    return unique_tracks



def sanitize_filename(name: str) -> str:
    """Sanitize strings for Windows safe filenames."""
    for char in r'<>:"/\|?*':
        name = name.replace(char, "_")
    return name.strip()


def check_node_installed() -> bool:
    """Checks if Node.js is available on PATH for yt-dlp JS runtime."""
    return shutil.which("node") is not None


# ==============================================================================
# DOWNLOAD ENGINE
# ==============================================================================

class YtDlpDownloader:
    def __init__(self, output_dir: str = "playlist/Top 10 (up to 2026)", audio_format: str = "mp3", audio_quality: str = "320", dry_run: bool = False):
        self.output_dir = Path(output_dir).resolve()
        self.audio_format = audio_format
        self.audio_quality = audio_quality
        self.dry_run = dry_run
        self.use_node = check_node_installed()

    def build_ydl_opts(self, track_info: dict, index: int, total: int):
        """Builds yt-dlp options with metadata, artwork, and ffmpeg postprocessing."""
        artist = track_info.get("artist", "Unknown Artist")
        title = track_info.get("title", "Unknown Title")
        rank = track_info.get("rank_display", str(index))
        
        # Clean prefix: 01, 02, etc.
        prefix = f"{index:02d}"
        filename_template = f"{prefix} - {sanitize_filename(artist)} - {sanitize_filename(title)}.%(ext)s"
        outtmpl = str(self.output_dir / filename_template)

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": outtmpl,
            "writethumbnail": True,
            "quiet": False,
            "no_warnings": False,
            "simulate": self.dry_run,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": self.audio_format,
                    "preferredquality": self.audio_quality,
                },
                {
                    "key": "FFmpegThumbnailsConvertor",
                    "format": "jpg",
                },
                {
                    "key": "EmbedThumbnail",
                },
                {
                    "key": "FFmpegMetadata",
                    "add_metadata": True,
                },
            ],
            # Pass custom metadata arguments to FFmpeg
            "postprocessor_args": {
                "ffmpeg": [
                    "-metadata", f"title={title}",
                    "-metadata", f"artist={artist}",
                    "-metadata", "album=Top 10 (up to 2026)",
                    "-metadata", f"track={index}/{total}",
                    "-metadata", "date=2026",
                ]
            },
        }

        if self.use_node:
            ydl_opts["js_runtimes"] = {"node": {}}

        return ydl_opts

    def download_track(self, track: dict, index: int, total: int, url_override: str = None) -> bool:
        """Downloads an individual track."""
        url = url_override or track.get("default_url")
        title = track.get("title")
        artist = track.get("artist")
        rank_disp = track.get("rank_display", str(index))

        print("\n" + "─" * 65)
        print(f" ▶ [{index}/{total}] Rank {rank_disp}: {artist} - {title}")
        print(f"   URL: {url}")
        if self.dry_run:
            print("   [DRY-RUN] Simulating metadata and stream extraction...")
        else:
            print("   Downloading audio & embedding cover art...")

        self.output_dir.mkdir(parents=True, exist_ok=True)
        ydl_opts = self.build_ydl_opts(track, index, total)

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f" ✔ Successfully processed: {artist} - {title}")
            return True
        except Exception as e:
            print(f" ✘ Failed to download {title}: {e}")
            return False

    def download_batch(self, tracks: list, version_preference: str = None) -> int:
        """Downloads a list of tracks sequentially."""
        total = len(tracks)
        success_count = 0

        print("\n" + "=" * 65)
        print(f" Starting download of {total} tracks to:")
        print(f" Directory: {self.output_dir}")
        print(f" Format: {self.audio_format.upper()} ({self.audio_quality}kbps)")
        print("=" * 65)

        for i, track in enumerate(tracks, start=1):
            url = None
            if version_preference and "versions" in track:
                if version_preference in track["versions"]:
                    url = track["versions"][version_preference]["url"]
                    print(f"   (Selected preferred version: {version_preference})")
            
            ok = self.download_track(track, i, total, url_override=url)
            if ok:
                success_count += 1

        print("\n" + "=" * 65)
        print(f" Download completed: {success_count}/{total} successful.")
        print(f" Destination folder: {self.output_dir}")
        print("=" * 65)
        return success_count


# ==============================================================================
# WEB PLAYER SYNC: scripts/music_player.js
# ==============================================================================

def sync_with_web_player(playlist_dir: Path = None, js_file_path: Path = None, append_mode: bool = False):
    """
    Scans the downloaded tracks in the playlist directory and updates
    `scripts/music_player.js` so the website's built-in audio player plays them!
    """
    root_dir = Path(__file__).resolve().parent
    if playlist_dir is None:
        playlist_dir = root_dir / "playlist" / "Top 10 (up to 2026)"
        if not playlist_dir.exists():
            playlist_dir = root_dir / "playlist"

    if js_file_path is None:
        js_file_path = root_dir / "scripts" / "music_player.js"

    if not js_file_path.exists():
        print(f"[WARN] Web player script not found at {js_file_path}")
        return False

    # Find audio files in playlist_dir
    audio_files = []
    for ext in ("*.mp3", "*.m4a", "*.opus", "*.flac", "*.wav"):
        audio_files.extend(list(playlist_dir.glob(ext)))
    
    audio_files.sort(key=lambda p: p.name)

    if not audio_files:
        print(f"[INFO] No audio files found in {playlist_dir} to sync.")
        return False

    print(f"\n[SYNC] Found {len(audio_files)} audio files in {playlist_dir.name}/.")
    
    new_tracks = []
    for f in audio_files:
        try:
            rel_path = f.resolve().relative_to(root_dir).as_posix()
        except Exception:
            rel_path = f"playlist/{f.name}"
        # Clean title from filename
        clean_title = f.stem
        # If filename starts with "01 - ", strip it for neat title display
        if len(clean_title) > 5 and clean_title[:2].isdigit() and clean_title[2:5] in (" - ", ". "):
            clean_title = clean_title[5:]
        new_tracks.append({"title": clean_title, "src": rel_path})

    # Read current js file
    with open(js_file_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    # Search for playlist definition
    start_marker = "const playlist = ["
    end_marker = "];"

    start_idx = js_content.find(start_marker)
    if start_idx == -1:
        print("[ERROR] Could not find 'const playlist = [' inside scripts/music_player.js")
        return False

    end_idx = js_content.find(end_marker, start_idx)
    if end_idx == -1:
        print("[ERROR] Could not find closing '];' of playlist array.")
        return False

    # Generate new playlist array block
    playlist_lines = [start_marker]
    for track in new_tracks:
        safe_title = track["title"].replace('"', '\\"')
        safe_src = track["src"].replace('"', '\\"')
        playlist_lines.append(f'    {{ title: "{safe_title}", src: "{safe_src}" }},')
    playlist_lines.append("  ];")
    
    new_playlist_block = "\n".join(playlist_lines)
    updated_content = js_content[:start_idx] + new_playlist_block + js_content[end_idx + len(end_marker):]

    with open(js_file_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f" ✔ Successfully updated {js_file_path} with {len(new_tracks)} tracks!")
    print("   Your Pixel Poem music player will now play these tracks in index.html!")
    return True


# ==============================================================================
# DISPLAY & INTERACTIVE CLI
# ==============================================================================

def print_banner():
    banner = r"""
╔══════════════════════════════════════════════════════════════════════╗
║                 TOP 10 (UP TO 2026) MUSIC DOWNLOADER                 ║
║                 Pixel Poem v2 • High-Quality yt-dlp                  ║
╚══════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def display_tracklists():
    """Prints formatted tracklists with plays and breakdown info."""
    print("\n" + "═" * 70)
    print(" 🌟 1. TOP 10 OVERALL (All Versions & Channels)")
    print("═" * 70)
    print(f" {'Rank':<8} {'Artist':<20} {'Song':<24} {'Total':<7}")
    print("─" * 70)
    for t in TOP_10_OVERALL:
        print(f" {t['rank_display']:<8} {t['artist']:<20} {t['title']:<24} {t['total_plays']:<7}")
        if "notes" in t:
            print(f"   └─ Versions: {t['notes']}")

    print("\n" + "═" * 70)
    print(" 🎵 2. TOP 10 SINGLE TRACKS (YouTube Music Only - 1,572 plays pool)")
    print("═" * 70)
    print(f" {'Rank':<8} {'Artist':<20} {'Track':<24} {'YT Music Plays':<15}")
    print("─" * 70)
    for t in TOP_10_YT_MUSIC:
        print(f" {t['rank_display']:<8} {t['artist']:<20} {t['title']:<24} {t['yt_music_plays']:<15}")

    unique = get_all_unique_tracks()
    print("\n" + "═" * 70)
    print(f" ℹ Total unique songs across both lists: {len(unique)}")
    print("═" * 70)


def interactive_menu():
    """Interactive console prompt for user navigation."""
    print_banner()
    while True:
        print("\nSelect an action:")
        print("  [1] Swap Playlist: Purge old songs, download new screenshot tracks & sync player")
        print("  [2] Download New Screenshot Songs (7 songs)")
        print("  [3] Download Top 10 Overall (11 songs - with ties)")
        print("  [4] Download Top 10 Single Tracks on YouTube Music (11 songs)")
        print("  [5] Download All Unique Tracks (22 unique songs)")
        print("  [6] Download Specific Song by Rank")
        print("  [7] View Detailed Tracklist & Version Breakdown")
        print("  [8] Sync Downloaded Songs with Web Player (scripts/music_player.js)")
        print("  [9] Purge Old Songs (Taylor Swift, Ado, Vaundy)")
        print("  [0] Exit")

        choice = input("\nEnter choice [0-9]: ").strip()

        if choice == "1":
            playlist_dir = Path("playlist")
            purge_old_songs(playlist_dir)
            downloader = YtDlpDownloader(output_dir="playlist")
            downloader.download_batch(NEW_SCREENSHOT_SONGS)
            sync_with_web_player(playlist_dir=playlist_dir)
        elif choice == "2":
            downloader = YtDlpDownloader(output_dir="playlist")
            downloader.download_batch(NEW_SCREENSHOT_SONGS)
            ask_sync = input("\nUpdate Pixel Poem web music player playlist now? [y/N]: ").strip().lower()
            if ask_sync == "y":
                sync_with_web_player(playlist_dir=Path("playlist"))
        elif choice == "3":
            downloader = YtDlpDownloader(output_dir="playlist/Top 10 (up to 2026)")
            downloader.download_batch(TOP_10_OVERALL)
            ask_sync = input("\nUpdate Pixel Poem web music player playlist now? [y/N]: ").strip().lower()
            if ask_sync == "y":
                sync_with_web_player()
        elif choice == "4":
            downloader = YtDlpDownloader(output_dir="playlist/Top 10 YT Music")
            downloader.download_batch(TOP_10_YT_MUSIC)
            ask_sync = input("\nUpdate Pixel Poem web music player playlist now? [y/N]: ").strip().lower()
            if ask_sync == "y":
                sync_with_web_player(playlist_dir=Path("playlist/Top 10 YT Music"))
        elif choice == "5":
            unique = get_all_unique_tracks()
            downloader = YtDlpDownloader(output_dir="playlist/Top 10 (up to 2026)")
            downloader.download_batch(unique)
            ask_sync = input("\nUpdate Pixel Poem web music player playlist now? [y/N]: ").strip().lower()
            if ask_sync == "y":
                sync_with_web_player()
        elif choice == "6":
            unique = get_all_unique_tracks()
            print("\nAvailable Tracks:")
            for i, t in enumerate(unique, start=1):
                print(f"  [{i:2d}] {t['artist']} - {t['title']} ({t.get('category')})")
            sel = input("\nEnter track number (e.g. 1 or 1,3,5): ").strip()
            try:
                indices = [int(x.strip()) for x in sel.split(",") if x.strip()]
                selected_tracks = [unique[i - 1] for i in indices if 1 <= i <= len(unique)]
                if selected_tracks:
                    downloader = YtDlpDownloader(output_dir="playlist/Top 10 (up to 2026)")
                    downloader.download_batch(selected_tracks)
                else:
                    print("[WARN] No valid tracks selected.")
            except Exception as e:
                print(f"[ERROR] Invalid input: {e}")
        elif choice == "7":
            display_tracklists()
        elif choice == "8":
            sync_with_web_player(playlist_dir=Path("playlist"))
        elif choice == "9":
            purge_old_songs(Path("playlist"))
        elif choice == "0":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please select from 0-9.")


# ==============================================================================
# MAIN ENTRYPOINT & CLI PARSER
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Top 10 (up to 2026) - YouTube & YouTube Music Audio Downloader",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--swap-playlist", action="store_true", help="Purge old songs, download new screenshot tracks into playlist/, and update music_player.js")
    parser.add_argument("--new", action="store_true", help="Download new screenshot tracks into playlist/")
    parser.add_argument("--purge-old", action="store_true", help="Purge obsolete songs from playlist folder")
    parser.add_argument("--all", "-a", action="store_true", help="Download all unique tracks across all lists")
    parser.add_argument("--overall", action="store_true", help="Download Top 10 Overall tracks (11 tracks)")
    parser.add_argument("--yt-music", action="store_true", help="Download Top 10 YouTube Music tracks (11 tracks)")
    parser.add_argument("--rank", "-r", type=str, help="Download specific rank(s), e.g. -r 1 or -r 1,3,7")
    parser.add_argument("--list", "-l", action="store_true", help="Display full track rankings and exit")
    parser.add_argument("--output", "-o", type=str, default="playlist", help="Destination output folder (default: playlist)")
    parser.add_argument("--format", "-f", type=str, default="mp3", choices=["mp3", "m4a", "flac", "opus", "wav"], help="Target audio format")
    parser.add_argument("--quality", "-q", type=str, default="320", help="Audio bitrate / quality (default: 320)")
    parser.add_argument("--version-pref", type=str, choices=["topic", "mv", "cozy_cove", "live"], help="Preferred version variant if available")
    parser.add_argument("--update-player", action="store_true", help="Update scripts/music_player.js with downloaded tracks")
    parser.add_argument("--dry-run", action="store_true", help="Simulate extraction and metadata without downloading audio")

    args = parser.parse_args()

    # If no flags passed, launch interactive menu
    if len(sys.argv) == 1:
        interactive_menu()
        return

    if args.list:
        print_banner()
        display_tracklists()
        return

    out_path = Path(args.output)

    if args.purge_old:
        purge_old_songs(out_path)
        if not (args.swap_playlist or args.new or args.all or args.overall or args.yt_music or args.rank):
            return

    if args.swap_playlist:
        print_banner()
        purge_old_songs(out_path)
        downloader = YtDlpDownloader(
            output_dir=str(out_path),
            audio_format=args.format,
            audio_quality=args.quality,
            dry_run=args.dry_run,
        )
        downloader.download_batch(NEW_SCREENSHOT_SONGS, version_preference=args.version_pref)
        sync_with_web_player(playlist_dir=out_path)
        return

    if args.update_player and not (args.all or args.overall or args.yt_music or args.rank or args.new):
        sync_with_web_player(playlist_dir=out_path)
        return

    downloader = YtDlpDownloader(
        output_dir=args.output,
        audio_format=args.format,
        audio_quality=args.quality,
        dry_run=args.dry_run,
    )

    selected_tracks = []
    if args.new:
        selected_tracks = NEW_SCREENSHOT_SONGS
    elif args.all:
        selected_tracks = get_all_unique_tracks()
    elif args.overall:
        selected_tracks = TOP_10_OVERALL
    elif args.yt_music:
        selected_tracks = TOP_10_YT_MUSIC
    elif args.rank:
        unique = get_all_unique_tracks()
        rank_targets = [r.strip() for r in args.rank.split(",")]
        for t in unique:
            if str(t.get("rank")) in rank_targets or t.get("rank_display") in rank_targets:
                selected_tracks.append(t)
        if not selected_tracks:
            try:
                indices = [int(r) for r in rank_targets]
                selected_tracks = [unique[i - 1] for i in indices if 1 <= i <= len(unique)]
            except Exception:
                pass

    if not selected_tracks:
        print("[ERROR] No tracks selected. Use --swap-playlist, --new, --all, --overall, --yt-music, or --rank <N>.")
        sys.exit(1)

    print_banner()
    downloader.download_batch(selected_tracks, version_preference=args.version_pref)

    if args.update_player:
        sync_with_web_player(playlist_dir=out_path)


if __name__ == "__main__":
    main()

