from typing import Dict

import requests


class MailGunAPI():
    def __init__(self, config: Dict[str, str]):
        domain: str = config['MAILGUN_DOMAIN']
        self.base: str = f'https://api.eu.mailgun.net/v3/{domain}'
        self.sender: str = f'olea <no-reply@{domain}>'
        self.auth = ('api', config['MAILGUN_API_KEY'])
        if not self.auth[1]:
            raise Exception("No mailgun key supplied.")

    def send(self, maildata: Dict[str, str]):
        maildata['from'] = self.sender

        response = requests.post(f'{self.base}/messages',
                                 auth=self.auth,
                                 data=maildata)
        return response
