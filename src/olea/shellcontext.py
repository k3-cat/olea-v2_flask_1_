from exts import db
from leaf.models import Leaf
from pink.models import Pink
from proj.models import Proj


def set_shellcontext(app):
    """set shell context objects."""
    def shell_context():
        return {'app': app, 'db': db, 'Pink': Pink, 'Proj': Proj, 'Leaf': Leaf}

    app.shell_context_processor(shell_context)
