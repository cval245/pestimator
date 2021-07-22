import factory
from . import models


class ApplTypeFactory(factory.django.DjangoModelFactory):
    application_type = 'utility'

    class Meta:
        model = models.ApplType
        django_get_or_create = ('application_type',)

    class Params:
        prov = factory.Trait(
            application_type='prov'
        )
        pct = factory.Trait(
            application_type='pct'
        )
        utility = factory.Trait(
            application_type='utility'
        )


class CountryFactory(factory.django.DjangoModelFactory):
    country = 'JP'
    active_bool = True
    currency_name = 'JPY'

    class Meta:
        model = models.Country
        django_get_or_create = ('country',)

    class Params:
        US = factory.Trait(
            country='US',
            currency_name='USD'
        )
        CN = factory.Trait(
            country='CN',
            currency_name='CNY'
        )


class EntitySizeFactory(factory.django.DjangoModelFactory):
    entity_size = 'default'

    class Meta:
        model = models.EntitySize
        django_get_or_create = ('entity_size',)

    class Params:
        small = factory.Trait(
            entity_size='small'
        )
        micro = factory.Trait(
            entity_size='micro'
        )

class OANumPerCountryFactory(factory.django.DjangoModelFactory):
    country = factory.SubFactory(CountryFactory)
    oa_num = factory.Faker('random_digit_not_null')

    class Meta:
        model = models.OANumPerCountry
        django_get_or_create = ('country',)

    class Params:
        small = factory.Trait(
            entity_size='small'
        )
        micro = factory.Trait(
            entity_size='micro'
        )

