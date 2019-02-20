import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:mercurial92@localhost/blogdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'sshhhh!'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    QUOTES_API_BASE_URL = 'http://quotes.stormconsultancy.co.uk/random.json'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True


config_options ={
    'development': DevConfig,
    'production': ProdConfig
    }


