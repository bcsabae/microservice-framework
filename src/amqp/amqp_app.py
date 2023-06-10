from typing import List

import src.amqp.client as client
from src.log.log import logger

import src.trigger.amqp_trigger as amqp_trigger
import src.amqp.handler as handler


class AmqpApp:
    def __init__(self, triggers: List[amqp_trigger.AmqpTrigger]):
        message_types = [trigger.message_type for trigger in triggers]
        message_handler = handler.AmqpMessageHandler(triggers)
        self.client = client.RabbitMQClient(message_handler)
        self.client.register_message_classes(message_types)

    def run(self):
        logger.info("Starting Aqmp App...")
        if not self.client.connect():
            return
        self.client._receive()
