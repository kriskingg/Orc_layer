from loguru import logger
import os

# Load log file path from environment variable
LOG_FILE = os.getenv("LOG_FILE_PATH", "app_logs.log")

# Set up logging to capture all relevant details and output to a file
logger.add(
    LOG_FILE, 
    rotation="500 MB", 
    level="DEBUG", 
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", 
    compression="zip"
)

logger.debug("Logging setup complete.")
