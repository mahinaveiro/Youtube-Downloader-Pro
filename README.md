# YouTube Downloader Pro

This is a simple, fully local tool to download YouTube videos and extract audio from them. It gives you a clean terminal interface where you can pick your exact video quality or audio bitrate, and it handles all the backend processing automatically.

## What it does

- Downloads YouTube videos in MP4 format (1080p, 720p, or 480p).
- Extracts audio and saves it as an MP3 (320kbps, 128kbps, or 64kbps).
- Shows a real-time progress bar so you know exactly how fast it's downloading.
- Runs 100% locally on your machine. No cloud servers, no limits.

## What you need

- Windows 10 or 11.
- Python 3.8 or higher installed on your PC.
- An internet connection.

## How to set it up

**1. Install Python (If you don't have it)**
1. Go to [python.org](https://www.python.org/downloads/)
2. Download the latest version for Windows
3. **IMPORTANT**: During installation, check the box that says **"Add Python to PATH"**
4. Click "Install Now"

**2. Get the files**
Download this repository. You can clone it using Git, or just click the green "Code" button on the GitHub page and download the ZIP file. Extract the ZIP to wherever you want to keep it (like `D:\YT_Downloader`).

**3. You're done**
I've already included `yt-dlp.exe` and `deno.exe` in the repository. You don't need to download or configure any of those separately. Just make sure they are in the same folder as `downloader.py`.

## Changing the save location

By default, the script saves videos to `G:\youtube-videos` and audio to `G:\youtube-audios`. If you don't have a G drive, it will throw an error. Here is how to change it to your own folders:

1. Open `downloader.py` in any text editor (Notepad, VS Code, etc.).
2. Look near the top of the file for these lines:
   ```python
   VIDEO_DIR = r"G:\youtube-videos"
   AUDIO_DIR = r"G:\youtube-audios"
   ```
3. Change the paths to wherever you want your files to go. For example:
   ```python
   VIDEO_DIR = r"D:\My Videos"
   AUDIO_DIR = r"D:\My Music"
   ```
4. Save the file. Make sure you keep the `r` before the quotes, it prevents Windows from messing up the backslashes in the path.

## How to use it

1. Open your terminal (Command Prompt or PowerShell) inside the project folder. The easiest way to do this is to open the folder in File Explorer, click the address bar at the top, type `cmd`, and hit Enter.
2. Run the script by typing:
   ```bash
   python d.py
   ```
3. Paste your YouTube link when it asks.
4. Choose media type:
   Type 1 for Video (MP4)
   Type 2 for Audio (MP3)
5. Choose quality:
   For Video: 1080p, 720p, or 480p
   For Audio: Best (~320kbps), Good (~128kbps), or Low (~64kbps)
6. Wait for the progress bar to finish. Your file will be saved to the folder you configured.

## Troubleshooting

**"python is not recognized..."**
You didn't add Python to your PATH during installation. You'll need to reinstall Python and check that specific box, or manually add it to your environment variables.

**"Target drive does not exist"**
The script is trying to save to a drive (like G:) that isn't plugged in or doesn't exist on your PC. Follow the "Changing the save location" section above to fix this.

**Downloads are failing or stuck**
YouTube changes their code sometimes. If it stops working, try updating the yt-dlp executable by running `yt-dlp.exe -U` in your terminal, or download the latest `yt-dlp.exe` from their GitHub releases and replace the one in this folder.

## Credits

This tool is built on top of some amazing open-source projects:
- [**yt-dlp**](https://github.com/yt-dlp/yt-dlp) (The actual downloading engine)
- [**Deno**](https://github.com/denoland/deno) (The JavaScript runtime needed to bypass YouTube's encryption)
