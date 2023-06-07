import src.http.http_app as http_app
import src.amqp.amqp_app as amqp_app
import src.trigger.http_trigger as http_trigger


class App:
    def __init__(self, triggers):
        self.http = http_app.HttpApp(__name__, [trigger for trigger in triggers
                                                if isinstance(trigger, http_trigger.HttpTrigger)])
        self.amqp = amqp_app.AmqpApp()

    def run(self):
        self.http.run('0.0.0.0', '5050')