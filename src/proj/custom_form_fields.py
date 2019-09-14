from enums import Dep
from exts.jsonform.main import Field


class RolesField(Field):
    def process_data(self, value):
        if not isinstance(value, dict):
            raise ValueError('invalid roles dict')
        self.data = dict()
        for dep_, roles in value.items():
            try:
                dep = Dep[dep_]
            except KeyError:
                raise ValueError(f'invalid dep: {dep_}')
            if not isinstance(roles, list):
                raise ValueError(f'invalid roles list for {dep}')
            for role in roles:
                if not isinstance(role, str):
                    raise ValueError(f'invalid role: {role}')
            self.data[dep] = roles
