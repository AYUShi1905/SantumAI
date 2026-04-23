# Santum AI PWA Project Details

*Extracted directly from email correspondence (Apr 8, 2026 - Apr 23, 2026)*

## Project Links & Scope
- **Project scope:** https://docs.google.com/document/d/1WoEDth93KQJRzsb3PUHzoJ6aljsVlL92Ext9-6k-rNU/edit?tab=t.94f7bseaa2k1
- **PMS:** https://pms.dddemo.net/hrms/taskassign.php?projectid=2317
- **Postman collection (works with stage site):** https://dddemo.net/wordpress/2026/santum/
- **Admin setting page (to configure plugin settings):** https://prnt.sc/a56iQ67sPLIX
- **Theme:** https://drive.google.com/file/d/1-DBJyGpk4fgxl2In6V52NfiDPsZoDE7S/view?usp=share_link

## Credentials & Access Details
**Server Hosting:**
- Login: https://identity.xneelo.com/
- User: support@dynamicdreamz.com
- Pass: DevDyna$#@321
- IP: 154.65.98.147

**WP Admin Credentials:**
- URL: https://santum.net/wp-login.php
- U: support@dynamicdreamz.com
- P: mfk3(%igJRX@vRG
- *Alternative Admin added:* U: support@dynamicdreamz.com | P: )(U^VJUwL0A)Q(HRYwbxI#MJ

**FTP Details:**
- `<Host>`santum.net`</Host>`
- `<Port>`21`</Port>`
- `<Protocol>`0`</Protocol>`
- `<Type>`0`</Type>`
- `<User>`santumcmarw`</User>`
- `<Pass>`T3gzOU9zakVRaXJRSjRtSE9uaDA=`</Pass>`

*Client Warning: "we have customized admin, theme and plugins. Please don't make any changes. Please note that site is live and these are sensitive areas, so be very careful with changes on your part."*

## Completed / In-Progress Work
- Made site copy to the staging area (https://dddemo.net/wordpress/2026/santum/)
- Created a plugin (PWA AI) to avoid modification to the existing codebase
- Added API endpoint for login and register by mobile number
- Added API endpoint to validate SMS OTP after registration
- Added hooks to enable OTP notification by external code from the plugin
- Set up the application, including routing, folder structure, APIs, PWA configuration, and CSS setup.
- Implemented the onboarding screen UI.
- Implemented the registration and login screen UI.
- Implemented the OTP screen UI.

## System Architecture & Technical Flow

### Core Stack
======================
- Custom Plugin: PWA AI
- Authentication: JWT Authentication for WP REST API
- Social Login: WP Social
- Membership System: Paid Membership Pro (PMPro)
- Credit System:
  - usermeta (`_pwa_credit`) for balance
  - `credit_log` table for transactions

### Authentication Flow
======================
Login Options:
1. Mobile + Password
2. Social Login

Mobile Login:
- Authenticate user
- Generate JWT token
- Token used for future API requests

Social Login:
- Redirect to provider
- Callback to https://santum.net/
- User created/fetched
- JWT generated
- Redirect back to app

### Registration & Verification
======================
Registration:
- User created as `{mobile}@santum.net`
- OTP generated
- Hook triggered: `do_action('pwa_send_sms_otp', $user_id, $otp, $expiry);`

Verification:
- OTP validated
- User marked verified

### Membership & Plans
======================
- Plans created in PMPro
- Admin maps: `level_id` → credit tokens

Flow:
- User selects plan
- Redirect to: `/membership-checkout/?level={level_id}`
- Payment completed
- Credits assigned
- Redirect back to app

### Credit System
======================
usermeta:
- `_pwa_credit` (current balance)

credit_log:
- user_id
- reference_id (unique)
- amount
- type (credit/debit)
- source
- note
- created_at

Operations:
- Increase → add + update balance
- Reduce → validate + deduct
- Sync → recalculate from logs

### AI Chat Flow
======================
- User sends request
- Credits deducted first
- AI processes request

Failure:
- Credits rolled back

### Profile Management
======================
User can update:
- Name
- DOB
- Language
- Interests

### System Flows
======================
1. Registration → Verification → Membership → AI Chat
2. Login → Edit Profile
3. Login → AI Chat

### Key Principles
======================
- `credit_log` = source of truth
- usermeta = cached balance
- `reference_id` ensures idempotency
- `pmpro_after_checkout` = primary credit hook
- confirmation page = fallback
- *Note: we need details on the plans that would be available as part of the PWA membership levels.*

## Subscription System Strategy

1) Santum.net Remains the Central System (WordPress as Master Backend)
- We will use the existing WordPress installation as the central authentication system. This means:
  - One email address per user
  - One password
  - One shared WordPress user database
- The PWA AI will connect to the same WordPress user system via secure API integration. No separate login database will be created.
- Users will use the same login credentials for both platforms.

2) Separate Subscription Systems (Independent Access Control)
- Although login is shared, subscriptions will remain separate and independent:
  - Santum.net subscription (Individual / Couples / Teens plans – existing structure remains unchanged)
  - PWA AI subscription (new subscription product)
