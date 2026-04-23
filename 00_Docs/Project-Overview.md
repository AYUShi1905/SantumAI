# Santum AI PWA - Project Overview

## What is this project?
The **Santum AI PWA** is a standalone Progressive Web Application (PWA) designed to provide users with emotional-wellbeing support through text-based counseling conversations. It acts as an AI therapist, currently using Llama 3 (via Groq) for high-performance inference, with plans to migrate to OpenAI's GPT-4.1 in future updates.

The app will serve as an extension to an existing counseling platform, `santum.net`, but will run as its own standalone web app with its own branding, installable on mobile devices.

## Core Features & Functionality
- **AI Counseling Chat:** Users can text chat with an AI for emotional support. Simple interactions (greetings, FAQ) are handled by a faster model (**Llama 3 8B** via Groq), while deeper, complex emotional reasoning uses a more advanced model (**Llama 3 70B** via Groq).
- **Future Migration:** Integration with OpenAI GPT-4.1 mini and GPT-4.1 is planned for future phases to handle increasingly complex reasoning tasks.
- **RAG (Retrieval-Augmented Generation):** The AI will be trained/fed with specific psychological content (like CBT manuals). Free users get basic content, while premium users get access to deeper, specialized CBT content.
- **Safety First:** The app includes crisis resources, mood check-ins, safety disclaimers, abuse detection, and a "Talk to a human therapist" escalation button.
- **Cross-Platform:** Built as a PWA, meaning it works as a website but can be installed on phones/desktops like a native app. Fully responsive across all devices and browsers.

## How it works (System Flow)
1. **Shared Ecosystem:** The PWA connects to the existing WordPress backend of `santum.net`. Users don't need to create a brand new account; they use their existing Santum login (or create one that syncs).
2. **Token & Subscription System:** 
   - Access to the AI is token-based. 
   - New users get a free trial (token-limited).
   - There are paid subscription tiers (Free, Standard, Premium).
   - When a user chats with the AI, tokens are deducted.
3. **Subscriptions:** Paid through the existing Santum.net setup. The PWA will check if the user has an active AI subscription before letting them chat.

## Technical Architecture
- **Frontend:** React.js (built on an "Amigo GPT" template, customized to match Santum's branding).
- **Backend (API/AI Logic):** Dedicated Node.js server for handling the OpenAI integration securely, managing chat sessions, token counting, and RAG processing.
- **Master Database/Auth:** WordPress (`santum.net`), utilizing custom plugins (PWA AI), JWT authentication, and Paid Memberships Pro for subscriptions.

## Timeline & Effort
- **Estimated Effort:** 200 Development Hours
- **Deadline:** May 21, 2026

## Summary for the Developer/Owner
You are building an AI chatbot frontend (React) and a middleware backend (Node.js) that acts as a bridge between OpenAI and the client's existing WordPress user/payment database. Your main challenges will be syncing token balances, ensuring the subscription gate works flawlessly, and making sure the AI acts safely as a therapist using the provided CBT manuals (RAG).