import factory

from user.factories import UserFactory
from . import models

class FamilyFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    family_name = factory.Sequence(lambda n: 'Family Name %04d' % n)
    family_no = factory.Sequence(lambda n: 'fam_no %04d' % n)


    class Meta:
        model = models.Family
