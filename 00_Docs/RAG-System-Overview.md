# Santum AI - RAG System Architectural Overview

## 1. System Objective
A high-performance, scalable Python-based RAG (Retrieval-Augmented Generation) microservice designed to provide emotional-wellbeing support by grounding AI responses in verified counseling and CBT manuals.

## 2. Core Tech Stack
| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **API Framework** | **FastAPI** | High-performance, asynchronous, and easy integration with Python AI libraries. |
| **Orchestration** | **LangChain** | Standardizes the "Chain" of logic between the user, the database, and the LLM. |
| **Vector Database** | **Qdrant** | Production-grade, Rust-based engine for sub-10ms semantic search. |
| **Embedding Model** | **Jina (v2-base-en)** | 8k context window allows for high-quality embedding of long manual sections. |
| **LLM (Brain)** | **Llama 3 (via Groq)** | Current primary LLM for all reasoning; ultra-fast inference. (OpenAI GPT-4.1 migration planned). |

## 3. Data Processing Flow (Ingestion)
*This happens once when new manuals are added.*
1.  **Parsing:** `PyMuPDF` extracts text from PDF/DOCX counseling manuals.
2.  **Chunking:** `RecursiveCharacterTextSplitter` breaks text into ~500-800 token pieces with 10% overlap to preserve context.
3.  **Embedding:** Jina converts these text chunks into 768-dimensional mathematical vectors.
4.  **Storage:** Vectors and their original text (metadata) are stored in a **Qdrant Collection**.

## 4. Request Lifecycle (Inference - Streaming)
*This happens every time a user sends a message.*
1.  **Balance Verification (Next.js):** Before calling the AI, Next.js verifies the user has enough credits.
2.  **User Query:** Next.js opens a `StreamingResponse` connection to the FastAPI backend.
3.  **Semantic Search & Prompting:**
    - FastAPI/Qdrant finds the manual context (Top 3-5 chunks).
    - LangChain constructs the grounded prompt.
4.  **Streaming Inference:** 
    - The LLM (Groq/OpenAI) begins generating the response.
    - FastAPI streams text "chunks" to Next.js in real-time.
5.  **Final Metadata Chunk:** 
    - Once the response is finished, FastAPI sends one final "metadata" packet containing the `total_tokens` (Input + Output).
6.  **Update UI & DB (Next.js):** 
    - Next.js displays the streaming text to the user.
    - Once the metadata packet is received, Next.js executes the final token deduction in the database.

## 5. Token & Credit Management
- **Source of Truth:** The system treats **1 LLM Token = 1 User Credit**.
- **Input (Prompt) Tokens:** Includes the manual context and history. This is the "RAG Tax."
- **Output (Completion) Tokens:** The AI's generated response.
- **Stream Delivery:** Token counts are delivered as the **final event** in the server-sent events (SSE) stream.
- **Deduction Logic:** Next.js waits for the stream to close, captures the final token count, and updates the user's balance.


## 6. Key Advantages
- **Independence:** The Python AI logic is decoupled from the Next.js frontend, allowing it to be scaled or upgraded separately.
- **Speed:** By using Groq and Qdrant, the "thinking time" of the AI is minimized for a better user experience in counseling.
- **Flexibility:** LangChain makes it trivial to switch between Jina/OpenAI for embeddings or Groq/GPT-4 for the brain.
