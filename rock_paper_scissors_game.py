import random

def play_game():
    player_score = 0
    computer_score = 0

    choices = ["rock", "paper", "scissors"]
    winning_rules = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper"
    }

    print("Welcome to Rock, Paper, Scissors!")
    print("Best of 3 wins the game. \n")

    while player_score < 3 and computer_score < 3:
        player_choice = input("Enter your choice (rock, paper, scissors): ").lower()
        if player_choice not in choices:
            print("Invalid choice. Please try again.\n")
            continue

        computer_choice = random.choice(choices)
        print(f"Computer chose: {computer_choice}")

        if player_choice == computer_choice:
            print("It's a tie!\n")
        elif winning_rules[player_choice] == computer_choice:
            player_score += 1
            print("You win this round!\n")
        else:
            computer_score += 1
            print("Computer wins this round!\n")
        print(f"Score -> You: {player_score}, Computer: {computer_score}\n")

    print("\nFinal Result:")
    if player_score == 3:
        print("🎉 Congratulations! You won the game!")
    else:
        print("💻 Computer won the game! Better luck next time!")

while True:
    play_game()
    replay = input("Do you want to play again? (yes/no): ").lower()
    if replay != 'yes':
        print("Thanks for playing! Goodbye!")
        break