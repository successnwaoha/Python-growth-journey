import csv
import os

CSV_FILE = "expenses.csv"

expenses = []


def load_expenses():
    """Load existing expenses from CSV into the `expenses` list."""
    if not os.path.exists(CSV_FILE):
        return
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                amount = float(row.get("amount", 0))
            except (TypeError, ValueError):
                # skip malformed rows
                continue
            expenses.append({
                "amount": amount,
                "category": row.get("category", "").lower(),
                "description": row.get("description", ""),
                "date": row.get("date", ""),
            })


def save_expenses():
    """Write the in-memory `expenses` list to CSV (overwrites file)."""
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ["amount", "category", "description", "date"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for expense in expenses:
            writer.writerow({
                "amount": expense["amount"],
                "category": expense.get("category", ""),
                "description": expense.get("description", ""),
                "date": expense.get("date", ""),
            })

def display_menu():
    print("\nWhat would you like to do?")
    print("1. Add Expense ➕")
    print("2. View Expenses 📄")
    print("3. View total Expenses 💵")
    print("4. View Total by Category 📊")
    print("5. View Total by Date 📅")
    print("6. Sort by Amount 📈")
    print("7. Exit 🚪")

print("-" * 40)
print("💰 Welcome to the Expense Tracker App!")
print("-" * 40)

# load existing expenses if any
load_expenses()

while True:
    display_menu()
    try:
        choice = int(input("Enter your choice (1-7): "))
        while choice > 7 or choice < 1:
            print("Invalid choice. Please select a number between 1 and 7.")
            choice = int(input("Enter your choice (1-7): "))
        if choice == 1:
            try:
                amount = float(input("Enter expense amount: "))
                if amount <= 0:
                    print("Amount must be positive. Try again.")
                    continue
            except ValueError:
                print("Invalid amount. Please enter a numeric value.")
                continue
            category = input("Enter expense category (e.g., food, transport): ").lower()
            description = input("Enter expense description: ")
            date = input("Enter expense date (YYYY-MM-DD): ")
            expenses.append({
                "amount": amount,
                "category": category,
                "description": description,
                "date": date,
            })
            # persist immediately
            save_expenses()
            print(f"Expense of {amount} added successfully and saved to {CSV_FILE}!")
        elif choice == 2:
            if not expenses :
                print("No expenses recorded yet.")
            else:
                print("\nYour Expenses:")
                for idx, expense in enumerate(expenses, start=1):
                    print(f"{idx}. Amount: {expense['amount']}, Category: {expense['category']}, Description: {expense['description']}, Date: {expense['date']}")
        elif choice == 3:
            total_expense = sum(expense["amount"] for expense in expenses)
            print(f"\nTotal Expenses: {total_expense}")
        elif choice == 4:
            category_totals = {}
            for expense in expenses:
                category = expense["category"]
                category_totals[category] = category_totals.get(category, 0) + expense["amount"]
            print("\nTotal Expenses by Category:")
            for category, total in category_totals.items():
                print(f"{category.capitalize()}: {total}")
        elif choice == 5:
            date_totals = {}
            for expense in expenses:
                date = expense["date"]
                date_totals[date] = date_totals.get(date, 0) + expense["amount"]
            print("\nTotal Expenses by Date:")
            for date, total in date_totals.items():
                print(f"{date}: {total}")
        elif choice == 6:
            sorted_expenses = sorted(expenses, key=lambda x: x["amount"])
            print("\nExpenses Sorted by Amount:")
            for expense in sorted_expenses:
                print(f"Amount: {expense['amount']}, Category: {expense['category']}, Description: {expense['description']}, Date: {expense['date']}")
        elif choice == 7:
            # persist on exit (in case anything changed)
            save_expenses()
            print("Exiting the Expense Tracker App. Goodbye!")
            break
    except ValueError:
        print("Please enter a valid integer.")