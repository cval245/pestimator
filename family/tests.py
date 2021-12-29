from django.test import TestCase
# Create your tests here.
from account.factories import UserProfileFactory
from application.factories import ApplDetailsFactory
from characteristics.factories import LanguageFactory, CountryFactory
from famform.factories import FamOptionsFactory, ApplOptionsFactory
from user.factories import UserFactory
from .factories import FamilyFactory


class FamilyTest(TestCase):

    # def test_create_appls_estimates_remaining_deducted_by_one(self):
    #     user = UserFactory()
    #     init_estimates_num = 3
    #     user_profile = UserProfileFactory(user=user, company_name='eeeee')
    #     user_profile.estimates_remaining = init_estimates_num
    #     family = FamilyFactory(user=user)
    #     language_cn = LanguageFactory(Chinese=True)
    #     country_cn = CountryFactory(CN=True)
    #     fam_option = FamOptionsFactory(family=family)
    #     details = ApplDetailsFactory(language=language_cn, num_pages_description=12)
    #     appl_option = ApplOptionsFactory(country=country_cn, details=details)
    #     family.create_appls(famOptions=fam_option)
    #     self.assertEquals(init_estimates_num - 1, user_profile.estimates_remaining)

    def test_add_more_here_test(self):
        self.fail('add more family tests')
