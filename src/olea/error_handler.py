from flask import jsonify
from sentry_sdk import init as sentry_sdk_init
from sentry_sdk.integrations.flask import FlaskIntegration


class OleaException(Exception):
    def __init__(self, code: str, **kwargs):
        super().__init__()
        self.code = code
        self.parms = kwargs


def register_error_handlers(app):
    @app.register_error_handler(OleaException)
    def handle_olea_exceptions(e):
        return jsonify({'code': e.code, 'parms': e.parms}), 409

    if not app.config.get('IGNORE_ERRORS', False):
        sentry_sdk_init(dsn=app.config['SENTRY_DSN'],
                        integrations=[FlaskIntegration()])
