from django.utils.module_loading import import_string
from djmoney import settings
from django.conf import settings


def update_currency_exchange(**kwargs):
    backend = settings.EXCHANGE_BACKEND
    backend = import_string(backend)()
    backend.update_rates(**kwargs)
