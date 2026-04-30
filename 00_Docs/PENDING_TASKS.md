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
*   **[x] Mood-Aware Response:** Dynamic tone adjustment (Sad/Happy/Stable) based on a numeric mood parameter (-1 to 1).
*   **[ ] Tiktoken Integration:** Implement precise token counting in `app/utils/tokens.py`.
*   **[x] Safety Prompt Engineering:** Refined system prompt for empathetic counseling, situational crisis triggers, and clinical boundaries.

## 2. Chat History Summarization (Complete)
*   **[x] Summarization Service:** Implemented using Llama 3 8B.
*   **[x] Summarization API:** Endpoint `POST /api/v1/summarize` registered and functional.
*   **[x] Chat Title Generation:** Endpoint `POST /api/v1/chat/title` implemented for UI session labeling.
*   **[x] Prompt Engineering:** Professional/empathetic summary prompt implemented.

## 3. Maintenance & Cleanup (New)
*   [x] **RAG Hallucination Fix:** Implemented greeting heuristic and prompt robustness to prevent irrelevant context usage for simple messages.
*   [x] Models Cleanup: De-duplicated `ChatMessage` and `ChatRequest` in `app/models/request.py`.
*   [x] Streamlit Frontend: Implemented a full-featured testing UI in `frontend/app.py`.
*   [ ] Tests: Add unit/integration tests for summarization and chat.

## 4. Security & Prompt Hardening (In Progress)
*   **[ ] Abuse Detection Layer:** Implement a dedicated moderation layer (e.g., Llama Guard) to filter abusive content before it reaches the counselor model.
*   **[ ] Session Guardrails:** Implement backend logic to verify session-start safety requirements (e.g., disclaimer acknowledgment state).
*   **[ ] Advanced Hardening:** Implement full security-first prompt architecture to prevent jailbreaking and instruction disclosure (Prop-01).
*   **[ ] Format Enforcement:** Integrate strict Markdown and empathy-first response rules into the `RAGService`.

## 5. Future Proposals (Planned)
*   **[ ] VectifyAI PageIndex:** Research into advanced PDF indexing (See `00_Docs/01_Future_Proposals/VectifyAI_PageIndex_Research.md`).

---
*Updated: April 29, 2026*
