import re

from .errors import ValidationError


class Regexp():
    """
    Validates the field against a user provided regexp.

    :param regex:
        The regular expression string to use. Can also be a compiled regular
        expression pattern.
    :param flags:
        The regexp flags to use, for example re.IGNORECASE. Ignored if
        `regex` is not a string.
    :param message:
        Error message to raise in case of a validation error.
    """
    def __init__(self, regex, flags=0, message='invalid input'):
        if isinstance(regex, str):
            regex = re.compile(regex, flags)
        self.regex = regex
        self.message = message

    def __call__(self, field):
        match = self.regex.match(field.data)
        if not match:
            raise ValidationError(self.message)


class Email(Regexp):
    """
    Validates an email address. Note that this uses a very primitive regular
    expression and should only be used in instances where you later verify by
    other means, such as email activation or lookups.

    :param message:
        Error message to raise in case of a validation error.
    """
    def __init__(self, message='invalid email address'):
        super().__init__(regex=r'^[a-z0-9._-]+@(?:[a-z0-9-]+\.)+[a-z]{2,4}$',
                         flags=re.IGNORECASE,
                         message=message)
