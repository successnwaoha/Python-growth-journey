def normalize_rate_str(rate_str: str) -> float:
    """Normalize a rate string (may contain commas) to a float.

    Examples:
        '1,234.56' -> 1234.56
        '820.5' -> 820.5
    """
    if rate_str is None:
        raise ValueError("rate_str is None")

    cleaned = str(rate_str).replace(",", "").strip()
    if not cleaned:
        raise ValueError("Empty rate string")

    return float(cleaned)
