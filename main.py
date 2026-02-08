import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import threading
# Optional for future sound playback
# from playsound import playsound

# -------------------------------
# Keywords
# -------------------------------

EMERGENCY_KEYWORDS = ["fire", "help", "danger", "alarm", "look out"]
NAME_WORDS = ["mom", "dad", "sister", "brother", "friend"]
TIME_WORDS = ["tomorrow", "monday", "soon", "later", "tonight"]

listening = False

# -------------------------------
# Sound Databases / Resources
# -------------------------------

# Emergency and environmental sounds for testing:
# Epidemic Sound: One of the databases used for sound (https://www.epidemicsound.com)
# Zapsplat: One of the databases used for sound (https://www.zapsplat.com)

# Example placeholders for future integration:
# DOORBELL_SOUND = "sounds/doorbell.mp3"  # from Epidemic Sound or Zapsplat
# FIRE_ALARM_SOUND = "sounds/fire_alarm.mp3"  # from Epidemic Sound or Zapsplat

# -------------------------------
# Main Window Setup
# -------------------------------

root = tk.Tk()
root.title("ClearConnect - Live Captions + Alerts")
root.geometry("800x600")
root.resizable(False, False)

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

title_label = tk.Label(main_frame, text="ClearConnect", font=("Helvetica", 26, "bold"))
title_label.pack(pady=10)

status_label = tk.Label(main_frame, text="Status: Ready", fg="black", font=("Arial", 14))
status_label.pack(pady=5)

caption_label = tk.Label(main_frame, text="Live Captions:", font=("Arial", 14, "bold"))
caption_label.pack(anchor="w", pady=(15, 5))

caption_box = scrolledtext.ScrolledText(
    main_frame,
    width=85,
    height=12,
    state="disabled",
    font=("Arial", 12),
    wrap="word"
)
caption_box.pack(pady=5)

alert_label = tk.Label(main_frame, text="No alerts", bg="lightgray", font=("Arial", 14), width=50, height=2)
alert_label.pack(pady=15)

# -------------------------------
# Display Captions with Highlight
# -------------------------------

def display_caption(text):
    caption_box.configure(state="normal")
    start_index = caption_box.index(tk.END)
    caption_box.insert(tk.END, text + "\n")

    # Highlight Emergency Keywords
    for word in EMERGENCY_KEYWORDS:
        idx = start_index
        while True:
            idx = caption_box.search(word, idx, nocase=1, stopindex=tk.END)
            if not idx:
                break
            end_idx = f"{idx}+{len(word)}c"
            caption_box.tag_add("emergency", idx, end_idx)
            idx = end_idx

    # Highlight Names
    for word in NAME_WORDS:
        idx = start_index
        while True:
            idx = caption_box.search(word, idx, nocase=1, stopindex=tk.END)
            if not idx:
                break
            end_idx = f"{idx}+{len(word)}c"
            caption_box.tag_add("name", idx, end_idx)
            idx = end_idx

    # Highlight Time Words
    for word in TIME_WORDS:
        idx = start_index
        while True:
            idx = caption_box.search(word, idx, nocase=1, stopindex=tk.END)
            if not idx:
                break
            end_idx = f"{idx}+{len(word)}c"
            caption_box.tag_add("time", idx, end_idx)
            idx = end_idx

    # Configure tag styles
    caption_box.tag_config("emergency", foreground="red", font=("Arial", 12, "bold"))
    caption_box.tag_config("name", foreground="blue", font=("Arial", 12, "bold"))
    caption_box.tag_config("time", foreground="green", font=("Arial", 12, "bold"))

    caption_box.see(tk.END)
    caption_box.configure(state="disabled")

# -------------------------------
# Flash Emergency Effect
# -------------------------------

def flash_alert():
    alert_label.config(bg="red")
    root.after(500, lambda: alert_label.config(bg="lightgray"))

# -------------------------------
# Keyword Detection
# -------------------------------

def check_keywords(text):
    lower_text = text.lower()
    for word in EMERGENCY_KEYWORDS:
        if word in lower_text:
            alert_label.config(text=f"🚨 EMERGENCY: {word.upper()}!")
            flash_alert()
            return

    for word in NAME_WORDS:
        if word in lower_text:
            alert_label.config(text=f"👤 Name Mentioned: {word}")
            return

    for word in TIME_WORDS:
        if word in lower_text:
            alert_label.config(text=f"⏰ Time Reference: {word}")
            return

    alert_label.config(text="No alerts")

# -------------------------------
# Speech Recognition Loop
# -------------------------------

def listen_loop():
    global listening
    recognizer = sr.Recognizer()
    
    try:
        microphone = sr.Microphone()
    except OSError:
        display_caption("[Error: No microphone found]")
        return

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)

    while listening:
        try:
            with microphone as source:
                audio = recognizer.listen(source, phrase_time_limit=5)
            text = recognizer.recognize_google(audio)
            display_caption("You said: " + text)
            check_keywords(text)
        except sr.UnknownValueError:
            display_caption("[Could not understand audio]")
        except sr.RequestError:
            display_caption("[Speech service unavailable]")
        except Exception as e:
            display_caption(f"[Error: {e}]")

# -------------------------------
# Start / Stop Buttons
# -------------------------------

def start_listening():
    global listening
    listening = True
    status_label.config(text="Status: Listening...", fg="green")
    thread = threading.Thread(target=listen_loop)
    thread.daemon = True
    thread.start()

def stop_listening():
    global listening
    listening = False
    status_label.config(text="Status: Stopped", fg="red")
    alert_label.config(text="No alerts")

# -------------------------------
# Fake Environmental Alerts
# -------------------------------

def doorbell_alert():
    alert_label.config(text="🔔 Doorbell Detected!")
    # Future integration: play sound from Epidemic Sound / Zapsplat
    # playsound(DOORBELL_SOUND)

def fire_alarm_alert():
    alert_label.config(text="🚨 Fire Alarm Detected!")
    flash_alert()
    # Future integration: play sound from Epidemic Sound / Zapsplat
    # playsound(FIRE_ALARM_SOUND)

# -------------------------------
# Buttons Frame
# -------------------------------

button_frame = tk.Frame(main_frame)
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="Start Listening", command=start_listening, font=("Arial", 12), width=18)
start_button.grid(row=0, column=0, padx=10, pady=5)

stop_button = tk.Button(button_frame, text="Stop Listening", command=stop_listening, font=("Arial", 12), width=18)
stop_button.grid(row=0, column=1, padx=10, pady=5)

doorbell_button = tk.Button(button_frame, text="Test Doorbell Alert", command=doorbell_alert, font=("Arial", 12), width=18)
doorbell_button.grid(row=1, column=0, padx=10, pady=5)

fire_button = tk.Button(button_frame, text="Test Emergency Alarm", command=fire_alarm_alert, font=("Arial", 12), width=18)
fire_button.grid(row=1, column=1, padx=10, pady=5)

# -------------------------------
# Run App
# -------------------------------

root.mainloop()
