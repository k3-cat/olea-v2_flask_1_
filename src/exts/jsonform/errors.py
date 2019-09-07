from olea.error_handler import OleaException


class ValidationError(ValueError):
    """
    Raised when a validator fails to validate its input.
    """
    def __init__(self, message: str = ''):
        ValueError.__init__(self, message)


class StopValidation(Exception):
    """
    Causes the validation chain to stop.

    If StopValidation is raised, no more validators in the validation chain are
    called. If raised with a message, the message will be added to the errors
    list.
    """
    def __init__(self, message: str = ''):
        Exception.__init__(self, message)


class FormError(OleaException):
    def __init__(self, msg):
        super().__init__(code='SEYW', parms={'msg': msg})


class FormValueError(OleaException):
    def __init__(self, msg):
        super().__init__(code='JQWV', parms={'msg': msg})
