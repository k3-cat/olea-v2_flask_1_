from exts.jsonform import BaseForm
from exts.jsonform.fields import IntegerField, StringField


class Apply(BaseForm):
    reason = StringField()
    amount = IntegerField()


class Transfer(BaseForm):
    aid = StringField()
    pervious_id = StringField()
