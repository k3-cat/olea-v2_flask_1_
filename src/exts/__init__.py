from .apscheduler_ import scheduler
from .mailgun import mailgun_client
from .sqlalchemy_ import db
from .storage import storage
from .flask_redis_ import redis_client


def init_extensions(app):
    db.init_app(app)
    redis_client.init_app(app)
    scheduler.init_app(app)
    mailgun_client.init_app(app)
    storage.init_app(app)

    scheduler.start()
