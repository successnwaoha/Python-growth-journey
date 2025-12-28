import json
import pandas as pd
import os
from datetime import datetime

RAW_PATH = "data/raw/usd_ngn_raw.json"
PROCESSED_PATH = "data/processed/usd_ngn_processed.csv"

def clean_exchange_rate():
    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError("Raw data not found. Run scraper.py first.")

    with open(RAW_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
    rate_str = raw["rate_raw"]

    from cleaner import normalize_rate_str
    rate = normalize_rate_str(rate_str)

    if rate <= 0:
        raise ValueError("Invalid exchange rate in raw data")

    cleaned = {
        "base": raw["base"],
        "target": raw["target"],
        "rate": rate,
        "date": raw["scraped_at"].split(" ")[0],
        "time": raw["scraped_at"].split(" ")[1],
        "source": raw["source"],
        "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    df = pd.DataFrame([cleaned])

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    print("✅ Data cleaned and saved")
    print(df)

if __name__ == "__main__":
    clean_exchange_rate()
