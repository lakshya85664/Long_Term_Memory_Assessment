
import math
import re
from collections import Counter


class MemoryRetriever:
    """Retrieve and rank long-term memories using text similarity."""

    def __init__(self, memory_store):
        self.memory_store = memory_store

    
    @staticmethod
    def tokenize(text):
        """Convert text into meaningful lowercase word tokens."""

        stop_words = {
            "the", "a", "an", "is", "are", "was", "were",
            "what", "who", "when", "where", "why", "how",
            "user", "users", "s", "me", "my", "i", "you",
            "your", "their", "they", "it", "this", "that",
            "about", "tell", "does", "do", "did", "and",
            "or", "of", "in", "on", "to", "for", "with",
            "from", "has", "have", "had"
        }

        tokens = re.findall(r"\b[a-z0-9]+\b", text.lower())

        return [
            token for token in tokens
            if token not in stop_words
        ]


    @staticmethod
    def cosine_similarity(query_tokens, memory_tokens):
        """Calculate cosine similarity between two word-frequency vectors."""

        query_vector = Counter(query_tokens)
        memory_vector = Counter(memory_tokens)

        if not query_vector or not memory_vector:
            return 0.0

        common_words = set(query_vector) & set(memory_vector)

        dot_product = sum(
            query_vector[word] * memory_vector[word]
            for word in common_words
        )

        query_magnitude = math.sqrt(
            sum(value ** 2 for value in query_vector.values())
        )

        memory_magnitude = math.sqrt(
            sum(value ** 2 for value in memory_vector.values())
        )

        if query_magnitude == 0 or memory_magnitude == 0:
            return 0.0

        return dot_product / (query_magnitude * memory_magnitude)

    def retrieve(self, query, top_k=5, min_score=0.0):
        """Return the most relevant memories for a query."""

        if not isinstance(query, str):
            raise ValueError("Query must be a string.")

        if (
            not isinstance(top_k, int)
            or isinstance(top_k, bool)
            or top_k <= 0
        ):
            raise ValueError("top_k must be a positive integer.")

        if (
            not isinstance(min_score, (int, float))
            or isinstance(min_score, bool)
            or not 0 <= min_score <= 1
        ):
            raise ValueError("min_score must be between 0 and 1.")

        query_tokens = self.tokenize(query)

        if not query_tokens:
            return []

        results = []

        for memory in self.memory_store.get_all():
            memory_tokens = self.tokenize(memory["text"])

            similarity = self.cosine_similarity(
                query_tokens,
                memory_tokens,
            )

            # Importance contributes only when there is a text match.
            if similarity == 0:
                score = 0.0
            else:
                score = (
                    0.85 * similarity
                    + 0.15 * memory["importance"]
                )

            if score >= min_score and similarity > 0:
                results.append({
                    **memory,
                    "similarity": round(similarity, 4),
                    "relevance_score": round(score, 4),
                })

        results.sort(
            key=lambda item: (
                item["relevance_score"],
                item["importance"],
                item["timestamp"],
            ),
            reverse=True,
        )

        return results[:top_k]
