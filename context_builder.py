
from memory_retriever import MemoryRetriever
from memory_summarizer import MemorySummarizer


class AgentContextBuilder:
    """Build agent context using persistent long-term memories."""

    def __init__(self, memory_store):
        self.memory_store = memory_store
        self.retriever = MemoryRetriever(memory_store)
        self.summarizer = MemorySummarizer()

    def build_context(self, query, top_k=5):
        """Retrieve, summarize and assemble relevant context."""

        if not isinstance(query, str) or not query.strip():
            raise ValueError("Query must be a non-empty string.")

        memories = self.retriever.retrieve(
            query=query,
            top_k=top_k,
        )

        summary = self.summarizer.summarize(memories)

        context = [
            "=== CURRENT USER QUERY ===",
            query.strip(),
            "",
            "=== LONG-TERM MEMORY SUMMARY ===",
            summary if summary else "No relevant memories available.",
            "",
            "=== RETRIEVED MEMORY DETAILS ===",
        ]

        if memories:
            for index, memory in enumerate(memories, start=1):
                context.append(
                    f"{index}. {memory['text']}"
                )
                context.append(
                    f"   Source: {memory['source']}"
                )
                context.append(
                    f"   Importance: {memory['importance']}"
                )
                context.append(
                    f"   Relevance: {memory['relevance_score']}"
                )
        else:
            context.append("No matching memories found.")

        return "\n".join(context)

    def inspect_context(self, query, top_k=5):
        """Return structured context information for debugging."""

        memories = self.retriever.retrieve(query, top_k=top_k)

        return {
            "query": query,
            "retrieved_count": len(memories),
            "summary": self.summarizer.summarize(memories),
            "memories": memories,
        }
