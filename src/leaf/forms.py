from enums import Dep
from exts.jsonform import BaseForm
from exts.jsonform.validators import Regexp
from exts.jsonform.fields import EnumField, StringField


class Pick(BaseForm):
    proj = StringField(validators=(
        Regexp(regex='[a-zA-z_-]{12}', message='invalid proj id'), ))
    dep = EnumField(Dep)
    role = StringField()


class SingleLeaf(BaseForm):
    leaf = StringField(validators=(
        Regexp(regex='[a-zA-z_-]{15}', message='invalid leaf id'), ))
