from olea.error_handler import OleaException


class NoFileSubmited(OleaException):
    def __init__(self):
        super().__init__(code='RRKY', parms=None)


class LeafNotExist(OleaException):
    def __init__(self):
        super().__init__(code='BPS8', parms=None)


class AccessDenied(OleaException):
    def __init__(self):
        super().__init__(code='0GB9', parms=None)


class DuplicateLeaf(OleaException):
    def __init__(self):
        super().__init__(code='VT39', parms=None)


class NotQualifiedToPick(OleaException):
    def __init__(self):
        super().__init__(code='CWAI', parms=None)


class StateLocked(OleaException):
    def __init__(self, current):
        super().__init__(code='L5OM', parms={'curret': current.name})


class NotAllowedType(OleaException):
    def __init__(self, mtype):
        super().__init__(code='C3D8', parms={'type': mtype})


class UnknowType(OleaException):
    def __init__(self):
        super().__init__(code='84RX', parms=None)
