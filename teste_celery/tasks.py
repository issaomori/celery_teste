from celery_config import app

@app.task(name='add')
def add(x, y):
    return x + y

@app.task(name='multiply')
def multiply(x, y):
    return x * y

@app.task(name='long_task')
def long_task(duration):
    import time
    time.sleep(duration)
    return 'Completed after {} seconds'.format(duration)
