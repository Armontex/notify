from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent  # server/

LOG_DIR = BASE_DIR / "logs"
ENV_PATH = BASE_DIR / ".env"
