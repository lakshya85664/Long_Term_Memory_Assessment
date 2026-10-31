
from memory_store import LongTermMemory
from memory_retriever import MemoryRetriever
from memory_summarizer import MemorySummarizer


store = LongTermMemory()
retriever = MemoryRetriever(store)
summarizer = MemorySummarizer()


query = "AI machine learning and AI agents"

print("\n--- SELECTING RELATED MEMORIES ---")
print("Query:", query)

selected_memories = retriever.retrieve(query, top_k=5)

for memory in selected_memories:
    print("-", memory["text"])

print("\n--- GENERATED SUMMARY ---")

summary = summarizer.summarize(selected_memories)

print(summary)

print("\n--- DUPLICATE REMOVAL TEST ---")

sample_memories = [
    {"text": "The user is learning Python. The user likes AI."},
    {"text": "The user is learning Python. The user builds AI agents."},
    {"text": "The USER IS LEARNING PYTHON."},
]

duplicate_summary = summarizer.summarize(sample_memories)

print(duplicate_summary)

print("\n--- EMPTY MEMORY TEST ---")

empty_summary = summarizer.summarize([])

print("Empty summary:", repr(empty_summary))

assert empty_summary == ""

print("\nSummarization demonstration completed.")
