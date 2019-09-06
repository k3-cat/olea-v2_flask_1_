from olea.error_handler import OleaException


class ProjNotExist(OleaException):
    def __init__(self):
        super().__init__(code='8DTM', parms=None)


class DuplicateProj(OleaException):
    def __init__(self):
        super().__init__(code='QUSO', parms=None)


class AccessDenied(OleaException):
    def __init__(self):
        super().__init__(code='25HC', parms=None)


class RoleNotExist(OleaException):
    def __init__(self):
        super().__init__(code='GT7K', parms=None)


class RoleInitedBefore(OleaException):
    def __init__(self):
        super().__init__(code='9NZ5', parms=None)


class InvalidSource(OleaException):
    def __init__(self):
        super().__init__(code='4JZE', parms=None)


class UnableToFetchTitle(OleaException):
    def __init__(self):
        super().__init__(code='ABE1', parms=None)


class IsBooked(OleaException):
    def __init__(self):
        super().__init__(code='93M2', parms=None)


class BookedBefore(OleaException):
    def __init__(self, timestamp):
        super().__init__(code='JZI0', parms={timestamp})


class CancellingRejected(OleaException):
    def __init__(self):
        super().__init__(code='4J67', parms=None)
