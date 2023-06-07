import logging
import logging.config
from typing import Dict, List
from src.config.config import config
import sys


class Logger:
    def __init__(self, error_handlers: List = None):
        self.error_handlers = error_handlers

        log_format = '[%(asctime)s] %(levelname)s: %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'

        file_handler = logging.FileHandler(config.log_file, mode='a')
        file_handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=date_format))

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=date_format))

        root_logger = logging.getLogger()
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        root_logger.setLevel(config.log_level)

    @staticmethod
    def info(message: str, extra: Dict = None):
        extra_str = f", extra: {[f'{key}:{str(item)}' for item, key in enumerate(extra)]}" if extra is not None else ""
        logging.info(f"{message}{extra_str}")

    @staticmethod
    def debug(message: str, extra: Dict = None):
        extra_str = f", extra: {[f'{key}:{str(item)}' for item, key in enumerate(extra)]}" if extra is not None else ""
        logging.debug(f"{message}{extra_str}")

    @staticmethod
    def warning(message: str, extra: Dict = None):
        extra_str = f", extra: {[f'{key}:{str(item)}' for item, key in enumerate(extra)]}" if extra is not None else ""
        logging.warning(f"{message}{extra_str}")

    def error(self, message: str, extra: Dict = None):
        extra_str = f", extra: {[f'{key}:{str(item)}' for item, key in enumerate(extra)]}" if extra is not None else ""
        for handler in self.error_handlers or None:
            handler.handle(message, extra=extra)
        logging.error(f"{message}{extra_str}")


logger = Logger()