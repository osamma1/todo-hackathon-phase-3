import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging():
    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # Create logger
    logger = logging.getLogger("todo_backend")
    logger.setLevel(logging.DEBUG)
    
    # Create file handler with rotation
    file_handler = RotatingFileHandler(
        "logs/todo_backend.log",
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Initialize the logger
logger = setup_logging()