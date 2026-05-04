# Santum AI - System Flow & Latency Analysis

This document analyzes the execution pipeline of the Santum AI RAG service, identifying bottlenecks and proposing optimizations to achieve sub-second response times.

## 1. Current Serial Pipeline (Bottleneck)

Currently, the system executes every verification and reasoning step in a sequence. Even with ultra-fast components, the cumulative "Time to First Token" (TTFT) is approximately **2.5 seconds**.

```mermaid
sequenceDiagram
    participant U as User
    participant A as API (FastAPI)
    participant M as Moderation (Groq 8B)
    participant R as Router (Groq 8B)
    participant RE as Rephraser (Groq 8B)
    participant E as Embedder (Gemini)
    participant Q as Qdrant DB
    participant L as Final LLM (Groq 70B)

    U->>A: Send Message
    Note over A: Start Timer
    A->>M: 1. Moderation Check (~0.6s)
    M-->>A: Safe: True
    A->>R: 2. Route Classification (~0.5s)
    R-->>A: "Complex"
    A->>RE: 3. History Rephrasing (~0.6s)
    RE-->>A: Standalone Question
    A->>E: 4. Generate Embedding (~0.4s)
    E-->>A: Vector
    A->>Q: 5. Vector Search (~0.1s)
    Q-->>A: Context Chunks
    A->>L: 6. Final Generation
    L-->>U: [Streaming First Token]
    Note over A: Total Wait: ~2.2s - 2.8s
```

### Bottleneck Analysis
- **Cumulative Delay:** The sum of multiple LLM calls creates a "stutter" in user experience.
- **Idle Time:** The database and final LLM sit idle for ~1.7 seconds while waiting for pre-processing.

---

## 2. Proposed Parallel Pipeline (Optimized)

By utilizing Python's `asyncio.gather`, we can trigger independent checks simultaneously. The "wait time" is reduced to the duration of the **single longest task**.

```mermaid
sequenceDiagram
    participant U as User
    participant A as API (FastAPI)
    participant M as Moderation (Groq 8B)
    participant R as Router/Rephraser (Groq 8B)
    participant E as Embedder (Gemini)
    participant Q as Qdrant DB
    participant L as Final LLM (Groq 70B)

    U->>A: Send Message
    Note over A: Start Timer
    
    par Parallel Execution
        A->>M: Moderation Check
        A->>R: Classification & Rephrasing
        A->>E: Generate Embedding
    end

    Note right of E: Embedding finishes first (~0.4s)
    E->>Q: Start Search (Early)
    Q-->>A: Context Ready

    Note right of M: Moderation finishes (~0.6s)
    Note right of R: Reasoning finishes (~0.7s)

    A->>L: Final Generation (Using pre-fetched context)
    L-->>U: [Streaming First Token]
    
    Note over A: Total Wait: ~0.8s - 1.1s
```

### Optimization Strategies
1.  **Concurrent Verification:** Run Moderation, Routing, and Embedding in parallel.
2.  **Speculative Retrieval:** Fetch vectors and query Qdrant before the Moderation check is even finished. If Moderation fails, we simply discard the search result.
3.  **Heuristic Shortcuts:**
    - Use Python logic to detect greetings (bypass retrieval).
    - Use Python logic to detect standalone queries (bypass rephrasing).
4.  **Consolidated Reasoning:** Merge the Router and Rephraser into a single LLM call if possible, or run them in parallel.

## 3. Implementation Status
- [x] Gemini Embedding Migration (Reduced from 20s to 0.4s)
- [x] Refactor API for `asyncio.create_task` concurrency and Early Exits
- [x] Implement Parallel Router/Moderation logic
- [x] Move Rephrasing logic into parallel stream and integrate with final generation
- [x] Implement cancellation of redundant background tasks (e.g., cancelling retrieval on greeting/safety failure)
