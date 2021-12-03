import factory
from . import models


class ApplTypeFactory(factory.django.DjangoModelFactory):
    application_type = 'utility'

    class Meta:
        model = models.ApplType
        django_get_or_create = ('application_type',)

    class Params:
        prov = factory.Trait(
            application_type='prov',
            long_name='Provisional Application',
            internal_bool='False',
        )
        pct = factory.Trait(
            application_type='pct',
            long_name='Provisional Application',
            internal_bool='False',
        )
        utility = factory.Trait(
            application_type='utility',
            long_name='Provisional Application',
            internal_bool='False',
        )
        ep = factory.Trait(
            application_type='ep',
            long_name='EP application',
            internal_bool=True,
        )
        epvalidation = factory.Trait(
            application_type='epvalidation',
            long_name='EP Validation Application',
            internal_bool=True,
        )
        nationalphase = factory.Trait(
            application_type='nationalphase',
            long_name='National Phase',
            internal_bool=True,
        )


class EPValidationTranslationRequiredFactory(factory.django.DjangoModelFactory):
    name = 'default name'
    applicable_bool = False


class CountryFactory(factory.django.DjangoModelFactory):
    country = 'US'
    active_bool = True
    ep_bool = False
    pct_accept_bool = True
    currency_name = 'USD'
    long_name = 'United States of America'
    color = '#25560'
    available_appl_types = factory.SubFactory(ApplTypeFactory)
    # isa_countries = factory.RelatedFactory(CountryFactory)
    ep_validation_translation_required = ''
    available_entity_sizes = ''
    available_doc_formats = ''
    available_languages = ''

    # @factory.post_generation
    # def Language(self, create, extracted, **kwargs):
    #     if not create:
    #         return
    #     if extracted:
    #         # self.Language.set(extracted)
    #         for lang in extracted:
    #             self.Language_set.add(lang)

    class Meta:
        model = models.Country
        django_get_or_create = ('country',)

    class Params:
        US = factory.Trait(
            country='US',
            active_bool=True,
            ep_bool=False,
            pct_analysis_bool=True,
            currency_name='USD',
            long_name='United States of America',
            color='#25560',
        )
        CN = factory.Trait(
            country='CN',
            active_bool=True,
            ep_bool=False,
            pct_analysis_bool=True,
            currency_name='CNY',
            long_name='China',
            color='#59C3C3',
        )
        JP = factory.Trait(
            country='JP',
            active_bool=True,
            ep_bool=False,
            pct_analysis_bool=True,
            currency_name='JPY',
            long_name='Japan',
            color='#E6AF2E',
        )
        KR = factory.Trait(
            country='KR',
            active_bool=True,
            ep_bool=False,
            pct_analysis_bool=True,
            currency_name='KRW',
            long_name='South Korea',
            color='#DE6B48',
        )
        EP = factory.Trait(
            country='EP',
            active_bool=True,
            ep_bool=True,
            pct_analysis_bool=True,
            currency_name='EUR',
            long_name='European Patent Office',
            color='#CAB1BD',
        )
        GB = factory.Trait(
            country='GB',
            active_bool=True,
            ep_bool=True,
            pct_analysis_bool=True,
            currency_name='GBP',
            long_name='Great Britain',
            color='#824C71',
        )
        DE = factory.Trait(
            country='DE',
            active_bool=True,
            ep_bool=True,
            pct_analysis_bool=True,
            currency_name='EUR',
            long_name='Germany',
            color='#4D243D',
        )
        FR = factory.Trait(
            country='FR',
            active_bool=True,
            ep_bool=True,
            pct_analysis_bool=True,
            currency_name='EUR',
            long_name='France',
            color='#6622CC',
        )


class LanguageFactory(factory.django.DjangoModelFactory):
    name = 'english'
    words_per_page = 800

    class Meta:
        model = models.Language
        django_get_or_create = ('name',)

    class Params:
        english = factory.Trait(
            name='english',
            words_per_page=800,
        )
        chinese = factory.Trait(
            name='chinese',
            words_per_page=1000,
        )
        korean = factory.Trait(
            name='korean',
            words_per_page=700,
        )
        japanese = factory.Trait(
            name='japanese',
            words_per_page=700,
        )
        german = factory.Trait(
            name='german',
            words_per_page=700,
        )
        french = factory.Trait(
            name='french',
            words_per_page=700,
        )


class EntitySizeFactory(factory.django.DjangoModelFactory):
    entity_size = 'default'
    description = 'default entity size description'

    class Meta:
        model = models.EntitySize
        django_get_or_create = ('entity_size',)

    class Params:
        small = factory.Trait(
            entity_size='small',
            description='small entity desc'
        )
        micro = factory.Trait(
            entity_size='micro',
            description='micro entity desc'
        )


class DocFormatFactory(factory.django.DjangoModelFactory):
    name = 'default name'
