import os

class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:robertnields2020@cta-gnosis-db-dev.cd1wzcrr5t3s.us-east-1.rds.amazonaws.com'
    SQLALCHEMY_DATABASE_USER = os.environ.get('POSTGRES_USER')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
