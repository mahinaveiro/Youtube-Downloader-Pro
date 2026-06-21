import os
import subprocess
import sys
import re
import json

# Config & Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
YTDLP_PATH = os.path.join(SCRIPT_DIR, "yt-dlp.exe")
DENO_PATH = os.path.join(SCRIPT_DIR, "deno.exe")  # New: Local JS Runtime

VIDEO_DIR = r"G:\youtube-videos" #Use your own dir here
AUDIO_DIR = r"G:\youtube-audios" #Use your own dir here

# ANSI Tweaks
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def check_dependencies():
    if not os.path.exists(YTDLP_PATH):
        print(f"{Colors.RED}[!] ERROR: Cannot find yt-dlp.exe in {SCRIPT_DIR}{Colors.END}")
        sys.exit(1)
    
    # New: Check for Deno JS Runtime
    if not os.path.exists(DENO_PATH):
        print(f"{Colors.RED}[!] ERROR: Cannot find deno.exe in {SCRIPT_DIR}{Colors.END}")
        print("    YouTube requires a JS engine. Download deno.exe and put it in this folder.")
        sys.exit(1)
    
    # Auto-create target directories if they don't exist
    for directory in [VIDEO_DIR, AUDIO_DIR]:
        drive = os.path.splitdrive(directory)[0] + "\\"
        if os.path.exists(drive):
            os.makedirs(directory, exist_ok=True)
        else:
            print(f"{Colors.RED}[!] ERROR: Target drive {drive} does not exist.{Colors.END}")
            sys.exit(1)

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "", filename).strip()

def get_video_info(url: str) -> dict:
    """Fetches basic metadata to show the user what they are about to download."""
    cmd = [YTDLP_PATH, "--js-runtimes", f"deno:{DENO_PATH}", "--dump-single-json", "--no-playlist", url]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return {
            "title": sanitize_filename(data.get("title", "Unknown_Title")),
            "uploader": data.get("uploader", "Unknown"),
            "duration": data.get("duration_string", "Unknown")
        }
    except Exception:
        return {"title": "Unknown_Title", "uploader": "Unknown", "duration": "Unknown"}

def download_media(url: str, media_type: str, quality: str):
    info = get_video_info(url)
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"  Title:    {Colors.BOLD}{info['title']}{Colors.END}")
    print(f"  Channel:  {info['uploader']}")
    print(f"  Duration: {info['duration']}{Colors.END}")
    print(f"{'='*60}{Colors.END}")

    if media_type == "video":
        if quality == "1":
            fmt = "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        elif quality == "2":
            fmt = "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        else:
            fmt = "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        target_dir = VIDEO_DIR
    else:
        if quality == "1":
            audio_qual = "0"   # Best (~320kbps)
        elif quality == "2":
            audio_qual = "5"   # Good (~128kbps)
        else:
            audio_qual = "9"   # Low (~64kbps)
        fmt = "bestaudio/best"
        target_dir = AUDIO_DIR

    cmd = [YTDLP_PATH, "--js-runtimes", f"deno:{DENO_PATH}"]
    
    if media_type == "audio":
        cmd.extend(["-x", "--audio-format", "mp3", "--audio-quality", audio_qual])
    
    cmd.extend(["-f", fmt])
    
    output_template = os.path.join(target_dir, "%(title)s.%(ext)s")
    cmd.extend(["-o", output_template, url])

    print(f"\n{Colors.YELLOW}[*] Starting download... (Progress bar below){Colors.END}\n")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\n{Colors.GREEN}[+] SUCCESS! File saved to: {target_dir}{Colors.END}")
    except subprocess.CalledProcessError as e:
        print(f"\n{Colors.RED}[!] Download failed or was interrupted.{Colors.END}")
    
    print(f"\n{Colors.CYAN}{'='*60}{Colors.END}\n")

def main():
    check_dependencies()
    
    while True:
        print(f"{Colors.HEADER}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗")
        print("║           YOUTUBE LOCAL DOWNLOADER PRO                 ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")
        
        url = input(f"{Colors.BLUE}[*] Enter YouTube URL (or 'q' to quit): {Colors.END}").strip()
        
        if url.lower() == 'q':
            print(f"{Colors.GREEN}[*] Exiting. Happy coding!{Colors.END}")
            break
            
        if not url.startswith("http"):
            print(f"{Colors.RED}[!] Invalid URL. Please enter a valid YouTube link.{Colors.END}\n")
            continue

        print(f"\n{Colors.BOLD}Select Media Type:{Colors.END}")
        print("  1. Video (MP4)")
        print("  2. Audio (MP3)")
        media_choice = input(f"{Colors.BLUE}[*] Choice (1 or 2): {Colors.END}").strip()
        
        if media_choice == "1":
            media_type = "video"
            print(f"\n{Colors.BOLD}Select Video Quality:{Colors.END}")
            print("  1. 1080p (Best)")
            print("  2. 720p (HD)")
            print("  3. 480p (SD)")
            qual_choice = input(f"{Colors.BLUE}[*] Choice (1, 2, or 3): {Colors.END}").strip()
            if qual_choice not in ["1", "2", "3"]: 
                qual_choice = "1"
        elif media_choice == "2":
            media_type = "audio"
            print(f"\n{Colors.BOLD}Select Audio Quality:{Colors.END}")
            print("  1. Best (~320 kbps)")
            print("  2. Good (~128 kbps)")
            print("  3. Low (~64 kbps)")
            qual_choice = input(f"{Colors.BLUE}[*] Choice (1, 2, or 3): {Colors.END}").strip()
            if qual_choice not in ["1", "2", "3"]: 
                qual_choice = "1"
        else:
            print(f"{Colors.RED}[!] Invalid choice. Defaulting to Video 1080p.{Colors.END}")
            media_type = "video"
            qual_choice = "1"

        download_media(url, media_type, qual_choice)

if __name__ == "__main__":
    # Enable ANSI colors in Windows 10/11 console
    os.system('') 
    main()