
import json
import pytest

from memory_store import LongTermMemory, MemoryRecord


def test_add_memory(tmp_path):
    store = LongTermMemory(tmp_path / "memories.json")
    record = store.add_memory("Learning Python", "conversation", 0.8)

    assert record.text == "Learning Python"
    assert store.count() == 1


def test_memory_has_required_metadata(tmp_path):
    store = LongTermMemory(tmp_path / "memories.json")
    record = store.add_memory("Learning AI", "profile", 0.9)

    data = record.to_dict()

    assert data["id"]
    assert data["text"] == "Learning AI"
    assert data["source"] == "profile"
    assert data["timestamp"]
    assert data["importance"] == 0.9


def test_unique_memory_ids(tmp_path):
    store = LongTermMemory(tmp_path / "memories.json")
    first = store.add_memory("Python")
    second = store.add_memory("Machine learning")

    assert first.id != second.id


def test_duplicate_memory_prevention(tmp_path):
    store = LongTermMemory(tmp_path / "memories.json")
    first = store.add_memory("Learning Python")
    second = store.add_memory("learning python")

    assert first.id == second.id
    assert store.count() == 1


def test_persistence_after_reload(tmp_path):
    path = tmp_path / "memories.json"

    store = LongTermMemory(path)
    store.add_memory("Persistent memory", "test", 0.7)

    reloaded = LongTermMemory(path)

    assert reloaded.count() == 1
    assert reloaded.get_all()[0]["text"] == "Persistent memory"


def test_empty_storage(tmp_path):
    store = LongTermMemory(tmp_path / "new.json")

    assert store.count() == 0


def test_clear_storage(tmp_path):
    store = LongTermMemory(tmp_path / "memories.json")
    store.add_memory("Temporary memory")
    store.clear()

    assert store.count() == 0
    assert json.loads(
        (tmp_path / "memories.json").read_text(encoding="utf-8")
    ) == []


def test_invalid_memory_text():
    with pytest.raises(ValueError):
        MemoryRecord("   ")


def test_invalid_importance():
    with pytest.raises(ValueError):
        MemoryRecord("Valid text", importance=1.5)


def test_malformed_json_storage(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(ValueError, match="malformed"):
        LongTermMemory(path)


def test_inspection_information(tmp_path):
    store = LongTermMemory(tmp_path / "memories.json")
    store.add_memory("Inspection test")

    result = store.inspect()

    assert result["memory_count"] == 1
    assert len(result["memories"]) == 1
    assert result["storage_path"]
