import cleaner
import pytest


def test_normalize_rate_str():
    assert cleaner.normalize_rate_str('1,234.56') == 1234.56
    assert cleaner.normalize_rate_str('820.5') == 820.5

    with pytest.raises(ValueError):
        cleaner.normalize_rate_str('')

    with pytest.raises(ValueError):
        cleaner.normalize_rate_str(None)
