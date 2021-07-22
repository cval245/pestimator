from datetime import date, datetime

import factory
from django.utils import timezone
import pytz
from faker.providers import BaseProvider

from characteristics.factories import CountryFactory, EntitySizeFactory
from family.factories import FamilyFactory
from user.factories import UserFactory
from . import models



class ApplDetailsFactory(factory.django.DjangoModelFactory):
    num_indep_claims = factory.Faker('random_int', min=1, max=50, step=1)
    num_pages = factory.Faker('random_int', min=1, max=50, step=1)
    num_claims = factory.Faker('random_int', min=1, max=50, step=1)
    num_drawings = factory.Faker('random_int', min=1, max=30, step=1)
    entity_size = factory.SubFactory(EntitySizeFactory)

    class Meta:
        model = models.ApplDetails


class ApplicationFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    title = factory.sequence(lambda n: "Title %03d" % n)
    family = factory.SubFactory(FamilyFactory)
    date_filing = factory.Faker('date_time', tzinfo=timezone.get_default_timezone())
    details = factory.SubFactory(ApplDetailsFactory)
    prior_appl = None
    country = factory.SubFactory(CountryFactory)

    class Meta:
        model = models.BaseApplication

    class Params:
        pass
        # prior_appl = factory.Trait(
        #     prior_appl=factory.SubFactory('application.factories.ApplicationFactory'))


class EPApplicationFactory(ApplicationFactory):

    class Meta:
        model = models.EPApplication


class BaseUtilityApplicationFactory(ApplicationFactory):

    class Meta:
        model = models.BaseUtilityApplication


class USUtilityApplicationFactory(BaseUtilityApplicationFactory):

    class Meta:
        model = models.USUtilityApplication


class PublicationFactory(factory.django.DjangoModelFactory):
    date_publication = factory.Faker('date_object')
    application = factory.SubFactory(ApplicationFactory)

    class Meta:
        model = models.Publication


class OfficeActionFactory(factory.django.DjangoModelFactory):
    date_office_action = factory.Faker('date_object')
    application = factory.SubFactory(BaseUtilityApplicationFactory)

    class Meta:
        model = models.OfficeAction


class USOfficeActionFactory(factory.django.DjangoModelFactory):
    date_office_action = factory.Faker('date_object')
    application = factory.SubFactory(BaseUtilityApplicationFactory)

    class Meta:
        model = models.USOfficeAction


class AllowanceFactory(factory.django.DjangoModelFactory):
    application = factory.SubFactory(ApplicationFactory)
    date_allowance = factory.Faker('date_object')

    class Meta:
        model = models.Allowance

class IssuanceFactory(factory.django.DjangoModelFactory):
    date_issuance = factory.Faker('date_object')
    application = factory.SubFactory(ApplicationFactory)

    class Meta:
        model = models.Issue
