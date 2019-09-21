import base64

from olea.error_handler import OleaException


class InvalidCredential(OleaException):
    def __init__(self):
        super().__init__(code='516O')


class KeyHasExpired(OleaException):
    def __init__(self, pub_key: bytes, expired_at):
        super().__init__(code='WWXB',
                         pub_key=base64.encodebytes(pub_key),
                         expired_at=expired_at.isoformat())


class InvalidSignature(OleaException):
    def __init__(self, pub_key: bytes):
        super().__init__(code='W3JI', pub_key=base64.encodebytes(pub_key))


class InvalidEuropaeaRequet(OleaException):
    def __init__(self):
        super().__init__(code='NB4Y')
