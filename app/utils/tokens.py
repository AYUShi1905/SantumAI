import tiktoken

def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    """
    Counts the number of tokens in a string using tiktoken.
    Default encoding is cl100k_base (GPT-4 / modern models).
    """
    if not text:
        return 0
        
    try:
        encoding = tiktoken.get_encoding(encoding_name)
        return len(encoding.encode(text))
    except Exception:
        # Fallback to rough estimation if tiktoken fails
        return len(text.split()) * 1.3
