import logging

def setup_logging(name=None, level=logging.INFO):
    """
    Sets up a reusable logger with consistent formatting.

    :param name: Optional logger name (default: root logger)
    :param level: Logging level (default: INFO)
    :return: Configured logger instance
    """
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger(name)
