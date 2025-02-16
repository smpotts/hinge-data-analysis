from loguru import logger
import sys

# remove default loguru logger
logger.remove()

logger.add(
    sys.stderr, 
    format="<green>{time}</green> | <cyan>{level}</cyan> | <red>{message}</red> | <yellow>{file}</yellow>:<yellow>{line}</yellow> | <blue>{function}</blue>", 
    level="DEBUG")
