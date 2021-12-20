import factory
from factory import RelatedFactory

from . import models


class FeeCategoryFactory(factory.django.DjangoModelFactory):
    name = 'default fee category name'

    class Meta:
        model = models.FeeCategory
        django_get_or_create = ('name',)


class TranslationImplementedPseudoEnumFactory(factory.django.DjangoModelFactory):
    name = 'no translation'

    class Meta:
        model = models.TranslationImplementedPseudoEnum
        django_get_or_create = ('name',)

    class Params:
        no_translation = factory.Trait(
            name='no translation',
        )
        full_translation = factory.Trait(
            name='full translation',
        )


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
            long_name='PCT Application',
            internal_bool='False',
        )
        utility = factory.Trait(
            application_type='utility',
            long_name='Utility Application',
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

    # applicable_bool = False

    class Meta:
        model = models.EPValidationTranslationRequired
        django_get_or_create = ('name',)

    class Params:
        NA = factory.Trait(name='N/A')
        NoTransIfOfficial = factory.Trait(name='no translation required if official language')
        Full = factory.Trait(name='full translation required')


class CountryFactory(factory.django.DjangoModelFactory):
    country = 'US'
    active_bool = True
    ep_bool = False
    pct_ro_bool = True
    pct_accept_bool = True
    currency_name = 'USD'
    long_name = 'United States of America'
    color = '#25560'
    ep_validation_translation_required = factory.SubFactory(EPValidationTranslationRequiredFactory)

    class Meta:
        model = models.Country
        django_get_or_create = ('country',)

    class Params:
        US = factory.Trait(
            country='US',
            active_bool=True,
            ep_bool=False,
            pct_ro_bool=True,
            pct_accept_bool=True,
            currency_name='USD',
            long_name='United States of America',
            color='#25560',
            ep_validation_translation_required=factory.SubFactory(EPValidationTranslationRequiredFactory, NA=True)
        )
        CN = factory.Trait(
            country='CN',
            active_bool=True,
            ep_bool=False,
            pct_ro_bool=True,
            pct_accept_bool=True,
            currency_name='CNY',
            long_name='China',
            color='#59C3C3',
            ep_validation_translation_required=factory.SubFactory(EPValidationTranslationRequiredFactory, NA=True)
        )
        JP = factory.Trait(
            country='JP',
            active_bool=True,
            ep_bool=False,
            pct_ro_bool=True,
            pct_accept_bool=True,
            currency_name='JPY',
            long_name='Japan',
            color='#E6AF2E',
            ep_validation_translation_required=factory.SubFactory(EPValidationTranslationRequiredFactory, NA=True)
        )
        KR = factory.Trait(
            country='KR',
            active_bool=True,
            ep_bool=False,
            pct_ro_bool=True,
            pct_accept_bool=True,
            currency_name='KRW',
            long_name='South Korea',
            color='#DE6B48',
            ep_validation_translation_required=factory.SubFactory(EPValidationTranslationRequiredFactory, NA=True)
        )
        EP = factory.Trait(
            country='EP',
            active_bool=True,
            ep_bool=True,
            pct_ro_bool=True,
            pct_accept_bool=True,
            currency_name='EUR',
            long_name='European Patent Office',
            color='#CAB1BD',
            ep_validation_translation_required=factory.SubFactory(EPValidationTranslationRequiredFactory,
                                                                  NoTransIfOfficial=True)
        )
        GB = factory.Trait(
            country='GB',
            active_bool=True,
            ep_bool=True,
            pct_ro_bool=True,
            pct_accept_bool=True,
            currency_name='GBP',
            long_name='Great Britain',
            color='#824C71',
            ep_validation_translation_required=factory.SubFactory(EPValidationTranslationRequiredFactory,
                                                                  NoTransIfOfficial=True)
        )
        DE = factory.Trait(
            country='DE',
            active_bool=True,
            ep_bool=True,
            pct_ro_bool=True,
            pct_accept_bool=True,
            currency_name='EUR',
            long_name='Germany',
            color='#4D243D',
            ep_validation_translation_required=factory.SubFactory(EPValidationTranslationRequiredFactory,
                                                                  NoTransIfOfficial=True)
        )
        FR = factory.Trait(
            country='FR',
            active_bool=True,
            ep_bool=True,
            pct_ro_bool=False,
            pct_accept_bool=False,
            currency_name='EUR',
            long_name='France',
            color='#6622CC',
            ep_validation_translation_required=factory.SubFactory(EPValidationTranslationRequiredFactory,
                                                                  NoTransIfOfficial=True)
        )
        IB = factory.Trait(
            country='IB',
            active_bool=True,
            ep_bool=False,
            pct_ro_bool=True,
            pct_accept_bool=False,
            currency_name='USD',
            long_name='International Bureau',
            color='#6622CC',
            ep_validation_translation_required=factory.SubFactory(EPValidationTranslationRequiredFactory,
                                                                  NA=True)
        )


class LanguageFactory(factory.django.DjangoModelFactory):
    name = 'English'
    words_per_page = 800
    ep_official_language_bool = False

    class Meta:
        model = models.Language
        django_get_or_create = ('name',)

    class Params:
        English = factory.Trait(
            name='English',
            words_per_page=800,
            ep_official_language_bool=True,
        )
        Chinese = factory.Trait(
            name='Chinese',
            words_per_page=1000,
            ep_official_language_bool=False,
        )
        Korean = factory.Trait(
            name='Korean',
            words_per_page=700,
            ep_official_language_bool=False,
        )
        Japanese = factory.Trait(
            name='Japanese',
            words_per_page=700,
            ep_official_language_bool=False,
        )
        German = factory.Trait(
            name='German',
            words_per_page=700,
            ep_official_language_bool=True,
        )
        French = factory.Trait(
            name='French',
            words_per_page=700,
            ep_official_language_bool=True,
        )


class EntitySizeFactory(factory.django.DjangoModelFactory):
    entity_size = 'default'
    description = 'default entity size description'
    default_bool = False
    country = factory.SubFactory(CountryFactory)

    class Meta:
        model = models.EntitySize
        django_get_or_create = ('entity_size',)

    class Params:
        us_small = factory.Trait(
            entity_size='small',
            description='small entity desc',
            country=factory.SubFactory(CountryFactory, US=True),
        )
        us_micro = factory.Trait(
            entity_size='micro',
            description='micro entity desc',
            country=factory.SubFactory(CountryFactory, US=True),
        )
        us_default = factory.Trait(
            entity_size='default',
            description='default entity desc',
            country=factory.SubFactory(CountryFactory, US=True),
        )


class DocFormatFactory(factory.django.DjangoModelFactory):
    name = 'default'

    class Meta:
        model = models.DocFormat
        django_get_or_create = ('name',)

    class Params:
        electronic = factory.Trait(
            name='electronic format'
        )
        paper = factory.Trait(
            name='paper format'
        )
        electronic_xml = factory.Trait(
            name='electronic format --XML'
        )
        electronic_pdf = factory.Trait(
            name='electronic format --PDF'
        )


class AvailableDocFormatsCountryFactory(factory.django.DjangoModelFactory):
    doc_format = factory.SubFactory(DocFormatFactory)
    country = factory.SubFactory(CountryFactory)
    appl_type = factory.SubFactory(ApplTypeFactory)
    default = False

    class Meta:
        model = models.DocFormatCountry
        django_get_or_create = ('doc_format', 'country', 'appl_type')


class AvailableLanguagesFactory(factory.django.DjangoModelFactory):
    language = factory.SubFactory(LanguageFactory)
    country = factory.SubFactory(CountryFactory)
    appl_type = factory.SubFactory(ApplTypeFactory)
    default = True

    class Meta:
        model = models.LanguageCountry
        django_get_or_create = ('language', 'country', 'appl_type')


class AvailableApplTypesFactory(factory.django.DjangoModelFactory):
    appltype = factory.SubFactory(ApplTypeFactory)

    class Meta:
        model = models.Country.available_appl_types.through
        django_get_or_create = ('country', 'appltype')


class AvailableISACountriesFactory(factory.django.DjangoModelFactory):
    to_country = factory.SubFactory(CountryFactory)

    class Meta:
        model = models.Country.isa_countries.through
        django_get_or_create = ('from_country', 'to_country')


def translate_appl_type(appl_type_name):
    if appl_type_name == 'utility':
        return factory.SubFactory(ApplTypeFactory, utility=True)
    elif appl_type_name == 'pct':
        return factory.SubFactory(ApplTypeFactory, pct=True)
    elif appl_type_name == 'nationalphase':
        return factory.SubFactory(ApplTypeFactory, nationalphase=True)
    elif appl_type_name == 'ep':
        return factory.SubFactory(ApplTypeFactory, ep=True)
    elif appl_type_name == 'epvalidation':
        return factory.SubFactory(ApplTypeFactory, epvalidation=True)
    elif appl_type_name == 'prov':
        return factory.SubFactory(ApplTypeFactory, prov=True)
    else:
        return None


def translate_country(country_country):
    if country_country == 'CN':
        return factory.SubFactory(CountryFactory, CN=True)
    elif country_country == 'US':
        return factory.SubFactory(CountryFactory, US=True)
    elif country_country == 'GB':
        return factory.SubFactory(CountryFactory, GB=True)
    elif country_country == 'DE':
        return factory.SubFactory(CountryFactory, DE=True)
    elif country_country == 'JP':
        return factory.SubFactory(CountryFactory, JP=True)
    elif country_country == 'KR':
        return factory.SubFactory(CountryFactory, KR=True)
    elif country_country == 'EP':
        return factory.SubFactory(CountryFactory, EP=True)
    elif country_country == 'FR':
        return factory.SubFactory(CountryFactory, FR=True)
    elif country_country == 'IB':
        return factory.SubFactory(CountryFactory, IB=True)
    else:
        return None


def generate_available_appl_type(appl_type_name):
    return factory.RelatedFactory(
        AvailableApplTypesFactory,
        factory_related_name='country',
        appltype=translate_appl_type(appl_type_name)
    )


def generate_available_language(language_name, appl_type_name, default_bool):
    return factory.RelatedFactory(
        AvailableLanguagesFactory,
        factory_related_name='country',
        language=factory.SubFactory(LanguageFactory, name=language_name),
        appl_type=translate_appl_type(appl_type_name),
        default=default_bool
    )


def generate_available_doc_formats(doc_format_name, appl_type_name):
    return factory.RelatedFactory(
        AvailableDocFormatsCountryFactory,
        factory_related_name='country',
        doc_format=factory.SubFactory(DocFormatFactory, name=doc_format_name),
        appl_type=translate_appl_type(appl_type_name)
    )


def generate_isa_countries(country_country):
    return factory.RelatedFactory(
        AvailableISACountriesFactory,
        factory_related_name='from_country',
        to_country=translate_country(country_country)
    )


class TotalCountryFactoryCN(CountryFactory):
    CN = True
    available_appl_types_pct = generate_available_appl_type('pct')
    available_appl_types_utility = generate_available_appl_type('utility')
    available_appl_types_nationalphase = generate_available_appl_type('nationalphase')

    language_chinese_pct = generate_available_language('Chinese', 'pct', True)
    language_chinese_utility = generate_available_language('Chinese', 'utility', True)
    language_chinese_nationalphase = generate_available_language('Chinese', 'nationalphase', True)

    doc_format_utility_electronic = generate_available_doc_formats('electronic format', 'utility')
    doc_format_utility_paper = generate_available_doc_formats('paper format', 'utility')
    doc_format_nationalphase_electronic = generate_available_doc_formats('electronic format', 'nationalphase')
    doc_format_nationalphase_paper = generate_available_doc_formats('paper format', 'nationalphase')
    doc_format_pct_paper = generate_available_doc_formats('paper format', 'pct')
    doc_format_pct_electronic_pdf = generate_available_doc_formats('electronic format --PDF', 'pct')
    doc_format_pct_electronic_xml = generate_available_doc_formats('electronic format --XML', 'pct')

    isa_country_cn = generate_isa_countries('CN')
    isa_country_ib = generate_isa_countries('IB')


class TotalCountryFactoryEP(CountryFactory):
    EP = True
    available_appl_types_pct = generate_available_appl_type('pct')
    available_appl_types_utility = generate_available_appl_type('ep')
    available_appl_types_nationalphase = generate_available_appl_type('nationalphase')

    language_chinese_pct = generate_available_language('English', 'pct', True)
    language_chinese_utility = generate_available_language('English', 'utility', True)
    language_chinese_nationalphase = generate_available_language('English', 'nationalphase', True)

    doc_format_utility_electronic = generate_available_doc_formats('electronic format', 'utility')
    doc_format_utility_paper = generate_available_doc_formats('paper format', 'utility')
    doc_format_nationalphase_electronic = generate_available_doc_formats('electronic format', 'nationalphase')
    doc_format_nationalphase_paper = generate_available_doc_formats('paper format', 'nationalphase')
    doc_format_pct_paper = generate_available_doc_formats('paper format', 'pct')
    doc_format_pct_electronic_pdf = generate_available_doc_formats('electronic format --PDF', 'pct')
    doc_format_pct_electronic_xml = generate_available_doc_formats('electronic format --XML', 'pct')

    isa_country_ep = generate_isa_countries('EP')
    isa_country_ib = generate_isa_countries('IB')


class TotalCountryFactoryGB(CountryFactory):
    GB = True
    available_appl_types_pct = generate_available_appl_type('pct')
    available_appl_types_utility = generate_available_appl_type('utility')
    available_appl_types_nationalphase = generate_available_appl_type('nationalphase')
    available_appl_types_ep_validation = generate_available_appl_type('epvalidation')

    language_chinese_pct = generate_available_language('English', 'pct', True)
    language_chinese_utility = generate_available_language('English', 'utility', True)
    language_chinese_nationalphase = generate_available_language('English', 'nationalphase', True)

    doc_format_utility_electronic = generate_available_doc_formats('electronic format', 'utility')
    doc_format_utility_paper = generate_available_doc_formats('paper format', 'utility')
    doc_format_nationalphase_electronic = generate_available_doc_formats('electronic format', 'nationalphase')
    doc_format_nationalphase_paper = generate_available_doc_formats('paper format', 'nationalphase')
    doc_format_pct_paper = generate_available_doc_formats('paper format', 'pct')
    doc_format_pct_electronic_pdf = generate_available_doc_formats('electronic format --PDF', 'pct')
    doc_format_pct_electronic_xml = generate_available_doc_formats('electronic format --XML', 'pct')

    isa_country_cn = generate_isa_countries('GB')
    isa_country_ep = generate_isa_countries('EP')
    isa_country_ib = generate_isa_countries('IB')


class TotalCountryFactoryUS(CountryFactory):
    US = True
    available_appl_types_pct = generate_available_appl_type('pct')
    available_appl_types_prov = generate_available_appl_type('prov')
    available_appl_types_utility = generate_available_appl_type('utility')
    available_appl_types_nationalphase = generate_available_appl_type('nationalphase')

    language_english_pct = generate_available_language('English', 'pct', True)
    language_english_utility = generate_available_language('English', 'utility', True)
    language_english_nationalphase = generate_available_language('English', 'nationalphase', True)
    language_english_prov = generate_available_language('English', 'prov', True)

    doc_format_utility_electronic = generate_available_doc_formats('electronic format', 'utility')
    doc_format_utility_paper = generate_available_doc_formats('paper format', 'utility')
    doc_format_prov_electronic = generate_available_doc_formats('electronic format', 'prov')
    doc_format_prov_paper = generate_available_doc_formats('paper format', 'prov')
    doc_format_nationalphase_electronic = generate_available_doc_formats('electronic format', 'nationalphase')
    doc_format_nationalphase_paper = generate_available_doc_formats('paper format', 'nationalphase')
    doc_format_pct_paper = generate_available_doc_formats('paper format', 'pct')
    doc_format_pct_electronic_pdf = generate_available_doc_formats('electronic format --PDF', 'pct')
    doc_format_pct_electronic_xml = generate_available_doc_formats('electronic format --XML', 'pct')

    isa_country_cn = generate_isa_countries('US')
    isa_country_ib = generate_isa_countries('IB')

    entity_size_small = factory.RelatedFactory(
        EntitySizeFactory,
        factory_related_name='country',
        us_small=True
    )

    entity_size_micro = factory.RelatedFactory(
        EntitySizeFactory,
        factory_related_name='country',
        us_micro=True
    )

    entity_size_default = factory.RelatedFactory(
        EntitySizeFactory,
        factory_related_name='country',
        us_default=True
    )
