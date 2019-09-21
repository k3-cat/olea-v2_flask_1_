from enums import Dep
from exts.jsonform import BaseForm, ValidationError
from exts.jsonform.fields import (EnumField, IntegerField, ListField,
                                  StringField)
from exts.jsonform.validators import Regexp
from exts.mailgun.plugins import EmailValidator

from .text_tools import measure_width


class SinglePink(BaseForm):
    pink = StringField(validators=(
        Regexp(regex='[a-zA-z_-]{9}', message='invalid pink id'), ))


class UpdateInfo(BaseForm):
    qq = IntegerField(optional=True,
                      min_val=100_000_000,
                      max_val=10_000_000_000)
    line = StringField(optional=True)
    email = StringField(optional=True, validators=(EmailValidator(), ))

    def validate(self):
        if self.qq.empty and self.line.empty:
            raise ValidationError('must provide ether qq or line')
        super().validate()


class Create(BaseForm):
    name = StringField()
    qq = IntegerField(optional=True,
                      min_val=100_000_000,
                      max_val=10_000_000_000)
    line = StringField(optional=True)
    email = StringField(validators=(EmailValidator(), ))
    deps = ListField(EnumField(Dep))

    def validate_name(self, field):
        if measure_width(field.data) > 16:
            raise ValidationError('name is too long')

    def validate(self):
        if self.qq.empty and self.line.empty:
            raise ValidationError('must provide ether qq or line')
        super().validate()
