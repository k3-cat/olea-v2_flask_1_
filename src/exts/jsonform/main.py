import enum
from collections import OrderedDict

from flask import request

from .errors import FormError, FormValueError, ValidationError


class Field():
    _default = None

    def __new__(cls, *args, **kwargs):
        if 'init' in kwargs:
            kwargs.pop('init')
            return super().__new__(cls)
        return UnboundField(cls, *args, **kwargs)

    def __init__(self,
                 validators: tuple = None,
                 optional: bool = False,
                 default=None,
                 init: bool = False):
        self.errors = list()
        self._data = None
        self.validators = validators or tuple()
        self.optional = optional
        self.default = default
        self.empty = False

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def validate(self):
        for validator in self.validators:
            try:
                validator(self)
            except ValidationError as e:
                self.errors.append(str(e))
        return not self.errors

    def mark_empty(self):
        if not self.optional:
            raise ValueError('cannot be left blank')
        self.data = self.default
        self.empty = True

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
        return f'<UnboundField({self.field_class.__name__}, {repr(self.args)}, {repr(self.kwargs)})>'


class AutoOption(enum.IntEnum):
    none = 0
    auto_process = 1
    auto_validate = 3


class JsonForm():
    def __init__(self, jsondata: dict, auto=AutoOption.none):
        self._fields = OrderedDict()
        for name, unbound_field in self.__class__.__dict__.items():
            if name[0] == '_' or callable(unbound_field):
                continue
            self._fields[name] = unbound_field.bind()
            setattr(self, name, self._fields[name])

        if auto >= AutoOption.auto_process:
            self.process(jsondata=jsondata)
        if auto is AutoOption.auto_validate:
            self.validate()

    def __getitem__(self, name):
        return self._fields[name].data

    def process(self, jsondata: dict):
        errors = OrderedDict()
        for name in set(jsondata.keys()).union(set(self._fields.keys())):
            if name not in self._fields:
                errors[name] = 'invalid field'
                continue
            try:
                if name not in jsondata or not self._fields[name]:
                    self._fields[name].mark_empty()
                else:
                    self._fields[name].process_data(jsondata[name])
            except ValueError as e:
                errors[name] = str(e)
        if errors:
            raise FormError(msg=errors)

    def validate(self):
        errors = OrderedDict()
        for name, field in self._fields.items():
            field.validate()
            field_errors = field.errors
            inline = getattr(self.__class__, f'validate_{name}', None)
            if inline is not None:
                try:
                    inline(self, field)
                except ValidationError as e:
                    field_errors.append(str(e))
            if field_errors:
                errors[name] = field_errors
        if errors:
            raise FormValueError(msg=errors)


class BaseForm(JsonForm):
    def __init__(self, data=None, auto=AutoOption.auto_validate):
        if not data and BaseForm.is_submitted():
            if not request.get_json():
                raise FormError(msg={'form': 'input must be json'})
        super().__init__(request.get_json(), auto)

    @staticmethod
    def is_submitted():
        return bool(request)
