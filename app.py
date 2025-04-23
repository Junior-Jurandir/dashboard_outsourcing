import os
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from config import app_config


db = SQLAlchemy()
migrate = Migrate()


from config import app_config, app_active


def create_app():
    config = app_config.get(app_active, app_config["development"])
    from admin.Admin import start_views

    app = Flask(__name__)
    app.secret_key = config.SECRET
    app.config.from_object(config)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["FLASK_ADMIN_SWATCH"] = "cosmo"
    start_views(app, db)
    Bootstrap(app)

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
        return redirect("/admin/")

    from models import User, Role, Impressora, Chamado, Bilhetagem

    return app
