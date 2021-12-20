from datetime import datetime

from django.test import TestCase

# Create your tests here.
from django.test import TestCase

from characteristics.factories import ApplTypeFactory, CountryFactory
from . import factories
from .factories import DefaultFilingTransformFactory, CustomFilingTransformFactory, TransComplexTimeFactory
from .models import CustomFilingTransform


class TransformManagerTest(TestCase):

    def test_calc_filing_date_for_appl_option_returns_dfltFilingTransform(self):
        appl_type = ApplTypeFactory(utility=True)
        appl_type_pct = ApplTypeFactory(pct=True)
        country = CountryFactory(CN=True)
        country_us = CountryFactory(US=True)
        prev_appl_type = None
        prev_date = datetime(2020, 5, 25)
        prev_appl_option = None
        dflFilTrans = DefaultFilingTransformFactory(appl_type=appl_type)
        cstmFilTrans_diff_appl_type = CustomFilingTransformFactory(country=country, appl_type=appl_type_pct)
        cstmFilTrans_diff_country = CustomFilingTransformFactory(country=country_us, appl_type=appl_type)
        date_filing = CustomFilingTransform.objects.calc_filing_date_for_appl_option(
            appl_type=appl_type,
            country=country,
            prev_appl_type=prev_appl_type,
            prev_date=prev_date,
            prev_appl_option=prev_appl_option
        )
        self.assertEquals((dflFilTrans.date_diff + prev_date), date_filing)

    def test_calc_filing_date_for_appl_option_returns_correct_cstm_filing_date(self):
        appl_type = ApplTypeFactory(utility=True)
        appl_type_pct = ApplTypeFactory(pct=True)
        country = CountryFactory(CN=True)
        country_us = CountryFactory(US=True)
        prev_appl_type = None
        prev_date = datetime(2020, 5, 25)
        prev_appl_option = None
        dflFilTrans = DefaultFilingTransformFactory(appl_type=appl_type)
        cstmFilTrans = CustomFilingTransformFactory(country=country, appl_type=appl_type)
        cstmFilTrans_diff_appl_type = CustomFilingTransformFactory(country=country, appl_type=appl_type_pct)
        cstmFilTrans_diff_country = CustomFilingTransformFactory(country=country_us, appl_type=appl_type)
        date_filing = CustomFilingTransform.objects.calc_filing_date_for_appl_option(
            appl_type=appl_type,
            country=country,
            prev_appl_type=prev_appl_type,
            prev_date=prev_date,
            prev_appl_option=prev_appl_option
        )
        self.assertEquals((cstmFilTrans.date_diff + prev_date), date_filing)

    def test_calc_filing_date_for_appl_option_returns_correct_complex_time_conditions(self):
        appl_type = ApplTypeFactory(utility=True)
        appl_type_pct = ApplTypeFactory(pct=True)
        country = CountryFactory(CN=True)
        country_us = CountryFactory(US=True)
        from famform.factories import ApplOptionsFactory
        first_appl_option = ApplOptionsFactory(date_filing=datetime(2020, 5, 25))
        prev_appl_option = ApplOptionsFactory(prev_appl_options=first_appl_option,
                                              date_filing=datetime(2022, 6, 4))
        prev_appl_type = None
        prev_date = prev_appl_option.date_filing
        dflFilTrans = DefaultFilingTransformFactory(appl_type=appl_type)
        cstmFilTrans = CustomFilingTransformFactory(country=country, appl_type=appl_type,
                                                    trans_complex_time_condition=TransComplexTimeFactory())

        date_filing = CustomFilingTransform.objects.calc_filing_date_for_appl_option(
            appl_type=appl_type,
            country=country,
            prev_appl_type=prev_appl_type,
            prev_date=prev_date,
            prev_appl_option=prev_appl_option
        )
        self.assertEquals((cstmFilTrans.date_diff + first_appl_option.date_filing), date_filing)


