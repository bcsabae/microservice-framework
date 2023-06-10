from typing import List

import src.amqp.model.message as message
import src.trigger.amqp_trigger as amqp_trigger
from src.log.log import logger


class AmqpMessageHandler:
    def __init__(self, triggers: List[amqp_trigger.AmqpTrigger]):
        self._triggers = triggers

    def handle(self, msg: message.CustomMessage):
        for trigger in self._triggers:
            if trigger.message_type == type(msg):
                logger.debug(f"Matching message {msg} with trigger {trigger}")
                trigger.execute(message=msg)
