import factory
from django.test import TestCase

# Create your tests here.
from characteristics.factories import ApplTypeFactory, CountryFactory, TotalCountryFactoryCN, \
    TotalCountryFactoryUS, EntitySizeFactory
from user.factories import UserFactory


class CharacteristicsTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.applType_prov = ApplTypeFactory(prov=True)
        self.applType_pct = ApplTypeFactory(pct=True)
        self.applType_utility = ApplTypeFactory(utility=True)
        self.applType_nat = ApplTypeFactory(nationalphase=True)
        self.country_CN = TotalCountryFactoryCN()
        self.country_US = TotalCountryFactoryUS()
        self.ep_country = EntitySizeFactory()

        print('suer', self.country_US.entitysize_set.all())

    def test_set_up(self):
        pass
