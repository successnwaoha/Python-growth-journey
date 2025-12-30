# brain.py
from nlp_utils import detect_intent, extract_entities
from vector_store import VectorStore
from memory import SessionMemory

# Initialize the components once
memory = SessionMemory()
store = VectorStore()

def process_message(user_input):
    # 1. Analyze the input
    intent = detect_intent(user_input)
    entities = extract_entities(user_input)
    
    # 2. Update memory with what we just found
    memory.update(intent, entities)
    
    # 3. Handle Greetings/Goodbyes
    if intent == "greeting":
        return "Hello! 👋 I'm your Python assistant. Ask me about loops, lists, or functions!"
    
    if intent == "goodbye":
        return "Goodbye! Happy coding!"

    if intent == "help":
        return "I can explain Python concepts like loops, lists, dictionaries, and functions."

    # 4. Handle Questions using ML (Vector Store)
    # We search the knowledge base for the user's input
    answer, confidence = store.search(user_input)
    
    if answer and confidence > 0.2:
        return f"{answer} (Confidence: {confidence})"

    # 5. Fallback: If ML fails, try using the last known entity from memory
    _, last_entity = memory.get_context()
    if last_entity:
        # Try searching specifically for the stored topic
        fallback_answer, _ = store.search(last_entity)
        if fallback_answer:
            return f"I'm not sure about that specific question, but regarding {last_entity}: {fallback_answer}"

    return "I'm sorry, I don't quite understand that. Try asking 'What is a loop?'"