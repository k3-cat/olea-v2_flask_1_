from enums import ProjCat
from exts.jsonform import BaseForm, ValidationError
from exts.jsonform.validators import Regexp, Optional
from exts.jsonform.fields import (DateField, EnumField, RolesField,
                                  StringField)


class SingleProj(BaseForm):
    proj = StringField(validators=(
        Regexp(regex='[a-zA-z_-]{12}', message='invalid proj id'), ))


class EditNote(BaseForm):
    proj = StringField(validators=(
        Regexp(regex='[a-zA-z_-]{12}', message='invalid proj id'), ))
    note = StringField()


class Create(BaseForm):
    base = StringField()
    pub_date = DateField(format='%d-%b-%Y')
    cat = EnumField(ProjCat)
    note = StringField(validators=(Optional(), ))
    suff = StringField(validators=(Optional(), ))

    def validate_note(self, field):
        if not field.data:
            field.data = '{N/A}'
        if '$|' not in field.data:
            raise ValidationError('wrong format of note')


class InitRoles(BaseForm):
    proj = StringField(validators=(
        Regexp(regex='[a-zA-z_-]{12}', message='invalid proj id'), ))
    roles = RolesField()
