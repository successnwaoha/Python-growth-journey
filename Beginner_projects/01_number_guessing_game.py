import random

user_guess = 0
number_of_guesses = 0
lucky_number = random.randint(1, 100)

difficulty = int(input("Choose a difficulty. Type '1' for Normal mode or '2' for Hard mode: "))
hint_frequency = 0
if difficulty == 1:
    hint_frequency = 2
elif difficulty == 2:
    hint_frequency = 6

min_start = max(1, lucky_number - 50)
max_start = lucky_number

messages = [
    "Careful, only 3 guesses left!",
    "Tick-tock… just 3 guesses remaining!",
    "Last few tries! 3 guesses left!"
]

low_hints = ["Too low!", "Oops, that's too small!", "Aim higher!"]
high_hints = ["Too high!", "Woah, that's too big!", "Try a smaller number!"]

encouragement = ["Keep going!", "You got this!", "Don't give up!"]

print ("The lucky number is:", lucky_number)

while user_guess != lucky_number:
    number_of_guesses += 1
    #claculate stages
    early_stage = number_of_guesses <= 3
    middle_stage = 4 <= number_of_guesses <= 7
    late_stage = 8 <= number_of_guesses <= 10
    if number_of_guesses == 7:
        print(random.choice(messages))
    if number_of_guesses <= 10:
        user_guess =int(input("Guess a number between 1 and 100: "))
        print ()
        if user_guess == lucky_number:
            break
        if early_stage:
            if user_guess < lucky_number:
                print(random.choice(low_hints))
            elif user_guess > lucky_number:
                print(random.choice(high_hints))
        elif number_of_guesses % hint_frequency == 0:
            if middle_stage:
                if lucky_number % 2 == 0:
                    print ("Hint: The number is even.")
                else:
                    print ("Hint: The number is odd.")
            if late_stage:
                start = random.randint(min_start, max_start)
                end = min(start + 50, 100)
                print(f"Hint: The number is between {start} and {end}")
        else:
            print ("Wrong guess. Try again.")
            print(random.choice(encouragement))
    else:
        print ("Sorry, you've used all your guesses. The lucky number was:", lucky_number)
        break
if user_guess == lucky_number:
    print(f"Congratulations! You guessed it in {number_of_guesses} tries!")