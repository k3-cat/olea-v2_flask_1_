from psycopg2.errorcodes import UNIQUE_VIOLATION
from sqlalchemy.exc import IntegrityError

from common_errors import DuplicatedObj

from . import db


def test_unique(obj: object):
    db.session.add(obj)
    try:
        db.session.commit()
    except IntegrityError as e:
        if e.orig.pgcode == UNIQUE_VIOLATION:
            raise DuplicatedObj(obj=obj)
        raise
