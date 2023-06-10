from abc import ABC, abstractmethod


class MissingArgumentError(Exception):
    def __init__(self, argument: str):
        self.message = f"Missing argument {argument}"

    def __str__(self):
        return self.message


class Trigger(ABC):
    def __init__(self, callback):
        self.callback = callback

    @abstractmethod
    def execute(self, **kwargs):
        raise NotImplementedError

    def __str__(self):
        return f"{type(self)} trigger with callback {self.callback.__name__}"
