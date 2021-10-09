web: gunicorn pestimator.wsgi
worker: celery -A pestimator worker --without-heartbeat --without-gossip --without-mingle
release: python manage.py migrate
beat: celery -A pestimator.celery beat --without-heartbeat --without-gossip --without-mingle