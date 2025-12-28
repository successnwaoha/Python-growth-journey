"""Manual tests for the scraper project without pytest.

Run: python3 run_manual_tests.py
"""
import os
import json
from types import SimpleNamespace

import scraper
import processor
import summary


class DummyResponse:
    def __init__(self, data, status_code=200):
        self._data = data
        self.status_code = status_code

    def json(self):
        return self._data


def fake_get(*args, **kwargs):
    return DummyResponse({"result": 820.25})


def main():
    # Monkeypatch requests.get
    scraper.requests.get = fake_get

    rate = scraper.fetch_rate()
    print('fetched rate:', rate)

    # write raw file
    os.makedirs('data/raw', exist_ok=True)
    data = {
        "base": "USD",
        "target": "NGN",
        "rate_raw": rate,
        "scraped_at": '2025-12-28 12:00:00',
        "source": 'exchangerate.host'
    }
    with open('data/raw/usd_ngn_raw.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    # run processor
    processor.clean_exchange_rate()

    # run summary
    print('summary:', summary.summarize())


if __name__ == '__main__':
    main()
