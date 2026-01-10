question_1 = {
    "question": "What is the capital of France?",
    "options": ["Paris", "London", "Berlin", "Madrid"],
    "answer": "Paris"
}

question_2 = {
    "question": "What is 2 + 2?",
    "options": ["3", "4", "5", "6"],
    "answer": "4"
}

question_3 = {
    "question": "What is the largest planet in our solar system?",
    "options": ["Earth", "Mars", "Jupiter", "Saturn"],
    "answer": "Jupiter"
}

question_4 = {
    "question": "Who wrote 'Romeo and Juliet'?",
    "options": ["Charles Dickens", "William Shakespeare", "Mark Twain", "Jane Austen"],
    "answer": "William Shakespeare"
}

question_5 = {
    "question": "What is the boiling point of water?",
    "options": ["90°C", "100°C", "110°C", "120°C"],
    "answer": "100°C"
}

questions = [question_1, question_2, question_3, question_4, question_5]

score = 0

print("\n📘 Welcome to the Quiz App!")
print("-" * 30)

for question in questions:
    print("\n" + question["question"])
    for idx, option in enumerate(question["options"], start=1):
        print(f"{idx}. {option}")

    while True:
        try:
            user_answer = int(input("Please enter the number of your answer: "))
            if 1 <= user_answer <= len(question["options"]):
                selected_option = question["options"][user_answer - 1]
                if selected_option == question["answer"]:
                    print("✅ Correct!")
                    score += 1
                else:
                    print(f"❌ Wrong! The correct answer is: {question['answer']}")
                break
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

print("\n🎉 Quiz Completed!")
print(f"Your final score: {score}/{len(questions)}")
