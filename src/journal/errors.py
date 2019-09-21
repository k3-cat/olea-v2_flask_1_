from olea.error_handler import OleaException
from common_errors import NonExistedObj


class JournalUpdated(OleaException):
    def __init__(self):
        super().__init__(code='AX2R')
