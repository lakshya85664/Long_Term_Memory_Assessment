# Long-Term Memory Assessment

## Project Overview
This project implements a lightweight persistent long-term memory system for an AI agent. It stores useful information across application runs, retrieves memories relevant to a new query, summarizes selected records, and assembles the results into structured agent context.

The implementation uses Python's standard library and JSON file storage. It does not require an external database, embedding service, or paid API.

## Learning Objectives
- Represent memories with unique identifiers and metadata.
- Persist records locally and reload them after restarting the application.
- Prevent duplicate memory content.
- Retrieve and rank relevant memories using text similarity and importance.
- Combine related memories while removing repeated sentences.
- Build inspectable context containing the current query and retrieved history.
- Test normal operation, edge cases, and malformed storage.

## Project Structure
```text
Long_Term_Memory_Assessment/
├── memory_store.py
├── memory_retriever.py
├── memory_summarizer.py
├── context_builder.py
├── storage_demo.py
├── retrieval_demo.py
├── summarization_demo.py
├── context_demo.py
├── data/memories.json
├── outputs/
└── tests/
    ├── test_memory_store.py
    ├── test_memory_retriever.py
    ├── test_memory_summarizer.py
    └── test_context_builder.py
```

## Implementation Details

### 1. Persistent memory storage
`MemoryRecord` represents a memory using an ID, text, source, timestamp, and importance value. `LongTermMemory` supports adding, saving, loading, listing, inspecting, counting, and clearing records. Records are serialized to `data/memories.json`. Saving uses a temporary file followed by replacement to reduce the chance of leaving a partially written JSON file. Duplicate text is detected without case sensitivity.

### 2. Retrieval and ranking
`MemoryRetriever` tokenizes text, removes common stop words, and calculates cosine similarity over word-frequency vectors. The final relevance score combines textual similarity (85%) and memory importance (15%). Results are sorted by score and limited by `top_k`. Queries without meaningful matching terms return no results.

### 3. Summarization
`MemorySummarizer` combines selected memory text and removes repeated sentences using case-insensitive normalized comparisons. It accepts dictionaries and objects with a `text` attribute and safely handles empty input.

### 4. Agent context construction
`AgentContextBuilder` combines the current query, a summary of retrieved memories, and individual memory details. It includes source, importance, and relevance information to support inspection and debugging. If no relevant memories are found, the context explicitly reports that state.

## Running the Project
Run these commands from the project root with the virtual environment activated:
```cmd
python storage_demo.py
python retrieval_demo.py
python summarization_demo.py
python context_demo.py
python -m pytest -v
```

## Test Results
The completed test suite contains **35 tests**, covering storage, metadata, unique IDs, duplicate prevention, persistence and reload, empty storage, clearing, malformed JSON, retrieval ranking, unrelated queries, top-k limits, summarization, duplicate sentence removal, and context assembly.

Verified result: **35 passed**.

## Design Decisions and Limitations
- Storage is a local JSON file and is suitable for a small educational project, not concurrent production workloads.
- Retrieval uses word-frequency cosine similarity, not pretrained semantic embeddings. It may miss synonyms or paraphrases that share few words.
- Stop-word filtering reduces false matches but is not a full natural-language understanding system.
- Importance is a manually supplied value between 0 and 1.
- Summarization is deterministic sentence deduplication and concatenation, not abstractive or LLM-based summarization.
- The context builder prepares text for an agent; it does not itself call an LLM.

## Reflection (approximately 300 words)
Building this long-term memory assessment helped me understand how an AI agent can retain useful information beyond a single interaction. Earlier exercises focused on short-term context and the memory lifecycle. In this project, I connected persistence, retrieval, summarization, and context construction into one workflow.

The first important part was designing a memory record with a unique identifier and useful metadata. Saving records in JSON and loading them when a new store instance is created demonstrated the difference between temporary conversation state and persistent memory. I also added duplicate-content prevention so repeated application runs would not keep inserting the same information.

The retrieval component was particularly useful for understanding relevance. I implemented tokenization, stop-word filtering, cosine similarity, and an importance-weighted score. During the demonstration, an unrelated cricket query initially returned memories because common words created false matches. Filtering stop words improved the result and showed why testing with unrelated queries is important, not just testing successful matches.

The summarizer combines retrieved records and removes repeated sentences. It is intentionally deterministic and does not claim to understand meaning in the way a language model would. The context builder then organizes the current query, a summary, and individual memory details into clearly labelled sections. This makes the result easier to inspect and pass to a downstream agent.

I also learned the value of testing edge cases. The 35 automated tests cover persistence, malformed JSON, duplicate records, invalid inputs, ranking, empty results, summarization, and context assembly. These tests give confidence that the components work together and make future changes safer.

The project has clear opportunities for improvement. A future version could use semantic embeddings and a dedicated vector database for stronger retrieval. It could also use an LLM to generate compact summaries, add memory expiration or updating policies, and protect persistent data with stronger validation and access controls. Overall, this assessment gave me practical experience designing a small but complete long-term memory layer for an AI agent.
