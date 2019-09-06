from enums import Perms
from exts.jsonform import BaseForm
from exts.jsonform.fields import EnumField, ListField, StringField
from exts.jsonform.validators import Regexp


class Login(BaseForm):
    name = StringField()
    pwd = StringField()


class SetPwd(BaseForm):
    pwd = StringField()


class ModiELemon(BaseForm):
    pink = StringField(validators=(
        Regexp(regex='[a-zA-z_-]{9}', message='invalid pink id'), ))
    asign = ListField(EnumField(Perms))
    revork = ListField(EnumField(Perms))
