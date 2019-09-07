from enums import Dep
from exts.jsonform import BaseForm, ValidationError
from exts.jsonform.fields import (EnumField, IntegerField, ListField,
                                  StringField)
from exts.jsonform.validators import Email, Regexp

from .measure_width import calc_width


class SinglePink(BaseForm):
    pink = StringField(validators=(
        Regexp(regex='[a-zA-z_-]{9}', message='invalid pink id'), ))


class UpdateInfo(BaseForm):
    qq = IntegerField(optional=True)
    line = StringField(optional=True)
    email = StringField(optional=True, validators=(Email(), ))

    def validate_qq(self, field):
        if len(str(field.data)) < 9 or len(str(field.data)) > 10:
            raise ValidationError('not a valid qq')


class Create(BaseForm):
    name = StringField()
    qq = IntegerField(optional=True)
    line = StringField(optional=True)
    email = StringField(validators=(Email(), ))
    deps = ListField(EnumField(Dep))

    def validate_name(self, field):
        if calc_width(field.data) > 16:
            raise ValidationError('name is too long')

    def validate_qq(self, field):
        if len(str(field.data)) < 9 or len(str(field.data)) > 10:
            raise ValidationError('not a valid qq')
