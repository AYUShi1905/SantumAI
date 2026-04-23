# Pending Tasks: Santum AI RAG System

This document tracks all approved features and improvements that are currently pending implementation.

## 1. Chat & Reasoning Phase
*   **[ ] Chat Request Models:** Implement `ChatRequest` and `Message` in `app/models/request.py`.
*   **[ ] Chat API Endpoint:** Create `POST /api/v1/chat/stream` in `app/api/v1/chat.py`.
*   **[ ] Tiktoken Integration:** Implement precise token counting in `app/utils/tokens.py`.
*   **[ ] Safety Prompt Engineering:** Refine the system prompt for empathetic counseling and crisis disclaimer.

## 2. Chat History Summarization (NEW)
*   **[ ] Summarization Service:** Create a service to condense multi-turn chat history into a single paragraph.
*   **[ ] Summarization API:** Create `POST /api/v1/summarize` for frontend history management.
*   **[ ] Efficiency Tuning:** Use a cost-effective model (Llama 3 8B) for summarization tasks.

## 3. Testing & Validation
*   **[ ] Unit Tests:** Add tests for `DocumentProcessorService` and `VectorDBService`.
*   **[ ] Integration Tests:** Add end-to-end tests for the Ingestion and Chat pipelines.

---
*Updated: April 23, 2026*
