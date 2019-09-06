from flask import current_app, g

from enums import Perms
from exts.id_tools import generate_id
from exts.sqlalchemy_ import BaseModel, Column, ForeignKey
from exts.sqlalchemy_.types import ArrayOfEnum, DateTime, Enum, String


class Lemon(BaseModel):
    __tablename__ = 'lemon'

    key = Column(String(42), primary_key=True)
    pink_id = Column(String, ForeignKey('pink.id', ondelete='CASCADE'))
    expire = Column(DateTime)

    def __init__(self, pink_id):
        super().__init__(pink_id=pink_id)
        self.key = generate_id(42)
        self.expire = g.now + current_app.config.get('TOKEN_LIFE')


class ELemon(BaseModel):
    __tablename__ = 'elemon'

    key = Column(String(42), primary_key=True)
    pink_id = Column(String, ForeignKey('pink.id', ondelete='CASCADE'))
    perms = Column(ArrayOfEnum(Enum(Perms)))

    def __init__(self, pink):
        super().__init__(pink=pink)
        self.key = generate_id(42)
        self.perms = list()

    def has_perm(self, perm):
        return perm in self.perms

    def modi(self, asigns, revorks):
        for perm in revorks:
            if perm in self.perms:
                self.perms.remove(perm)
        self.perms.extend(asigns)
