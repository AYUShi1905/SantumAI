# Project Overview: Santum AI PWA

## Project Summary
A standalone AI Counselling Progressive Web Application (PWA) providing emotional-wellbeing support. Currently powered by Llama 3 (via Groq) for high-performance inference, with future migration to GPT-4.1 planned. The system includes user-friendly registration, subscription flows, a token system, and deep API integration.

## Core Technical Stack
- **PWA AI:** Custom Plugin
- **Authentication:** JWT Authentication for WP REST API
- **Social Login:** WP Social
- **Membership System:** Paid Membership Pro (PMPro)
- **Credit System:**
    - `usermeta` (`_pwa_credit`) for current balance
    - `credit_log` table for transaction history
- **Frontend:** React.js
- **Backend:** Node.js / WordPress (as central system)

---

## System Architecture & Flows

### 1. Authentication Flow
- **Login Options:**
    - Mobile + Password
    - Social Login
- **Mobile Login Process:**
    - Authenticate user -> Generate JWT token -> Token used for future API requests
- **Social Login Process:**
    - Redirect to provider -> Callback to `https://santum.net/` -> User created/fetched -> JWT generated -> Redirect back to app

### 2. Registration & Verification
- **Registration:**
    - User created as `{mobile}@santum.net`
    - OTP generated
    - Hook: `do_action('pwa_send_sms_otp', $user_id, $otp, $expiry);`
- **Verification:**
    - OTP validated
    - User marked as verified

### 3. Membership & Plans
- **Admin Configuration:** `level_id` → credit tokens
- **Checkout Flow:**
    - User selects plan -> Redirect to `/membership-checkout/?level={level_id}` -> Payment completion -> Credits assigned -> Redirect back to app

### 4. Credit System Operations
- **Source of Truth:** `credit_log` table
- **Operations:**
    - **Increase:** Add + update balance
    - **Reduce:** Validate + deduct
    - **Sync:** Recalculate from logs
- **AI Chat Flow:**
    - User sends request -> Credits deducted first -> AI processes request -> (On failure) Credits rolled back

### 5. Profile Management
- Users can update: Name, DOB, Language, Interests.

---

## Detailed Scope of Work

### 1. Frontend (PWA) Customization
- Branding (logo, typography, colors, fonts, images)
- Mood check-in sliders
- Crisis resources button
- "Talk to a human therapist" escalation
- Plan-aware UI (Free, Standard, Premium)
- Token balance display and status indicators

### 2. AI Chat Module
- Multi-model strategy (**Llama 3 8B** for simple tasks/FAQ, **Llama 3 70B** for complex reasoning)
- Conversation loading and history view
- Responses capped to 250 words
- Real-time token usage calculation
- Context handling and safety measures (guardrails, disclaimer)

### 3. API Integration (Santum.net)
- Validate subscription status via API
- Sync user profile between PWA and website
- Fetch token balance and subscription type
- Handle session-based authentication (JWT / secure cookies)

### 4. Retrieval-Augmented Generation (RAG)
- Processing of custom content (PDF, DOCX)
- Content available based on plan level
- Tone calibration (empathetic, non-judgmental)
- Vector embedding storage and retrieval

---

## Access & Development Info
- **Main Backend:** `https://santum.net` (WordPress)
- **Staging Area:** `https://dddemo.net/wordpress/2026/santum/`
- **Admin Setting Page:** `https://prnt.sc/a56iQ67sPLIX`
- **Estimated Hours:** 200 Hours
- **Deadline:** 21st May, 2026
- **Key Principles:**
    - `credit_log` is the absolute source of truth.
    - `reference_id` ensures idempotency for credit transactions.
    - `pmpro_after_checkout` is the primary credit hook.
