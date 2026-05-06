import logging
import sys
from core.config import settings

def setup_logging():
    """
    Configures the global logging settings for the application.
    Defaults to INFO level to keep logs clean even if DEBUG=True is set for server reload.
    """
    # Force INFO level even if settings.DEBUG is True to avoid verbose library logs
    log_level = logging.INFO
    
    # Configure the root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
        force=True  # Overrides any existing default configuration (like from Uvicorn)
    )

    # Log that initialization is complete
    logger = logging.getLogger(__name__)
    
    # Silence noisy third-party libraries
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("groq").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    logger.info(f"Logging initialized with level: {logging.getLevelName(log_level)}")
