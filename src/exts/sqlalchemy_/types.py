import re

from sqlalchemy import TypeDecorator, cast
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.types import (JSON, Boolean, Date, DateTime, Enum, Integer,
                              LargeBinary, String, Text)


class ArrayOfEnum(TypeDecorator):
    impl = ARRAY

    def bind_expression(self, bindvalue):
        return cast(bindvalue, self)

    def result_processor(self, dialect, coltype):
        super_rp = super(ArrayOfEnum, self).result_processor(dialect, coltype)

        def handle_raw_string(value):
            inner = re.match(r"^{(.*)}$", value).group(1)

            return inner.split(",") if inner else []

        def process(value):
            if value is None:
                return None

            return super_rp(handle_raw_string(value))

        return process


__all__ = [
    'ArrayOfEnum', 'ARRAY', 'Boolean', 'Date', 'DateTime', 'Enum', 'Integer',
    'JSON', 'LargeBinary', 'String', 'Text'
]
