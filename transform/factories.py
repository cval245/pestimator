import factory
from django.utils import timezone

from characteristics.factories import CountryFactory, ApplTypeFactory
from . import models


class BaseTransformFactory(factory.django.DjangoModelFactory):
    date_diff = 'P1Y'
    country = factory.SubFactory(CountryFactory)

    class Meta:
        model = models.BaseTransform
        abstract = True


class CustomFilingTransformFactory(BaseTransformFactory):
    appl_type = factory.SubFactory(ApplTypeFactory)
    prev_appl_type = None

    class Meta:
        model = models.CustomFilingTransform
        abstract = False


class PublicationTransformFactory(BaseTransformFactory):
    class Meta:
        model = models.PublicationTransform
        abstract = False


class OATransformFactory(BaseTransformFactory):
    class Meta:
        model = models.OATransform
        abstract = False


class USOATransformFactory(OATransformFactory):
    class Meta:
        model = models.USOATransform
        abstract = False


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
    date_diff = 'P1Y'
    appl_type = factory.SubFactory(ApplTypeFactory)

    class Meta:
        model = models.BaseDefaultTransform
        abstract = True


class DefaultFilingTransformFactory(BaseDefaultTransformFactory):
    class Meta:
        model = models.DefaultFilingTransform
        abstract = False


class DefaultPublTransformFactory(BaseDefaultTransformFactory):
    class Meta:
        model = models.DefaultPublTransform
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
