import os

class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Som3$ec5etK*y'
    UPLOAD_FOLDER = './uploads/'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://finalproject:lilly@localhost/finalproject'
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    #set SECRET_KEY=YourRandomSecretKey
    #set DATABASE_URL=postgresql://finalproject:lilly@localhost/finalproject
class DevelopmentConfig(Config):
    """Development Config that extends the Base Config Object"""
    DEVELOPMENT = True
    DEBUG = True

class ProductionConfig(Config):
    """Production Config that extends the Base Config Object"""
    DEBUG = False