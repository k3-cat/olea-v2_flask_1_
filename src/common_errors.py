from olea.error_handler import OleaException


class NonExistedObj(OleaException):
    def __init__(self, cls):
        super().__init__(code='BYDE', cls=cls.__name__)


class AccessDenied(OleaException):
    def __init__(self, obj: object):
        super().__init__(code='UJCB', obj=obj.__name__)


class DuplicatedObj(OleaException):
    def __init__(self, obj: object):
        super().__init__(code='JQ9I', obj=obj.__name__)
