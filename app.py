import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import app_config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    env = os.getenv("FLASK_ENV", "development")
    config = app_config[env]

    app = Flask(__name__)
    app.secret_key = config.SECRET
    app.config.from_object(config)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["FLASK_ADMIN_SWATCH"] = "cosmo"

    db.init_app(app)
    migrate.init_app(app, db)

    config.APP = app

    @app.after_request
    def after_request(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
        return response

    @app.route("/")
    def index():
        return "App Flask funcionando."

    from model import User, Role, Impressora, Chamado, Bilhetagem

    return app
