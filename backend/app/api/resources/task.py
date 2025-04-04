from flask_restx import Namespace, Resource
from app.extensions import celery


task_ns = Namespace('tasks', description='Celery task operations')

@task_ns.route('/<task_id>', methods=['GET'])
class ExportTaskStatusResource(Resource):
    """Get the status of a Celery task"""
    def get(self, task_id):
        result = celery.AsyncResult(task_id)
        return {
            'task_id': task_id,
            'status': result.status,
            'result': result.result if result.ready() else None
        }