import os
from datetime import timedelta

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'JFP.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
PERMANENT_SESSION_LIFETIME = timedelta(days=7)


MAIL_SERVER='smtp.naver.com'
MAIL_PORT = 465
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
SECRET_KEY = '12345678910'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
SECURITY_PASSWORD_SALT = '12345'