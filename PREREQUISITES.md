# Santum AI - Deployment Guide & Prerequisites

This document outlines the system requirements, environment configurations, and external service dependencies required to set up and deploy the Santum AI FastAPI server.

## 1. System Requirements
- **Runtime:** Python 3.10 or higher.
- **Operating System:** Linux (recommended) or macOS.
- **Memory:** Minimum 4GB RAM (8GB recommended for production).
- **Disk Space:** 500MB for application files and dependencies.

## 2. External Service Dependencies
The application requires API access to a Vector Database and LLM providers.

### Option A: Cloud Services (Recommended for Production)
| Service | Purpose | Source |
| :--- | :--- | :--- |
| **Qdrant Cloud** | Managed Vector Database | [qdrant.tech](https://qdrant.tech/) |
| **Google Gemini** | Document Embeddings | [Google AI Studio](https://aistudio.google.com/) |
| **Groq** | **OpenAI Substitute** (Inference) | [Groq Cloud](https://console.groq.com/) |

> **Crucial Note:** This project uses **Groq** as the primary inference engine. While the original architecture was designed with OpenAI (GPT-4) in mind, **Groq is utilized as a high-performance, cost-effective substitute** to achieve sub-second response times for Llama 3 (8B/70B) models. The backend is optimized for the Groq API, and an OpenAI API key is **not** required for current operations.

### Option B: Local Qdrant (Open Source)
Qdrant can be hosted locally via Docker for data privacy or cost optimization.

**Run Qdrant via Docker:**
```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

**Environment Update for Local Qdrant:**
When running locally, update these variables in the `.env` file:
```env
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=  # Leave empty if no API key is configured in Docker
```


## 3. Environment Configuration
Create a `.env` file in the `app/` directory. Use the following template as a guide. All variables marked with `REQUIRED` must be populated.

```env
# --- Qdrant Vector DB ---
QDRANT_API_KEY=your_qdrant_api_key        # REQUIRED
QDRANT_URL=your_qdrant_cluster_url        # REQUIRED
COLLECTION_NAME=santum_ai_production     # REQUIRED

# --- Google Gemini Embeddings ---
GOOGLE_API_KEY=your_google_api_key        # REQUIRED
GOOGLE_EMBEDDING_MODEL=gemini-embedding-001

# --- Groq LLMs ---
GROQ_API_KEY=your_groq_api_key            # REQUIRED
GROQ_MODEL_SIMPLE=llama3-8b-8192
GROQ_MODEL_REASONING=llama3-70b-8192
GROQ_MODEL_MODERATION=llama3-70b-8192      # Note: Use Llama 3 for safety checks

# --- App Settings ---
PROJECT_NAME="Santum AI Production"
DEBUG=False

# --- LangSmith Tracing (Optional) ---
LANGSMITH_TRACING=false
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=santum-ai

# --- Rate Limiting (Gemini Free Tier) ---
EMBEDDING_BATCH_SIZE=5
EMBEDDING_DELAY_SECONDS=10.0
```

## 4. Installation Steps

### 1. Repository Setup
```bash
git clone https://github.com/AYUShi1905/SantumAI.git
cd SANTUM-AI/app
```

### 2. Environment Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Deployment Commands

### Backend (Production)
Run the FastAPI application using `uvicorn` with multiple workers.
```bash
# From within the 'app' directory
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

