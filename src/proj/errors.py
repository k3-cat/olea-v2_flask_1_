from olea.error_handler import OleaException
from common_errors import AccessDenied, NonExistedObj

__all__ = [
    'AccessDenied', 'NonExistedObj', 'DuplicateProj', 'RolesExisted',
    'InvalidSource', 'UnableToFetchTitle', 'IsBooked', 'BookedBefore',
    'CancellingRejected'
]


class DuplicateProj(OleaException):
    def __init__(self):
        super().__init__(code='QUSO')


class RolesExisted(OleaException):
    def __init__(self):
        super().__init__(code='9NZ5')


class InvalidSource(OleaException):
    def __init__(self):
        super().__init__(code='4JZE')


class UnableToFetchTitle(OleaException):
    def __init__(self):
        super().__init__(code='ABE1')


class IsBooked(OleaException):
    def __init__(self):
        super().__init__(code='93M2')


class BookedBefore(OleaException):
    def __init__(self, timestamp):
        super().__init__(code='JZI0', timestamp=timestamp)


class CancellingRejected(OleaException):
    def __init__(self):
        super().__init__(code='4J67')


class RoleIsTaken(OleaException):
    def __init__(self):
        super().__init__(code='4J67')