- A user may have: Only Santum subscription, Only PWA AI subscription, Both, Neither.
- Access will always be controlled based on the relevant subscription type.

3) New User Flow
- If a user registers via Santum.net (existing live site):
  - Account is created in WordPress
  - User selects a Santum plan
  - Questionnaire is completed
  - Payment is processed
  - Access is granted
- If a user registers via PWA AI:
  - Account is created in the same WordPress database
  - User is directed to AI subscription
  - Payment is processed
  - Access is granted

4) Cross-Platform Access
- If a Santum user clicks to access PWA AI:
  - System checks AI subscription
  - If active → direct access
  - If not active → prompt to subscribe
- If a PWA AI user clicks to access Santum.net:
  - System checks Santum subscription
  - If active → direct access
  - If not active → redirect to plan selection and questionnaire
- Users will not need to create another account or maintain separate passwords.

## Task Details: SANTUM AI PWA PROJECT OVERVIEW

Web App Name: PWA Application (Frontend: React.js and Backend: Node.js)
Estimated Hours: 200 Hours
Deadline: 21st May, 2026

You will build and deliver a standalone full AI Counselling Progressive Web Application (PWA) that provides users with emotional-wellbeing support using a combination of GPT4.1 mini and GPT4.1, for text-based conversations. Inclusive of simple, user-friendly registration and subscription flow, token system and API integration.

The PWA will be developed on Amigo GPT React template, as a frontend base. UI design and style will remain same, however cosmetic adjustments will be implemented (colours, fonts etc). Design to be fully responsive with all screen sizes, including mobile phones, tablets, laptops and desktops. PWA will also be compatible with all browsers such as Safari, Chrome, Firefox, Edge, Samsung Internet, and Opera.

The PWA will have its own domain, branding and will be installable on mobile and desktop devices via the browser 'Add to Home Screen'. It will have a clean on-page technical SEO status, and will connect with Santum.net using following core objectives:
- Integration to OpenAI GPT4.1 mini/GPT4.1 API
- Wordpress (Santum.net) master authentication and subscription management
- Dedicated Node.js backend for token management, usage tracking, security, RAG
- Token based subscription system
- Subscription payments via our existing Santum.net PayFast setup
- User account mapping and login
- Redirecting users to create full Santum.net counselling accounts
- Linking PWA ↔ Website for subscription management
- Implementing foundational RAG

The PWA will support:
- One free trial AI session (token-limited)
- Two paid monthly subscription tiers
- Token-controlled AI chat sessions with safety disclaimers

Wordpress integration, as per Dynamic Dreamz document (point 3.2), with our developer's support:
- Authentication setup
- Subscription configuration
- Webhooks & Payment handling
- API requirements

AI backend development - Node.js, as per Dynamic Dreamz document (point 3.3):
- Secure GPT proxy backend
- Chat session management
- Token management system
- Subscription and access control logic
- Safety, guardrails & compliance

