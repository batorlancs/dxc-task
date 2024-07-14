import sys
from loguru import logger


def configure_logger():
    logger_format_simple = (
        "<white>{time:YYYY-MM-DD HH:mm:ss.SSS}</white> | "
        "<level>{level: <8}</level> | "
        "- <level>{message}</level>"
    )

    logger.remove()
    logger.add(sys.stderr, format=logger_format_simple)


configure_logger()
