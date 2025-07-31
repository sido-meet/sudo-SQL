import sys
from loguru import logger

# Remove default handler
logger.remove()

# Configure console logger
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    colorize=True,
)

# Configure file logger
logger.add(
    "logs/sudo-sql.log",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    rotation="10 MB",
    retention="7 days",
    enqueue=True,  # Make logging asynchronous
    backtrace=True,
    diagnose=True,
)

__all__ = ["logger"]
