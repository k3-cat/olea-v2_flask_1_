import base64
import datetime

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from flask import current_app, g, request

from exts.id_tools import generate_id
from exts.sqlalchemy_ import BaseModel, Column, ForeignKey
from exts.sqlalchemy_.types import JSON, DateTime, LargeBinary, String

from .errors import PubicKeyExisted


class Lemon(BaseModel):
    __tablename__ = 'lemon'

    key = Column(String, primary_key=True)
    pink_id = Column(String, ForeignKey('pink.id', ondelete='CASCADE'))
    expire = Column(DateTime)

    def __init__(self, pink_id):
        super().__init__(pink_id=pink_id)
        self.key = generate_id(42)
        self.expire = g.now + current_app.config.get('TOKEN_LIFE')


class Duck(BaseModel):
    __tablename__ = 'duck'

    pink_id = Column(String,
                     ForeignKey('pink.id', ondelete='CASCADE'),
                     primary_key=True)
    pub_key = Column(LargeBinary(32))
    key_signature = Column()
    perms = Column(JSON)

    def __init__(self, pink_id):
        super().__init__(pink_id=pink_id)
        self.key = generate_id(42)
        self.perms = dict()

    def check_signature(self):
        try:
            signature = base64.decodebytes(request.headers['signature'])
            timestamp = datetime.datetime.fromisoformat(
                request.headers['timestamp'])
        except KeyError:
            return False
        if not g.now - datetime.timedelta(seconds=5) <= timestamp < g.now:
            return False
        public_key = Ed25519PublicKey.from_public_bytes(self.pub_key)
        try:
            public_key.verify(
                signature,
                f'{timestamp.isoformat}|{request.get_json()}'.encode('utf-8'))
        except InvalidSignature:
            return False
        return True

    def has_perm(self, perm):
        if perm not in self.perms:
            if 'all' in self.perms:
                perm = 'all'
            else:
                return False
        if self.perms[perm][0] == 'all':
            return True
        for scope in request.headers.get('scopes', 'all'):
            if scope not in self.perms[perm]:
                return False
        return True

    def set_pub_key(self, pub_key):
        if self.pub_key:
            raise PubicKeyExisted(pub_key=self.pub_key)
        self.pub_key = pub_key
