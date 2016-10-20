from flask import request
from flask_restful import Resource
from app import api, db
from app.models import Tasks


class TaskList(Resource):
    def get(self):
        tasks = Tasks.query.all()
        return {'tasks': [task.to_json() for task in tasks]}

    def post(self):
        task = Tasks.from_json(request.json)
        db.session.add(task)
        db.session.commit()
        return task.to_json()


class Task(Resource):
    pass


api.add_resource(TaskList, '/todo/api/tasks', endpoint='tasks')
