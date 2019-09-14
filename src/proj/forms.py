from enums import ProjCat
from exts.jsonform import BaseForm, ValidationError
from exts.jsonform.fields import DateField, EnumField, StringField
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
    note = StringField(optional=True, default='$|\n')
    suff = StringField(optional=True, default='')

    def validate_note(self, field):
        if not field.data:
            field.data = '{N/A}'
        if '$|\n' not in field.data:
            raise ValidationError('wrong pattern of note')


class InitRoles(BaseForm):
    proj = StringField(validators=(
        Regexp(regex='[a-zA-z_-]{12}', message='invalid proj id'), ))
    roles = RolesField()
