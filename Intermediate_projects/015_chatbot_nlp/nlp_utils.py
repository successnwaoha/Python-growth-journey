import spacy

nlp = spacy.load("en_core_web_sm")

def detect_intent(text):
    text = text.lower()
    if any(word in text for word in ["hi", "hello", "hey"]): return "greeting"
    if any(word in text for word in ["bye", "goodbye", "exit"]): return "goodbye"
    if any(word in text for word in ["help", "what can you do"]): return "help"
    if any(word in text for word in ["how", "what", "explain", "tell me"]): return "question"
    return "unknown"

def extract_entities(text):
    doc = nlp(text.lower())
    # Custom keywords for our Python domain
    keywords = ["loop", "list", "dictionary", "function", "variable", "class"]
    found = [token.text for token in doc if token.text in keywords]
    return found