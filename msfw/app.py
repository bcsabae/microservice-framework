import threading

import msfw.amqp.amqp_app as amqp_app
import msfw.http.http_app as http_app
import msfw.trigger.amqp_trigger as amqp_trigger
import msfw.trigger.http_trigger as http_trigger
from msfw.log.log import logger


class App:
    def __init__(self, triggers, is_http_enabled=True, is_amqp_enabled=True):
        self._http_flag = is_http_enabled
        self._amqp_flag = is_amqp_enabled

        if self._http_flag:
            self.http = http_app.HttpApp(__name__, [trigger for trigger in triggers
                                                    if isinstance(trigger, http_trigger.HttpTrigger)])
        if self._amqp_flag:
            self.amqp = amqp_app.AmqpApp([trigger for trigger in triggers
                                          if isinstance(trigger, amqp_trigger.AmqpTrigger)])

        if self._http_flag:
            self.http_thread = threading.Thread(target=self.http.run, args=('0.0.0.0', '5050'))
        if self._amqp_flag:
            self.amqp_thread = threading.Thread(target=self.amqp.run)

    def run(self):
        if self._http_flag:
            self.http_thread.start()
        if self._amqp_flag:
            self.amqp_thread.start()

        try:
            if self._http_flag:
                self.http_thread.join()
            if self._amqp_flag:
                self.amqp_thread.join()
        except KeyboardInterrupt:
            logger.warning("App was shut down forcefully, exiting")
            exit(0)
        logger.info("Finished execution of app")
