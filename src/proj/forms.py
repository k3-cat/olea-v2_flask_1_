from enums import ProjCat
from exts.jsonform import BaseForm
from exts.jsonform.fields import DateField, EnumField, StringField, ListField
from exts.jsonform.validators import Regexp

from .custom_form_fields import RolesField


class SingleProj(BaseForm):
    proj = StringField(validators=(
        Regexp(regex='[a-zA-z_-]{12}', message='invalid proj id'), ))


class EditNote(BaseForm):
    proj = StringField(validators=(
        Regexp(regex='[a-zA-z_-]{12}', message='invalid proj id'), ))
    note = StringField()


class Create(BaseForm):
    base = StringField()
    pub_date = DateField(pattern='%d-%b-%Y')
    cat = EnumField(ProjCat)
    note = ListField(StringField(), min_entries=2, max_entries=2)
    suff = StringField(optional=True, default='')


class InitRoles(BaseForm):
    proj = StringField(validators=(
        Regexp(regex='[a-zA-z_-]{12}', message='invalid proj id'), ))
    roles = RolesField()
