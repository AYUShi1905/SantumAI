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
*   **Confirmation:** After completing a task, briefly summarize the result and stop to wait for further instructions.

## 5. Research & Context
*   **Ignore Old Docs:** Always ignore the `00_Docs/Original/` directory during research unless specifically instructed otherwise.
*   **Source of Truth:** Use `GEMINI.md`, `00_Docs/PENDING_TASKS.md`, and `00_Docs/CODING_STANDARDS.md` as your primary guides.
