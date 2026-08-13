import pyperclip
import time
import yt_dlp
import os
import shutil
from win10toast import ToastNotifier  # <--- NEW LIBRARY

# ===========================
# ⚙️ CONFIGURATION
# ===========================
BATCH_ID = "082"
USERNAMES = [
    "nja__mbi", "yvonne_njeka", "mnyama.mkali66", "official_nyambura", 
    "dee.sassy1", "eunny_szn", "ivymukash", "queenlavie5",
    "wowcollection01", "trivahnjoki", "lovelylinet1", "lushieynyambu"
]

BASE_DIR = os.path.join(os.path.expanduser("~"), "Videos", "tt", BATCH_ID)
# ===========================

# Initialize the Notifier
toaster = ToastNotifier()

def send_phone_notification(title, message):
    """Sends a notification to Windows, which KDE Connect forwards to Phone"""
    try:
        # threaded=True prevents the script from freezing while the popup is shown
        toaster.show_toast(title, message, duration=5, threaded=True)
    except Exception as e:
        print(f"⚠️ Could not send notification: {e}")

def download_and_sort(link):
    print(f"\n🚀 Link detected: {link}")
    
    # notify phone that download started
    send_phone_notification("TikTok Downloader", "⬇️ Download Started...")

    ydl_opts = {
        "format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "outtmpl": os.path.join(BASE_DIR, "%(uploader)s_%(id)s.%(ext)s"),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            filename = ydl.prepare_filename(info)
            
            pre, ext = os.path.splitext(filename)
            if not os.path.exists(filename):
                filename = pre + ".mp4"

            uploader = info.get("uploader", "unknown")

            if uploader in USERNAMES:
                target_subfolder = uploader
            else:
                target_subfolder = "others"
            
            destination_folder = os.path.join(BASE_DIR, target_subfolder)
            os.makedirs(destination_folder, exist_ok=True)
            
            final_path = os.path.join(destination_folder, os.path.basename(filename))
            
            if os.path.exists(final_path):
                try:
                    os.remove(final_path)
                except:
                    pass
            
            shutil.move(filename, final_path)
            
            success_msg = f"✅ Saved to: {target_subfolder}"
            print(success_msg)
            
            # --- NOTIFY PHONE HERE ---
            send_phone_notification("Download Complete!", f"Video saved in: {target_subfolder}")

    except Exception as e:
        error_msg = f"❌ Failed: {str(e)}"
        print(error_msg)
        # Notify phone of failure
        send_phone_notification("Download Failed", "Check PC console for details.")

def main():
    print(f"👀 Watching Clipboard for TikTok links...")
    print(f"📂 Saving to: {BASE_DIR}")
    print("------------------------------------------")

    last_text = pyperclip.paste()

    try:
        while True:
            try:
                current_text = pyperclip.paste()
                
                if current_text != last_text:
                    last_text = current_text
                    
                    if "tiktok.com" in current_text:
                        download_and_sort(current_text)
                    else:
                        pass 

                time.sleep(1.0) 
            
            except KeyboardInterrupt:
                break
            except Exception as loop_error:
                print(f"⚠️ Clipboard error: {loop_error}")
                time.sleep(2)
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping watcher.")

if __name__ == "__main__":
    main()