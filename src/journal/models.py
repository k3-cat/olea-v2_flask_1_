from hashlib import sha3_256

from flask import g

from exts.id_tools import generate_id
from exts.sqlalchemy_ import BaseModel, Column, ForeignKey, relationship
from exts.sqlalchemy_.types import DateTime, Integer, LargeBinary, String, Text

from .errors import JournalUpdated


class Apl(BaseModel):
    __tablename__ = 'apl'

    id = Column(String, primary_key=True)
    pink_id = Column(String, ForeignKey('pink.id'))
    amount = Column(Integer)
    reason = Column(Text)

    def __init__(self, amount, reason):
        super().__init__(pink_id=g.pink_id, amount=amount, reason=reason)
        self.id = generate_id(6)


class Txn(BaseModel):
    __tablename__ = 'txn'

    id = Column(LargeBinary(32), primary_key=True)
    previous_id = Column(LargeBinary(32), ForeignKey('txn.id'))
    debit = Column(Integer)
    credit = Column(Integer)
    reason = Column(String)
    pink_id = Column(String, ForeignKey('pink.id'))
    timestamp = Column(DateTime)

    previous = relationship('Txn', remote_side=[id])

    def __init__(self, debit, credit, reason, previous_id):
        if previous_id != Txn.query.order_by(Txn.timestamp.desc()).first().id:
            raise JournalUpdated()
        super().__init__(previous=previous_id,
                         debit=debit,
                         credit=credit,
                         reason=reason,
                         pink_id=g.pink_id,
                         timestamp=g.now)
        self.id = sha3_256(
            f'{previous_id}_{debit}_{credit}_{reason}_{self.pink_id}_{self.timestamp}'
            .encode('utf-16')).digest()
