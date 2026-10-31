
import pytest

from memory_summarizer import MemorySummarizer


@pytest.fixture
def summarizer():
    return MemorySummarizer()


def test_empty_summary(summarizer):
    assert summarizer.summarize([]) == ""


def test_single_memory(summarizer):
    result = summarizer.summarize([
        {"text": "Python is useful."}
    ])

    assert result == "Python is useful."


def test_combines_multiple_memories(summarizer):
    result = summarizer.summarize([
        {"text": "Python is useful."},
        {"text": "AI is interesting."},
    ])

    assert "Python is useful." in result
    assert "AI is interesting." in result


def test_removes_duplicate_sentences(summarizer):
    result = summarizer.summarize([
        {"text": "Python is useful."},
        {"text": "Python is useful."},
    ])

    assert result == "Python is useful."


def test_duplicate_detection_ignores_case(summarizer):
    result = summarizer.summarize([
        {"text": "Python is useful."},
        {"text": "PYTHON IS USEFUL."},
    ])

    assert result == "Python is useful."


def test_accepts_memory_objects(summarizer):
    class ExampleMemory:
        text = "Learning AI is interesting."

    result = summarizer.summarize([ExampleMemory()])

    assert result == "Learning AI is interesting."


def test_invalid_input(summarizer):
    with pytest.raises(ValueError):
        summarizer.summarize("not a list")


def test_invalid_memory_record(summarizer):
    with pytest.raises(ValueError):
        summarizer.summarize([{"source": "conversation"}])
