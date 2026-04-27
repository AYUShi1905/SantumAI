# Pending Tasks: Santum AI RAG System

This document tracks all approved features and improvements.

## 0. Ingestion Pipeline (Complete)
*   **[x] PDF Support:** Implemented with margin-cropping logic.
*   **[x] DOCX Support:** Implemented (Includes Table Extraction logic).
*   **[x] Scanned PDF Detection:** Returns error for non-text PDFs.
*   **[x] File Management:** Added List, Delete by Filename, and Clear All endpoints.

## 1. Chat & Reasoning Phase
*   **[x] Chat Request Models:** Updated with `PlanLevel` and `use_reasoning` override.
*   **[x] Production RAG Endpoint:** `/chat/stream` implemented with automated model switching.
*   **[x] Multi-Model Strategy:** Implemented `RouterService` for 8B vs 70B switching.
*   **[x] Plan-Aware RAG:** Content filtering based on subscription level (CBT vs non-CBT).
*   **[ ] Tiktoken Integration:** Implement precise token counting in `app/utils/tokens.py`.
*   **[x] Safety Prompt Engineering:** Refined system prompt for empathetic counseling, situational crisis triggers, and clinical boundaries.

## 2. Chat History Summarization (Complete)
*   **[x] Summarization Service:** Implemented using Llama 3 8B.
*   **[x] Summarization API:** Endpoint `POST /api/v1/summarize` registered and functional.
*   **[x] Prompt Engineering:** Professional/empathetic summary prompt implemented.

## 3. Maintenance & Cleanup (New)
*   [x] **RAG Hallucination Fix:** Implemented greeting heuristic and prompt robustness to prevent irrelevant context usage for simple messages.
*   [x] Models Cleanup: De-duplicated `ChatMessage` and `ChatRequest` in `app/models/request.py`.
*   [x] Streamlit Frontend: Implemented a full-featured testing UI in `frontend/app.py`.
*   [ ] Tests: Add unit/integration tests for summarization and chat.


## 5. Future Proposals (Planned)
*   **[ ] Prompt Hardening & Markdown:** Implementation of strict security guardrails and conversational formatting (See `00_Docs/01_Future_Proposals/Prompt_Hardening_and_Markdown_Strategy.md`).
*   **[ ] VectifyAI PageIndex:** Research into advanced PDF indexing (See `00_Docs/01_Future_Proposals/VectifyAI_PageIndex_Research.md`).

---
*Updated: April 24, 2026*
