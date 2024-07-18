from celery import Celery

# Configurar o Celery para usar Redis como broker e backend
app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

app.conf.update(
    task_default_queue='default',
    task_routes={
        'tasks.add': {'queue': 'default'},
        'tasks.multiply': {'queue': 'default'},
        'tasks.long_task': {'queue': 'default'}
    }
)
