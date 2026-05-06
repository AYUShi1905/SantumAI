# Santum AI - Coding Standards & Architecture

## 1. Core Principles

*   **Modular Monolith:** Organize code into logical modules (services, routes, models) within a single repository to avoid the overhead of microservices while maintaining clean boundaries.
*   **Single Responsibility Principle (SRP):** Each class, function, or module should have one clearly defined purpose.
*   **Don't Over-Engineer:** Favor readability and simplicity over complex abstractions. Only decouple when it provides a clear benefit for testing or reuse.
*   **Explicit over Implicit:** Use type hints (Python `typing`) and explicit configurations.
*   **Asynchronous First:** Utilize `async/await` for all I/O bound operations (API calls, DB queries) to maximize FastAPI's performance.

## 2. Folder Structure (FastAPI Microservice)

The `app/` directory follows a service-oriented structure:

```text
app/
├── main.py                # App entry point & middleware configuration
├── .env                   # Environment variables (not committed)
├── requirements.txt       # Project dependencies
├── api/                   # API Route Handlers (Controllers)
│   └── v1/                # Versioned API endpoints
│       ├── chat.py        # AI Chat & Streaming logic
│       └── ingest.py      # Document processing endpoints
├── core/                  # Global Configuration & Security
│   ├── config.py          # Pydantic Settings & Env vars
│   └── constants.py       # Static system constants
├── services/              # Business Logic Layer (The "Brain")
│   ├── rag_service.py     # LangChain & RAG orchestration
│   ├── vector_db.py       # Qdrant client & semantic search logic
│   ├── llm_provider.py    # OpenAI/Groq wrappers & model logic
│   ├── processor.py       # PDF parsing & text chunking logic
│   └── prompt_builder.py  # Centralized persona & security prompt logic
├── models/                # Data Schemas (Pydantic)
│   ├── request.py         # API Request models
│   └── response.py        # API Response & Metadata models
├── utils/                 # Shared Utilities
│   ├── logger.py          # Structured logging
│   └── tokens.py          # Tiktoken/Token counting helpers
└── tests/                 # Test Suite
    ├── unit/              # Service-level tests
    └── integration/       # API endpoint tests
```

## 3. Implementation Guidelines

### 3.1 Naming Conventions
*   **Files/Modules:** `snake_case.py`
*   **Classes:** `PascalCase`
*   **Functions/Variables:** `snake_case`
*   **Constants:** `UPPER_SNAKE_CASE`

### 3.2 Service Layer (SRP)
*   Routes in `api/` should only handle request validation and calling the appropriate service.
*   Complex logic (LangChain, Qdrant queries) must reside in `services/`.
*   Services should be class-based to allow for dependency injection and easier mocking during testing.

### 3.3 Error Handling
*   Use standard FastAPI `HTTPException` for client-facing errors.
*   Implement a global exception handler for logging internal server errors without leaking sensitive stack traces to the client.

### 3.4 RAG Specifics
*   **Embeddings:** All documents must be embedded using the Google Gemini `text-embedding-004` model (768 dimensions).
*   **Streaming:** Use `StreamingResponse` for AI chat to ensure low latency.
*   **Metadata:** The final chunk of any stream MUST be a JSON object containing `total_tokens`.

### 3.5 Type Safety
*   Strictly use Pydantic models for all API I/O.
*   Always include return type hints for functions.

### 3.6 Prompt Engineering
*   **Centralization:** NEVER hardcode system prompts in `rag_service.py` or API routes. All persona, security, and formatting instructions must reside in `services/prompt_builder.py`.
*   **Security Hardening:** All prompts must include the "Instruction Disclosure Defense" and "Jailbreak Defense" blocks.
*   **Format Enforcement:** Conversational Markdown rules (Selective Bolding, Empathy-First) must be strictly managed within the Builder.
