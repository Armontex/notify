from loguru import logger
import sys
from pathlib import Path

LOG_FORMAT = "<green>{time:HH:mm:ss}</green> | <level>{level}</level> | " \
             "{name}:{function}:{line} - {message}"

logger.remove()

log_dir = Path("server/logs") # FIXME: Сделать абсолютный путь
log_dir.mkdir(exist_ok=True)


logger.add(
    log_dir / "server.log",
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    level="INFO",
    format=LOG_FORMAT
)


logger.add(
    sys.stdout,
    colorize=True,
    level="DEBUG",
    format=LOG_FORMAT
)