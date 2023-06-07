import pydantic


class Message(pydantic.BaseModel):
    source: str
    type: str
    body: str
