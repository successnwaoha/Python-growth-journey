currencies = {
    "USD": 1.0,
    "EUR": 0.85,
    "GBP": 0.74,
    "JPY": 154.74,
    "NGN": 1500.0,
    }

print("-" * 45)
print("💱 Welcome to the Currency Converter App!")
print("-" * 45)

def display_menu():
    print("\nWhat would you like to do?")
    print("1. Convert Currency")
    print("2. View Supported Currencies")
    print("3. Exit")

def display_supported_currencies():
    print("\nSupported Currencies:")
    for currency in currencies.keys():
        print(f"- {currency}")
def currency_converter():
    try:
        choice = int(input("Enter your choice (1-3): "))
        while choice > 3 or choice < 1:
            print("Invalid choice. Please select a number between 1 and 3.")
            choice = int(input("Enter your choice (1-3): "))
        if choice == 1:
            from_currency = input("Enter the currency you want to convert from (e.g., USD): ").upper()
            to_currency = input("Enter the currency you want to convert to (e.g., EUR): ").upper()
            if from_currency == to_currency:
                print("Both currencies are the same. No conversion needed.")
                return
            while True:
                try:
                    amount = float(input("Enter the amount to convert: "))
                    break
                except ValueError:
                    print("Invalid amount. Please enter a numeric value.")
            if from_currency in currencies and to_currency in currencies:
                converted_amount = (amount / currencies[from_currency]) * currencies[to_currency]
                print(f"{amount:.2f} {from_currency} is equal to {converted_amount:.2f} {to_currency}.")
            else:
                print("One or both of the specified currencies are not supported.")
                display_supported_currencies()
        elif choice == 2:
            display_supported_currencies()
        elif choice == 3:
            print("Exiting the Currency Converter App. Goodbye!")
            exit()
    except ValueError:
        print("Invalid input. Please enter numeric values where required.")

while True:
    display_menu()
    currency_converter()
    again = input("\nDo you want to perform another operation? (yes/no): ").lower()
    if again != "yes":
        print("Thank you for using the Currency Converter App! Goodbye!")
        break
    