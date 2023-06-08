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
    def _extract_extra_string(extra):
        return f", extra: {[f'{key}:{str(item)}' for key, item in extra.items()]}" if extra is not None else ""

    def info(self, message: str, extra: Dict = None):
        logging.info(f"{message}{self._extract_extra_string(extra)}")

    def debug(self, message: str, extra: Dict = None):
        logging.debug(f"{message}{self._extract_extra_string(extra)}")

    def warning(self, message: str, extra: Dict = None):
        logging.warning(f"{message}{self._extract_extra_string(extra)}")

    def error(self, message: str, extra: Dict = None):
        for handler in self.error_handlers or []:
            handler.handle(message, extra=extra)
        logging.error(f"{message}{self._extract_extra_string(extra)}")


logger = Logger()