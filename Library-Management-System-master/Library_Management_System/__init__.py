from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.ProductionConfig")

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from .views import main
    app.register_blueprint(main)

    with app.app_context():
        from .models import User, Book, Copy
        db.create_all()

    return app
