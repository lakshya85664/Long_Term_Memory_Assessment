
import pytest

from memory_store import LongTermMemory
from context_builder import AgentContextBuilder


@pytest.fixture
def builder(tmp_path):
    store = LongTermMemory(tmp_path / "memories.json")

    store.add_memory(
        "The user is learning Python and AI.",
        "conversation",
        0.9,
    )
    store.add_memory(
        "The user prefers backend development.",
        "profile",
        0.8,
    )

    return AgentContextBuilder(store)


def test_context_contains_query(builder):
    context = builder.build_context("Python")

    assert "CURRENT USER QUERY" in context
    assert "Python" in context


def test_context_contains_summary(builder):
    context = builder.build_context("Python")

    assert "LONG-TERM MEMORY SUMMARY" in context
    assert "learning Python" in context


def test_context_contains_memory_details(builder):
    context = builder.build_context("backend development")

    assert "RETRIEVED MEMORY DETAILS" in context
    assert "Source: profile" in context


def test_unrelated_query_context(builder):
    context = builder.build_context("favourite cricket team")

    assert "No relevant memories available." in context
    assert "No matching memories found." in context


def test_context_inspection(builder):
    result = builder.inspect_context("Python")

    assert result["query"] == "Python"
    assert result["retrieved_count"] >= 1
    assert result["summary"]


def test_invalid_query(builder):
    with pytest.raises(ValueError):
        builder.build_context("   ")


def test_invalid_top_k(builder):
    with pytest.raises(ValueError):
        builder.build_context("Python", top_k=0)
