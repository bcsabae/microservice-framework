import sys

import flask

from src.app import App
from src.trigger.http_trigger import HttpTrigger
from src.trigger.amqp_trigger import AmqpTrigger
from src.log.log import logger
from src.amqp.model.message import CustomMessage


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
    raise NotImplementedError


class TestMessage(CustomMessage):
    key1: str
    key2: str


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
        is_http_enabled=False
    )
    app.run()