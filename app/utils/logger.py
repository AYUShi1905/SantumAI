import logging
import sys
from core.config import settings

def setup_logging():
    """
    Configures the global logging settings for the application.
    Sets the log level based on the DEBUG setting and directs output to stdout.
    """
    # Determine the log level based on the DEBUG flag in settings
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    
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
    
    logger.info(f"Logging initialized with level: {logging.getLevelName(log_level)}")
