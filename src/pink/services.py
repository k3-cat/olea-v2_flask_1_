from __future__ import annotations

from exts import db, mailgun
from exts.sqlalchemy_.utils import test_unique

from .errors import (AccessDenied, CommonPwd, NonExistedObj, PwdTooShort,
                     PwdTooWeek)
from .models import Pink
from .passlib_ import olea_context
from .pwd_tools import WEAK_MAX, generate_pwd, is_common_pwd, measure_strength
from auth.models import Lemon, Duck


class PinkService():
    @staticmethod
    def query_pink(id: str, europaea: bool = False) -> Pink:
        pink: Pink = Pink.query.get(id)
        if not pink:
            raise NonExistedObj(cls=Pink)
        if not pink.active and not europaea:
            raise AccessDenied(obj=pink)
        return pink

    @staticmethod
    def init_by_id(id: str):
        pink = PinkService.query_pink(id)
        return PinkService(pink)

    @staticmethod
    def init_by_create(name: str, qq: int, line: str, email: str,
                       deps: list) -> PinkService:
        pink: Pink = Pink(name=name,
                          qq=str(qq),
                          line=line,
                          email=email,
                          deps=deps)
        test_unique(pink)
        pink_service = PinkService(pink)
        pink_service.reset_pwd(init=True)
        return pink_service

    def __init__(self, pink):
        self.pink = pink
        self.id = pink.id
        db.session.add(self.pink)

    def set_pwd(self, pwd):
        if len(pwd) < 8:
            raise PwdTooShort()
        if is_common_pwd(pwd):
            raise CommonPwd()
        strength = measure_strength(pwd)
        if strength < WEAK_MAX:
            raise PwdTooWeek(strength=strength)
        self.pink.pwd = pwd

    def verify_pwd(self, pwd: str) -> bool:
        return olea_context.verify(pwd, self.pink._pwd)

    def reset_pwd(self, init=False):
        pwd = generate_pwd()
        self.pink.pwd = pwd
        if init:
            mailgun.send(subject='初次见面, 这里是olea',
                         to=(self.pink.email, ),
                         template='new_pink',
                         values={
                             'name': self.pink.name,
                             'pwd': pwd
                         })
        else:
            mailgun.send(subject='新的口令',
                         to=(self.pink.email, ),
                         template='reset_pink',
                         values={
                             'name': self.pink.name,
                             'pwd': pwd
                         })

    def update_info(self, qq: int, line: str, email: str):
        if qq:
            self.pink.qq = str(qq)
        if line:
            self.pink.line = line
        if email:
            self.pink.email = email

    def deactive(self):
        self.pink.active = False
        db.session.delete(Duck.query.get(self.id))
        for lemon in Lemon.query.filter_by(pink_id=self.id):
            db.session.delete(lemon)
