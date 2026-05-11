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
*   **[x] Mood-Aware Response:** Multi-dimensional EQ (Happiness, Stress, Energy) on a 1-10 scale.
*   **[x] Tiktoken Integration:** Implemented precise token counting in `app/utils/tokens.py`.
*   **[x] Safety Prompt Engineering:** Refined system prompt for empathetic counseling, situational crisis triggers, and clinical boundaries.
*   **[x] Human Therapist Redirection:** Integrated [Santum.net](https://Santum.net) referral logic into `ModerationService` and `RAGService` for professional care requests.
*   **[x] Dynamic Plan Limits:** Implemented 80/100/120 word caps for Input/Output across Free/Standard/Premium tiers.

## 2. Chat History Summarization (Complete)
*   **[x] Summarization Service:** Implemented using Llama 3 8B.
*   **[x] Summarization API:** Endpoint `POST /api/v1/summarize` registered and functional.
*   **[x] Chat Title Generation:** Endpoint `POST /api/v1/chat/title` implemented for UI session labeling.
*   **[x] Prompt Engineering:** Professional/empathetic summary prompt implemented.

## 3. Maintenance & Cleanup (New)
*   [x] **RAG Hallucination Fix:** Implemented greeting heuristic and prompt robustness to prevent irrelevant context usage for simple messages.
*   [x] **Embedding Migration:** Switched from Jina HTTP API (20s latency) to Google Gemini `gemini-embedding-001` (Fast/Free tier).
*   [x] **Latency Optimization (Parallelism):** 
    *   [x] Refactor API to use background tasks (`asyncio.create_task`) for true concurrent Moderation, Routing, and Speculative Retrieval with **Early Exits**.
    *   [x] **Router/Rephraser Merger:** Merge classification and rephrasing into a single LLM call to save tokens and time.
    *   [x] **Heuristic Bypass:** Implement fast Python-based greeting detection and early-exit logic to skip retrieval for introductory messages (Sub-100ms goal).
    *   [x] Standalone Query Integration: Fixed logic to ensure the rephrased query from the Router is actually used in the final LLM generation.
    *   [x] **Staged Embedding Generation:** Implemented async batching (100 docs) and delays (10s) with logging to handle Gemini rate limits.
    *   [x] Models Cleanup: De-duplicated `ChatMessage` and `ChatRequest` in `app/models/request.py`.
*   [x] Streamlit Frontend: Implemented a full-featured testing UI in `frontend/app.py`.
*   [ ] Tests: Add unit/integration tests for summarization and chat.

## 4. Security & Prompt Hardening (Complete)
*   **[x] Abuse Detection Layer:** Implement a dedicated moderation layer (e.g., GPT-OSS-Safeguard-20B) to filter abusive content before it reaches the counselor model.
*   **[ ] Session Guardrails:** Implement backend logic to verify session-start safety requirements (e.g., disclaimer acknowledgment state).
*   **[x] Advanced Hardening:** Implement full security-first prompt architecture to prevent jailbreaking and instruction disclosure (Prop-01).
*   **[x] Format Enforcement:** Integrate strict Markdown and empathy-first response rules into the `RAGService`.

## 5. Future Proposals (Planned)
*   **[ ] VectifyAI PageIndex:** Research into advanced PDF indexing (See `00_Docs/01_Future_Proposals/VectifyAI_PageIndex_Research.md`).

---
*Updated: May 11, 2026*
