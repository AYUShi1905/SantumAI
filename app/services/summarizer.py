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

    async def summarize(self, chat_history: List[ChatMessage], existing_summary: str = None) -> str:
        """
        Generates or extends a concise summary of the provided chat history.
        """
        if not chat_history:
            return existing_summary or ""

        lc_messages = self._convert_messages(chat_history)
        
        system_prompt = (
            "You are an expert supervisor for a counseling service. "
            "Your task is to provide a concise, third-person summary of the conversation between a User and an AI Counselor. "
            "Do NOT respond to the user. Do NOT provide advice. "
            "Only summarize: \n"
            "1. The user's primary emotional concerns.\n"
            "2. The main topics discussed.\n"
            "3. The counselor's approach or suggestions.\n"
            "Format the output as a single, empathetic, and professional paragraph (max 180 words)."
        )

        if existing_summary:
            human_prompt = (
                "Here is an EXISTING SUMMARY of the previous part of the conversation:\n"
                f"{existing_summary}\n\n"
                "Please extend and update this summary based on the following NEW MESSAGES:\n"
                "{chat_history}\n\n"
                "Return a single consolidated summary that integrates both the old and new points seamlessly."
            )
        else:
            human_prompt = "Please summarize this conversation history:\n\n{chat_history}"

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", human_prompt)
        ])

        chain = prompt | self.llm
        
        response = await chain.ainvoke({"chat_history": lc_messages})
        
        return response.content

    async def generate_title(self, chat_history: List[ChatMessage]) -> str:
        """
        Generates a 3-5 word professional title for the conversation.
        """
        if not chat_history:
            return "New Conversation"

        lc_messages = self._convert_messages(chat_history)

        system_prompt = (
            "You are an expert at categorizing counseling sessions. "
            "Your task is to generate a short, professional, and empathetic title (3-5 words) for the chat history provided. "
            "The title should reflect the main topic or emotional focus. "
            "Do NOT use quotes. Do NOT use a period at the end. "
            "Examples: 'Workplace Anxiety Support', 'Grief and Loss Exploration', 'Coping with Relationship Stress'."
        )

        human_prompt = "Please generate a title for this conversation history:\n\n{chat_history}"

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", human_prompt)
        ])

        chain = prompt | self.llm
        
        response = await chain.ainvoke(
            {"chat_history": lc_messages},
            config={"run_name": "TitleGenerator"}
        )
        
        # Clean up response in case LLM added quotes or extra text
        title = response.content.strip().strip('"').strip("'")
        return title
le
