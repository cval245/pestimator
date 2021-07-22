import factory
from django.utils import timezone

from application.factories import ApplDetailsFactory
from characteristics.factories import CountryFactory, ApplTypeFactory, EntitySizeFactory
from family.factories import FamilyFactory
from user.factories import UserFactory
from . import models
from .models import FamEstFormData, FamOptions, ApplOptions, BaseOptions, PublOptions, OAOptions, AllowOptions, \
    IssueOptions


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
    init_appl_indep_claims = factory.Faker('random_int', min=1, max=10, step=1)
    init_appl_claims = factory.Faker('random_int', min=1, max=50, step=1)
    init_appl_drawings = factory.Faker('random_int', min=1, max=50, step=1)
    init_appl_pages = factory.Faker('random_int', min=1, max=50, step=1)
    date_created = factory.Faker('date_object')

    method = factory.Faker('boolean')
    meth_country = factory.SubFactory(CountryFactory)

    entity_size = factory.SubFactory(EntitySizeFactory)

    class Meta:
        model = FamEstFormData


class FamOptionsFactory(factory.django.DjangoModelFactory):
    family = factory.SubFactory(FamilyFactory)

    class Meta:
        model = FamOptions


class ApplOptionsFactory(factory.django.DjangoModelFactory):
    title = factory.sequence(lambda n: "Title %03d" % n)
    country = factory.SubFactory(CountryFactory)
    appl_type = factory.SubFactory(ApplTypeFactory)
    date_filing = factory.Faker('date_time', tzinfo=timezone.get_default_timezone())
    details = factory.SubFactory(ApplDetailsFactory)
    fam_options = factory.SubFactory(FamOptionsFactory)
    prev_appl_options = None

    class Meta:
        model = ApplOptions

class BaseOptionsFactory(factory.django.DjangoModelFactory):
    date_diff = 'P1Y'
    appl = factory.SubFactory(ApplOptionsFactory)

    class Meta:
        abstract = True
        model = BaseOptions



class PublOptionFactory(BaseOptionsFactory):

    class Meta:
        model = PublOptions
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