from typing import List

import src.amqp.client as client
from src.log.log import logger


class AmqpApp:
    def __init__(self, message_types: List):
        self.client = client.RabbitMQClient()
        self.client.register_message_classes(message_types)

    def run(self):
        logger.info("Starting Aqmp App...")
        if not self.client.connect():
            return
        self.client._receive()
