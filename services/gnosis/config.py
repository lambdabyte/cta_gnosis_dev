import os
from app.clients import SM_Client

class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    dev_sm_client = SM_Client('psql-gnosis-dev', 'us-east-1')
    secret = dev_sm_client.get_secret()
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}'.format(secret['username'], secret['password'], secret['host'])
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'