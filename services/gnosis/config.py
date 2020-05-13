import os

class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
<<<<<<< HEAD
    dev_sm_db_client = SM_Client('psql-gnosis-dev', 'us-east-1')
    db_secret = dev_sm_db_client.get_secret()
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}'.format(db_secret['username'], db_secret['password'], db_secret['host'])
    dev_sm_session_client = SM_Client('session-gnosis-dev', 'us-east-1')
    session_key = dev_sm_session_client.get_secret()
    SECRET_KEY = session_key['session_key']
=======
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:robertnields2020@cta-gnosis-db-dev.cd1wzcrr5t3s.us-east-1.rds.amazonaws.com'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
>>>>>>> parent of c086565... cq
