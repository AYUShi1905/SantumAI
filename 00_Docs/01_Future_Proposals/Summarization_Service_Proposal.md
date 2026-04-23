# Feature Proposal: Chat Summarization Service

## 1. Overview
To improve user experience and reduce token usage in long-running conversations, the Frontend requires an endpoint that can condense a multi-turn chat history into a single, concise paragraph that captures the essence of the communication.

## 2. Requirement
*   **Input:** A list of `Message` objects (Human and AI roles).
*   **Output:** A single string (paragraph) summarizing the key topics, emotional state, and advice given during the conversation.

## 3. Technical Implementation Plan

### 3.1 Service Layer (`app/services/summarizer.py`)
*   Create a `SummarizationService` class.
*   Use a faster, cost-effective model (e.g., Llama 3 8B via Groq) for the summarization task.
*   **Prompt Strategy:** "Summarize the following interaction between an AI counselor and a user. Focus on the main emotional concerns and the core advice provided. Keep it to a single, empathetic paragraph."

### 3.2 API Layer (`app/api/v1/summarize.py`)
*   **Endpoint:** `POST /api/v1/summarize`
*   **Request Model:** `SummarizeRequest` (contains the `chat_history`).
*   **Response Model:** `SummarizeResponse` (contains the `summary` string).

## 4. Benefits
*   **Memory Efficiency:** The Frontend can store this summary as a "long-term memory" instead of keeping hundreds of messages.
*   **Quick Context:** Allows the user to quickly see a summary of their progress.
*   **Token Saving:** In future sessions, the summary can be passed to the AI instead of the full history.

## 5. Next Steps
*   This task is currently **Pending** and will be implemented after the core Chat/Streaming endpoint is verified.

---
*Created on April 23, 2026, as per user directive for frontend feature expansion.*
