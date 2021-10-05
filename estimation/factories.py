import random

import factory
from dateutil.relativedelta import relativedelta
from djmoney.money import Money
from faker.providers import BaseProvider

from application.factories import ApplicationFactory
from characteristics.factories import EntitySizeFactory, CountryFactory, ApplTypeFactory, LanguagesFactory
from . import models
from .models import FilingEstimateTemplate, PublicationEstTemplate, OAEstimateTemplate, USOAEstimateTemplate, \
    AllowanceEstTemplate, IssueEstTemplate, LawFirmEst, BaseEst, FilingEstimate, OAEstimate, USOAEstimate, \
    PublicationEst, IssueEst, AllowanceEst, TranslationEstTemplate, DefaultTranslationEstTemplate
import random
class MoneyProvider(BaseProvider):
   def money(self):
       return Money(random.random()*1000, 'USD')

class DiffProvider(BaseProvider):
    def diff(self):
        return relativedelta(days=random.randint(0, 365))

factory.Faker.add_provider(MoneyProvider)
factory.Faker.add_provider(DiffProvider)

class LineEstimationTemplateConditionsFactory(factory.django.DjangoModelFactory):
    condition_claims_min = None
    condition_claims_max = None
    condition_indep_claims_min = None
    condition_indep_claims_max = None
    condition_pages_min = None
    condition_pages_max = None
    condition_pages_desc_min = None
    condition_pages_desc_max = None
    condition_drawings_min = None
    condition_drawings_max = None
    condition_entity_size = factory.SubFactory(EntitySizeFactory)
    condition_annual_prosecution_fee = False
    condition_complex = None
    condition_time_complex = None
    prior_pct = None
    prior_pct_same_country = None
    prev_appl_date_excl_intermediary_time = False

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



class LawFirmEstTemplateFactory(factory.django.DjangoModelFactory):
    law_firm_cost = factory.Faker('money')
    date_diff = 'P1Y'

    class Meta:
        model = models.LawFirmEstTemplate


class BaseEstTemplateFactory(factory.django.DjangoModelFactory):
    official_cost = factory.Faker('money')
    date_diff = factory.Faker('diff')
    country = factory.SubFactory(CountryFactory)
    appl_type = factory.SubFactory(ApplTypeFactory)
    conditions = factory.SubFactory(LineEstimationTemplateConditionsFactory)
    law_firm_template = factory.SubFactory(LawFirmEstTemplateFactory)

    class Meta:
        abstract = True


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
    oa_final_bool = False
    oa_first_final_bool = False

    class Meta:
        model = USOAEstimateTemplate
        abstract = False

    class Params:
        nfoa = factory.Trait(
            oa_final_bool=False,
            oa_first_final_bool=False,
        )
        first_foa = factory.Trait(
            oa_final_bool=True,
            oa_first_final_bool=False,
        )
        second_foa = factory.Trait(
            oa_final_bool=True,
            oa_first_final_bool=True
        )


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

    # date_filing = factory.Faker('date_time', tzinfo=timezone.get_default_timezone())

    class Meta:
        model = LawFirmEst


class TranslationEstTemplateFactory(factory.django.DjangoModelFactory):
    start_language = factory.SubFactory(LanguagesFactory)
    end_language = factory.SubFactory(LanguagesFactory)
    date_diff = factory.Faker('diff')
    cost_per_word = factory.Faker('money')

    class Meta:
        model = TranslationEstTemplate


class DefaultTranslationEstTemplateFactory(factory.django.DjangoModelFactory):
    date_diff = factory.Faker('diff')
    cost_per_word = factory.Faker('money')

    class Meta:
        model = DefaultTranslationEstTemplate


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
