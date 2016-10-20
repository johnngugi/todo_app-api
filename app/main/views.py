from flask_restful import Resource
from app import api
from app.models import Tasks


class TodoList(Resource):
    def get(self):
        tasks = Tasks.query.all()
        return {'tasks': [task.to_json() for task in tasks]}


api.add_resource(TodoList, '/todo/api/tasks', endpoint='tasks')
