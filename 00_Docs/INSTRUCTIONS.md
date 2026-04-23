# Project Instructions & Mandates

## 1. Environment Management
*   **Mandate:** Whenever a new environment variable is added to `app/core/config.py`, it **MUST** also be added to `app/.example.env` with a placeholder or sensible default.
*   **Security:** Never commit the actual `.env` file containing real API keys.

## 2. Documentation Updates
*   Any significant architectural changes or model switches must be reflected in the relevant documentation files in `00_Docs/`.

## 3. Modular Development
*   Adhere strictly to the `00_Docs/CODING_STANDARDS.md` regarding folder structure and the Service Layer pattern (SRP).
