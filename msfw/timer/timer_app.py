from typing import List

import msfw.trigger.timer_trigger as timer_trigger


class TimerApp:
    def __init__(self, triggers: List[timer_trigger.TimerTrigger]):
        self._triggers = triggers.copy()
        pass

    def run(self):
        for trigger in self._triggers:
            trigger.execute()

    def stop(self):
        for trigger in self._triggers:
            trigger.stop()

    def is_alive(self):
        for trigger in self._triggers:
            if trigger.is_waiting():
                return True
