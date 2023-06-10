import json
from typing import List

import pika
import pika.exceptions
import pydantic

import msfw.amqp.handler as handler
import msfw.amqp.model.factory as factory
import msfw.amqp.model.message as message
from msfw.config.config import config
from msfw.log.log import logger


class RabbitMQClient:
    message_handler: handler.AmqpMessageHandler

    def __init__(self, message_handler: handler.AmqpMessageHandler):
        self.connection = None
        self.channel = None
        self.host = config.message_broker_host
        self.queue = config.message_broker_queue
        self.routing_key = config.app_name
        RabbitMQClient.message_handler = message_handler
        self.receiver_thread = None
        self.message_classes = []
        self.message_factory = factory.MessageFactory(self.message_classes)

    def register_message_classes(self, classes: List):
        self.message_classes = classes.copy()
        self.message_factory = factory.MessageFactory(self.message_classes)
        factory.factory = self.message_factory

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host)
            )
        except pika.exceptions.AMQPConnectionError as e:
            logger.error("Cannot establish connection", extra={
                "exception": str(e),
                "host": self.host
            })
            return False
        except Exception as e:
            logger.error("An error occured while attempting connection to AMQP host", extra={
                "exception": str(e),
                "host": self.host
            })
            return False
        self.channel = self.connection.channel()
        self.channel.queue_declare(self.queue)
        return True

    def disconnect(self):
        self.connection.close()

    def receive(self):
        self.channel.basic_consume(queue=self.queue, on_message_callback=self._incoming_message_callback, auto_ack=True)
        logger.info(f"Start listening on queue {self.queue}...")
        self.channel.start_consuming()

    @staticmethod
    def _incoming_message_callback(ch, method, properties, body):
        logger.debug("Received message", extra={'body': body})
        try:
            parsed_body = json.loads(body)
        except json.JSONDecodeError as e:
            logger.error("Error parsing incoming RabbitMQ message", extra={
                'exception': str(e),
                'body': body
            })
            return
        try:
            incoming_message = message.Message.parse_obj(parsed_body)
            message_type = incoming_message.type

            parsed_message = factory.factory.make_message(message_type, {
                "source": incoming_message.source,
                **incoming_message.body
            })
        except ValueError as e:
            logger.error("Failed to parse message", extra={
                'exception': str(e),
                'body': parsed_body
            })
            return
        except factory.MessageClassNotFound as e:
            logger.error(f"Failed to instantiate message", extra={
                'exception': str(e),
                'body': parsed_body
            })
            return
        logger.info(f"Handling message {incoming_message.type}: {incoming_message.body}")
        logger.info(f"Instantiated message of type {parsed_message.__class__.__name__}", extra=parsed_message.dict())
        RabbitMQClient.message_handler.handle(parsed_message)

    def send(self, body):
        if isinstance(body, pydantic.BaseModel):
            body = body.dict()
        self.channel.basic_publish(exchange='', routing_key=self.routing_key, body=str(body))
