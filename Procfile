web: gunicorn core.wsgi --log-file -
worker: celery -A core worker -l info
beat: celery -A core beat -l info
