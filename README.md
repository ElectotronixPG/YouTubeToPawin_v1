# YouTubeToPawin v1 — YouTube to Pawin-Tech Music Uploader

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://github.com/ElectotronixPG/YouTubeToPawin_v1/releases)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://python.org)

A cute desktop application for Windows that downloads YouTube audio and automatically uploads it to your **Pawin-Tech Music Platform** library.

---

## 🎵 Features

- ✅ Login with your Pawin-Tech platform account
- ✅ Paste any YouTube video or playlist URL
- ✅ Automatically download audio as MP3
- ✅ Upload directly to your Music Library
- ✅ Baby cute GUI style with pastel colors
- ✅ Saves login credentials locally for quick access
- ✅ Works on Windows 10 and Windows 11

---

## 📥 Download

Download the latest pre-built Windows executable from the [Releases](https://github.com/ElectotronixPG/YouTubeToPawin_v1/releases) page.

Or download directly from your Pawin-Tech Platform website on the **YouTube Download** page.

---

## 🛠️ Requirements (for running from source)

- Python 3.10 or higher
- [Node.js](https://nodejs.org/) (required by yt-dlp for YouTube challenge solving)
- [FFmpeg](https://ffmpeg.org/) (for audio conversion)

Install Python dependencies:

```bash
pip install yt-dlp requests customtkinter pillow
```

---

## 🚀 Running from Source

```bash
python YouTubeToPawin_v1_GUI.py
```

---

## 🔨 Building the Executable

```bash
pip install pyinstaller
pyinstaller --noconfirm --onedir --windowed --icon=icon.ico --name "YouTubeToPawin_v1" YouTubeToPawin_v1_GUI.py
```

---

## ⚙️ Configuration

On first run, the app asks for your **Pawin-Tech Platform** email and password. These are saved locally to `config.json` for future use.

The app connects to:
```
https://pawin-techplatform.pawin-tech.cloud/api
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🌸 Credits

Built with:
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — YouTube downloading
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — GUI framework
- [Requests](https://requests.readthedocs.io/) — HTTP client
