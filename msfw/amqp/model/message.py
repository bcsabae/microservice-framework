from typing import Dict

import pydantic


class Message(pydantic.BaseModel):
    source: str
    type: str
    body: Dict


class CustomMessage(pydantic.BaseModel):
    source: str

    def __str__(self):
        return str(self.dict())


class AmqpHealthCheckMessage(CustomMessage):
    pass
