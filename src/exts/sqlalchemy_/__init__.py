from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .main import ModelBase, SQLAlchemy

__all__ = [
    'BaseModel', 'Column', 'ForeignKey', 'UniqueConstraint', 'db',
    'relationship'
]

BaseModel = declarative_base(cls=ModelBase)
db = SQLAlchemy(Model=BaseModel)
