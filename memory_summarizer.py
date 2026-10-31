
import re


class MemorySummarizer:
    """Create concise summaries from selected memory records."""

    @staticmethod
    def normalize(text):
        """Normalize text for duplicate detection."""
        return re.sub(r"\s+", " ", text.strip()).casefold()

    @staticmethod
    def extract_text(memory):
        """Extract text from a dictionary or memory record."""

        if isinstance(memory, dict):
            text = memory.get("text")
        else:
            text = getattr(memory, "text", None)

        if not isinstance(text, str):
            raise ValueError("Each memory must contain valid text.")

        return text.strip()

    def summarize(self, memories):
        """Combine memory records and remove repeated sentences."""

        if memories is None:
            return ""

        if not isinstance(memories, (list, tuple)):
            raise ValueError("Memories must be a list or tuple.")

        if not memories:
            return ""

        unique_sentences = []
        seen_sentences = set()

        for memory in memories:
            text = self.extract_text(memory)

            if not text:
                continue

            # Split text into individual sentences.
            sentences = re.split(r"(?<=[.!?])\s+", text)

            for sentence in sentences:
                sentence = sentence.strip()

                if not sentence:
                    continue

                normalized = self.normalize(sentence)

                if normalized not in seen_sentences:
                    seen_sentences.add(normalized)
                    unique_sentences.append(sentence)

        return " ".join(unique_sentences)
