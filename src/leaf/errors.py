from common_errors import AccessDenied, NonExistedObj
from olea.error_handler import OleaException

__all__ = [
    'AccessDenied', 'NonExistedObj', 'NoFileSubmited', 'DuplicateLeaf',
    'NotQualifiedToPick', 'StateLocked', 'UnallowedType', 'UnknowType'
]


class NoFileSubmited(OleaException):
    def __init__(self):
        super().__init__(code='RRKY')


class DuplicateLeaf(OleaException):
    def __init__(self):
        super().__init__(code='VT39')


class NotQualifiedToPick(OleaException):
    def __init__(self):
        super().__init__(code='CWAI')


class StateLocked(OleaException):
    def __init__(self, current):
        super().__init__(code='L5OM', curret=current.name)


class UnallowedType(OleaException):
    def __init__(self, mtype):
        super().__init__(code='C3D8', type=mtype)


class UnknowType(OleaException):
    def __init__(self):
        super().__init__(code='84RX')
