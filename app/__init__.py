from flask import Flask
from app.config import Config
from app.extensions import db, migrate
from app.blueprints import medicine_bp



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    #migrate.init_app(app, db)
    app.register_blueprint(medicine_bp, url_prefis='/medicine')
    #app.register_blueprint(orders_bp)
    #app.register_blueprint(ram_bp)

    return app