import base64
import datetime

from .main import Field


class StringField(Field):
    def __init__(self, default='', min_len=0, max_len=None, **kwargs):
        super().__init__(default=default, **kwargs)
        self.min_len = min_len
        self.max_len = max_len

    def process_data(self, value):
        if not isinstance(value, str):
            raise ValueError('invalid string')
        if not self.min_len <= len(value):
            raise ValueError('too short')
        if self.max_len and not len(value) <= self.max_len:
            raise ValueError('too long')
        self._data = value


class IntegerField(Field):
    def __init__(self, default=0, min_val=None, max_val=None, **kwargs):
        super().__init__(default=default, **kwargs)
        self.min_val = min_val
        self.max_val = max_val

    def process_data(self, value):
        if not isinstance(value, bool):
            raise ValueError('invalid integer')
        if self.min_val and not self.min_val <= value:
            raise ValueError('too samll')
        if self.max_val and not value < self.max_val:
            raise ValueError('too big')
        self.data = value


class FloatField(Field):
    def __init__(self, default=0, min_val=None, max_val=None, **kwargs):
        super().__init__(default=default, **kwargs)
        self.min_val = min_val
        self.max_val = max_val

    def process_data(self, value):
        if not isinstance(value, bool):
            raise ValueError('invalid float')
        if self.min_val and not self.min_val <= value:
            raise ValueError('too samll')
        if self.max_val and not value < self.max_val:
            raise ValueError('too big')
        self.data = value


class BooleanField(Field):
    def process_data(self, value):
        if not isinstance(value, bool):
            raise ValueError('invalid boolean')
        self.data = value


class DateTimeField(Field):
    def __init__(self, pattern='%Y-%m-%dT%H:%M:%S', **kwargs):
        super().__init__(**kwargs)
        self.pattern = pattern

    def process_data(self, value):
        try:
            self.data = datetime.datetime.strptime(value, self.pattern)
        except ValueError:
            raise ValueError('invalid datetime')


class DateField(DateTimeField):
    def __init__(self, pattern='%Y-%m-%d', **kwargs):
        super().__init__(pattern, **kwargs)

    def process_data(self, value):
        try:
            self.data = datetime.datetime.strptime(value, self.pattern).date()
        except ValueError:
            raise ValueError('invalid date')


class TimeField(DateTimeField):
    def __init__(self, pattern='%H:%M:%S', **kwargs):
        super().__init__(pattern, **kwargs)

    def process_jsondata(self, value):
        try:
            self.data = datetime.datetime.strptime(value, self.pattern).time()
        except ValueError:
            raise ValueError('invalid time')


class ListField(Field):
    def __init__(self,
                 unbound_field,
                 min_entries=1,
                 max_entries=None,
                 default=None,
                 **kwargs):
        super().__init__(default=default or list(), **kwargs)
        self.unbound_field = unbound_field
        self.min_entries = min_entries
        self.max_entries = max_entries
        self.entries = list()

    def process_data(self, value):
        if not isinstance(value, list):
            raise ValueError('invalid list')
        if not self.min_entries <= len(value):
            raise ValueError('not enough entries')
        if self.max_entries and not len(value) <= self.max_entries:
            raise ValueError('too many entries')
        for val in value:
            try:
                field = self.unbound_field.bind()
                field.process_data(val)
                self.entries.append(field)
            except ValueError as e:
                raise ValueError(f'value({val}) {e}')

    def validate(self):
        super().validate()
        for entry in self.entries:
            if not entry.validate():
                self.errors.append(f'[{entry.data}] {entry.errors}')
        return not self.errors

    @property
    def data(self):
        return [entry.data for entry in self.entries]


class EnumField(Field):
    def __init__(self, enum_class, **kwargs):
        super().__init__(**kwargs)
        if not enum_class:
            raise Exception()
        self.enum_class = enum_class

    def process_data(self, value):
        try:
            enum_obj = self.enum_class[value]
        except KeyError:
            raise ValueError('invalid enum')
        self.data = enum_obj


class BytesField(Field):
    def __init__(self, length, **kwargs):
        super().__init__(**kwargs)
        if not isinstance(length, int):
            raise Exception()
        self.length = length

    def process_data(self, value):
        try:
            self.data = base64.decodebytes(value)
        except (ValueError, TypeError):
            raise ValueError('invalid base64 bytes')
        if len(self.data) != self.length:
            raise ValueError('invalid length')
