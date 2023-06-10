from abc import ABC, abstractmethod
from typing import Dict


class ErrorHandler(ABC):
    @abstractmethod
    def handle(self, message: str, extra: Dict = None):
        raise NotImplementedError