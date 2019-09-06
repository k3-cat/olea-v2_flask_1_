import importlib

from . import comm, instance


def loader(env, package):
    if '.' in env:
        raise Exception('! UNSAFE !')
    return importlib.import_module(f'.{env}', package=package)


def load_config(app, env):
    app.config.from_object(comm)
    app.config.from_object(instance)
    app.config.from_object(loader(env, package=__package__))
