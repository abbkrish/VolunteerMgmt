web: gunicorn config.wsgi:application
worker: celery worker --app=volunteermgmtdjango.taskapp --loglevel=info
