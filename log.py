import logging
from logging.handlers import RotatingFileHandler

log_handler = RotatingFileHandler("bank_management.log", maxBytes=5000000, backupCount=5)
log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logging.basicConfig(
    level=logging.INFO,
    handlers=[log_handler]
)
logger = logging.getLogger()
