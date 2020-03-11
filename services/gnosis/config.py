import os

class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:robertnields2020@cta-gnosis-db-dev.cd1wzcrr5t3s.us-east-1.rds.amazonaws.com'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'