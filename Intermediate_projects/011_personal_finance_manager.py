import json
import datetime

print("-" * 50)
print("   💼 Welcome to the Personal Finance Manager App!")
print("-" * 50)

finance_data = {
    "incomes": [],
    "expenses": []
}

def load_data():
    """Loads JSON or creates default data structure."""
    try:
        with open("finance_data.json", "r", encoding="utf-8") as finance_file:
            data = json.load(finance_file)
            if "incomes" not in data or "expenses" not in data:
                raise ValueError("Invalid data structure")
            return data
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return {
            "incomes": [],
            "expenses": []
        }
        
def save_data():
    """Saves finance data to JSON."""
    with open("finance_data.json", "w", encoding="utf-8") as finance_file:
        json.dump(finance_data, finance_file, indent=4)

def display_menu():
    """Display the main menu options"""
    print("Please choose an option:")
    print ("1. Add income")
    print ("2. View income")
    print ("3. Add expense")
    print ("4. View expenses")
    print ("5. Monthly summary")
    print ("6. Balance")
    print ("7. Exit")

def add_income():
    """Add a new income entry. """
    while True:
        try:
            amount = float(input("Enter income amount: "))
            if amount <= 0:
                print("Please enter a valid positive amount.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    category = input("Enter income source/category: ")
    description = input("Enter description: ")
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    finance_data["incomes"].append({
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    })
    save_data()
    print("Income added successfully!")
    
def view_incomes():
    """View all recorded incomes."""
    if not finance_data["incomes"]:
        print("No incomes recorded.")
        return
    print("\nIncomes:")
    for idx, income in enumerate(finance_data["incomes"], start=1):
        print(f"{idx}. Amount: ₦{income['amount']:,} \nCategory: {income['category']} \nDescription: {income['description']} \nDate: {income['date']}")
    print()
    
def add_expense():
    """Add a new expense entry."""
    while True:
        try:
            amount = float(input("Enter expense amount: "))
            if amount <= 0:
                print("Please enter a valid positive amount.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    category = input("Enter expense category: ")
    description = input("Enter description: ")
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    finance_data["expenses"].append({
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    })
    save_data()
    print("Expense added successfully!")

def view_expenses():
    """View all recorded expenses."""
    if not finance_data["expenses"]:
        print("No expenses recorded.")
        return
    print("\nExpenses:")
    for idx, expense in enumerate(finance_data["expenses"], start=1):
        print(f"{idx}. ₦{expense['amount']:,} \nCategory: {expense['category']} \nDescription: {expense['description']} \nDate: {expense['date']}")
    print()

def monthly_summary():
    """Ask for month and year, then display total incomes and expenses."""
    month = input("Enter month (MM): ")
    year = input("Enter year (YYYY): ")
    total_income = sum(income["amount"] for income in finance_data["incomes"] if income["date"].startswith(f"{year}-{month}"))
    total_expense = sum(expense["amount"] for expense in finance_data["expenses"] if expense["date"].startswith(f"{year}-{month}"))
    print(f"\nSummary for {month}-{year}:")
    print(f"Total Income: ₦{total_income:,}")
    print(f"Total Expenses: ₦{total_expense:,}")
    print(f"Net Balance: ₦{total_income - total_expense:,}\n")

def view_balance():
    """Display income, expense, and overall balance."""
    total_income = sum(income["amount"] for income in finance_data["incomes"])
    total_expense = sum(expense["amount"] for expense in finance_data["expenses"])
    print(f"\nOverall Balance:")
    print(f"Total Income: ₦{total_income:,}")
    print(f"Total Expenses: ₦{total_expense:,}")
    print(f"Net Balance: ₦{total_income - total_expense:,}\n")

def exit_app():
    """Save data and exit the application."""
    save_data()
    print("Data saved. Exiting the Personal Finance Manager. Goodbye!")
    exit()

finance_data = load_data()
while True:
    display_menu()
    while True:
        try:            
            choice = int(input("Enter your choice (1-7): "))
            if choice < 1 or choice > 7:
                print("Please enter a number between 1 and 7.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    if choice == 1:
        add_income()
    elif choice == 2:
        view_incomes()
    elif choice == 3:
        add_expense()
    elif choice == 4:
        view_expenses()
    elif choice == 5:
        monthly_summary()
    elif choice == 6:
        view_balance()
    elif choice == 7:
        exit_app()