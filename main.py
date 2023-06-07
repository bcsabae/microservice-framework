import sys

import flask

from src.app import App
from src.trigger.http_trigger import HttpTrigger
from src.log.log import logger


def hello_callback():
    logger.info("Now in hello")
    return "Hello world"


def post_callback(body):
    logger.info("Now in post callback", extra=body)
    return flask.jsonify(body)


if __name__ == '__main__':
    post_callback.methods = ["POST"]

    http_triggers = [
        HttpTrigger('/hello', "GET", hello_callback),
        HttpTrigger('/test', "POST", post_callback)
    ]

    amqp_triggers = []

    app = App(triggers=http_triggers+amqp_triggers)

    app.run()