from flask import abort, current_app, g, request

from exts.id_tools import generate_id
from exts.sqlalchemy_ import BaseModel, Column, ForeignKey, relationship
from exts.sqlalchemy_.types import JSON, DateTime, LargeBinary, String

from .errors import KeyHasExpired
from .signature_tools import check_signature


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

    id = Column(String, primary_key=True)
    pink_id = Column(String, ForeignKey('pink.id', ondelete='SET NULL'))
    perms = Column(JSON)

    duck_keys = relationship('DuckKey',
                             back_populates='duck',
                             lazy='dynamic',
                             cascade='all, delete-orphan',
                             passive_deletes=True)

    def __init__(self, pink_id):
        super().__init__(pink_id=pink_id)
        self.id = generate_id(9)
        self.perms = dict()

    def check_signature(self, signature, content):
        duck_key = self.duck_key
        if duck_key.expired_at and g.now > duck_key.expired_at:
            raise KeyHasExpired(pub_key=duck_key.pub_key,
                                expired_at=duck_key.expired_at)
        check_signature(pub_key=duck_key.pub_key,
                        signature=signature,
                        content=content)

    def has_perm(self, perm):
        if perm not in self.perms:
            if 'all' in self.perms:
                perm = 'all'
            else:
                abort(403)
        if self.perms[perm][0] == 'all':
            return
        for scope in request.headers.get('scopes', 'all'):
            if scope not in self.perms[perm]:
                abort(403)

    @property
    def duck_key(self):
        return self.duck_keys.order_by(DuckKey.created_at.desc()).first()

    @duck_key.setter
    def duck_key(self, pub_key, signature):
        new_pub_key = DuckKey(self, pub_key, signature)
        self.duck_key.expired_at = g.now
        self.duck_keys.append(new_pub_key)


class DuckKey(BaseModel):
    __tablename__ = 'duckkey'

    duck_id = Column(String,
                     ForeignKey('duck.id', ondelete='CASCADE'),
                     primary_key=True)
    pub_key = Column(LargeBinary(32))
    key_signature = Column(LargeBinary(32))
    created_at = Column(DateTime)
    expired_at = Column(DateTime)

    duck = relationship('Duck',
                        back_populates='duck_keys',
                        passive_deletes=True)

    def __init__(self, duck, pub_key, signature):
        check_signature(duck, signature=signature, content=pub_key)
        super().init(duck=duck, pub_key=pub_key, key_signature=signature)
        self.created_at = g.now
