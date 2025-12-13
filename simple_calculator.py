print ("Hi there! Welcome to the Simple Calculator.")

def add(a, b):
    return a + b
def subtract(a, b):
    return a - b
def multiply(a, b):
    return a * b
def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "Error! Division by zero."

def calculate():
    print ("\nWhat operation would you like to perform?")
    print ("1. Addition")
    print ("2. Subtraction")
    print ("3. Multiplication")
    print ("4. Division")
    while True:
        operation = input("\nEnter the number corresponding to the operation (1/2/3/4): ")
        if operation in ['1', '2', '3', '4']:
            if operation == '1':
                print ("Addition? Let's gooooo!")
            if operation == '2':
                print ("Subtraction? You got it!")
            if operation == '3':
                print ("Multiplication? Awesome choice!")
            if operation == '4':
                print ("Division eh? Here we go!")
            break
        else:
            print("Invalid input. Please enter 1, 2, 3, or 4.")
    while True:
        try:
            num1 = float(input("\nEnter the first number: "))
            num2 = float(input("Enter the second number: "))
            break
        except ValueError:
            print("Invalid input! Please enter numeric values for both numbers.")
    if operation == '1':
        result = add(num1, num2)
        op_symbol = '+'
    elif operation == '2':
        result = subtract(num1, num2)
        op_symbol = '-'
    elif operation == '3':
        result = multiply(num1, num2)
        op_symbol = '*'
    elif operation == '4':
        result = divide(num1, num2)
        op_symbol = '/'
    else:
        result = "Invalid operation selected."
        op_symbol = ''
    print (f"---------------------------------\n{num1} {op_symbol} {num2} = {result}\n---------------------------------")

while True:
    calculate()
    play_again = input("Do you want to perform another calculation? (yes/no): ").lower()
    if play_again != 'yes':
        print("Thank you for using the Simple Calculator. Goodbye!")
        break