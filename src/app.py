import src.http.http_app as http_app
import src.amqp.amqp_app as amqp_app
import src.trigger.http_trigger as http_trigger
import threading
from src.log.log import logger


class App:
    def __init__(self, triggers):
        self.http = http_app.HttpApp(__name__, [trigger for trigger in triggers
                                                if isinstance(trigger, http_trigger.HttpTrigger)])
        self.amqp = amqp_app.AmqpApp()

        self.http_thread = threading.Thread(target=self.http.run, args=('0.0.0.0', '5050'))
        self.amqp_thread = threading.Thread(target=self.amqp.run)

    def run(self):
        self.http_thread.start()
        self.amqp_thread.start()

        self.http_thread.join()
        self.amqp_thread.join()
        logger.info("Finished execution of app")
