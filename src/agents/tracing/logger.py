import logging
import logging.config
from .config import LOGGING_CONFIG


def setup_logging(logger_name: str) -> logging.Logger:
    ''' 
    Logger surfaces log messages for debugging purposesn which returns a printable string, for internal use only.
    '''
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(logger_name)
    logger.setLevel(
        logging.DEBUG
    )
    return logger