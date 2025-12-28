import os
import json
import pandas as pd
import pytest

import processor


def test_clean_exchange_rate_creates_csv(tmp_path, monkeypatch):
    raw = {
        "base": "USD",
        "target": "NGN",
        "rate_raw": "820.5",
        "scraped_at": "2025-12-28 12:00:00",
        "source": "exchangerate.host"
    }

    raw_dir = tmp_path / "data" / "raw"
    raw_dir.mkdir(parents=True)
    raw_file = raw_dir / "usd_ngn_raw.json"
    with open(raw_file, 'w', encoding='utf-8') as f:
        json.dump(raw, f)

    processed_dir = tmp_path / "data" / "processed"
    processed_file = processed_dir / "usd_ngn_processed.csv"

    # monkeypatch module-level paths
    monkeypatch.setattr(processor, 'RAW_PATH', str(raw_file))
    monkeypatch.setattr(processor, 'PROCESSED_PATH', str(processed_file))

    processor.clean_exchange_rate()

    assert processed_file.exists()
    df = pd.read_csv(processed_file)
    assert df['rate'].iloc[0] == 820.5
    assert df['base'].iloc[0] == 'USD'
