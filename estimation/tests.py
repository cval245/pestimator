from django.test import TestCase

from characteristics.models import Country
from famform.factories import FamEstFormDataFactory
from family.factories import FamilyFactory
from user.factories import UserFactory
from . import models
from . import factories


class TestLawFirmEst(TestCase):

    def test_func(self):
        lawfirmEst = factories.LawFirmEstFactory()
        family = FamilyFactory()
        user = UserFactory()
        appl = factories.ApplicationFactory()
        country_US = factories.CountryFactory(US=True)
        country_CN = factories.CountryFactory(CN=True)
        lawFirmEst = factories.LawFirmEstFactory()
        famform = FamEstFormDataFactory.create(countries=[country_US, country_CN])


        # appl_two = factories.ApplicationFactory(prior_appl=appl)
        # print(lawfirmEst, appl)
