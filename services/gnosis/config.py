import os
from app.clients import SM_Client

class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    dev_sm_db_client = SM_Client('psql-gnosis-dev', 'us-east-1')
    db_secret = dev_sm_db_client.get_secret()
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}'.format(db_secret['username'], db_secret['password'], db_secret['host'])
    dev_sm_session_client = SM_Client('session-gnosis-dev', 'us-east-1')
    session_key = dev_sm_session_client.get_secret()
    SECRET_KEY = session_key['session_key']
