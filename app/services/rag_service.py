from typing import AsyncGenerator, List, Dict, Any
import json
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage

from app.services.llm_provider import LLMProviderService
from app.services.vector_db import VectorDBService

class RAGService:
    """
    Orchestration service for the Retrieval-Augmented Generation pipeline.
    """

    def __init__(self):
        self.llm_service = LLMProviderService()
        self.vector_db_service = VectorDBService()

    def _get_prompts(self) -> tuple:
        """Defines the system prompts for retrieval and answering."""
        
        # Contextualize Question Prompt
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        # QA System Prompt
        system_prompt = (
            "You are an empathetic and non-judgmental AI counselor. "
            "Use the following pieces of retrieved context from counseling manuals "
            "to answer the user's question. If you don't know the answer, "
            "stay supportive and suggest talking to a human therapist. "
            "Keep responses concise (max 250 words).\n\n"
            "{context}"
        )
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        return contextualize_q_prompt, qa_prompt

    async def get_streaming_response(
        self, 
        query: str, 
        chat_history: List[BaseMessage],
        use_reasoning: bool = False
    ) -> AsyncGenerator[str, None]:
        """
        Generates a streaming RAG response.
        Final chunk will contain token usage metadata.
        """
        llm = self.llm_service.get_llm(use_reasoning=use_reasoning)
        vectorstore = self.vector_db_service.get_vectorstore()
        retriever = vectorstore.as_retriever()

        contextualize_q_prompt, qa_prompt = self._get_prompts()

        # Create history-aware retriever
        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, contextualize_q_prompt
        )

        # Create QA chain
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

        # Create full retrieval chain
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        total_tokens = 0
        
        async for chunk in rag_chain.astream({"input": query, "chat_history": chat_history}):
            # LangChain retrieval chain yields dictionaries. 
            # 'answer' is the key for the generated text.
            if "answer" in chunk:
                yield chunk["answer"]
                # Rough token estimation for streaming (tiktoken should be used for precision)
                total_tokens += len(chunk["answer"].split()) * 1.3 

        # Final metadata chunk as required by docs
        metadata = {
            "total_tokens": int(total_tokens),
            "status": "completed"
        }
        yield f"\n{json.dumps(metadata)}"
