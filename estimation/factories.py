import random
from datetime import datetime

import factory
from dateutil.relativedelta import relativedelta
from djmoney.money import Money
from faker.providers import BaseProvider

from application.factories import ApplicationFactory, OfficeActionFactory, USOfficeActionFactory, PublicationFactory, \
    AllowanceFactory, IssuanceFactory
from characteristics.factories import DetailedFeeCategoryFactory, EntitySizeFactory, CountryFactory, ApplTypeFactory, \
    LanguageFactory, \
    DocFormatFactory, FeeCategoryFactory
from . import models
from .models import FilingEstimateTemplate, PublicationEstTemplate, OAEstimateTemplate, USOAEstimateTemplate, \
    AllowanceEstTemplate, IssueEstTemplate, LawFirmEst, BaseEst, FilingEstimate, OAEstimate, USOAEstimate, \
    PublicationEst, IssueEst, AllowanceEst, TranslationEstTemplate, DefaultTranslationEstTemplate, \
    ComplexTimeConditions, ComplexConditions
import random


class MoneyProvider(BaseProvider):

    def money(self):
        return Money(random.random() * 1000, 'USD')

    def moneyCN(self):
        return Money(random.random() * 1000, 'CNY')


class DiffProvider(BaseProvider):

    def diff(self):
        return relativedelta(days=random.randint(0, 720))


factory.Faker.add_provider(MoneyProvider)
factory.Faker.add_provider(DiffProvider)


class ComplexTimeConditionsFactory(factory.django.DjangoModelFactory):
    name = 'from priority date'

    class Meta:
        model = ComplexTimeConditions
        django_get_or_create = ('name',)


class ComplexConditionsFactory(factory.django.DjangoModelFactory):
    name = 'multiply each by template above minimum indep claims'

    class Meta:
        model = ComplexConditions
        django_get_or_create = ('name',)


class LineEstimationTemplateConditionsFactory(factory.django.DjangoModelFactory):
    condition_claims_multiple_dependent_min = None
    condition_claims_multiple_dependent_max = None
    condition_claims_min = None
    condition_claims_max = None
    condition_indep_claims_min = None
    condition_indep_claims_max = None

    condition_pages_total_min = None
    condition_pages_total_max = None
    condition_pages_desc_min = None
    condition_pages_desc_max = None
    condition_pages_claims_min = None
    condition_pages_claims_max = None
    condition_pages_drawings_min = None
    condition_pages_drawings_max = None

    condition_drawings_min = None
    condition_drawings_max = None
    condition_entity_size = None

    condition_annual_prosecution_fee = False
    condition_annual_prosecution_fee_until_grant = False
    condition_renewal_fee_from_filing_after_grant = False
    condition_complex = None
    condition_time_complex = None
    prior_pct = None
    prior_pct_same_country = None
    prev_appl_date_excl_intermediary_time = False
    prior_appl_exists = None
    isa_country_fee_only = False
    doc_format = None
    language = None

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
    date_diff = factory.Faker('diff')

    class Meta:
        model = models.LawFirmEstTemplate

    class Params:
        CN = factory.Trait(law_firm_cost=factory.Faker('moneyCN'))

class BaseEstTemplateFactory(factory.django.DjangoModelFactory):
    official_cost = factory.Faker('money')
    date_diff = factory.Faker('diff')
    country = factory.SubFactory(CountryFactory)
    appl_type = factory.SubFactory(ApplTypeFactory)
    conditions = factory.SubFactory(LineEstimationTemplateConditionsFactory)
    law_firm_template = factory.SubFactory(LawFirmEstTemplateFactory)
    description = 'ddd'
    fee_code = 'ddd'
    fee_category = factory.SubFactory(FeeCategoryFactory)
    detailed_fee_category = factory.SubFactory(DetailedFeeCategoryFactory)
    date_enabled = datetime.now()
    date_disabled = None

    class Meta:
        abstract = True

    class Params:
        CN = factory.Trait(
            official_cost=factory.Faker('moneyCN'),
            law_firm_template=factory.SubFactory(LawFirmEstTemplateFactory, CN=True),
            country=factory.SubFactory(CountryFactory, CN=True),
        )


class FilingEstimateTemplateFactory(BaseEstTemplateFactory):
    class Meta:
        model = FilingEstimateTemplate
        abstract = False


class PublicationEstTemplateFactory(BaseEstTemplateFactory):
    class Meta:
        model = PublicationEstTemplate
        abstract = False
        # django_get_or_create = ('appl_type',)


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
    start_language = factory.SubFactory(LanguageFactory)
    end_language = factory.SubFactory(LanguageFactory)
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
    office_action = factory.SubFactory(OfficeActionFactory)

    class Meta:
        model = OAEstimate


class USOAEstimateFactory(BaseEstFactory):
    office_action = factory.SubFactory(USOfficeActionFactory)

    class Meta:
        model = USOAEstimate


class PublicationEstFactory(BaseEstFactory):
    publication = factory.SubFactory(PublicationFactory)

    class Meta:
        model = PublicationEst


class AllowanceEstFactory(BaseEstFactory):
    allowance = factory.SubFactory(AllowanceFactory)

    class Meta:
        model = AllowanceEst


class IssueEstFactory(BaseEstFactory):
    issue = factory.SubFactory(IssuanceFactory)

    class Meta:
        model = IssueEst
