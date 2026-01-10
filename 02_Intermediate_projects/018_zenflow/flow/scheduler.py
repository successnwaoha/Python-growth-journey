import os
import time
import yaml
from pathlib import Path
from datetime import datetime, timedelta

def send_mac_notification(title, message):
    command = f'display notification "{message}" with title "{title}"'
    os.system(f"osascript -e '{command}'")

def start_scheduler():
    # 1. Load the config
    # We use .. because config.yaml is one folder up from 'flow/'
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    reminders = config.get('reminders', [])
    
    # 1. We add a "last_notified" timestamp to every task in our memory
    for item in reminders:
        # We pretend we just notified them now so the timer starts from now
        item['last_notified'] = datetime.now()

    print(f"Scheduler active. Checking reminders...")
    
    # 2. The simple loop
    # For now, we will just check every 60 seconds
    while True:
        now = datetime.now()
        
        for item in reminders:
            task = item['task']
            interval = item['interval_minutes']
            last_run = item['last_notified']
            
            # 2. Check: Has 'interval' minutes passed since 'last_run'?
            if now >= last_run + timedelta(minutes=interval):
                send_mac_notification("ZenFlow", f"Time to: {task}")
                print(f"[{now.strftime('%H:%M:%S')}] Triggered: {task}")
                
                # 3. Update the 'last_notified' time to NOW
                item['last_notified'] = now
        
        # Sleep for just 10 seconds before checking again
        # This way, we never miss a reminder by more than 10 seconds
        time.sleep(10)

if __name__ == "__main__":
    start_scheduler()