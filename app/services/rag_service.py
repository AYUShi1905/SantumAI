from typing import AsyncGenerator, List, Dict, Any, Optional
import json
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage

from qdrant_client.http import models as rest
from services.llm_provider import LLMProviderService
from services.vector_db import VectorDBService
from services.router import RouterService
from models.request import PlanLevel
from utils.tokens import count_tokens

class RAGService:
    """
    Orchestration service for the Retrieval-Augmented Generation pipeline.
    """

    def __init__(self):
        self.llm_service = LLMProviderService()
        self.vector_db_service = VectorDBService()
        self.router_service = RouterService()

    def _get_prompts(self, history_summary: Optional[str] = None) -> tuple:
        """Defines the system prompts for retrieval and answering."""
        
        # Contextualize Question Prompt
        contextualize_messages = []
        if history_summary:
            contextualize_messages.append(("system", f"Summary of previous conversation: {history_summary}"))
            
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        
        contextualize_messages.extend([
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        contextualize_q_prompt = ChatPromptTemplate.from_messages(contextualize_messages)

        # QA System Prompt
        qa_messages = []
        if history_summary:
            qa_messages.append(("system", f"Summary of previous conversation: {history_summary}"))

        system_prompt = (
            "You are an empathetic and non-judgmental AI counselor. "
            "Use the following pieces of retrieved context from counseling manuals "
            "to answer the user's question. If you don't know the answer, "
            "stay supportive and suggest talking to a human therapist. "
            "Keep responses concise (max 250 words).\n\n"
            "{context}"
        )
        
        qa_messages.extend([
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        qa_prompt = ChatPromptTemplate.from_messages(qa_messages)

        return contextualize_q_prompt, qa_prompt

    async def get_streaming_response(
        self, 
        query: str, 
        chat_history: List[BaseMessage],
        plan_level: PlanLevel = PlanLevel.FREE,
        use_reasoning: Optional[bool] = None,
        history_summary: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        Generates a streaming RAG response.
        Final chunk will contain token usage metadata.
        """
        # 1. Automatic Routing (Model Switching)
        if use_reasoning is None:
            classification = await self.router_service.classify(query)
            use_reasoning = (classification == "complex")
        
        llm = self.llm_service.get_llm(use_reasoning=use_reasoning)
        vectorstore = self.vector_db_service.get_vectorstore()
        
        # 2. Plan-based Filtering
        # If user is NOT premium, they only get non-CBT content
        search_kwargs = {"k": 5}
        if plan_level != PlanLevel.PREMIUM:
            search_kwargs["filter"] = rest.Filter(
                must=[
                    rest.FieldCondition(
                        key="metadata.is_cbt_manual",
                        match=rest.MatchValue(value=False)
                    )
                ]
            )
        
        retriever = vectorstore.as_retriever(search_kwargs=search_kwargs)

        contextualize_q_prompt, qa_prompt = self._get_prompts(history_summary=history_summary)

        # Create history-aware retriever
        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, contextualize_q_prompt
        )

        # Create QA chain
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

        # Create full retrieval chain
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        full_response = ""
        
        async for chunk in rag_chain.astream({"input": query, "chat_history": chat_history}):
            if "answer" in chunk:
                answer_part = chunk["answer"]
                full_response += answer_part
                yield answer_part

        # Calculate precise tokens using tiktoken
        total_tokens = count_tokens(full_response)

        # Final metadata chunk as required by docs
        metadata = {
            "total_tokens": total_tokens,
            "status": "completed",
            "model_used": "reasoning" if use_reasoning else "simple",
            "plan": plan_level
        }
        yield f"\n\n{json.dumps(metadata)}"
