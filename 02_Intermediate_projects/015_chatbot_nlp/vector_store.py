from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class VectorStore:
    def __init__(self):
        self.knowledge = {
            "loop": "Loops repeat actions in Python using for and while statements.",
            "list": "Lists store ordered collections of items and are mutable.",
            "dictionary": "Dictionaries store key-value pairs.",
            "function": "Functions are reusable blocks of code defined with def."
        }
        self.vectorizer = TfidfVectorizer()
        self.topics = list(self.knowledge.keys())
        self.vectors = self.vectorizer.fit_transform(list(self.knowledge.values()))

    def search(self, query):
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.vectors)[0]
        best_index = similarities.argmax()
        score = similarities[best_index]

        if score < 0.1:
            return None, 0.0

        topic = self.topics[best_index]
        return self.knowledge[topic], round(float(score), 2)