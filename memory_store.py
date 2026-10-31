
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path


class MemoryRecord:
    """Represents one persistent long-term memory."""

    def __init__(
        self,
        text,
        source="unknown",
        importance=0.5,
        memory_id=None,
        timestamp=None,
    ):
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Memory text must be a non-empty string.")

        if not isinstance(source, str) or not source.strip():
            raise ValueError("Source must be a non-empty string.")

        if (
            not isinstance(importance, (int, float))
            or isinstance(importance, bool)
            or not 0 <= importance <= 1
        ):
            raise ValueError("Importance must be between 0 and 1.")

        self.id = memory_id or str(uuid.uuid4())
        self.text = text.strip()
        self.source = source.strip()
        self.timestamp = timestamp or datetime.now(
            timezone.utc
        ).isoformat()
        self.importance = float(importance)

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "source": self.source,
            "timestamp": self.timestamp,
            "importance": self.importance,
        }

    @classmethod
    def from_dict(cls, data):
        required = {
            "id",
            "text",
            "source",
            "timestamp",
            "importance",
        }

        if not isinstance(data, dict) or not required.issubset(data):
            raise ValueError("Invalid memory record structure.")

        return cls(
            text=data["text"],
            source=data["source"],
            importance=data["importance"],
            memory_id=data["id"],
            timestamp=data["timestamp"],
        )


class LongTermMemory:
    """Store and retrieve persistent long-term memories."""

    def __init__(self, storage_path="data/memories.json"):
        self.storage_path = Path(storage_path)
        self.memories = []
        self.load()

    def add_memory(self, text, source="unknown", importance=0.5):
        record = MemoryRecord(
            text=text,
            source=source,
            importance=importance,
        )

        # Prevent duplicate content (case-insensitive).
        normalized = record.text.casefold()

        for existing in self.memories:
            if existing.text.casefold() == normalized:
                return existing

        self.memories.append(record)
        self.save()
        return record

    def save(self):
        self.storage_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = [memory.to_dict() for memory in self.memories]

        temporary_path = self.storage_path.with_suffix(
            self.storage_path.suffix + ".tmp"
        )

        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        temporary_path.replace(self.storage_path)

    def load(self):
        if not self.storage_path.exists():
            self.memories = []
            return

        try:
            with self.storage_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("Storage must contain a JSON list.")

            loaded_memories = [
                MemoryRecord.from_dict(item) for item in data
            ]

            # Reject duplicate IDs or duplicate content in storage.
            ids = [memory.id for memory in loaded_memories]
            contents = [
                memory.text.casefold() for memory in loaded_memories
            ]

            if len(ids) != len(set(ids)):
                raise ValueError("Duplicate memory IDs found.")

            if len(contents) != len(set(contents)):
                raise ValueError("Duplicate memory content found.")

            self.memories = loaded_memories

        except (json.JSONDecodeError, ValueError, TypeError, KeyError):
            self.memories = []
            raise ValueError(
                f"Memory storage is malformed: {self.storage_path}"
            )

    def get_all(self):
        return [memory.to_dict() for memory in self.memories]

    def inspect(self):
        return {
            "storage_path": str(self.storage_path),
            "memory_count": len(self.memories),
            "memories": self.get_all(),
        }

    def count(self):
        return len(self.memories)

    def clear(self):
        self.memories.clear()
        self.save()
