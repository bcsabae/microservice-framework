from abc import ABC, abstractmethod


class Trigger(ABC):
    def __init__(self, callback):
        self.callback = callback

    @abstractmethod
    def execute(self):
        raise NotImplementedError