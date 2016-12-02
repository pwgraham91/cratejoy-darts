import os

basedir = os.path.abspath(os.path.dirname(__file__))

# WTF
WTF_CSRF_ENABLED = True
SECRET_KEY = '8ac5f2eb-01af-4ef9-90ad-8c4c25cdf775'

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/darts'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


class Auth:
    CLIENT_ID = 'clientid.apps.googleusercontent.com'
    CLIENT_SECRET = 'clientsecred'
    REDIRECT_URI = 'https://0f999789.ngrok.io/gCallback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'

debug = True
ENVIRONMENT = 'dev'

base_url = 'http://127.0.0.1:8000/'
