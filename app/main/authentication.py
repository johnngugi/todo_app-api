from flask import request, abort, g
from app import api, db
from app.models import User
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


class NewUserApi(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        if username is None or password is None:
            abort(400)
        if User.query.filter_by(username=username).first() is not None:
            abort(400)
        user = User(username=username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return {'username': user.username}


class UserApi(Resource):

    decorators = [auth.login_required]

    def get(self, id):
        user = User.query.get(id)
        if not user:
            abort(400)
        return {'username': user.username, 'user_tasks': 'http://127.0.0.1:5000/todo/api/tasks/' + str(user.id)}

    def put(self, id):
        user = User.query.get(id)
        if not user:
            abort(404)
        user.username = request.json.get('username')
        user.hash_password(request.json.get('password'))
        db.session.commit()
        return {'username': user.username, 'user_tasks': 'http://127.0.0.1:5000/todo/api/tasks/' + str(user.id)}


api.add_resource(NewUserApi, '/todo/api/users', endpoint='sign_up')
api.add_resource(UserApi, '/todo/api/users/<id>', endpoint='get_user')
api.add_resource(UserApi, '/todo/api/users/<username>', endpoint='users')
