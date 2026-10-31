
import pytest

from memory_store import LongTermMemory
from memory_retriever import MemoryRetriever


@pytest.fixture
def retriever(tmp_path):
    store = LongTermMemory(tmp_path / "memories.json")

    store.add_memory(
        "The user is learning Python programming.",
        "conversation",
        0.9,
    )
    store.add_memory(
        "The user prefers backend development.",
        "profile",
        0.8,
    )
    store.add_memory(
        "The user is interested in AI agents.",
        "conversation",
        0.85,
    )

    return MemoryRetriever(store)


def test_relevant_memory_retrieval(retriever):
    results = retriever.retrieve("Python programming")

    assert results
    assert "Python" in results[0]["text"]


def test_backend_memory_retrieval(retriever):
    results = retriever.retrieve("backend development")

    assert results
    assert "backend" in results[0]["text"].lower()


def test_unrelated_query_returns_empty(retriever):
    results = retriever.retrieve("favourite cricket team")

    assert results == []


def test_empty_query_returns_empty(retriever):
    assert retriever.retrieve("   ") == []


def test_top_k_limit(retriever):
    results = retriever.retrieve("Python AI backend", top_k=2)

    assert len(results) <= 2


def test_results_are_ranked(retriever):
    results = retriever.retrieve("Python programming AI agents")

    scores = [item["relevance_score"] for item in results]

    assert scores == sorted(scores, reverse=True)


def test_invalid_top_k(retriever):
    with pytest.raises(ValueError):
        retriever.retrieve("Python", top_k=0)


def test_invalid_min_score(retriever):
    with pytest.raises(ValueError):
        retriever.retrieve("Python", min_score=2)


def test_retrieval_contains_scores(retriever):
    results = retriever.retrieve("Python")

    assert "similarity" in results[0]
    assert "relevance_score" in results[0]
