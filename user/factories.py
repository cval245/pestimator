
import factory
from django.utils import timezone

from . import models

class UserFactory(factory.django.DjangoModelFactory):
    username = factory.sequence(lambda n: 'username%04d' % n)
    first_name = factory.sequence(lambda n: 'first_name%04d' % n)
    last_name = factory.sequence(lambda n: 'last_name%04d' % n)
    email = factory.Faker('email')
    is_staff = False
    is_active = True
    date_joined = factory.Faker('date_time', tzinfo=timezone.get_default_timezone())

    class Meta:
        model = models.User