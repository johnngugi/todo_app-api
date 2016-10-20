from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()
api = Api()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    from main import todo
    api.init_app(todo)
    app.register_blueprint(todo)
    return app
