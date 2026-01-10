import random

characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-+"
lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
special_characters = "!@#$%^&*()-+"
print("+********************************************************+")
print("|         Welcome to the Password Generator!             |")
print("+********************************************************+")

def generate_password():
    password = []
    try:
        length = int(input("Enter the desired password length (minimum 6): "))
        if length < 6 or length > 30:
            print("Password length must be at least 6 and at most 30. Please try again.")
            return
        else:
            password += random.choice(lowercase)
            password += random.choice(uppercase)
            password += random.choice(digits)
            password += random.choice(special_characters)
            for _ in range(length - 4):
                password += random.choice(characters)
            random.shuffle(password)
            final_password = ''.join(password)
            print ("Your new password is ready 🔐")
            print(f"Generated Password: {final_password}")
    except ValueError:
        print("Please enter a valid integer.")

while True:
    generate_password()
    again = input("Do you want to generate another password? (yes/no): ").strip().lower()
    if again != "yes":
        print("Thank you for using the Password Generator! Goodbye!")
        break