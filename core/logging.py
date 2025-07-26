import logging
from core.config import config

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s %(levelname)s %(module)s: %(message)s',
    handlers=[logging.StreamHandler()]
)

def get_logger(name="healthcare_ai_ed"):
    return logging.getLogger(name)
