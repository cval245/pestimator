import factory
from django.utils import timezone

from user.factories import UserFactory
from . import models


class UserProfileFactory(factory.django.DjangoModelFactory):
    # estimates_remaining = 3
    user = factory.SubFactory(UserFactory)
    company_name = factory.sequence(lambda n: 'company_name%04d' % n)
    address = factory.sequence(lambda n: 'address%04d' % n)
    city = factory.sequence(lambda n: 'city%04d' % n)
    state = factory.sequence(lambda n: 'state%04d' % n)
    zip_code = factory.Faker('random_int', min=50000, max=80000, step=1)

    # estimates_remaining = 3#factory.Faker('random_int', min=3, max=10, step=1)

    class Meta:
        model = models.UserProfile
