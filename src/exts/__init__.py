from .apscheduler_ import scheduler
from .mailgun import mailgun
from .sqlalchemy_ import db
from .storage import storage
from .flask_redis_ import redis_ as redis


def init_extensions(app):
    db.init_app(app)
    redis.init_app(app)
    scheduler.init_app(app)
    mailgun.init_app(app)
    storage.init_app(app)

    scheduler.start()
