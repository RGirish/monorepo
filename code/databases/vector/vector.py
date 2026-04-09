from typing import List

import numpy as np
import ollama
from sklearn.metrics.pairwise import cosine_similarity


class VectorDatabase:
    def __init__(self):
        self._data = []
        self._model = "embeddinggemma"

    def add(self, text):
        vector = self._embed(text)
        self._data.append([text, vector])

    def search(self, text: str, max_items: int = 5) -> List[str]:
        search_term_embedding = self._embed(text)
        A = np.array([search_term_embedding])

        similarity_scores = []
        for (datum, vector) in self._data:
            B = np.array([vector])
            score = cosine_similarity(A, B)
            similarity_scores.append([score, datum])

        similarity_scores.sort(reverse=True)
        return [t for _, t in similarity_scores][:max_items]

    def _embed(self, text):
        response = ollama.embed(
            model=self._model,
            input=text,
        )
        return response.embeddings[0]


if __name__ == '__main__':
    vector_db = VectorDatabase()
    for text in [
        "The National Weather Service issued a thunderstorm warning for the tri-state area tonight.",
        "Humidity levels are expected to spike, making the afternoon feel significantly warmer than the actual temperature.",
        "A lingering high-pressure system is keeping the skies clear and the winds calm for the weekend.",
        "Meteorologists at The Weather Channel predict an unusually early start to the spring thaw.",
        "Dense fog blanketed the valley this morning, reducing visibility to less than a quarter mile.",
        "The Climate Prediction Center suggests a high probability of El Niño conditions persisting through winter.",
        "Scattered showers might dampen your outdoor plans, so keep an umbrella handy.",
        "A biting north wind made the morning commute feel like a trek through the Arctic.",
        "Record-breaking heatwaves are becoming more frequent according to NASA's Global Climate Change records.",
        "The evening sky turned a deep violet as the storm clouds finally began to break.",
        "The New York Stock Exchange saw a surge in tech stocks during early trading hours.",
        "Classic sourdough bread requires a long fermentation process to develop its signature tang.",
        "You can find step-by-step assembly instructions on the IKEA Support Page for your new furniture.",
        "Quantum physics explores the behavior of matter and energy at the most fundamental levels.",
        "The American Red Cross is currently seeking volunteers for its upcoming blood drive.",
        "Learning a new language improves cognitive flexibility and strengthens memory retention over time.",
        "Check the Official NBA Standings to see if your team made the playoff cut.",
        "A well-balanced diet should include a variety of leafy greens, lean proteins, and healthy fats.",
        "The Metropolitan Museum of Art is hosting a new exhibit featuring 19th-century sculpture.",
        "Regular software updates are essential for maintaining the security of your personal devices."
    ]:
        vector_db.add(text)

    items = vector_db.search("Weather")
    for item in items:
        print(item)
