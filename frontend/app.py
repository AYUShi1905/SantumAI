import streamlit as st
import requests
import json
from typing import List, Dict

# Configuration
st.set_page_config(page_title="Santum AI - Testing Interface", layout="wide")

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "backend_url" not in st.session_state:
    st.session_state.backend_url = "http://localhost:8000/api/v1"
if "current_summary" not in st.session_state:
    st.session_state.current_summary = None

# Sidebar: Controls & Ingestion
with st.sidebar:
    st.title("⚙️ Santum AI Controls")
    
    st.session_state.backend_url = st.text_input("Backend API URL", value=st.session_state.backend_url)
    
    st.divider()
    
    st.subheader("👤 User Configuration")
    plan_level = st.selectbox("Plan Level", ["free", "standard", "premium"], index=0)
    reasoning_mode = st.radio("Reasoning Mode", ["Auto", "Force Simple (8B)", "Force Reasoning (70B)"], index=0)
    remaining_tokens = st.slider("Remaining Tokens", min_value=0, max_value=5000, value=1000, step=100)
    
    use_reasoning = None
    if reasoning_mode == "Force Simple (8B)":
        use_reasoning = False
    elif reasoning_mode == "Force Reasoning (70B)":
        use_reasoning = True

    st.divider()

    st.subheader("📄 Ingestion Management")
    is_cbt_manual = st.checkbox("Is CBT Manual?", value=False, help="Mark this if the document is a core therapeutic manual.")
    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])
    
    if st.button("Upload File", use_container_width=True) and uploaded_file:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        data = {"is_cbt_manual": is_cbt_manual}
        try:
            with st.spinner("Processing document..."):
                response = requests.post(
                    f"{st.session_state.backend_url}/ingest/file", 
                    files=files,
                    data=data
                )
                if response.status_code == 200:
                    st.success(f"Successfully ingested {uploaded_file.name}")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Connection failed: {str(e)}")

    if st.button("List Ingested Files", use_container_width=True):
        try:
            response = requests.get(f"{st.session_state.backend_url}/ingest/files")
            if response.status_code == 200:
                files = response.json().get("files", [])
                if files:
                    st.info("**Currently Embedded Files:**\n\n" + "\n".join([f"- {f}" for f in files]))
                else:
                    st.warning("No files found in collection.")
            else:
                st.error("Failed to fetch file list.")
        except Exception as e:
            st.error(f"Connection failed: {str(e)}")

    if st.button("Clear All Data", use_container_width=True):
        if st.checkbox("Confirm wipe all data?"):
            try:
                response = requests.delete(f"{st.session_state.backend_url}/ingest/all")
                if response.status_code == 200:
                    st.success("Vector database cleared.")
                else:
                    st.error("Failed to clear data.")
            except Exception as e:
                st.error(f"Connection failed: {str(e)}")

    st.divider()
    st.subheader("Running Summary")
    if st.session_state.current_summary:
        st.info(st.session_state.current_summary)
    else:
        st.caption("No summary generated yet. Chat a bit and click the summarize button below.")

# Main Chat Interface
st.title("💬 Santum AI Counselor")
st.caption("Empathetic AI counseling powered by Llama 3 & RAG")

# Summary Section
if st.button("📝 Summarize Conversation"):
    if not st.session_state.messages:
        st.warning("No conversation to summarize.")
    else:
        try:
            with st.spinner("Updating summary..."):
                payload = {
                    "chat_history": st.session_state.messages,
                    "existing_summary": st.session_state.current_summary
                }
                response = requests.post(f"{st.session_state.backend_url}/summarize", json=payload)
                if response.status_code == 200:
                    summary = response.json().get("summary", "")
                    st.session_state.current_summary = summary
                    st.info(f"**Updated Session Summary:**\n\n{summary}")
                else:
                    st.error("Summarization failed.")
        except Exception as e:
            st.error(f"Connection failed: {str(e)}")

if st.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.session_state.current_summary = None
    st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("How are you feeling today?"):
    # User message
    st.session_state.messages.append({"role": "human", "content": prompt})
    with st.chat_message("human"):
        st.markdown(prompt)

    # AI message streaming
    with st.chat_message("ai"):
        placeholder = st.empty()
        full_response = ""
        
        payload = {
            "message": prompt,
            "chat_history": st.session_state.messages[:-1], # Exclude current message
            "plan_level": plan_level,
            "use_reasoning": use_reasoning,
            "history_summary": st.session_state.current_summary,
            "remaining_tokens": remaining_tokens
        }
        
        try:
            response = requests.post(
                f"{st.session_state.backend_url}/chat/stream", 
                json=payload, 
                stream=True
            )
            response.raise_for_status()
            
            # Use a buffer to handle potential metadata split across chunks
            buffer = ""
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    # Check if this chunk or the buffer contains the metadata marker
                    if "\n\n{" in chunk:
                        parts = chunk.split("\n\n{", 1)
                        if parts[0]:
                            full_response += parts[0]
                            placeholder.markdown(full_response + "▌")
                        buffer = "{" + parts[1]
                    elif buffer:
                        buffer += chunk
                    else:
                        full_response += chunk
                        placeholder.markdown(full_response + "▌")
            
            # Finalize display
            placeholder.markdown(full_response)
            
            # Metadata display
            if buffer:
                try:
                    metadata = json.loads(buffer.strip())
                    st.caption(
                        f"Response completed | "
                        f"Tokens: {metadata.get('total_tokens', 'N/A')} | "
                        f"Model: {metadata.get('model_used', 'N/A')} | "
                        f"Plan: {metadata.get('plan', 'N/A')} | "
                        f"Status: {metadata.get('status', 'completed')}"
                    )
                except:
                    # If it wasn't valid JSON, it might be trailing text
                    full_response += buffer
                    placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "ai", "content": full_response})
            
        except Exception as e:
            st.error(f"Streaming failed: {str(e)}")
