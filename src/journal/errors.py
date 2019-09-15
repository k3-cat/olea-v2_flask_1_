from olea.error_handler import OleaException


class JournalUpdated(OleaException):
    def __init__(self):
        super().__init__(code='AX2R')
