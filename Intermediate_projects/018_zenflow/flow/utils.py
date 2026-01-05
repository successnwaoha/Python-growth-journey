import json
import shutil
from pathlib import Path

HISTORY_FILE = Path.home() / ".flow_history.json"

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

def undo_moves():
    if not HISTORY_FILE.exists():
        print("No history found.")
        return

    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)

    for original, current in history:
        if Path(current).exists():
            shutil.move(current, original)
            print(f"Restored: {original}")
    
    HISTORY_FILE.unlink() # Delete history after undo