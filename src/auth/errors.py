from olea.error_handler import OleaException


class InvalidCredential(OleaException):
    def __init__(self):
        super().__init__(code='516O', parms=None)
