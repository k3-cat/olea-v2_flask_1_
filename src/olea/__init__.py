import os

from flask import Flask

from exts import init_extensions

from .blueprint import register_blueprints
from .command import register_commands
from .config import load_config
from .error_handler import register_error_handlers
from .hook import hook_hooks
from .shellcontext import set_shellcontext


def create_app(env=os.getenv('FLASK_ENV') or 'prod'):
    print('----- olea -----')
    app = Flask('olea')

    load_config(app, env)
    # configure_logger(app)
    register_error_handlers(app)
    init_extensions(app)
    register_blueprints(app)
    hook_hooks(app)
    set_shellcontext(app)
    register_commands(app)
    return app
