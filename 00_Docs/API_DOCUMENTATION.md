# Santum AI RAG Service - API Documentation

This document provides detailed information about the available API endpoints for the Santum AI RAG Service.

**Base URL:** `http://localhost:8000/api/v1` (Default local development)  
**Version:** `1.0.0`

---

## 1. Chat & Reasoning
Endpoints for interacting with the AI counselor.

### **POST /chat/stream** (Production RAG)
Streams an AI response grounded in retrieved counseling manuals. Includes automated model switching (8B vs 70B).

**Request Body:**
```json
{
  "message": "I've been feeling very anxious lately about my job.",
  "chat_history": [
    {"role": "human", "content": "Hi"},
    {"role": "ai", "content": "Hello! How can I support you today?"}
  ],
  "history_summary": "The user previously discussed their career goals and general life stressors.",
  "plan_level": "premium",
  "use_reasoning": null
}
```

**Parameters:**
- `message` (string): The current user query.
- `chat_history` (array): List of previous messages in `{"role": "human/ai", "content": "..."}` format. Usually the last 5 full messages.
- `history_summary` (string, optional): A summary of the conversation history prior to the `chat_history`.
- `plan_level` (enum): `free`, `standard`, or `premium`. Controls access to CBT manuals.
- `use_reasoning` (boolean, optional): Set to `true` to force Llama 3 70B, `false` for 8B. If `null`, the system routes automatically.

**Response:** A text stream (SSE) where the final chunk is a JSON object containing:
```json
{
  "total_tokens": 145,
  "status": "completed",
  "model_used": "reasoning",
  "plan": "premium"
}
```

---

## 2. Ingestion Pipeline
Endpoints for managing the knowledge base.

### **POST /ingest/file**
Uploads and processes a document (PDF/DOCX) for RAG.

**Request (Multipart/Form-Data):**
- `file` (Binary): The document.
- `is_cbt_manual` (boolean): `true` if this is a restricted CBT manual (Premium only).
- `header_margin` (float, default 0.1): Top margin to ignore in PDFs.
- `footer_margin` (float, default 0.1): Bottom margin to ignore in PDFs.

**Response:**
```json
{
  "message": "File successfully processed and ingested",
  "filename": "cbt_manual.pdf",
  "chunks_processed": 42
}
```

### **GET /ingest/files**
Lists all unique filenames currently stored in the vector database.

### **DELETE /ingest/file?filename=...**
Deletes all chunks associated with a specific file.

### **DELETE /ingest/all**
Clears the entire vector collection.

---

## 3. Summarization
### **POST /summarize**
Summarizes a long chat history into a concise, professional counselor's summary.

**Request Body:**
```json
{
  "chat_history": [...]
}
```

**Response:**
```json
{
  "summary": "The user discussed job-related anxiety and explored coping mechanisms...",
  "original_count": 12,
  "status": "success"
}
```

---

## 4. System & Observability
- **GET /health**: Returns system status and project metadata.
- **LangSmith Tracing**: If `LANGSMITH_TRACING=true` is set in environment, all `/chat` and `/summarize` calls are automatically traced in your LangSmith project for debugging.

---

## 5. Model Strategy (Internal Logic)
- **Simple Tasks**: Greetings, FAQ, and basic info use **Llama 3 8B**.
- **Complex Reasoning**: Emotional support and counseling use **Llama 3 70B**.
- **Routing**: Handled automatically by the `RouterService` unless overridden by `use_reasoning`.
