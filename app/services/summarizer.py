from typing import List
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from services.llm_provider import LLMProviderService
from models.request import ChatMessage

class SummarizationService:
    """
    Service for condensing chat history into concise summaries.
    """

    def __init__(self):
        self.llm_service = LLMProviderService()
        # Summarization typically uses the faster/cheaper model (8B)
        self.llm = self.llm_service.get_llm(use_reasoning=False, streaming=False)

    def _convert_messages(self, chat_history: List[ChatMessage]) -> List[BaseMessage]:
        """Converts internal ChatMessage models to LangChain BaseMessage objects."""
        lc_messages = []
        for msg in chat_history:
            role = msg.role.lower()
            if role == "human":
                lc_messages.append(HumanMessage(content=f"User: {msg.content}"))
            elif role == "ai":
                lc_messages.append(AIMessage(content=f"Counselor: {msg.content}"))
        return lc_messages

    async def summarize(self, chat_history: List[ChatMessage]) -> str:
        """
        Generates a concise summary of the provided chat history.
        """
        if not chat_history:
            return ""

        lc_messages = self._convert_messages(chat_history)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are an expert supervisor for a counseling service. "
                "Your task is to provide a concise, third-person summary of the conversation between a User and an AI Counselor. "
                "Do NOT respond to the user. Do NOT provide advice. "
                "Only summarize: \n"
                "1. The user's primary emotional concerns.\n"
                "2. The main topics discussed.\n"
                "3. The counselor's approach or suggestions.\n"
                "Format the output as a single, empathetic, and professional paragraph (max 150 words)."
            )),
            ("human", "Please summarize this conversation history:\n\n{chat_history}")
        ])

        chain = prompt | self.llm
        
        response = await chain.ainvoke({"chat_history": lc_messages})
        
        return response.content
