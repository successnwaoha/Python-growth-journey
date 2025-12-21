print("\n-" * 35)
print("📒 Welcome to the Contact Book App!")
print("-" * 35)

def display_menu():
    print ("\nWhat would you like to do?")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Search Contact")
    print("4. Delete Contact")
    print("5. Exit")

contacts = {
    "Alice": {
    "phone": "123-456-7890", "email": "alice@example.com"
    },
    "Bob": {
    "phone": "987-654-3210", "email": "bob@example.com"
    }
        }
        
while True:
    display_menu()
    try:
        choice = int(input("Enter your choice (1-5): "))
        while choice > 5 or choice < 1:
            print("Invalid choice. Please select a number between 1 and 5.")
            choice = int(input("Enter your choice (1-5): "))
        if choice == 1:
            name = input("Enter contact name: ").capitalize()
            if name in contacts:
                overwrite = input(f"Contact '{name}' already exists, do you want to overwrite it? (yes/no): ").lower()
                if overwrite != "yes":
                    continue
            phone = input("Enter contact phone number: ")
            email = input("Enter contact email address: ")
            contacts[name] = {"phone": phone, "email": email}
            print(f"Contact '{name}' added successfully!")
        elif choice == 2:
            if not contacts:
                print("No contacts available.")
            else:
                print("\nYour Contacts:")
                for name, info in contacts.items():
                    print(f"\nName: {name}, \nPhone: {info['phone']}, Email: {info['email']}")
        elif choice == 3:
            search_name = input("Enter the name of the contact to search: ").capitalize()
            if search_name in contacts:
                info = contacts[search_name]
                print(f"Found Contact - \nName: {search_name}, \nPhone: {info['phone']}, Email: {info['email']}")
            else:
                print(f"Contact '{search_name}' not found.")
        elif choice == 4:
            delete_name = input("Enter the name of the contact to delete: ").capitalize()
            if delete_name in contacts:
                confirm = input("Are you sure you want to delete this contact? (yes/no): ): ").lower()
                if confirm == "yes":
                    del contacts[delete_name]
                    print(f"Contact '{delete_name}' deleted successfully.")
                else:
                    print("Deletion cancelled.")
            else:
                print(f"Contact '{delete_name}' not found.")
        elif choice == 5:
            print("Exiting the Contact Book App. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 5.")
    except ValueError:
        print("Please enter a valid integer.")

