import requests
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime

# 1. Configuration - A list of URLs to track
URLS = [
    "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    "https://books.toscrape.com/catalogue/the-dirty-little-secrets-of-getting-your-dream-job_994/index.html"
]
TARGET_PRICE = 50.0

def check_prices():
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # Loop through each URL in our list
    for url in URLS:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Get the title of the book so we know which one we are looking at
        title = soup.find("h1").get_text()
        
        # Get price text
        price_text = soup.find("p", class_="price_color").get_text()
        
        # PRO FIX: Keep only digits and decimal points (ignores Â, £, etc.)
        # This joins only the characters that are digits or a dot
        price_numeric = "".join(char for char in price_text if char.isdigit() or char == ".")
        price = float(price_numeric)
        
        print(f"Book: {title} | Price: £{price}")

        # Save to CSV
        log_to_csv(title, price)

        if price < TARGET_PRICE:
            send_alert(title, price, url)

def log_to_csv(title, price):
    file_exists = False
    try:
        with open("price_history.csv", "r") as f:
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    with open("price_history.csv", "a", newline="") as f:
        writer = csv.writer(f)
        # If the file is new, write the header first
        if not file_exists:
            writer.writerow(["Timestamp", "Book Title", "Price"])
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, title, price])

def send_alert(title, price, url):
    print(f"--- ALERT: {title} dropped to £{price}! Buy here: {url} ---")

if __name__ == "__main__":
    print("Tracker started...")
    while True:
        check_prices()
        print("Done checking. Waiting 1 hour...")
        time.sleep(3600)