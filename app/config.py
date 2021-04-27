import os

class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Som3$ec5etK*y'
    UPLOAD_FOLDER = './app/static/uploads'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://finalproject:lilly@localhost/finalproject'
    #DATABASE_URL='postgresql://mxijebqfvcprxh:fa3bf93a3e526e04a34f7e8a9d2b825a56d8b5646352958215a93e8e0485a586@ec2-34-206-8-52.compute-1.amazonaws.com:5432/d7qphv8v5jdgqp'
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