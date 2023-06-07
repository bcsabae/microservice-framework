import src.amqp.client as client
from src.log.log import logger


class AmqpApp:
    def __init__(self):
        self.client = client.RabbitMQClient()

    def run(self):
        logger.info("Starting Aqmp App...")
        if not self.client.connect():
            return
        self.client._receive()
