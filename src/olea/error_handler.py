import sentry_sdk
from flask import jsonify


class OleaException(Exception):
    def __init__(self, code: str, parms: dict()):
        super().__init__()
        self.code = code
        self.parms = parms or dict()


def register_error_handlers(app):
    def handle_olea_exceptions(e):
        return jsonify({'code': e.code, 'parms': e.parms}), 409

    app.register_error_handler(OleaException, handle_olea_exceptions)
    if app.env == 'prod':
        sentry_sdk.init(
            dsn=app.config['SENTRY_DSN'],
            integrations=[sentry_sdk.integrations.flask.FlaskIntegration()])