import traceback
from typing import List

import msfw.amqp.client as client
import msfw.amqp.handler as handler
import msfw.amqp.model.message as message
import msfw.trigger.amqp_trigger as amqp_trigger
from msfw.log.log import logger


class AmqpApp:
    def __init__(self, triggers: List[amqp_trigger.AmqpTrigger]):
        healthcheck_trigger = amqp_trigger.AmqpTrigger(message.AmqpHealthCheckMessage, self.health_callback)
        triggers.append(healthcheck_trigger)

        message_types = [trigger.message_type for trigger in triggers]
        message_handler = handler.AmqpMessageHandler(triggers)
        self.client = client.RabbitMQClient(message_handler)
        self.client.register_message_classes(message_types)

    @staticmethod
    def health_callback(msg: message.AmqpHealthCheckMessage):
        logger.info(f"Healthcheck from {msg.source}: OK")

    def run(self):
        try:
            logger.info("Starting Amqp App...")
            if not self.client.connect():
                return
            self.client.receive()
        except Exception:
            logger.error(f"Unhandled exception occurred", extra={"traceback": traceback.format_exc()})
            logger.info("Disconnecting client")
            self.client.disconnect()
            return
