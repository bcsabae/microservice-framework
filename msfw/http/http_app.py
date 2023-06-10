from typing import List

import flask


class HttpApp(flask.Flask):
    def __init__(self, import_name: str, triggers: List):
        super().__init__(import_name)
        self.blueprint = flask.Blueprint('main', import_name)

        for trigger in triggers:
            self.blueprint.add_url_rule(trigger.route, trigger.route,
                                        view_func=trigger.execute,
                                        methods=[trigger.method])

        self.blueprint.add_url_rule('/health', 'health', lambda: flask.jsonify("ok"))
        self.blueprint.register_error_handler(Exception, self.handle_error)

        self.register_blueprint(self.blueprint)

    @staticmethod
    def handle_error(error):
        response = flask.jsonify(
            {
                'error': str(error),
                'code': 500
            }
        )
        response.status_code = getattr(error, 'code', 500)
        return response
