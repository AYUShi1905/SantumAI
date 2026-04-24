# Pending Tasks: Santum AI RAG System

This document tracks all approved features and improvements.

## 0. Ingestion Pipeline (Complete)
*   **[x] PDF Support:** Implemented with margin-cropping logic.
*   **[x] DOCX Support:** Implemented (Includes Table Extraction logic).
*   **[x] Scanned PDF Detection:** Returns error for non-text PDFs.
*   **[x] File Management:** Added List, Delete by Filename, and Clear All endpoints.

## 1. Chat & Reasoning Phase
*   **[/] Chat Request Models:** Implemented but needs cleanup (duplicate models).
*   **[/] Chat API Endpoint:** Test endpoint created (`/chat/test-stream`). **Next Task:** Production RAG-based `/chat/stream`.
*   **[ ] Tiktoken Integration:** Implement precise token counting in `app/utils/tokens.py`.
*   **[ ] Safety Prompt Engineering:** Refine the system prompt for empathetic counseling and crisis disclaimer.

## 2. Chat History Summarization (Complete)
*   **[x] Summarization Service:** Implemented using Llama 3 8B.
*   **[x] Summarization API:** Endpoint `POST /api/v1/summarize` registered and functional.
*   **[x] Prompt Engineering:** Professional/empathetic summary prompt implemented.

## 3. Maintenance & Cleanup (New)
*   **[ ] Models Cleanup:** De-duplicate `Message`, `ChatMessage`, and `ChatRequest` in `app/models/request.py`.
*   **[ ] Tests:** Add unit/integration tests for summarization and chat.

---
*Updated: April 23, 2026*
