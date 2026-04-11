import logging
import sys

def setup_logger():
    # Configure root logger
    logger = logging.getLogger("filahaty")
    logger.setLevel(logging.INFO)
    
    # Formatter with detailed info but clean for farming app
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Add handler once
    if not logger.handlers:
        logger.addHandler(console_handler)
    
    return logger

# Export a single logger instance
logger = setup_logger()
