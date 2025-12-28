import time
import requests
from datetime import datetime
import json
import random

URL = "https://api.exchangerate.host/convert?from=USD&to=NGN"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
MAX_RETRIES = 5


def fetch_rate():
    """Fetch the USD->NGN rate from exchangerate.host and return it as a string.

    The endpoint returns JSON; we try to extract the numeric rate from either the
    'result' field or 'info.rate'. Returns the rate as a plain string (no commas)
    to keep compatibility with the downstream `processor` which expects a string.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(URL, headers=HEADERS, timeout=10)

            if response.status_code != 200:
                raise ValueError("Non-200 response")

            # Parse JSON response instead of scraping HTML
            try:
                data = response.json()
            except ValueError:
                data = None

            rate_val = None
            # Common shapes from exchangerate.host
            if isinstance(data, dict):
                if "result" in data and data["result"] is not None:
                    rate_val = data["result"]
                elif "info" in data and isinstance(data["info"], dict) and "rate" in data["info"]:
                    rate_val = data["info"]["rate"]
                elif "rates" in data and isinstance(data["rates"], dict) and "NGN" in data["rates"]:
                    rate_val = data["rates"]["NGN"]

            # Fallback: try to find a number in the text body
            if rate_val is None:
                import re
                m = re.search(r"(\d+[\d,]*\.?\d*)", response.text)
                if m:
                    rate_val = m.group(1).replace(",", "")

            if rate_val is None:
                # Include a short preview of the response to help debug
                preview = (response.text[:200] + "...") if len(response.text) > 200 else response.text
                raise ValueError(f"Rate not found in JSON response - preview: {preview}")

            # Validation
            rate = float(rate_val)
            if rate <= 0:
                raise ValueError("Invalid rate value")

            # Return as plain string (no commas)
            return f"{rate:.6f}".rstrip("0").rstrip(".")

        except Exception as e:
            wait = 2 ** attempt + random.random()
            print(f"⚠️ Attempt {attempt} failed: {e}. Retrying in {wait:.1f}s...")
            time.sleep(wait)

    raise RuntimeError("❌ Failed to fetch exchange rate after retries")

if __name__ == "__main__":
    rate_raw = fetch_rate()

    data = {
        "base": "USD",
        "target": "NGN",
        "rate_raw": rate_raw,
        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": "exchangerate.host"
    }

    # Ensure directory exists
    import os
    os.makedirs("data/raw", exist_ok=True)

    with open("data/raw/usd_ngn_raw.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("✅ Raw exchange rate data saved")
