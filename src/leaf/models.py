from __future__ import annotations

from typing import IO, TYPE_CHECKING, Dict

from flask import current_app, g

from enums import Dep, LeafState, MangoType
from exts import storage
from exts.id_tools import generate_id
from exts.sqlalchemy_ import (BaseModel, Column, ForeignKey, UniqueConstraint,
                              relationship)
from exts.sqlalchemy_.types import (ARRAY, JSON, Boolean, DateTime, Enum,
                                    LargeBinary, String)

from .audio_tools import get_audio_info
from .errors import NotQualifiedToPick, StateLocked, UnallowedType, UnknowType
from .file_tools import EXTS, is_allowed_type, special_save

if TYPE_CHECKING:
    from proj.models import Proj
    from pink.models import Pink


class Leaf(BaseModel):
    __tablename__ = 'leaf'

    id = Column(String, primary_key=True)
    proj_id = Column(String, ForeignKey('proj.id', ondelete='CASCADE'))
    dep = Column(Enum(Dep))
    role = Column(String)
    pink_id = Column(String, ForeignKey('pink.id'))
    state = Column(Enum(LeafState), default=LeafState.waiting)
    track = Column(ARRAY(String), default=list())
    timestamp = Column(DateTime)

    pink = relationship('Pink', back_populates='leafs')
    proj = relationship('Proj', back_populates='leafs')
    mangos = relationship('Mango',
                          back_populates='leaf',
                          cascade='all, delete-orphan',
                          passive_deletes=True)
    schedule = relationship('Schedule',
                            back_populates='leaf',
                            uselist=False,
                            cascade='all, delete-orphan',
                            passive_deletes=True)
    __table_args__ = (UniqueConstraint('proj_id',
                                       'dep',
                                       'role',
                                       'pink_id',
                                       name='_leaf_uc'), )

    def __init__(self, freerole, pink):
        if freerole.dep not in pink.deps:
            raise NotQualifiedToPick()
        super().__init__(proj_id=freerole.progress_id,
                         dep=freerole.dep,
                         role=freerole.role,
                         pink=pink,
                         timestamp=g.now)
        self.id = generate_id(15)
        self.proj.call_elf(dep=None, mango=None, pos=None)
        freerole.take(leaf_id=self.id)

    def drop(self, force: bool = False) -> None:
        if self.state != LeafState.normal and not force:
            raise StateLocked(current=self.state)
        self.state = LeafState.droped_m if not force else LeafState.droped_f
        self.track.append(f'drop|{g.now}' if not force else f'f_drop|{g.now}')
        self.proj.progress.put_role(leaf_id=self.id)

    def f_drop(self) -> None:
        self.pink.cc += 1
        self.drop(force=True)

    def submit(self, f: IO) -> None:
        if self.state != LeafState.normal:
            raise StateLocked(current=self.state)
        mango = Mango(leaf=self, f=f)
        self.state = LeafState.paused_fin
        self.proj.run_elfs(dep=self.dep, mango=mango, pos=True)
        self.track.append(f'fin|{g.now}')
        return mango

    def download(self):
        if self.state != LeafState.paused_fin:
            raise StateLocked(current=self.state)
        mango = self.mangos[-1]
        mango.download()
        return mango.id, mango.name

    def redo(self) -> None:
        if self.state != LeafState.paused_fin:
            raise StateLocked(current=self.state)
        mango: Mango = self.mangos[-1]
        mango.delete()
        self.state = LeafState.normal
        self.proj.run_elfs(dep=self.dep, mango=mango, pos=False)
        self.track.append(f'redo|{g.now}')

    def to_dict(self, lv: int) -> Dict[str, str]:
        if lv == 0:
            return {
                'id': self.id,
                'proj_id': self.proj_id,
                'dep_': self.dep.name,
                'role': self.role,
                'pink_id': self.pink.id,
                'state': self.state.name
            }


class Mango(BaseModel):
    __tablename__ = 'mango'

    id = Column(String, primary_key=True)
    leaf_id = Column(String, ForeignKey('leaf.id', ondelete='CASCADE'))
    mtype = Column(Enum(MangoType))
    fp = Column(LargeBinary(32))
    deleted = Column(Boolean, default=False)
    timestamp = Column(DateTime)
    metainfo = Column(JSON)

    leaf = relationship('Leaf', back_populates='mangos')

    @property
    def name(self):
        leaf = self.leaf
        return f'{leaf.dep}-{leaf.role} [{leaf.pink.name}-{self.id[:6]}].{EXTS[self.mtype]}'

    def __init__(self, leaf: Leaf, f: IO):
        super().__init__(leaf=leaf)
        self.id = generate_id(18)
        self.timestamp = g.now
        path = f'{current_app.root_path}/{self.id}'
        self.fp, self.mtype = special_save(f=f, path=path)
        if self.mtype is MangoType.unknown:
            raise UnknowType()
        if not is_allowed_type(self.dep, self.mtype):
            raise UnallowedType(mtype=self.mtype)
        # fetch info
        if self.mtype // 10 == 5:
            self.metainfo = get_audio_info(path=path)
        else:
            self.metainfo = None

        storage.upload(mango=self, path=path)

    def download(self) -> None:
        storage.download(mango=self)

    def delete(self) -> None:
        self.deleted = True


class Schedule(BaseModel):
    __tablename__ = 'schedule'

    leaf_id = Column(String,
                     ForeignKey('leaf.id', ondelete='CASCADE'),
                     primary_key=True)
    begin = Column(DateTime)
    due = Column(DateTime)
    paused_at = Column(DateTime)

    leaf = relationship('Leaf', back_populates='schedule')
