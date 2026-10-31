
from memory_store import LongTermMemory


memory = LongTermMemory()

print("\n--- ADDING LONG-TERM MEMORIES ---")

memory.add_memory(
    "The user is learning AI and machine learning.",
    source="conversation",
    importance=0.9,
)

memory.add_memory(
    "The user prefers backend development.",
    source="user_profile",
    importance=0.8,
)

memory.add_memory(
    "The user is interested in building AI agents.",
    source="conversation",
    importance=0.85,
)

print("Memories stored:", memory.count())

print("\n--- MEMORY INSPECTION ---")

for record in memory.get_all():
    print(record)

print("\n--- PERSISTENCE CHECK ---")

reloaded_memory = LongTermMemory()

print("Memories after reload:", reloaded_memory.count())

for record in reloaded_memory.get_all():
    print(record["text"])
