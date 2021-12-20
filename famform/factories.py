from random import random

import factory
from dateutil.relativedelta import relativedelta
from django.utils import timezone

# from application.factories import ApplDetailsFactory
from faker.providers import BaseProvider

from application.factories import ApplDetailsFactory
from characteristics.factories import CountryFactory, ApplTypeFactory, EntitySizeFactory, \
    TranslationImplementedPseudoEnumFactory, DocFormatFactory, LanguageFactory, translate_country
from characteristics.models import DocFormat
from family.factories import FamilyFactory
from user.factories import UserFactory
from .models import FamEstFormData, FamOptions, ApplOptions, BaseOptions, PublOptions, OAOptions, AllowOptions, \
    IssueOptions, ApplOptionsParticulars, PCTCountryCustomization, EPMethodCustomization, PCTMethodCustomization, \
    CustomApplOptions, CustomApplDetails, EPCountryCustomization, ParisCountryCustomization, RequestExaminationOptions


class DiffProvider(BaseProvider):

    def diff(self):
        return relativedelta(days=random.randint(0, 720))


factory.Faker.add_provider(DiffProvider)


class CustomApplDetailsFactory(factory.django.DjangoModelFactory):
    num_indep_claims = factory.Faker('random_int', min=1, max=10, step=1)
    num_claims = factory.Faker('random_int', min=1, max=50, step=1)
    num_claims_multiple_dependent = factory.Faker('random_int', min=1, max=10, step=1)
    num_drawings = factory.Faker('random_int', min=1, max=50, step=1)
    num_pages_description = factory.Faker('random_int', min=1, max=50, step=1)
    num_pages_drawings = factory.Faker('random_int', min=1, max=50, step=1)
    num_pages_claims = factory.Faker('random_int', min=1, max=50, step=1)
    entity_size = factory.SubFactory(EntitySizeFactory)
    language = factory.SubFactory(LanguageFactory)

    class Meta:
        model = CustomApplDetails

    class Params:
        NONE = factory.Trait(
            num_indep_claims=None,
            num_claims=None,
            num_claims_multiple_dependent=None,
            num_drawings=None,
            num_pages_description=None,
            num_pages_drawings=None,
            num_pages_claims=None,
            entity_size=None,
            language=None
        )
        NUM_CLAIMS = factory.Trait(
            num_indep_claims=None,
            num_claims=5,
            num_claims_multiple_dependent=None,
            num_drawings=None,
            num_pages_description=None,
            num_pages_drawings=None,
            num_pages_claims=None,
            entity_size=None,
            language=None
        )


class CustomApplOptionsFactory(factory.django.DjangoModelFactory):
    request_examination_early_bool = False
    doc_format = factory.SubFactory(DocFormatFactory)

    class Meta:
        model = CustomApplOptions


class PCTMethodCustomizationFactory(factory.django.DjangoModelFactory):
    custom_appl_details = factory.SubFactory(CustomApplDetailsFactory)
    custom_appl_options = factory.SubFactory(CustomApplOptionsFactory)

    class Meta:
        model = PCTMethodCustomization


class EPMethodCustomizationFactory(factory.django.DjangoModelFactory):
    custom_appl_details = factory.SubFactory(CustomApplDetailsFactory)
    custom_appl_options = factory.SubFactory(CustomApplOptionsFactory)

    class Meta:
        model = EPMethodCustomization
        # django_get_or_create = ('fam_est_form_data', 'country')


class PCTCountriesFactory(factory.django.DjangoModelFactory):
    fam_est_form_data = factory.SubFactory('famform.factories.FamEstFormDataFactory')
    country = factory.SubFactory(CountryFactory)
    custom_appl_details = factory.SubFactory(CustomApplDetailsFactory)
    custom_appl_options = factory.SubFactory(CustomApplOptionsFactory)

    class Meta:
        model = PCTCountryCustomization
        django_get_or_create = ('fam_est_form_data', 'country')


def generate_pct_countries(pct_country_country):
    return factory.RelatedFactory(
        PCTCountriesFactory,
        factory_related_name='fam_est_form_data',
        country=translate_country(pct_country_country)
    )


class EPCountriesFactory(factory.django.DjangoModelFactory):
    fam_est_form_data = factory.SubFactory('famform.factories.FamEstFormDataFactory')
    country = factory.SubFactory(CountryFactory)
    custom_appl_details = factory.SubFactory(CustomApplDetailsFactory)
    custom_appl_options = factory.SubFactory(CustomApplOptionsFactory)

    class Meta:
        model = EPCountryCustomization
        django_get_or_create = ('fam_est_form_data', 'country')


