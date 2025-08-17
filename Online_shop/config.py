import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site3.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STRIPE_PUBLIC_KEY = os.environ.get('')
    STRIPE_SECRET_KEY = os.environ.get('sk_test_26PHem9AhJZvU623DfE1x4sd')
