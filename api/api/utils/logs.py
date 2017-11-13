import logging
import logging.config
from api import settings
logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("api")
