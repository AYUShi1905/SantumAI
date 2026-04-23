# Future Proposal: Vectorless, Reasoning-Based RAG (PageIndex)

## 1. Overview
As an alternative to the current Vector-based RAG (Qdrant + Jina), this proposal explores the **PageIndex** framework by VectifyAI. It moves away from mathematical semantic similarity and toward a "reasoning-first" approach that mimics how a human expert navigates a document using a Table of Contents (ToC).

## 2. Why Consider This?
Traditional vector-based RAG often struggles with:
*   **Chunking Errors:** Splitting tables or related context across arbitrary 600-token boundaries.
*   **Semantic Noise:** Returning "mathematically similar" but logically irrelevant snippets.
*   **Structured Documents:** Finding specific sections or exercises in long, hierarchical manuals (like CBT handbooks).

## 3. Core Architecture: "The Semantic Tree"
Instead of a flat database of chunks, PageIndex builds a **Hierarchical Tree Index**:
1.  **Structural Extraction:** Uses an LLM to identify the Table of Contents (ToC) and page ranges.
2.  **Tree Construction:** Creates a JSON tree where each node is a chapter or section with a precise page range.
3.  **Semantic Summarization:** Generates summaries for every node in the tree.
4.  **Reasoning-Based Search:** An LLM "navigates" the tree by reading summaries and drilling down into the most relevant branches.

## 4. Key Advantages
*   **No Vector DB/Embeddings:** Eliminates the need for Qdrant and Jina.
*   **High Precision:** Proven 98.7% accuracy on complex benchmarks (FinanceBench).
*   **Context Preservation:** Never splits a logical section in half; always retrieves complete, relevant pages.
*   **Traceability:** Provides a clear "reasoning path" (e.g., "I searched Section 2.1 because the summary mentioned anxiety...").

## 5. Potential Drawbacks & Risks
*   **Latency:** Navigating the tree requires multiple LLM calls per query, which can be slower than a single vector search.
*   **Cost:** Increased LLM token usage during the "Search" phase.
*   **Maturity:** PageIndex is a very new framework (released late 2025) and is still considered experimental compared to LangChain/Qdrant.

## 6. Recommended Action
Do not implement this for the current production phase. The existing **Vector-based system** is more stable, cost-effective for streaming, and widely supported. This proposal should be revisited for a "Version 2.0" once the core system is live and the PageIndex framework has matured.

---
*Created on April 23, 2026, as a research record for future architectural updates.*
