import base64

from olea.error_handler import OleaException


class InvalidCredential(OleaException):
    def __init__(self):
        super().__init__(code='516O')


class PubicKeyExisted(OleaException):
    def __init__(self, pub_key: bytes):
        super().__init__(code='516O', pub_key=base64.encodebytes(pub_key))