## PRESUMED SCOPE OF WORK

1. Frontend (PWA) Customization
- Branding (logo, topography, colours, fonts, images etc)
- Mood check-in sliders
- Crisis resources button
- "Talk to a human therapist" escalation
- Plan-aware UI (Free, Standard, Premium)
- Token balance display
- Subscription status indicators
- Error handling states
- API integration wiring

2. User Account & Authentication
- Email-based login inside the PWA
- Signup/login handled on WP Santum.net (redirect from PWA)
- One free AI session for new users
- Basic profile & user information screen
- JWT or secure cookie validation
- Secure token storage
- Session persistence across browser and devices
- Auto logout on expiration
- Redirect logic between WP and PWA

3. AI Chat Module
- Multi-Model strategy using 'GPT4.1mini' and 'GPT4.1' for text-based emotional-support chat
- GPT4.1 mini for simple tasks like greetings, Santum / PWA info, simple questions, coping tips, FAQ etc
- GPT-4.1 for everything else, like deeper conversations, emotional context or complex reasoning
- Conversation loading and history view
- Responses capped to 250 words per response
- Real-time token usage calculation/display
- Rate limit notifications
- Chat history, summarized older chat history (display last 5 responses in full, rest will be summarized)
- Context handling within the conversation
- Safety measures, guardrails, and disclaimer prompts
- Crisis-response fallback messages (UI handling)
- Abuse detection
- Disclaimer presentation

4. Subscription Flow (PWA-Webiste)
- Direct web subscription via Santum.net
- PWA syncs subscription status in real-time
- After payment → PWA fetches updated subscription status
- Token limits automatically update based on the selected plan
- Token limits and pricing for each plan will be provided by us

5. Token Management
- Free trial token allocation
- Monthly reset for new token cycle
- Token usage counter
- Session limits for each plan (Free, Standard, Premium)
- Prompt to upgrade plan on token expiry
- Pause subscription when website payment fails
- Auto-resume after successful payment

6. API Integration With Santum.net
- Validate subscription status via API
- Sync user profile between PWA ↔ website
- Fetch token balance and subscription type
- Handle reactivation after successful payment
- Session based authentication (JWT / secure cookies)
- Notifications for: Payment failure, Subscription paused, Subscription renewed, Token cycle reset
- Our website developer will provide the necessary backend APIs from Santum.net. You will integrate those APIs into PWA.

7. PWA Navigation & UI
- Fully responsive UI (Mobile/Tablet/Desktop)
- PWA install prompt 'Add To Home Screen'
- Clean, modern mobile UI (style and colour scheme based on santum.net)
- AI chat screen
- Profile & settings
- Subscription status (view only)
- Help / FAQ / Safety screens / T's&C's / Privacy Policy
- External links to Santum.net
- Offline-safe handling for network failures
- Browser compatibility (Chrome, Firefox, Safari, Edge)

8. Implementation of basic Retrieval-Augmented Generation layer (RAG)
- Processing of our content (PDF, DOCX etc)
- CBT manual content will only be embedded and available for Premium plan users
- All other content will be embedded and available for Free and Standard plans users
- Tone calibration (empathetic, non-judgmental, reflective)
- Converting content into vector embeddings
- Storing embeddings in secure database
- Retrieving relevant content based on user queries
- Injecting retrieved content into GPT prompts before generating responses
- Testing and relevance tunning

9. Operational Components
- Assist with hosting company selection (reliability/value), and setup
- Assist with correct Open AI account registration and setup
- Ensure compatibility with all browsers (Safari, Chrome, Firefox, Edge, Samsung Internet, and Opera)
- Test and adjust responsiveness for all screen sizes (mobile phones, tablets, laptops and desktops)
- Test all functions in live mode, and fix glitches
- Fix on-page technical SEO issues (according to detailed SEMrush report)
- Check and adjust Indexing issues (as outlined in GSC report)

## Attachments
- Logo Source files 21-4.zip
- Logo Source files 20-4.zip