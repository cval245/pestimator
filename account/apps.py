from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        # Import celery app now that Django is mostly ready.
        # This initializes Celery and autodiscovers tasks
        import pestimator.celery
