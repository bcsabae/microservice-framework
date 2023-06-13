import traceback

import msfw.trigger.trigger as trigger
import threading

from msfw.log.log import logger


class TimerTrigger(trigger.Trigger):
    def __init__(self, callback, delay):
        self.delay = delay
        self._timer_thread = None
        super().__init__(callback)

    def execute(self, **kwargs):
        logger.info(f"Periodic callback was triggered, executing {self.callback.__name__}")
        try:
            self.callback(**kwargs)
        except Exception as e:
            logger.error("Exception during handling of timer callback", extra={
                'callback': self.callback.__name__,
                'exception': e,
                'traceback': traceback.format_exc()
            })
        finally:
            self._timer_thread = threading.Timer(self.delay, self.execute)
            logger.debug(f"Delaying execution with {self.delay} seconds")
            self._timer_thread.start()

    def stop(self):
        logger.info(f"Stopping periodic execution of {self.callback.__name__}")
        self._timer_thread.cancel()

    def is_waiting(self):
        return self._timer_thread.is_alive()
