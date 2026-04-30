from langchain_groq import ChatGroq
from core.config import settings



def get_llm() -> ChatGroq:
    """
        Returns a configured ChatGroq instance.
        
        Args:
            use_reasoning: If True, uses the Llama 3 70B model; otherwise 8B.
            streaming: Whether to enable streaming responses.
    """
    api_key = settings.GROQ_API_KEY
    return ChatGroq(
            api_key=api_key,
            model_name="openai/gpt-oss-safeguard-20b",
            temperature=0.7, # Default temperature for counseling
            max_tokens=1024  # Capped based on project requirements (approx 250 words)
        )



llm = get_llm()

try:
    res = llm.invoke("")
    print(res)
except Exception as e:
    print(f"An error occurred: {e}")