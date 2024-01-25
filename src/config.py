import os
import logging

FASTAPI_ENV = os.getenv("FASTAPI_ENV", "dev")
LOCALE_STR = os.getenv("LOCALE_STR", "en_US.utf8")
logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s",
    level=logging.INFO if FASTAPI_ENV != "dev" else logging.DEBUG
)
logger = logging.getLogger('expiry_calendar')
