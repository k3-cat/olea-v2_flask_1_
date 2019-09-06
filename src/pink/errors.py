from olea.error_handler import OleaException


class PinkNotExist(OleaException):
    def __init__(self):
        super().__init__(code='3MVG', parms=None)


class DuplicatePink(OleaException):
    def __init__(self):
        super().__init__(code='JLKC', parms=None)


class AccessDenied(OleaException):
    def __init__(self):
        super().__init__(code='I2NT', parms=None)


class PwdTooWeek(OleaException):
    def __init__(self, strength: float):
        super().__init__(code='DZ7H', parms={'strength': str(strength)})


class CommonPwd(OleaException):
    def __init__(self):
        super().__init__(code='QNL2', parms=None)


class PwdTooShort(OleaException):
    def __init__(self):
        super().__init__(code='P1GU', parms=None)
