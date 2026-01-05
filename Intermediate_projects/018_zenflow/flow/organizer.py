import yaml
import shutil
import json  # New import
from pathlib import Path
from datetime import datetime

# Define where to save the "undo" data
HISTORY_FILE = Path(__file__).parent.parent / "undo_history.json"

def run_organizer(dry_run=False):
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    rules = config['rules']
    source_dir = Path(config['source_path']).expanduser()
    
    moved_files_log = []
    undo_data = [] # We will store { "from": "...", "to": "..." } here

    for file_path in source_dir.iterdir():
        if file_path.is_file():
            ext = file_path.suffix.lower()
            for folder_name, extensions in rules.items():
                if ext in extensions:
                    dest_folder = source_dir / folder_name
                    
                    if not dry_run:
                        dest_folder.mkdir(exist_ok=True)
                        new_location = dest_folder / file_path.name
                        
                        if not new_location.exists():
                            # Record the paths BEFORE moving
                            undo_data.append({
                                "old": str(file_path),
                                "new": str(new_location)
                            })
                            
                            shutil.move(str(file_path), str(new_location))
                            # ... (your logging code here) ...

    # Save the undo data to a file
    if undo_data:
        with open(HISTORY_FILE, "w") as f:
            json.dump(undo_data, f)

def run_undo():
    if not HISTORY_FILE.exists():
        print("Nothing to undo!")
        return

    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    for entry in history:
        if Path(entry["new"]).exists():
            shutil.move(entry["new"], entry["old"])
            print(f"Restored: {Path(entry['old']).name}")

    # Delete history after undoing so we don't undo the same thing twice
    HISTORY_FILE.unlink()
    print("Undo complete.")