from olea.error_handler import OleaException


class ValidationError(ValueError):
    def __init__(self, msg: str = ''):
        ValueError.__init__(self, msg)


class FormError(OleaException):
    def __init__(self, msg):
        super().__init__(code='SEYW', msg=msg)


class FormValueError(OleaException):
    def __init__(self, msg):
        super().__init__(code='JQWV', msg=msg)
