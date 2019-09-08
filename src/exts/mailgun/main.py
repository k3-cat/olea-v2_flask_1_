from typing import Dict

from .api import MailGunAPI
from .message import build_message


class MailGun(object):
    app = None

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app) -> None:
        self.app = app
        self.mailgun_api = MailGunAPI(app.config)

        if 'MUTE_MAILGUN' in self.app.config and self.app.config[
                'MUTE_MAILGUN']:
            self._send = lambda a, b, c, d: None
        else:
            self._send = self._send_

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['mail'] = self

    def send(self, subject: str, to: str, template: str,
             values: Dict[str, str]):
        self._send(subject, to, template, values)

    def _send_(self, subject: str, to: str, template: str,
               values: Dict[str, str]):
        maildata = build_message(subject, to, template, values)
        self.mailgun_api.send(maildata)
