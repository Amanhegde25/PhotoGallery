import logging
import os
import sys
from datetime import datetime

# Check if running on Vercel (serverless environment)
IS_VERCEL = os.environ.get("VERCEL", False)

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter(
        "[%(asctime)s] %(filename)s:%(lineno)d - %(levelname)s - %(message)s"
    )
    
    # Always add stream handler for stdout (works everywhere)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    # Add file handler only for local development (not Vercel)
    if not IS_VERCEL:
        LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
        os.makedirs(LOG_DIR, exist_ok=True)
        LOG_FILE = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
        LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)
        
        file_handler = logging.FileHandler(LOG_FILE_PATH)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

if __name__ == "__main__":
    logger.info("Logger has been set up successfully.")