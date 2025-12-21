import csv
import os

print("-" * 50)
print("💼 Welcome to the Personal Finance Manager App!")
print("-" * 50)

def display_menu():
    print("\nWhat would you like to do?")
    print("1. Add Expense ➕")
    print("2. View Expenses 📄")
    print("3. View total Expenses 💵")
    print("4. View Total by Category 📊")
    print("5. View Total by Date 📅")
    print("6. Sort by Amount 📈")
    print("7. Exit 🚪")

CSV_FILE = "personal_finance.csv"