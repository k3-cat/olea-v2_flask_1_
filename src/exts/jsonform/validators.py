import re

from .errors import ValidationError


class Regexp(object):
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
    def __init__(self, regex, flags=0, message=None):
        if isinstance(regex, str):
            regex = re.compile(regex, flags)
        self.regex = regex
        self.message = message

    def __call__(self, field, message=None):
        match = self.regex.match(field.data or '')
        if not match:
            if message is None:
                if self.message is None:
                    message = field.gettext('Invalid input.')
                else:
                    message = self.message

            raise ValidationError(message)
        return match


class IPAddress(object):
    """
    Validates an IP address.

    :param ipv4:
        If True, accept IPv4 addresses as valid (default True)
    :param ipv6:
        If True, accept IPv6 addresses as valid (default False)
    :param message:
        Error message to raise in case of a validation error.
    """
    def __init__(self, ipv4=True, ipv6=False, message=None):
        if not ipv4 and not ipv6:
            raise Exception(
                'IP Address Validator must have at least one of ipv4 or ipv6 enabled.'
            )
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.message = message

    def __call__(self, field):
        value = field.data
        valid = False
        if value:
            valid = (self.ipv4 and self.check_ipv4(value)) or (
                self.ipv6 and self.check_ipv6(value))

        if not valid:
            message = self.message
            if message is None:
                message = field.gettext('Invalid IP address.')
            raise ValidationError(message)

    @classmethod
    def check_ipv4(cls, value):
        parts = value.split('.')
        if len(parts) == 4 and all(x.isdigit() for x in parts):
            numbers = list(int(x) for x in parts)
            return all(num >= 0 and num < 256 for num in numbers)
        return False

    @classmethod
    def check_ipv6(cls, value):
        parts = value.split(':')
        if len(parts) > 8:
            return False

        num_blank = 0
        for part in parts:
            if not part:
                num_blank += 1
            else:
                try:
                    value = int(part, 16)
                except ValueError:
                    return False
                else:
                    if value < 0 or value >= 65536:
                        return False

        if num_blank < 2:
            return True
        elif num_blank == 2 and not parts[0] and not parts[1]:
            return True
        return False


class HostnameValidation(object):
    """
    Helper class for checking hostnames for validation.

    This is not a validator in and of itself, and as such is not exported.
    """
    hostname_part = re.compile(r'^(xn-|[a-z0-9]+)(-[a-z0-9]+)*$',
                               re.IGNORECASE)
    tld_part = re.compile(r'^([a-z]{2,20}|xn--([a-z0-9]+-)*[a-z0-9]+)$',
                          re.IGNORECASE)

    def __init__(self, require_tld=True, allow_ip=False):
        self.require_tld = require_tld
        self.allow_ip = allow_ip

    def __call__(self, hostname):
        if self.allow_ip:
            if IPAddress.check_ipv4(hostname) or IPAddress.check_ipv6(
                    hostname):
                return True

        # Encode out IDNA hostnames. This makes further validation easier.
        hostname = hostname.encode('idna')

        # Turn back into a string in Python 3x
        if not isinstance(hostname, str):
            hostname = hostname.decode('ascii')

        # Check that all labels in the hostname are valid
        parts = hostname.split('.')
        for part in parts:
            if not part or len(part) > 63:
                return False
            if not self.hostname_part.match(part):
                return False

        if self.require_tld:
            if len(parts) < 2 or not self.tld_part.match(parts[-1]):
                return False

        return True


class Email(Regexp):
    """
    Validates an email address. Note that this uses a very primitive regular
    expression and should only be used in instances where you later verify by
    other means, such as email activation or lookups.

    :param message:
        Error message to raise in case of a validation error.
    """
    def __init__(self, message=None):
        if message is None:
            message = 'Invalid email address.'
        self.validate_hostname = HostnameValidation(require_tld=True, )
        super(Email, self).__init__(r'^.+@([^.@][^@]+)$', re.IGNORECASE,
                                    message)

    def __call__(self, field):
        match = super(Email, self).__call__(field, self.message)
        if not self.validate_hostname(match.group(1)):
            raise ValidationError(self.message)
