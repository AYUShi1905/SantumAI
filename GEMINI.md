# Santum AI - Project Instructions & Mandates

## 1. Environment Management
*   **Mandate:** Whenever a new environment variable is added to `app/core/config.py`, it **MUST** also be added to `app/.example.env` with a placeholder or sensible default.
*   **Pre-Modification Check:** Before making any modifications, you **MUST** read `app/core/config.py` and `app/.example.env` to understand the required variables and configuration state.
*   **Security:** Never commit the actual `.env` file containing real API keys.

## 2. Documentation Updates
*   Any significant architectural changes or model switches must be reflected in the relevant documentation files in `00_Docs/`.
*   **Pending Tasks:** You **MUST** update `00_Docs/PENDING_TASKS.md` whenever a task is completed (mark as [x]) or a new task is identified. Keep this file as the accurate "Source of Truth" for progress.

## 3. Modular Development
*   Adhere strictly to the `00_Docs/CODING_STANDARDS.md` regarding folder structure and the Service Layer pattern (SRP).

## 4. Task Execution & Autonomy
*   **Wait for Instruction:** Never jump to the next task or implement new features/endpoints immediately after finishing one.
*   **Explicit Approval:** You **MUST** wait for the user to explicitly say "proceed," "next task," or provide a specific directive before moving on to any new work.
## 6. Frontend Status
*   **Mandate:** The `frontend/` directory and the Streamlit application are for **internal testing purposes only**. 
*   **Restriction:** Do **NOT** include frontend components in deployment guides, prerequisite documentation, or architectural overviews unless explicitly instructed to do so. Focus all production-related efforts exclusively on the FastAPI backend.

## 7. LLM Provider Strategy
*   **Mandate:** **Groq** is the primary LLM provider and acts as a high-performance **substitute for OpenAI**. 
*   **Constraint:** Although some internal docs mention future OpenAI (GPT-4) migration, the current production implementation **MUST** stay focused on Groq. All documentation, environment variables, and code changes should prioritize Groq's infrastructure and Llama 3 models.
