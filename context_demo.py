
from memory_store import LongTermMemory
from context_builder import AgentContextBuilder


store = LongTermMemory()
builder = AgentContextBuilder(store)


query = "How can I use my AI and machine learning knowledge to build agents?"

print("\n--- COMPLETE AGENT CONTEXT ---")

context = builder.build_context(
    query=query,
    top_k=5,
)

print(context)


print("\n--- CONTEXT INSPECTION ---")

inspection = builder.inspect_context(
    query=query,
    top_k=5,
)

print("Query:", inspection["query"])
print("Retrieved count:", inspection["retrieved_count"])
print("Summary:", inspection["summary"])

print("\n--- EMPTY RESULT CHECK ---")

empty_context = builder.build_context(
    "What is my favourite cricket team?"
)

print(empty_context)

print("\nContext demonstration completed.")
