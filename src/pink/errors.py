from common_errors import AccessDenied, NonExistedObj, DuplicateObj
from olea.error_handler import OleaException

__all__ = [
    'AccessDenied', 'NonExistedObj', 'DuplicateObj', 'DuplicateObj',
    'PwdTooWeek', 'CommonPwd', 'PwdTooShort'
]


class PwdTooWeek(OleaException):
    def __init__(self, strength: float):
        super().__init__(code='DZ7H', strength=str(strength))


class CommonPwd(OleaException):
    def __init__(self):
        super().__init__(code='QNL2')


class PwdTooShort(OleaException):
    def __init__(self):
        super().__init__(code='P1GU')
