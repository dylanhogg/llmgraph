import os
from typing import Optional

from dotenv import load_dotenv
from loguru import logger

load_dotenv()


def get(name: str, default: Optional[str] = None) -> str:
    logger.trace(f"env.get called with name '{name}' and default '{default}'")
    if os.getenv(name) is None and default is None:
        raise Exception(f"{name} environment variable is not set.")
    elif os.getenv(name) is None:
        return default
    else:
        return os.environ[name]
