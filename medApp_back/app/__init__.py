from flask import Flask
from app.config import Config
from app.extensions import db, migrate
from app.blueprints.journal import journal_bp
from app.blueprints.medicine import medicine_bp
from app.blueprints.training import training_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(journal_bp)
    app.register_blueprint(medicine_bp)
    app.register_blueprint(training_bp)

    return app
