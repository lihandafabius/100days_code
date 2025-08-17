from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
import stripe
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    ckeditor = CKEditor(app)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Stripe setup
    stripe.api_key = app.config['STRIPE_SECRET_KEY']

    with app.app_context():
        db.create_all()

    # Import blueprints (routes)
    from myapp.routes import main
    app.register_blueprint(main)

    return app
