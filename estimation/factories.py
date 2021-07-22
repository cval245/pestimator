import factory
from djmoney.money import Money
from faker.providers import BaseProvider

from application.factories import ApplicationFactory
from characteristics.factories import EntitySizeFactory, CountryFactory, ApplTypeFactory
from . import models
from .models import FilingEstimateTemplate, PublicationEstTemplate, OAEstimateTemplate, USOAEstimateTemplate, \
    AllowanceEstTemplate, IssueEstTemplate, LawFirmEst, BaseEst, FilingEstimate, OAEstimate, USOAEstimate, \
    PublicationEst, IssueEst, AllowanceEst

class MoneyProvider(BaseProvider):
   def money(self):
       return Money(555, 'USD')

factory.Faker.add_provider(MoneyProvider)

class LineEstimationTemplateConditionsFactory(factory.django.DjangoModelFactory):
    condition_claims_min = None
    condition_claims_max = None
    condition_pages_min = None
    condition_pages_max = None
    condition_drawings_min = None
    condition_drawings_max = None
    condition_entity_size = factory.SubFactory(EntitySizeFactory)

    class Meta:
        model = models.LineEstimationTemplateConditions

    class Params:
        min_20 = factory.Trait(
            condition_claims_min=20,
            condition_pages_min=20,
            condition_drawings_min=20,
        )

        max_10 = factory.Trait(
            condition_claims_max=10,
            condition_pages_max=10,
            condition_drawings_max=10,
        )



class LawFirmEstFactory(factory.django.DjangoModelFactory):
    law_firm_cost = factory.Faker('money')
    date_diff = 'P1Y'

    class Meta:
        model = models.LawFirmEstTemplate


class BaseEstTemplateFactory(factory.django.DjangoModelFactory):
    official_cost = factory.Faker('money')
    date_diff = 'P1Y'
    country = factory.SubFactory(CountryFactory)
    appl_type = factory.SubFactory(ApplTypeFactory)
    conditions = factory.SubFactory(LineEstimationTemplateConditionsFactory)
    law_firm_template = factory.SubFactory(LawFirmEstFactory)

    class Meta:
        abstract = True
        django_get_or_create = ('appl_type',)


class FilingEstimateTemplateFactory(BaseEstTemplateFactory):
    class Meta:
        model = FilingEstimateTemplate
        abstract = False


class PublicationEstTemplateFactory(BaseEstTemplateFactory):
    class Meta:
        model = PublicationEstTemplate
        abstract = False
        #django_get_or_create = ('appl_type',)

class OAEstimateTemplateFactory(BaseEstTemplateFactory):
    class Meta:
        model = OAEstimateTemplate
        abstract = False


class USOAEstimateTemplateFactory(BaseEstTemplateFactory):
    country = factory.SubFactory(CountryFactory, country='US')
    oa_type = 'NFOA'

    class Meta:
        model = USOAEstimateTemplate
        abstract = False

class AllowanceEstTemplateFactory(BaseEstTemplateFactory):
    class Meta:
        model = AllowanceEstTemplate
        abstract = False

class IssueEstTemplateFactory(BaseEstTemplateFactory):
    class Meta:
        model = IssueEstTemplate
        abstract = False


class LawFirmEstFactory(factory.django.DjangoModelFactory):
    law_firm_cost = factory.Faker('money')
    date = factory.Faker('date_object')
    #date_filing = factory.Faker('date_time', tzinfo=timezone.get_default_timezone())

    class Meta:
        model = LawFirmEst


class BaseEstFactory(factory.django.DjangoModelFactory):
    official_cost = factory.Faker('money')
    date = factory.Faker('date_object')
    law_firm_est = factory.SubFactory(LawFirmEstFactory)
    application = factory.SubFactory(ApplicationFactory)

    class Meta:
        model = BaseEst

class FilingEstimateFactory(BaseEstFactory):
    class Meta:
        model = FilingEstimate

class OAEstimateFactory(BaseEstFactory):
    class Meta:
        model = OAEstimate

class USOAEstimateFactory(BaseEstFactory):
    class Meta:
        model = USOAEstimate

class PublicationEstFactory(BaseEstFactory):
    class Meta:
        model = PublicationEst


class AllowanceEstFactory(BaseEstFactory):
    class Meta:
        model = AllowanceEst


class IssueEstFactory(BaseEstFactory):
    class Meta:
        model = IssueEst

