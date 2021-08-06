web: gunicorn pestimator.wsgi
worker: celery -A pestimator worker
release: python manage.py migrate
