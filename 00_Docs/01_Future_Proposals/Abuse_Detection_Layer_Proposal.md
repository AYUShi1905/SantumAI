# Proposal: Abuse Detection Layer (Moderation Service)

## 1. Overview
To ensure the safety of both the users and the system, Santum AI requires a dedicated **Abuse Detection Layer**. This layer will act as a "Security Guard," intercepting every user message before it reaches the core LLM (Counselor) to filter out hate speech, harassment, and extreme verbal abuse.

## 2. Technical Architecture
The moderation logic will be decoupled from the therapeutic generation logic to improve reliability and reduce token costs.

*   **Placement:** A new `ModerationService` in `app/services/moderation.py` will be called at the very beginning of the `chat/stream` endpoint.
*   **Model Selection:** 
    *   **Primary:** `Llama Guard 3` (via Groq) for ultra-fast, category-based moderation.
    *   **Fallback:** OpenAI Moderation API (if high accuracy is required for specific languages).
*   **Response Flow:**
    1. User sends message.
    2. `ModerationService` analyzes the text.
    3. If **UNSAFE**: The request is aborted, and a standardized "Safety Refusal" is returned.
    4. If **SAFE**: The message proceeds to the `RouterService`.

## 3. Moderation Categories
The layer will be configured to detect and flag the following:
*   **Violence & Physical Harm:** Threats or glorification of violence.
*   **Hate Speech:** Discrimination based on race, religion, sexual orientation, etc.
*   **Harassment:** Severe verbal abuse directed at the AI counselor.
*   **Self-Harm:** Identifying mentions of self-harm to trigger immediate crisis resources (988 Lifeline).
*   **Sexual Content:** Explicit or non-consensual sexual content.

## 4. Key Benefits
*   **Cost Efficiency:** Blocks abusive users before they consume expensive GPT-4 / 70B tokens.
*   **Jailbreak Resistance:** A separate model check is harder to bypass than simple system instructions.
*   **Auditability:** Allows for separate logging of safety violations to improve system guardrails over time.

## 5. Implementation Steps
1. Create `app/services/moderation.py`.
2. Configure `Llama Guard` classification prompt.
3. Update `app/api/v1/chat.py` to call the moderation layer before the RAG pipeline.
4. Define standardized safety refusal responses.
