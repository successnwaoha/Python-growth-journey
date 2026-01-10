import types
import pytest

import scraper


class DummyResponse:
    def __init__(self, data, status_code=200):
        self._data = data
        self.status_code = status_code

    def json(self):
        return self._data


def test_fetch_rate_from_result(monkeypatch):
    data = {"result": 832.5}

    def fake_get(*args, **kwargs):
        return DummyResponse(data)

    monkeypatch.setattr('requests.get', fake_get)

    rate = scraper.fetch_rate()
    assert isinstance(rate, str)
    assert float(rate) == 832.5


def test_fetch_rate_from_info(monkeypatch):
    data = {"info": {"rate": 832.75}}

    def fake_get(*args, **kwargs):
        return DummyResponse(data)

    monkeypatch.setattr('requests.get', fake_get)

    rate = scraper.fetch_rate()
    assert isinstance(rate, str)
    assert float(rate) == 832.75


def test_fetch_rate_raises_after_retries(monkeypatch):
    # Simulate non-200 responses
    class BadResponse:
        def __init__(self):
            self.status_code = 500
            self.text = ""

        def json(self):
            return {}

    call_count = {"n": 0}

    def fake_get(*args, **kwargs):
        call_count["n"] += 1
        return BadResponse()

    monkeypatch.setattr('requests.get', fake_get)

    with pytest.raises(RuntimeError):
        scraper.fetch_rate()
    assert call_count["n"] >= scraper.MAX_RETRIES


def test_fetch_rate_from_rates_key(monkeypatch):
    data = {"rates": {"NGN": 833.1}}

    def fake_get(*args, **kwargs):
        return DummyResponse(data)

    monkeypatch.setattr('requests.get', fake_get)

    rate = scraper.fetch_rate()
    assert isinstance(rate, str)
    assert float(rate) == 833.1
