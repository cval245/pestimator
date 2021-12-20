import factory

from user.factories import UserFactory
from . import models

class FamilyFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    family_name = factory.Sequence(lambda n: 'Family Name %04d' % n)
    family_no = factory.Sequence(lambda n: 'fam_no %04d' % n)
    unique_display_no = factory.Faker('random_int', min=1, max=80000, step=1)


    class Meta:
        model = models.Family