def generate_ep_countries(ep_country_country):
    return factory.RelatedFactory(
        EPCountriesFactory,
        factory_related_name='fam_est_form_data',
        country=translate_country(ep_country_country)
    )


class ParisCountriesFactory(factory.django.DjangoModelFactory):
    fam_est_form_data = factory.SubFactory('famform.factories.FamEstFormDataFactory')
    country = factory.SubFactory(CountryFactory)
    custom_appl_details = factory.SubFactory(CustomApplDetailsFactory)
    custom_appl_options = factory.SubFactory(CustomApplOptionsFactory)

    class Meta:
        model = ParisCountryCustomization
        django_get_or_create = ('fam_est_form_data', 'country')


def generate_paris_countries(paris_country_country):
    return factory.RelatedFactory(
        ParisCountriesFactory,
        factory_related_name='fam_est_form_data',
        country=translate_country(paris_country_country)
    )


class FamEstFormDataFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    family = factory.SubFactory(FamilyFactory)

    # countries = models.ManyToManyField(Country)
    @factory.post_generation
    def countries(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.countries.set(extracted)
            # for country in extracted:
            #     self.countries.add(country)

    init_appl_filing_date = factory.Faker('date_object')
    init_appl_country = factory.SubFactory(CountryFactory)
    init_appl_type = factory.SubFactory(ApplTypeFactory)
    init_appl_details = factory.SubFactory(ApplDetailsFactory)
    init_appl_options = factory.SubFactory(CustomApplOptionsFactory)

    date_created = factory.Faker('date_object')
    pct_method = factory.Faker('boolean')
    pct_method_customization = factory.SubFactory(PCTMethodCustomizationFactory)
    pct_country = factory.SubFactory(CountryFactory)
    isa_country = factory.SubFactory(CountryFactory)
    ep_method = False
    ep_method_customization = factory.SubFactory(EPMethodCustomizationFactory)

    pct_countries = generate_pct_countries('CN')
    ep_countries = generate_ep_countries('GB')
    paris_countries = generate_paris_countries('US')

    class Meta:
        model = FamEstFormData


class FamOptionsFactory(factory.django.DjangoModelFactory):
    family = factory.SubFactory(FamilyFactory)

    class Meta:
        model = FamOptions


class ApplOptionsParticularsFactory(factory.django.DjangoModelFactory):
    request_examination_early_bool = False
    doc_format = factory.SubFactory(DocFormatFactory)

    class Meta:
        model = ApplOptionsParticulars


class ApplOptionsFactory(factory.django.DjangoModelFactory):
    title = factory.sequence(lambda n: "Title %03d" % n)
    country = factory.SubFactory(CountryFactory)
    appl_type = factory.SubFactory(ApplTypeFactory)
    # date_filing = factory.Faker('date_time', tzinfo=timezone.get_default_timezone())
    date_filing = factory.Faker('date_object')
    # translation_full_required = False
    translation_implemented = factory.SubFactory(TranslationImplementedPseudoEnumFactory)
    details = factory.SubFactory('application.factories.ApplDetailsFactory')
    fam_options = factory.SubFactory(FamOptionsFactory)
    prev_appl_options = None
    particulars = factory.SubFactory(ApplOptionsParticularsFactory)

    class Meta:
        model = ApplOptions


class BaseOptionsFactory(factory.django.DjangoModelFactory):
    date_diff = factory.Faker('diff')
    appl = factory.SubFactory(ApplOptionsFactory)

    class Meta:
        abstract = True
        model = BaseOptions


class PublOptionFactory(BaseOptionsFactory):
    class Meta:
        model = PublOptions
        abstract = False


class RequestExaminationOptionFactory(BaseOptionsFactory):
    class Meta:
        model = RequestExaminationOptions
        abstract = False


class OAOptionsFactory(BaseOptionsFactory):
    oa_prev = None

    class Meta:
        model = OAOptions
        abstract = False


class AllowOptionsFactory(BaseOptionsFactory):
    class Meta:
        model = AllowOptions
        abstract = False


class IssueOptionsFactory(BaseOptionsFactory):
    class Meta:
        model = IssueOptions
        abstract = False
