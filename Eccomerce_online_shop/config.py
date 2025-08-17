import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site3.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
    STRIPE_SECRET_KEY = os.environ.get('sk_test_26PHem9AhJZvU623DfE1x4sd')

    # Define the upload folder for file uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/images/uploads')

    # Ensure the folder exists (create if it doesn't)
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Flask-Mail Configuration
    MAIL_SERVER = 'smtp.gmail.com'  # Example: for Gmail
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Add your email
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Add your email password
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')  # Default email sender
