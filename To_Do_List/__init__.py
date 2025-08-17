
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import Config
from datetime import datetime

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()


def create_app():
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}


    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    # Configure login manager
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from To_Do_List.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app