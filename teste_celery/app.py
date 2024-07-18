from flask import Flask, request, jsonify
from tasks import add, multiply, long_task
from celery.result import AsyncResult
from tasks import app as celery_app

app = Flask(__name__)

@app.route('/add', methods=['POST'])
def add_task():
    data = request.get_json()
    task = add.apply_async((data['x'], data['y']))
    return jsonify({'task_id': task.id}), 202

@app.route('/multiply', methods=['POST'])
def multiply_task():
    data = request.get_json()
    task = multiply.apply_async((data['x'], data['y']))
    return jsonify({'task_id': task.id}), 202

@app.route('/long_task', methods=['POST'])
def long_task_route():
    data = request.get_json()
    task = long_task.apply_async((data['duration'],))
    return jsonify({'task_id': task.id}), 202

@app.route('/queue-info')
def queue_info():
    inspector = celery_app.control.inspect()
    active_tasks = inspector.active()  # Tarefas ativas
    scheduled_tasks = inspector.scheduled()  # Tarefas agendadas
    reserved_tasks = inspector.reserved()  # Tarefas reservadas
    revoked_tasks = inspector.revoked()  # Tarefas revogadas

    queue_info = {
        'active_tasks': active_tasks,
        'scheduled_tasks': scheduled_tasks,
        'reserved_tasks': reserved_tasks,
        'revoked_tasks': revoked_tasks
    }

    return jsonify(queue_info)

@app.route('/status/<task_id>')
def task_status(task_id):
    task_result = AsyncResult(task_id, app=celery_app)  # Usar a instância do Celery configurada
    result = {
        'task_id': task_id,
        'status': task_result.status,
        'result': task_result.result
    }
    print("result", result)
    return jsonify(result)
if __name__ == '__main__':
    app.run(debug=True)
