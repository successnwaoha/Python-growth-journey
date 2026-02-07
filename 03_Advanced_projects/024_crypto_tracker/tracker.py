import requests
import json
import os
from time import sleep

# 1. Configuration
BASE_URL = "https://api.coingecko.com/api/v3/simple/price"
# We'll stick to USD and NGN for this example
CURRENCIES = "usd,ngn" 

def load_portfolio():
    if not os.path.exists("portfolio.json"):
        print("Error: portfolio.json not found!")
        return {}
    with open("portfolio.json", "r") as f:
        return json.load(f)

def get_crypto_prices(coin_ids):
    ids_string = ",".join(coin_ids)
    
    # We send all currencies in ONE string separated by commas
    params = {
        "ids": ids_string,
        "vs_currencies": CURRENCIES,
        "include_24hr_change": "true"
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200: # Fixed the typo here
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def display_portfolio():
    portfolio = load_portfolio()
    if not portfolio: return

    prices = get_crypto_prices(portfolio.keys())
    if not prices: return

    print("\n" + "="*85)
    header = f"{'COIN':<12} {'PRICE (USD)':<15} {'ROI %':<10} {'PROFIT/LOSS':<15} {'VALUE (NGN)':<15}"
    print(header)
    print("-" * 85)

    total_usd = 0
    total_ngn = 0

    for coin, data in portfolio.items():
        # Get data from our JSON
        amount = data['amount']
        buy_price = data['buy_price']

        # Get live data from API
        coin_api_data = prices.get(coin, {})
        current_price_usd = coin_api_data.get("usd", 0)
        current_price_ngn = coin_api_data.get("ngn", 0)
        change_24h = coin_api_data.get("usd_24h_change", 0)

        # 1. Math for Profit/Loss (ROI)
        # ROI = ((Current - Bought) / Bought) * 100
        roi_percent = ((current_price_usd - buy_price) / buy_price) * 100
        profit_loss_usd = (current_price_usd - buy_price) * amount

        # 2. Total values
        value_usd = current_price_usd * amount
        value_ngn = current_price_ngn * amount
        total_usd += value_usd
        total_ngn += value_ngn
        
        # 3. Choose Emoji based on 24h change
        emoji = "🟢" if change_24h > 0 else "🔴"
        
        # Format the ROI and Profit strings
        roi_str = f"{roi_percent:+.2f}%"
        pl_str = f"${profit_loss_usd:+,.2f}"

        print(f"{emoji} {coin.capitalize():<10} ${current_price_usd:<14,.2f} {roi_str:<9} {pl_str:<14} ₦{value_ngn:,.2f}")

    print("-" * 85)
    print(f"TOTAL PORTFOLIO: ${total_usd:,.2f} | ₦{total_ngn:,.2f}")
    print("="*85 + "\n")

if __name__ == "__main__":
    while True:
        display_portfolio()
        print("Updating in 60 seconds... (Press Ctrl+C to stop)")
        sleep(60)