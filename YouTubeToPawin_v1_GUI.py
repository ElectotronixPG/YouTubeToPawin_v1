import os
import sys
import json
import time
import requests
import yt_dlp
import traceback
import threading
import customtkinter as ctk
import tkinter as tk

# ============================================================
#   YouTubeToPawin v1 — GUI Desktop Uploader
#   Platform: Windows
#   License: MIT
#   Source: https://github.com/ElectotronixPG/YouTubeToPawin_v1
# ============================================================

CONFIG_FILE = "config.json"
BASE_URL = "https://pawin-techplatform.pawin-tech.cloud/api"

# ---- Config ----
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

# ---- API ----
def login(email, password):
    try:
        res = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password}, timeout=15)
        if res.status_code == 200:
            return res.json().get('token')
    except Exception as e:
        pass
    return None

def upload_audio(file_path, title, token, log_fn):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (f"{title}.mp3", f, 'audio/mpeg')}
            data = {'title': title}
            res = requests.post(f"{BASE_URL}/music/upload", headers=headers, files=files, data=data, timeout=120)
            if res.status_code == 201:
                log_fn(f"✅ Uploaded: {title}")
                return True
            else:
                log_fn(f"❌ Upload failed: {res.status_code}")
                return False
    except Exception as e:
        log_fn(f"❌ Upload error: {e}")
        return False


# ---- GUI App ----
class YouTubeToPawinApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("✨ YouTube To Music Library ✨")
        self.geometry("660x540")
        self.resizable(False, False)
        self.configure(fg_color="#FFF5F7")

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("pink")

        self.token = None
        self.config = load_config()

        self._build_ui()
        self._restore_saved_login()

    def _build_ui(self):
        # Title
        title_label = ctk.CTkLabel(
            self, text="✨ YouTube To Music Library ✨",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color="#c9507a"
        )
        title_label.pack(pady=(24, 4))

        subtitle = ctk.CTkLabel(
            self, text="Upload YouTube audio straight to your Pawin-Tech Library 🎶",
            font=ctk.CTkFont(size=12), text_color="#b07090"
        )
        subtitle.pack(pady=(0, 16))

        # Login frame
        login_frame = ctk.CTkFrame(self, fg_color="#FFE8EF", corner_radius=16)
        login_frame.pack(padx=30, fill="x", pady=(0, 12))

        ctk.CTkLabel(login_frame, text="📧 Email", font=ctk.CTkFont(size=13, weight="bold"), text_color="#c9507a").pack(anchor="w", padx=20, pady=(16, 0))
        self.email_entry = ctk.CTkEntry(login_frame, placeholder_text="yourname@example.com", width=560, height=38, corner_radius=10, border_color="#f4a0b5", fg_color="white")
        self.email_entry.pack(padx=20, pady=(4, 0))

        ctk.CTkLabel(login_frame, text="🔒 Password", font=ctk.CTkFont(size=13, weight="bold"), text_color="#c9507a").pack(anchor="w", padx=20, pady=(10, 0))
        self.pass_entry = ctk.CTkEntry(login_frame, placeholder_text="••••••••", show="*", width=560, height=38, corner_radius=10, border_color="#f4a0b5", fg_color="white")
        self.pass_entry.pack(padx=20, pady=(4, 16))

        # URL frame
        url_frame = ctk.CTkFrame(self, fg_color="#FFE8EF", corner_radius=16)
        url_frame.pack(padx=30, fill="x", pady=(0, 12))

        ctk.CTkLabel(url_frame, text="🎬 YouTube URL", font=ctk.CTkFont(size=13, weight="bold"), text_color="#c9507a").pack(anchor="w", padx=20, pady=(16, 0))
        self.url_entry = ctk.CTkEntry(url_frame, placeholder_text="https://www.youtube.com/watch?v=...", width=560, height=38, corner_radius=10, border_color="#f4a0b5", fg_color="white")
        self.url_entry.pack(padx=20, pady=(4, 16))

        # Start button
        self.start_btn = ctk.CTkButton(
            self, text="🌸  Start Download & Upload  🌸",
            command=self._start_process,
            height=48, corner_radius=24,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#e87fa3", hover_color="#c9507a",
            text_color="white"
        )
        self.start_btn.pack(padx=30, fill="x", pady=(0, 12))

        # Log box
        self.log_box = ctk.CTkTextbox(self, height=120, corner_radius=12, fg_color="#FFF0F5", text_color="#7a3050", font=ctk.CTkFont(size=12))
        self.log_box.pack(padx=30, fill="x", pady=(0, 16))
        self.log_box.configure(state="disabled")

        # Version
        ctk.CTkLabel(self, text="Version 1 🌸", font=ctk.CTkFont(size=10), text_color="#d4a0b5").pack(pady=(0, 8))

    def _restore_saved_login(self):
        if self.config.get("username"):
            self.email_entry.insert(0, self.config["username"])
        if self.config.get("password"):
            self.pass_entry.insert(0, self.config["password"])

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _start_process(self):
        email = self.email_entry.get().strip()
        password = self.pass_entry.get().strip()
        url = self.url_entry.get().strip()

        if not email or not password:
            self.log("⚠️ Please enter your email and password!")
            return
        if not url:
            self.log("⚠️ Please paste a YouTube URL!")
            return

        self.start_btn.configure(state="disabled", text="⏳ Processing...")
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")
        self.log("🔑 Logging in...")

        threading.Thread(target=self._run_process, args=(email, password, url), daemon=True).start()

    def _run_process(self, email, password, url):
        token = login(email, password)
        if not token:
            self.log("❌ Login failed! Check your email and password.")
            self.after(0, lambda: self.start_btn.configure(state="normal", text="🌸  Start Download & Upload  🌸"))
            return

        self.log("✅ Login successful!")
        # Save credentials
        save_config({"username": email, "password": password})

        self.log("⏳ Downloading audio from YouTube...")

        upload_result = [False]

        class UploadPostProcessor(yt_dlp.postprocessor.PostProcessor):
            def __init__(self_pp):
                super().__init__()

            def run(self_pp, info):
                file_path = info.get('filepath')
                title = info.get('title', 'YouTube Audio')
                self.log(f"🎵 Downloaded: {title}")
                if file_path and os.path.exists(file_path):
                    self.log("📤 Uploading to Music Library...")
                    success = upload_audio(file_path, title, token, self.log)
                    upload_result[0] = success
                    try:
                        os.remove(file_path)
                    except:
                        pass
                return [], info

        ydl_opts = {
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s_%(id)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'js_runtimes': {'node': {}},
            'remote_components': ['ejs:github'],
            'extractor_args': {'youtube': {'player_client': ['web']}},
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.add_post_processor(UploadPostProcessor())
                ydl.download([url])
        except Exception as e:
            self.log(f"❌ Error: {e}")

        if upload_result[0]:
            self.log("🎉 All done! Check your Music Library!")
        else:
            self.log("⚠️ Process finished. Check the log above.")

        self.after(0, lambda: self.start_btn.configure(state="normal", text="🌸  Start Download & Upload  🌸"))


if __name__ == "__main__":
    app = YouTubeToPawinApp()
    app.mainloop()
