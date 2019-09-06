from collections import OrderedDict

from flask import request

from .errors import FormError, ValidationError

_Auto = object()


class JsonForm():
    def __init__(self, jsondata: dict):
        self.errors = OrderedDict()
        self._fields = OrderedDict()
        self._data = None

        for name, unbound_field in self.__class__.__dict__.items():
            if name[0] == '_' or callable(unbound_field):
                continue
            self._fields[name] = unbound_field.bind()
            setattr(self, name, self._fields[name])

        self.process(jsondata=jsondata)

    @property
    def data(self):
        if not self._data:
            self._data = {
                name: field.data
                for name, field in self._fields.items()
            }
        return self._data

    def process(self, jsondata: dict):
        for name, value, in jsondata.items():
            if name not in self._fields:
                self.errors['FORM'] = ['BAD REQUEST']
                return
            self._fields[name].process(value)
            if self._fields[name].errors:
                self.errors[name] = self._fields[name].errors

    def validate(self):
        if self.errors:  # process error
            return False
        for name, field in self._fields.items():
            errors = list()
            if not field.validate():
                errors.extend(field.errors)
                continue
            inline = getattr(self.__class__, 'validate_%s' % name, None)
            if inline is not None:
                try:
                    inline(self, field)
                except ValidationError as e:
                    errors.append(str(e))
            if errors:
                self.errors[name] = errors
        if self.errors:
            raise FormError(msg=self.errors)
        return self


class BaseForm(JsonForm):
    def __init__(self, data=_Auto):
        if data is _Auto and BaseForm.is_submitted():
            if not request.get_json():
                self.errors['FORM'] = 'MUST BE JSON'
        jsonstr = request.get_json()
        super().__init__(jsonstr)

    @staticmethod
    def is_submitted():
        return bool(request)
