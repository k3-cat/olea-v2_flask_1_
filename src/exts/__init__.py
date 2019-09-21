from .apscheduler_ import scheduler
from .mailgun import MailGun
from .sqlalchemy_ import db
from .storage import Storage
from .flask_redis_ import FlaskRedis

redis = FlaskRedis()
mailgun = MailGun()
storage = Storage()


def init_extensions(app):
    db.init_app(app)
    redis.init_app(app)
    scheduler.init_app(app)
    mailgun.init_app(app)
    storage.init_app(app)

    scheduler.start()
