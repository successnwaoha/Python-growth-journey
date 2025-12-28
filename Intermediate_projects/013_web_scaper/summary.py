import pandas as pd
import os

PROCESSED_PATH = "data/processed/usd_ngn_processed.csv"


def summarize(path: str = PROCESSED_PATH) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError("Processed CSV not found. Run processor.clean_exchange_rate() first.")

    df = pd.read_csv(path)
    if df.empty:
        return {}

    rates = df['rate'].astype(float)
    result = {
        'count': int(rates.count()),
        'min': float(rates.min()),
        'max': float(rates.max()),
        'mean': float(rates.mean())
    }
    return result


if __name__ == '__main__':
    print(summarize())
