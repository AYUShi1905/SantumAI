# Documentation: `/chat/stream` Endpoint

The `/chat/stream` endpoint is the primary entry point for the Santum AI counseling service. It provides a real-time, streaming response grounded in therapeutic manuals using Retrieval-Augmented Generation (RAG).

## 1. Endpoint Details
- **Path:** `/api/v1/chat/stream`
- **Method:** `POST`
- **Content-Type:** `application/json`
- **Response-Type:** `text/event-stream`

## 2. Request Schema (`ChatRequest`)

| Field | Type | Description |
| :--- | :--- | :--- |
| `message` | `string` | The current user input/question. |
| `chat_history` | `List[ChatMessage]` | The last few full messages (role: "human" or "ai"). |
| `history_summary` | `Optional[str]` | A condensed summary of older parts of the conversation. |
| `plan_level` | `string` | "free", "standard", or "premium". |
| `use_reasoning` | `Optional[bool]` | `true` (70B), `false` (8B), or `null` (auto-route). |
| `remaining_tokens`| `int` | The user's current token balance. |

## 3. Core Logic & Lifecycle

### A. Token Enforcement
The system checks `remaining_tokens` immediately. If the balance is `<= 0`, it returns an error message and terminates.

### B. Automatic Routing
If `use_reasoning` is not provided:
1. The **RouterService** classifies the query using a fast model (8B).
2. **Simple** queries (greetings, FAQs) route to the **Llama-3 8B** model.
3. **Complex** queries (emotional venting, counseling) route to the **Llama-3 70B** model.

### C. Heuristic Greeting Shield
To save tokens and latency, queries containing only 1-2 words (e.g., "Hello", "Hi there") bypass the Vector Database entirely.

### D. Plan-Aware Retrieval (RAG)
If retrieval is triggered:
- **Free/Standard:** Filters out documents marked as `is_cbt_manual: true`.
- **Premium:** Has access to the full knowledge base, including specialized CBT manuals.

### E. Balanced Empathy Prompting
The response length and tone are dynamically adjusted:
- **Introductory openers:** ~50 words (warm but brief).
- **Complex concerns:** ~250 words (full reflective listening).

## 4. Response Format
The endpoint streams text chunks. The final chunk of the stream is always a JSON metadata object separated by two newlines (`\n\n`).

### Example Success Metadata:
```json
{
  "total_tokens": 145,
  "status": "completed",
  "model_used": "reasoning",
  "plan": "premium"
}
```

### Example Truncated Metadata (Token limit hit):
```json
{
  "total_tokens": 500,
  "status": "truncated",
  "model_used": "simple",
  "plan": "free"
}
```

## 5. Usage Example (Python/Requests)

```python
import requests
import json

payload = {
    "message": "I'm feeling a bit anxious today.",
    "chat_history": [],
    "plan_level": "premium",
    "remaining_tokens": 1000
}

response = requests.post("http://localhost:8000/api/v1/chat/stream", json=payload, stream=True)

for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
    if "\n\n{" in chunk:
        text, metadata = chunk.split("\n\n{")
        print(f"TEXT: {text}")
        print(f"METADATA: {{{metadata}")
    else:
        print(chunk, end="", flush=True)
```
