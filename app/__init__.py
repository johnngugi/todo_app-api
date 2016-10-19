from flask import Flask
from flask_restful import Api

api = Api()


def create_app(config_name):
    app = Flask(__name__)
    from main import todo
    api.init_app(todo)
    app.register_blueprint(todo)
    return app