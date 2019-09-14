from typing import Dict

from .api import MailGunAPI
from .message import build_message


class MailGun(object):
    def __init__(self):
        self.app = None
        self.mailgun_api = None
        self._send = None

    def init_app(self, app) -> None:
        self.app = app
        self.mailgun_api = MailGunAPI(app.config)

        if not app.config.get('FAKE_MAILGUN', False):
            self._send = self._send_
        else:
            self._send = lambda a, b, c, d: None

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
