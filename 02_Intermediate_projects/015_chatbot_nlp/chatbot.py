# chatbot.py
from brain import process_message

print("🤖 Chatbot is running. Type 'exit' to quit.")

while True:
    user_input = input("You: ")
    
    if user_input.lower() in ["exit", "quit"]:
        print("Bot: Goodbye! 👋")
        break

    # We send the text to the brain and get a response back
    response = process_message(user_input)
    
    print("Bot:", response)