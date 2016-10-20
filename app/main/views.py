from flask import request, g
from flask_restful import Resource
from app import api, db
from app.models import Tasks
from .authentication import auth


class TaskList(Resource):
    decorators = [auth.login_required]

    def get(self):
        tasks = Tasks.query.all()
        return {'tasks': [task.to_json() for task in tasks]}

    def post(self):
        task = Tasks.from_json(request.json)
        task.author = g.user
        db.session.add(task)
        db.session.commit()
        return task.to_json()


class Task(Resource):
    pass


api.add_resource(TaskList, '/todo/api/tasks', endpoint='tasks')
