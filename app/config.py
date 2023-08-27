import os


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://user:password@production_host/production_db')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'
