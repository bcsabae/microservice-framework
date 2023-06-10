import sys

import flask

from msfw.app import App
from msfw.trigger.http_trigger import HttpTrigger
from msfw.trigger.amqp_trigger import AmqpTrigger
from msfw.log.log import logger
from msfw.amqp.model.message import CustomMessage
import pydantic


def hello_callback():
    logger.info("Now in hello")
    return "Hello world"


def post_callback(body):
    logger.info("Now in post callback", extra=body)
    return flask.jsonify(body)


def amqp_callback(message):
    message_type = type(message)
    source = message.source
    logger.info(f"Now in AMQP callback, got {message_type} message from {source}", extra={
        "message": str(message)
    })
    logger.info(f"Content: {message.data}, {type(message.data)}")


class CustomDataType(pydantic.BaseModel):
    num: int
    comment: str


class TestMessage(CustomMessage):
    key1: str
    key2: str
    data: CustomDataType


if __name__ == '__main__':
    post_callback.methods = ["POST"]

    http_triggers = [
        HttpTrigger('/hello', "GET", hello_callback),
        HttpTrigger('/test', "POST", post_callback)
    ]

    amqp_triggers = [
        AmqpTrigger(TestMessage, amqp_callback)
    ]

    app = App(
        triggers=http_triggers+amqp_triggers,
        is_http_enabled=True
    )
    app.run()
