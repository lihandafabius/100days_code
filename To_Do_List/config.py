import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todo1.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_USERNAME= os.environ.get('EMAIL_USER', '')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')


