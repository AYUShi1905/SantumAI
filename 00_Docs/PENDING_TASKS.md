# Pending Tasks: Santum AI RAG System

This document tracks all approved features and improvements.

## 0. Ingestion Pipeline (Complete)
*   **[x] PDF Support:** Implemented with margin-cropping logic.
*   **[x] DOCX Support:** Implemented (Includes Table Extraction logic).
*   **[x] Scanned PDF Detection:** Returns error for non-text PDFs.
*   **[x] File Management:** Added List, Delete by Filename, and Clear All endpoints.
*   **[x] Ingestion Reporting:** Added a consolidated run report at the end of the JSON ingestion script to display success/failure stats per file.


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
*   **[x] Selective & Tiered RAG:** Implemented tiered retrieval (k=1/2/3) and conversational bypass (Prop-02).
*   **[x] Memory Optimization:** Limited recent context to 6 messages to prevent context bloat (Prop-02).
*   **[x] Natural Follow-up Logic:** Implemented dynamic Socratic follow-ups that only trigger when conversationally appropriate, with automatic suppression for greetings.

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
*   [x] **Prompt Softening:** Softened "Santum.net" recommendation logic to be conditional and clinically relevant.
*   [x] **Safety Policy Nuance:** Refined moderation policy to distinguish between social anxiety/stress and active crisis. Implemented generalized intent-based classification to prevent false positives for clinical terms like "depression" (Verified).
*   [x] **Configuration Synchronization:** Added missing environment variable (`GROQ_MODEL_MODERATION`) to `Settings` and `.example.env`.
*   [x] **LangSmith Trace Bundling:** Wrapped RAG service request flows in a `@traceable` decorator to bundle parallel traces under a single parent run.
*   [x] **OpenAI Migration:** Migrated primary LLM provider from Groq to OpenAI, transitioning to the `gpt-4.1` model family (including counseling, moderation, and routing) and updating configuration keys.
*   [x] **OpenAI Embeddings Migration:** Migrated vector retriever to `text-embedding-3-small` (1536 dimensions) and implemented automatic database dimension mismatch detection and collection recreation.
*   [x] Streamlit Frontend: Implemented a full-featured testing UI in `frontend/app.py`.
*   [x] Tests: Add unit/integration tests for summarization and chat.
*   [x] **Pre-deployment Check Script:** Implemented `check_project.py` in the `app` folder to compile python files and run the test suite.
*   [x] **CI/CD Workflow:** Added `.github/workflows/ci.yml` to run tests and trigger Render deployment hook only for backend changes under `app/`.

## 4. Security & Prompt Hardening (Complete)
*   **[x] Abuse Detection Layer:** Implement a dedicated moderation layer (e.g., GPT-OSS-Safeguard-20B) to filter abusive content before it reaches the counselor model.
*   **[x] Session Guardrails:** (Handled on Frontend) Disclaimer acknowledgment state is enforced directly by the client UI.
*   **[x] Advanced Hardening:** Implement full security-first prompt architecture to prevent jailbreaking and instruction disclosure (Prop-01).
*   **[x] Format Enforcement:** Integrate strict Markdown and empathy-first response rules into the `RAGService`.

## 5. Future Proposals (Planned)
*   **[x] RAG Tier Restrictions:** Implement metadata-based RAG filtering (`is_restricted` check) to trigger soft upgrade prompts on the Free tier. (See [RAG_Tier_Restrictions_Plan.md](00_Docs/RAG_Data/RAG_Tier_Restrictions_Plan.md)).
*   **[x] RAG Data Embedding:** Run the OpenAI-to-Qdrant embedding pipeline for the new JSON RAG dataset in `01_Embed_Ready` using metadata pruning and rate-limiting safeguards. (See [RAG_Embedding_Plan.md](00_Docs/RAG_Data/RAG_Embedding_Plan.md)).
*   **[ ] Domain-Based Retrieval:** Update the `RouterService` to classify query domains (e.g., `cbt_panic`, `cbt_depression`) and apply Qdrant metadata filters dynamically to restrict RAG retrieval to the relevant domain.

---
*Updated: July 1, 2026*
