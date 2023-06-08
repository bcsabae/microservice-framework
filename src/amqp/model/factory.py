from typing import List, Dict

from src.log.log import logger


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
        try:
            cls = self._get_class(name)
            instance = cls.parse_obj(obj)
            return instance
        except MessageClassNotFound as e:
            logger.error(f"Cannot instantiate message of type {name}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Cannot instantiate message of type {name}: {e}", extra=obj)
            return None


factory = MessageFactory([])
