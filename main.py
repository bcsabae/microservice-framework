import sys

import flask

from msfw.app import App
from msfw.trigger.http_trigger import HttpTrigger
from msfw.trigger.amqp_trigger import AmqpTrigger
from msfw.log.log import logger
from msfw.amqp.model.message import CustomMessage
import pydantic

from msfw.trigger.timer_trigger import TimerTrigger


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


def timer_callback():
    logger.info("Hello world from timer trigger")


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

    timer_triggers = [
        TimerTrigger(timer_callback, 5)
    ]

    app = App(
        triggers=http_triggers+amqp_triggers+timer_triggers,
        is_http_enabled=True,
        is_amqp_enabled=True,
        is_timer_enabled=True
    )
    app.run()
