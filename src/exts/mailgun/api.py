from typing import Dict

import requests

BASE_URL = 'https://api.mailgun.net'


class MailGunAPI():
    def __init__(self, config: Dict[str, str]):
        domain: str = config['MAILGUN_DOMAIN']
        self.endpoints = {
            'send': f'{BASE_URL}/v3/{domain}/messages',
            'validate': f'{BASE_URL}/v4/address/validate'
        }
        self.sender = f'{config["MAILGUN_SENDER"]} <no-reply@{domain}>'
        self.auth = ('api', config['MAILGUN_API_KEY'])
        if not self.auth[1]:
            raise Exception('no mailgun key supplied')

    def send(self, maildata: Dict[str, str]):
        maildata['from'] = self.sender
        response = requests.post(self.endpoints['send'],
                                 auth=self.auth,
                                 data=maildata)
        return response

    def validate_adr(self, address: str):
        return requests.get(self.endpoints['validate'],
                            auth=self.auth,
                            params={'address': address})
