import re

from .errors import ValidationError


class Regexp():
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
    def __init__(self, message='invalid email address'):
        super().__init__(regex=r'^[a-z0-9._-]+@(?:[a-z0-9-]+\.)+[a-z]{2,4}$',
                         flags=re.IGNORECASE,
                         message=message)
