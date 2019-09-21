from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Union

from flask import g

from enums import Dep, ProgressState, ProjCat
from exts.id_tools import generate_id
from exts.sqlalchemy_ import (BaseModel, Column, ForeignKey, UniqueConstraint,
                              relationship)
from exts.sqlalchemy_.types import (JSON, Boolean, Date, DateTime, Enum, ARRAY,
                                    String, Text)

from .elfs import run_elfs
from .errors import BookedBefore, CancellingRejected, IsBooked, RolesExisted
from .info_builder import build_basic_info, build_complexity_info

if TYPE_CHECKING:
    from leaf.models import Mango
    from pink.models import Pink


class Proj(BaseModel):
    __tablename__ = 'proj'

    id = Column(String, primary_key=True)
    title = Column(String, index=True)
    source = Column(String)
    pub_date = Column(Date)
    suff = Column(String)
    cat = Column(Enum(ProjCat))
    _note = Column(ARRAY(Text))
    complexity = Column(JSON)
    finish_at = Column(DateTime, index=True)

    leafs = relationship('Leaf',
                         back_populates='proj',
                         cascade='all, delete-orphan',
                         lazy='dynamic',
                         passive_deletes=True)
    progress = relationship('Progress',
                            uselist=False,
                            back_populates='proj',
                            cascade='all, delete-orphan',
                            passive_deletes=True)
    __table_args__ = (UniqueConstraint('source',
                                       'pub_date',
                                       'suff',
                                       name='_proj_uc'), )

    @property
    def display_title(self):
        return f'{self.title}({self.suff})' if self.suff else self.title

    @property
    def note(self) -> list:
        return self._note

    @note.setter
    def note(self, note, static: bool = False):
        self._note[not static] = note.replace('$|\n', ' ')

    def __init__(self, base: str, pub_date, cat, suff, note):
        super().__init__(pub_date=pub_date, suff=suff, cat=cat, note=note)
        self.title, self.source = build_basic_info(base=base, cat=cat)
        self.id = generate_id(12)
        self.complexity = build_complexity_info(self)
        Progress(proj=self)

    def call_elf(self, dep: Dep, mango: Mango, pos: bool) -> None:
        run_elfs(proj=self, dep=dep, mango=mango, pos=pos)

    def get_complexity_display(self) -> Dict[str, str]:
        result = self.complexity.copy()
        result['al'] = 0
        result['cl'] = 0
        for audio_length in self.complexity['al'].values():
            result['al'] += audio_length
        for audio_length in self.complexity['cl'].values():
            result['cl'] += audio_length
        return result

    def to_dict(self, lv: int) -> Dict[str, Union[str, List[str]]]:
        if lv == 0:
            return {
                'id': self.id,
                'title': self.display_title,
                'cat': self.cat.name,
                'url': self.source if self.cat is ProjCat.normal else None,
                'complexity': self.get_complexity_display(),
                'note': self.note.split('$|\n', 1),
                'booked': self.progress.booking_pink is not None
            } # yapf: disable
        if lv == 1:
            return {
                'id': self.id,
                'title': self.display_title,
                'cat': self.cat.name,
                'url': self.source if self.cat is ProjCat.normal else None,
                'pub_date': self.pub_date,
                'complexity': self.get_complexity_display(),
                'note': self.note.split('$|\n', 1),
                'booked_user': self.progress.booking_pink,
                'leafs': [leaf.to_dict(lv=0) for leaf in self.leafs.all()],
                'free_roles': [role.to_dict() for role in self.progress.freeroles]
            } # yapf: disable


class Progress(BaseModel):
    __tablename__ = 'progress'

    proj_id = Column(String,
                     ForeignKey('proj.id', ondelete='CASCADE'),
                     primary_key=True)
    state = Column(Enum(ProgressState), default=ProgressState.s0)
    booking_pink = Column(String, ForeignKey('pink.id'))
    booking_history = Column(JSON)
    unfinished = Column(JSON)

    proj = relationship('Proj', back_populates='progress')
    freeroles = relationship('FreeRole',
                             back_populates='progress',
                             cascade='all, delete-orphan',
                             lazy='dynamic',
                             passive_deletes=True)

    def __init__(self, proj: Proj):
        super().__init__(proj=proj)
        self.unfinished = dict()
        self.booking_history = dict()

    def set_roles(self, roles: Dict[Dep, List[str]]) -> None:
        if self.freeroles.first():
            raise RolesExisted()
        roles_ = {(dep, role)
                  for dep, roles in roles.items() for role in set(roles)}
        self.unfinished = {
            dep.name: len(set(roles))
            for dep, roles in roles.items()
        }
        for role_tup in roles_:
            self.freeroles.append(
                FreeRole(progress_id=self.proj_id,
                         dep=role_tup[0],
                         role=role_tup[1]))

    def book(self, pink_id: str) -> None:
        if self.booking_pink:
            raise IsBooked()
        if g.pink_id in self.booking_history:
            raise BookedBefore(timestamp=self.booking_history[pink_id])
        self.booking_pink = pink_id
        self.booking_history[pink_id] = g.now

    def put_role(self, leaf_id: str):
        freerole: FreeRole = self.freeroles.filter_by(leaf_id=leaf_id).first()
        freerole.leaf_id = None
        if freerole.proxy:
            # TODO: re-
            pass

    def cancell_booking(self, pink_id: str) -> None:
        if self.booking_pink != pink_id:
            raise CancellingRejected()
        self.booking_pink = None


class FreeRole(BaseModel):
    __tablename__ = 'freerole'

    id = Column(String, primary_key=True)
    progress_id = Column(String,
                         ForeignKey('progress.proj_id', ondelete='CASCADE'))
    dep = Column(Enum(Dep))
    role = Column(String)
    leaf_id = Column(String)
    proxy = Column(Boolean, default=False)
    requirements = Column(ARRAY(String))

    progress = relationship('Progress', back_populates='freeroles')

    def __init__(self, progress_id: str, dep: Dep, role: str):
        super().__init__(progress_id=progress_id, dep=dep, role=role)
        self.id = generate_id(9)
        self.requirements = list()

    def to_dict(self):
        return (self.id, self.dep.name, self.role)
