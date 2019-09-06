import datetime

from enums import Dep, LeafState
from leaf.models import Leaf
from pink.models import Pink
from proj.models import Proj

from .errors import StopValidation, ValidationError


class Field():
    _default = None

    def __new__(cls, *args, **kwargs):
        if 'init' in kwargs:
            kwargs.pop('init')
            return super().__new__(cls)
        return UnboundField(cls, *args, **kwargs)

    def __init__(self,
                 validators: tuple = None,
                 default=None,
                 init: bool = False):
        self.errors: list = None
        self._data = None
        self.validators = validators or tuple()
        if default:
            self._default = default

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def default(self):
        return self._default

    def validate(self):
        self.errors = list()
        for validator in self.validators:
            try:
                validator(self)
            except ValidationError as e:
                self.errors.append(str(e))
            except StopValidation as e:
                if str(e):
                    self.errors.append(str(e))
                else:
                    self.errors = list()
                break
        return not self.errors

    def process(self, value):
        if not value:
            self._data = self.default
            return
        try:
            self.process_data(value)
        except ValueError as e:
            self.errors = [str(e)]

    def process_data(self, value):
        raise NotImplementedError()


class UnboundField():
    def __init__(self, field_class, *args, **kwargs):
        self.field_class = field_class
        self.args = args
        self.kwargs = kwargs
        self.kwargs['init'] = True

    def bind(self):
        return self.field_class(*self.args, **self.kwargs)

    def __repr__(self):
        return '<UnboundField(%s, %r, %r)>' % (self.field_class.__name__,
                                               self.args, self.kwargs)


class StringField(Field):
    """
    This field is the base string field.
    """

    _default = ''

    def process_data(self, value):
        if isinstance(value, str):
            self._data = value
        else:
            raise ValueError()


class IntegerField(Field):
    """
    A text field, except all input is coerced to an integer.
    """
    def process_data(self, value):
        try:
            self.data = int(value)
        except (ValueError, TypeError):
            self.data = None
            raise ValueError('invalid integer value')


class FloatField(Field):
    """
    A text field, except all input is coerced to an float.
    """
    def process_data(self, value):
        try:
            self.data = float(value)
        except (ValueError, TypeError):
            self.data = None
            raise ValueError('invalid float value')


class BooleanField(Field):
    """
    A boolean field.

    :param false_values:
        If provided, a sequence of strings each of which is an exact match
        string of what is considered a "false" value. Defaults to the tuple
        ``('false', '')``
    """
    false_values = ('false', '')

    def __init__(self, validators=None, false_values=None, **kwargs):
        super(BooleanField, self).__init__(validators, **kwargs)
        if false_values is not None:
            self.false_values = false_values

    def process_data(self, value):
        self.data = bool(value)


class DateTimeField(Field):
    """
    A text field which stores a `datetime.datetime` matching a format.
    """
    def __init__(self, validators=None, format_='%Y-%m-%d %H:%M:%S', **kwargs):
        super().__init__(validators, **kwargs)
        self.format = format_

    def process_data(self, value):
        try:
            self.data = datetime.datetime.strptime(value, self.format)
        except ValueError:
            raise ValueError('invalid datetime value')


class DateField(DateTimeField):
    """
    Same as DateTimeField, except stores a `datetime.date`.
    """
    def __init__(self, validators=None, format='%Y-%m-%d', **kwargs):
        super().__init__(validators, format, **kwargs)

    def process_data(self, value):
        try:
            self.data = datetime.datetime.strptime(value, self.format).date()
        except ValueError:
            raise ValueError('invalid date value')


class TimeField(DateTimeField):
    """
    Same as DateTimeField, except stores a `time`.
    """
    def __init__(self, validators=None, format_='%H:%M', **kwargs):
        super().__init__(validators, format_, **kwargs)

    def process_jsondata(self, value):
        try:
            self.data = datetime.datetime.strptime(value, self.format).time()
        except ValueError:
            raise ValueError('invalid time value')


class ListField(Field):
    def __init__(self,
                 unbound_field,
                 validators=None,
                 min_entries=0,
                 max_entries=None,
                 default=None,
                 **kwargs):
        super().__init__(validators, default=default or list(), **kwargs)
        self.unbound_field = unbound_field
        self.min_entries = min_entries
        self.max_entries = max_entries
        self.entries = list()

    def process_data(self, value):
        if not isinstance(value, list):
            raise ValueError('invalid list value')
        if len(value) < self.min_entries:
            raise ValueError('too short')
        if self.max_entries and len(value) > self.max_entries:
            raise ValueError('too long')
        for val in value:
            try:
                field = self.unbound_field.bind()
                field.process(val)
                self.entries.append(field)
            except ValueError as e:
                raise ValueError(f'value[{val}]: {e}')

    def validate(self):
        super().validate()
        for entry in self.entries:
            if not entry.validate():
                self.errors.append(f'value[{entry.data}]: {entry.errors}')
        return not self.errors

    @property
    def data(self):
        return [entry.data for entry in self.entries]


class EnumField(Field):
    def __init__(self, enum_class, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not enum_class:
            raise Exception()
        self.enum_class = enum_class

    def process_data(self, value):
        try:
            enum_obj = self.enum_class[value]
        except KeyError:
            raise ValueError('invalid enum value')
        self.data = enum_obj


class RolesField(Field):
    def process_data(self, value):
        if not isinstance(value, dict):
            raise ValueError('invalid roles dict')
        self.data = dict()
        for k, v in value.items():
            try:
                k = Dep[k]
            except KeyError:
                raise ValueError(f'{k} is invalid dep')
            if not isinstance(v, list):
                raise ValueError('invalid roles list')
            for role in v:
                if not isinstance(role, str):
                    raise ValueError('invalid role')
            self.data[k] = v
