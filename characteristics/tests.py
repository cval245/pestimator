from django.test import TestCase

# Create your tests here.
from characteristics.factories import ApplTypeFactory, CountryFactory
from user.factories import UserFactory


class CharacteristicsTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.applType_prov = ApplTypeFactory(prov=True)
        self.applType_pct = ApplTypeFactory(pct=True)
        self.applType_utility = ApplTypeFactory(utility=True)
        self.country_US = CountryFactory(US=True)
        self.country_CN = CountryFactory(CN=True)
        self.country_JP = CountryFactory(country='JP')

    def test_set_up(self):
        pass
