import datetime

SQLALCHEMY_TRACK_MODIFICATIONS = False

TOKEN_LIFE = datetime.timedelta(days=90)

D50_DUE = datetime.timedelta(days=7)
D71_DUE = datetime.timedelta(days=4)
D72_DUE = datetime.timedelta(days=3)
D73_DUE = datetime.timedelta(days=7)

MAILGUN_DOMAIN = 'mail.k-olea.com'
MAILGUN_SENDER = 'olea'

BUCKET_NAME = 'olea-storage'
