
from memory_store import LongTermMemory
from memory_retriever import MemoryRetriever


store = LongTermMemory()
retriever = MemoryRetriever(store)


queries = [
    "What is the user learning about AI and machine learning?",
    "What type of software development does the user prefer?",
    "Tell me about the user's interest in AI agents.",
    "What is the user's favourite cricket team?",
]

for query in queries:
    print("\n" + "=" * 65)
    print("QUERY:", query)
    print("=" * 65)

    results = retriever.retrieve(query, top_k=3)

    if not results:
        print("No relevant memories found.")
        continue

    for index, result in enumerate(results, start=1):
        print(f"\nRank: {index}")
        print("Memory:", result["text"])
        print("Source:", result["source"])
        print("Importance:", result["importance"])
        print("Similarity:", result["similarity"])
        print("Relevance Score:", result["relevance_score"])


print("\n--- TOP-K VERIFICATION ---")

results = retriever.retrieve(
    "AI machine learning",
    top_k=2,
)

print("Requested maximum:", 2)
print("Results returned:", len(results))

assert len(results) <= 2

print("Top-k verification passed.")
