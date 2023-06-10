from typing import List, Dict


class MessageClassNotFound(Exception):
    def __init__(self, name: str):
        self._message = f"No message class found with name {name}"

    def __str__(self):
        return self._message


class MessageFactory:
    def __init__(self, classes: List):
        self._classes = classes.copy()

    def _get_class(self, name: str):
        for cls in self._classes:
            if name == cls.__name__:
                return cls
        raise MessageClassNotFound(name)

    def make_message(self, name: str, obj: Dict):
        cls = self._get_class(name)
        instance = cls.parse_obj(obj)
        return instance


factory = MessageFactory([])
