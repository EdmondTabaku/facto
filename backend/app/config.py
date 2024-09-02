import os


class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'mysql+pymysql://yeti:yeti@localhost:3306/predicter'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
