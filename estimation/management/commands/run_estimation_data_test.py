from django.core.management.base import BaseCommand

from characteristics.models import ApplType, Country, DetailedFeeCategory, EntitySize
from estimation.models import FilingEstimateTemplate


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    entity_size_us_micro = 0
    entity_size_us_small = 0
    entity_size_us_default = 0
    appl_type_pct = 0
    appl_type_utility = 0
    appl_type_ep = 0
    appl_type_nationalphase = 0
    appl_type_prov = 0
    appl_type_epvalid = 0

    def determine_exactly_one_present(self, selected_trans, appl_type, prev_appl_type, missing_arr, country):
        searched = [x for x in selected_trans if x.prev_appl_type == prev_appl_type]
        if len(searched) == 0:
            missing_arr.append({'country': country, 'appl_type': appl_type, 'prev_appl_type': prev_appl_type})
        elif len(searched) > 1:
            raise Exception('duplicate found', appl_type, 'prev_appl_type', prev_appl_type)
        return missing_arr

    def handle(self, *args, **options):

        self.appl_type_utility = ApplType.objects.get(application_type='utility')
        self.appl_type_pct = ApplType.objects.get(application_type='pct')
        self.appl_type_ep = ApplType.objects.get(application_type='ep')
        self.appl_type_nationalphase = ApplType.objects.get(application_type='nationalphase')
        self.appl_type_prov = ApplType.objects.get(application_type='prov')
        self.appl_type_epvalid = ApplType.objects.get(application_type='epvalidation')
        # countries = Country.objects.filter(active_bool=True).select_related()
        self.test_all_us()
        self.stdout.write(self.style.SUCCESS('Successfully ran run_estimation_data_test'))

    def test_all_us(self):
        country_us = Country.objects.get(country='US')
        self.entity_size_us_micro = EntitySize.objects.get(country=country_us, entity_size='micro')
        self.entity_size_us_small = EntitySize.objects.get(country=country_us, entity_size='small')
        self.entity_size_us_default = EntitySize.objects.get(country=country_us, entity_size='default')
        templates = FilingEstimateTemplate.objects.filter(country=country_us)

        detailed_fee_cat = DetailedFeeCategory.objects.get(
            country=country_us,
            name="Basic filing fee - Utility (paper filing also requires non-electronic filing fee under 1.16(t))")
        self.test_pct_and_utility(detailed_fee_cat=detailed_fee_cat, templates=templates)

        detailed_fee_cat = DetailedFeeCategory.objects.get(
            country=country_us,
            name="Each independent claim in excess of three")
        self.test_pct_and_utility(detailed_fee_cat=detailed_fee_cat, templates=templates)

        detailed_fee_cat = DetailedFeeCategory.objects.get(
            country=country_us,
            name="Each claim in excess of 20")
        self.test_pct_and_utility(detailed_fee_cat=detailed_fee_cat, templates=templates)

        detailed_fee_cat = DetailedFeeCategory.objects.get(
            country=country_us,
            name="Multiple dependent claim")
        self.test_pct_and_utility(detailed_fee_cat=detailed_fee_cat, templates=templates)

        detailed_fee_cat = DetailedFeeCategory.objects.get(
            country=country_us,
            name="Utility application size fee - for each additional 50 sheets that exceeds 100 sheets")
        self.test_pct_and_utility(detailed_fee_cat=detailed_fee_cat, templates=templates)

        detailed_fee_cat = DetailedFeeCategory.objects.get(
            country=country_us,
            name="Provisional application size fee - for each additional 50 sheets that exceeds 100 sheets")
        temp_prov = templates.filter(detailed_fee_category=detailed_fee_cat, appl_type=self.appl_type_prov)
        self.fundamental_us_test(templates=temp_prov,
                                 detailed_fee_category=detailed_fee_cat,
                                 appl_type=self.appl_type_prov)

        detailed_fee_cat = DetailedFeeCategory.objects.get(
            country=country_us,
            name="Utility search fee")
        self.test_pct_and_utility(detailed_fee_cat=detailed_fee_cat, templates=templates)

        detailed_fee_cat = DetailedFeeCategory.objects.get(
            country=country_us,
            name="Utility examination fee")
        self.test_pct_and_utility(detailed_fee_cat=detailed_fee_cat, templates=templates)

        detailed_fee_cat = DetailedFeeCategory.objects.get(
            country=country_us,
            name="Utility issue fee")
        temp_utility = templates.filter(detailed_fee_category=detailed_fee_cat, appl_type=self.appl_type_utility)
        self.fundamental_us_test(templates=temp_utility,
                                 detailed_fee_category=detailed_fee_cat,
                                 appl_type=self.appl_type_utility)

        detailed_fee_cat = DetailedFeeCategory.objects.get(
            country=country_us,
            name="For maintaining an original or any reissue patent, due at 3.5 years")
        temp_utility = templates.filter(detailed_fee_category=detailed_fee_cat, appl_type=self.appl_type_utility)
        self.fundamental_us_test(templates=temp_utility,
                                 detailed_fee_category=detailed_fee_cat,
                                 appl_type=self.appl_type_utility)

        detailed_fee_cat = DetailedFeeCategory.objects.get(
            country=country_us,
            name="For maintaining an original or any reissue patent, due at 7.5 years")
        temp_utility = templates.filter(detailed_fee_category=detailed_fee_cat, appl_type=self.appl_type_utility)
        self.fundamental_us_test(templates=temp_utility,
                                 detailed_fee_category=detailed_fee_cat,
                                 appl_type=self.appl_type_utility)

        detailed_fee_cat = DetailedFeeCategory.objects.get(
            country=country_us,
            name="For maintaining an original or any reissue patent, due at 11.5 years")
        temp_utility = templates.filter(detailed_fee_category=detailed_fee_cat, appl_type=self.appl_type_utility)
        self.fundamental_us_test(templates=temp_utility,
                                 detailed_fee_category=detailed_fee_cat,
                                 appl_type=self.appl_type_utility)

        detailed_fee_cat = DetailedFeeCategory.objects.get(
            country=country_us,
            name="Request for continued examination (RCE) - 1st request (see 37 CFR 1.114)")
        temp_utility = templates.filter(detailed_fee_category=detailed_fee_cat, appl_type=self.appl_type_utility)
        self.fundamental_us_test(templates=temp_utility,
                                 detailed_fee_category=detailed_fee_cat,
                                 appl_type=self.appl_type_utility)

        detailed_fee_cat = DetailedFeeCategory.objects.get(
            country=country_us,
            name="Request for continued examination (RCE) - 2nd and subsequent request (see 37 CFR 1.114)")
        temp_utility = templates.filter(detailed_fee_category=detailed_fee_cat, appl_type=self.appl_type_utility)
        self.fundamental_us_test(templates=temp_utility,
                                 detailed_fee_category=detailed_fee_cat,
                                 appl_type=self.appl_type_utility)

        detailed_fee_cat = DetailedFeeCategory.objects.get(
            country=country_us,
            name="Processing fee, except in provisional applications")
        temp_utility = templates.filter(detailed_fee_category=detailed_fee_cat, appl_type=self.appl_type_utility)
        self.fundamental_us_test(templates=temp_utility,
                                 detailed_fee_category=detailed_fee_cat,
                                 appl_type=self.appl_type_utility)

    def test_pct_and_utility(self, detailed_fee_cat, templates):
        temp_utility = templates.filter(detailed_fee_category=detailed_fee_cat, appl_type=self.appl_type_utility)
        temp_pct = templates.filter(detailed_fee_category=detailed_fee_cat, appl_type=self.appl_type_pct)
        self.fundamental_us_test(templates=temp_utility,
                                 detailed_fee_category=detailed_fee_cat,
                                 appl_type=self.appl_type_utility)
        self.fundamental_us_test(templates=temp_pct,
                                 detailed_fee_category=detailed_fee_cat,
                                 appl_type=self.appl_type_utility)

    def fundamental_us_test(self, templates, appl_type, detailed_fee_category):
        temp_utility = templates.filter(detailed_fee_category=detailed_fee_category, appl_type=appl_type)
        len_micro = temp_utility.filter(conditions__condition_entity_size=self.entity_size_us_micro).count()
        if len_micro < 1:
            print('missing micro entity size ==> ', appl_type.application_type, ' ==> ', detailed_fee_category.name)
        elif len_micro > 1:
            print('Too Many micro entity size ==> ', appl_type.application_type, ' ==> ', detailed_fee_category.name,
                  ' count ', len_micro)
        len_small = temp_utility.filter(conditions__condition_entity_size=self.entity_size_us_small).count()
        if len_small < 1:
            print('missing small entity size ==> ', appl_type.application_type, ' ==> ', detailed_fee_category.name)
        elif len_small > 1:
            print('Too Many small entity size ==> ', appl_type.application_type, ' ==> ', detailed_fee_category.name,
                  ' count ', len_small)

        len_default = temp_utility.filter(conditions__condition_entity_size=self.entity_size_us_default).count()
        if len_default < 1:
            print('missing default entity size ==> ', appl_type.application_type, ' ==> ', detailed_fee_category.name)
        elif len_default > 1:
            print('Too Many small entity size ==> ', appl_type.application_type, ' ==> ', detailed_fee_category.name,
                  ' count ', len_default)