class TransComplexTimeTest(TestCase):

    def test_calc_complex_time_conditions(self):
        appl_type = ApplTypeFactory(utility=True)
        country = CountryFactory(CN=True)
        from famform.factories import ApplOptionsFactory
        first_appl_option = ApplOptionsFactory(date_filing=datetime(2020, 5, 25))
        prev_appl_option = ApplOptionsFactory(prev_appl_options=first_appl_option,
                                              date_filing=datetime(2022, 6, 4))
        prev_date = prev_appl_option.date_filing
        cstmFilTrans = CustomFilingTransformFactory(country=country, appl_type=appl_type,
                                                    trans_complex_time_condition=TransComplexTimeFactory())
        trans_complex = TransComplexTimeFactory(name='from priority date')
        date_filing = trans_complex.calc_complex_time_conditions(
            prev_appl_option=prev_appl_option,
            prev_date=prev_date,
            filing_transform=cstmFilTrans)

        self.assertEquals((cstmFilTrans.date_diff + first_appl_option.date_filing), date_filing)

    def test_calc_from_priority_date_returns_from_priority_date_two_appls_prior(self):
        appl_type = ApplTypeFactory(utility=True)
        country = CountryFactory(CN=True)
        from famform.factories import ApplOptionsFactory
        first_appl_option = ApplOptionsFactory(date_filing=datetime(2020, 5, 25))
        prev_appl_option = ApplOptionsFactory(prev_appl_options=first_appl_option,
                                              date_filing=datetime(2022, 6, 4))
        prev_date = prev_appl_option.date_filing
        cstmFilTrans = CustomFilingTransformFactory(country=country, appl_type=appl_type,
                                                    trans_complex_time_condition=TransComplexTimeFactory())
        trans_complex = TransComplexTimeFactory(name='from priority date')
        date_filing = trans_complex.calc_from_priority_date(prev_appl_option=prev_appl_option,
                                                            prev_date=prev_date,
                                                            filing_transform=cstmFilTrans)

        self.assertEquals((cstmFilTrans.date_diff + first_appl_option.date_filing), date_filing)

    def test_calc_from_priority_date_returns_from_priority_date_three_appls_prior(self):
        appl_type = ApplTypeFactory(utility=True)
        country = CountryFactory(CN=True)
        from famform.factories import ApplOptionsFactory
        first_appl_option = ApplOptionsFactory(date_filing=datetime(2020, 5, 25))
        second_appl_option = ApplOptionsFactory(date_filing=datetime(2020, 5, 25))
        prev_appl_option = ApplOptionsFactory(prev_appl_options=second_appl_option,
                                              date_filing=datetime(2022, 6, 4))
        prev_date = prev_appl_option.date_filing
        cstmFilTrans = CustomFilingTransformFactory(country=country, appl_type=appl_type,
                                                    trans_complex_time_condition=TransComplexTimeFactory())
        trans_complex = TransComplexTimeFactory(name='from priority date')
        date_filing = trans_complex.calc_from_priority_date(prev_appl_option=prev_appl_option,
                                                            prev_date=prev_date,
                                                            filing_transform=cstmFilTrans)

        self.assertEquals((cstmFilTrans.date_diff + first_appl_option.date_filing), date_filing)

    def test_calc_from_priority_date_returns_from_priority_date_zero_appls_prior(self):
        appl_type = ApplTypeFactory(utility=True)
        country = CountryFactory(CN=True)
        prev_appl_option = None
        prev_date = datetime(2020, 1, 1)
        cstmFilTrans = CustomFilingTransformFactory(country=country, appl_type=appl_type,
                                                    trans_complex_time_condition=TransComplexTimeFactory())
        trans_complex = TransComplexTimeFactory(name='from priority date')
        date_filing = trans_complex.calc_from_priority_date(prev_appl_option=prev_appl_option,
                                                            prev_date=prev_date,
                                                            filing_transform=cstmFilTrans)

        self.assertEquals((cstmFilTrans.date_diff + prev_date), date_filing)
