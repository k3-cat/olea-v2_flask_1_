from exts.jsonform import BaseForm
from exts.jsonform.fields import StringField, BytesField


class Login(BaseForm):
    name = StringField()
    pwd = StringField()


class SetPwd(BaseForm):
    pwd = StringField()


class SetPubKey(BaseForm):
    pub_key = BytesField(32)
