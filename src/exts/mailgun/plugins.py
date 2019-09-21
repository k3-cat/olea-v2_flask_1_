from exts.jsonform.errors import ValidationError
from exts import mailgun


class EmailValidator():
    def __call__(self, field):
        result = mailgun.validate_adr(field.data)
        if result['risk'] in ('high', 'medium'):
            raise ValidationError(msg=', '.join(result['reason']))
