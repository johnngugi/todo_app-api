from flask import request, g, jsonify
from flask_restful import Resource
from app import api, db
from app.models import Tasks
from .authentication import auth


class TaskListApi(Resource):
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

    def put(self, task_id):
        task = Tasks.query.get(task_id)
        task.name = request.json.get('name')
        task.description = request.json.get('description')
        task.is_done = request.json.get('is_done')
        task.category = request.json.get('category')
        task.priority = request.json.get('priority')
        db.session.commit()
        return {'task': task.to_json()}

    def delete(self, task_id):
        task = Tasks.query.get(task_id)
        db.session.delete(task)
        db.session.commit()
        return {'result': True}


class TaskApi(Resource):
    decorators = [auth.login_required]

    def get(self, user_id):
        tasks = Tasks.query.filter_by(user_id=user_id).all()
        return {'tasks': [task.to_json() for task in tasks]}


api.add_resource(TaskListApi, '/todo/api/tasks', endpoint='get_tasks')
api.add_resource(TaskListApi, '/todo/api/tasks/<int:task_id>', endpoint='update_task')
api.add_resource(TaskListApi, '/todo/api/tasks/<int:task_id>', endpoint='delete_task')
api.add_resource(TaskApi, '/todo/api/tasks/<int:user_id>', endpoint='get_user_tasks')
