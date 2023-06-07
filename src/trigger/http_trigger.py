import src.trigger.trigger as trigger
import flask


class HttpTrigger(trigger.Trigger):
    def __init__(self, route: str, method: str, callback):
        super().__init__(callback)
        self.route = route
        self.method = method

    def execute(self):
        request = flask.request
        args = None
        if request.method == "GET":
            args = request.args.to_dict()
        if request.method == "POST":
            args = request.json
        return self.callback(args) if args else self.callback()