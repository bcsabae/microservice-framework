import msfw.trigger.trigger as trigger


class AmqpTrigger(trigger.Trigger):
    def __init__(self, message_type, callback):
        super().__init__(callback)
        self.message_type = message_type

    def execute(self, **kwargs):
        if "message" not in kwargs:
            raise trigger.MissingArgumentError("message")
        self.callback(kwargs["message"])

