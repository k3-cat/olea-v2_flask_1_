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

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['mail'] = self

    def send(self, subject: str, to: str, template: str,
             values: Dict[str, str]):
        if self.app.env != 'prod':
            return
        maildata = build_message(subject, to, template, values)
        return self.mailgun_api.send(maildata)
