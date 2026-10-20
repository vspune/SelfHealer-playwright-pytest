import logging


def get_logger(name: str) -> logging.Logger:
    """Return a logger; format and level come from the log_* settings in pytest.ini."""
    return logging.getLogger(name)
