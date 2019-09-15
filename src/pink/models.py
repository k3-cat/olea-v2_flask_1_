from typing import Any, Dict

from enums import Dep, LeafState
from exts.id_tools import generate_id
from exts.sqlalchemy_ import BaseModel, Column, relationship
from exts.sqlalchemy_.types import (ArrayOfEnum, Boolean, DateTime, Enum,
                                    Integer, String)
from leaf.models import Leaf

from .errors import CommonPwd, PwdTooShort, PwdTooWeek
from .passlib_ import olea_context
from .pwd_tools import WEAK_MAX, is_common_pwd, measure_strength


class Pink(BaseModel):
    __tablename__ = 'pink'

    id = Column(String, primary_key=True)
    name = Column(String, unique=True)
    qq = Column(String)
    line = Column(String)
    email = Column(String)
    deps = Column(ArrayOfEnum(Enum(Dep)))
    _pwd = Column(String)
    cc = Column(Integer, default=0)
    la = Column(DateTime)
    active = Column(Boolean, default=True)

    leafs = relationship('Leaf',
                         back_populates='pink',
                         lazy='dynamic',
                         passive_deletes=True)

    @property
    def pwd(self):
        return self._pwd

    @pwd.setter
    def pwd(self, pwd: str) -> None:
        if len(pwd) < 8:
            raise PwdTooShort()
        if is_common_pwd(pwd):
            raise CommonPwd()
        strength = measure_strength(pwd)
        if strength < WEAK_MAX:
            raise PwdTooWeek(strength=strength)
        self._pwd = olea_context.hash(pwd)

    def __init__(self, name: str, qq: str, line: str, email: str, deps: list):
        super().__init__(name=name, qq=qq, line=line, email=email, deps=deps)
        self.id = generate_id(9)

    def verify_pwd(self, pwd: str) -> bool:
        return olea_context.verify(pwd, self._pwd)

    def to_dict(self, lv: int) -> Dict[str, Any]:
        if lv == 0:
            return {
                'id': self.id,
                'name': self.name,
                'qq': self.qq,
                'line': self.line,
                'deps': list(set([dep.name[0:2] for dep in self.deps])),
            }
        if lv == 1:
            return {
                'id': self.id,
                'name': self.name,
                'qq': self.qq,
                'line': self.line,
                'deps': [dep.name for dep in self.deps],
                'cc': self.cc,
                'la': self.la,
                'leafs': [
                    leaf.to_dict(lv=0) for leaf in self.leafs.filter(Leaf.state.in_(
                        (LeafState.normal, LeafState.waiting, LeafState.paused_fin, LeafState.paused_tmp))).all()
                ]
            } # yapf: disable
