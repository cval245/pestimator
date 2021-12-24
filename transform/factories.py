import factory
from django.utils import timezone

from characteristics.factories import CountryFactory, ApplTypeFactory
from estimation.factories import DiffProvider
from . import models

factory.Faker.add_provider(DiffProvider)


class TransComplexTimeFactory(factory.django.DjangoModelFactory):
    name = 'from priority date'

    class Meta:
        model = models.TransComplexTime
        django_get_or_create = ('name',)


class BaseTransformFactory(factory.django.DjangoModelFactory):
    date_diff = factory.Faker('diff')
    country = factory.SubFactory(CountryFactory)
    appl_type = factory.SubFactory(ApplTypeFactory)
    trans_complex_time_condition = factory.SubFactory(TransComplexTimeFactory)

    class Meta:
        model = models.BaseTransform
        abstract = True


class CustomFilingTransformFactory(BaseTransformFactory):
    prev_appl_type = None

    class Meta:
        model = models.CustomFilingTransform
        abstract = False


class PublicationTransformFactory(BaseTransformFactory):
    class Meta:
        model = models.PublicationTransform
        abstract = False


class RequestExaminationTransformFactory(BaseTransformFactory):
    class Meta:
        model = models.RequestExaminationTransform
        abstract = False


class OATransformFactory(BaseTransformFactory):
    class Meta:
        model = models.OATransform
        abstract = False


class USOATransformFactory(OATransformFactory):
    final_oa_bool = False

    class Meta:
        model = models.USOATransform
        abstract = False

    class Params:
        FOA = factory.Trait(final_oa_bool=True)
        NFOA = factory.Trait(final_oa_bool=False)


class AllowanceTransformFactory(BaseTransformFactory):
    class Meta:
        model = models.AllowanceTransform
        abstract = False


class IssueTransformFactory(BaseTransformFactory):
    class Meta:
        model = models.IssueTransform
        abstract = False


class CountryOANumFactory(factory.django.DjangoModelFactory):
    country = factory.SubFactory(CountryFactory)
    oa_total = factory.Faker('random_digit')

    class Meta:
        model = models.CountryOANum


class DefaultCountryOANumFactory(factory.django.DjangoModelFactory):
    oa_total = factory.Faker('random_digit')

    class Meta:
        model = models.DefaultCountryOANum


class BaseDefaultTransformFactory(factory.django.DjangoModelFactory):
    date_diff = factory.Faker('diff')
    appl_type = factory.SubFactory(ApplTypeFactory)

    class Meta:
        model = models.BaseDefaultTransform
        django_get_or_create = ('appl_type',)
        abstract = True


class DefaultFilingTransformFactory(BaseDefaultTransformFactory):
    class Meta:
        model = models.DefaultFilingTransform
        abstract = False


class DefaultPublTransformFactory(BaseDefaultTransformFactory):
    class Meta:
        model = models.DefaultPublTransform
        abstract = False


class DefaultRequestExaminationTransformFactory(BaseDefaultTransformFactory):
    class Meta:
        model = models.DefaultRequestExaminationTransform
        abstract = False


class DefaultOATransformFactory(BaseDefaultTransformFactory):
    class Meta:
        model = models.DefaultOATransform
        abstract = False


class DefaultAllowanceTransformFactory(BaseDefaultTransformFactory):
    class Meta:
        model = models.DefaultAllowanceTransform
        abstract = False


class DefaultIssueTransformFactory(BaseDefaultTransformFactory):
    class Meta:
        model = models.DefaultIssueTransform
        abstract = False
