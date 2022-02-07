from django.core.management.base import BaseCommand, CommandError

# from polls.models import Question as Poll
from characteristics.models import ApplType, Country
from transform.models import AllowanceTransform, CountryOANum, CustomFilingTransform, IssueTransform, OATransform, \
    PublicationTransform, \
    RequestExaminationTransform, USOATransform


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def determine_exactly_one_present(self, selected_trans, appl_type, prev_appl_type, missing_arr, country):
        searched = [x for x in selected_trans if x.prev_appl_type == prev_appl_type]
        if len(searched) == 0:
            missing_arr.append({'country': country, 'appl_type': appl_type, 'prev_appl_type': prev_appl_type})
        elif len(searched) > 1:
            raise Exception('duplicate found', appl_type, 'prev_appl_type', prev_appl_type)
        return missing_arr

    def handle(self, *args, **options):
        countries = Country.objects.filter(active_bool=True).select_related()
        appl_type_utility = ApplType.objects.get(application_type='utility')
        appl_type_ep = ApplType.objects.get(application_type='ep')
        appl_type_pct = ApplType.objects.get(application_type='pct')
        appl_type_nationalphase = ApplType.objects.get(application_type='nationalphase')
        appl_type_prov = ApplType.objects.get(application_type='prov')
        appl_type_epvalid = ApplType.objects.get(application_type='epvalidation')

        self.detect_data_test_custom_filing_transforms(
            countries=countries,
            appl_type_utility=appl_type_utility,
            appl_type_nationalphase=appl_type_nationalphase,
            appl_type_ep=appl_type_ep,
            appl_type_prov=appl_type_prov,
            appl_type_pct=appl_type_pct,
            appl_type_epvalid=appl_type_epvalid)

        print('-------------')
        self.detect_data_test_publication_transforms(countries=countries, appl_type_prov=appl_type_prov)
        print('-------------')
        self.detect_data_test_allowance_transforms(countries=countries, appl_type_prov=appl_type_prov,
                                                   appl_type_pct=appl_type_pct)

        print('-------------')
        self.detect_data_test_issue_transforms(countries=countries, appl_type_prov=appl_type_prov,
                                               appl_type_pct=appl_type_pct, appl_type_ep=appl_type_ep)
        print('-------------')
        self.detect_data_test_request_examination_transforms(countries=countries, appl_type_prov=appl_type_prov,
                                                             appl_type_epvalid=appl_type_epvalid)
        print('-------------')
        self.detect_data_test_oa_transforms(countries=countries, appl_type_prov=appl_type_prov,
                                            appl_type_epvalid=appl_type_epvalid)
        print('-------------')
        self.detect_data_test_usoa_transforms(appl_type_prov=appl_type_prov, appl_type_epvalid=appl_type_epvalid,
                                              appl_type_ep=appl_type_ep)
        print('-------------')
        self.detect_data_test_country_oa_num(countries=countries, appl_type_prov=appl_type_prov,
                                             appl_type_epvalid=appl_type_epvalid)
        print('-------------')
        self.stdout.write(self.style.SUCCESS('Successfully ran datatests'))

    def detect_data_test_custom_filing_transforms(self, countries, appl_type_pct,
                                                  appl_type_prov, appl_type_epvalid,
                                                  appl_type_ep, appl_type_utility,
                                                  appl_type_nationalphase):
        for c in countries:
            trans = CustomFilingTransform.objects.filter(country=c)
            for appl_type in c.available_appl_types.all():
                self.has_all_prev_appl_types(
                    appl_type=appl_type,
                    appl_type_pct=appl_type_pct,
                    appl_type_prov=appl_type_prov,
                    appl_type_epvalid=appl_type_epvalid,
                    appl_type_ep=appl_type_ep,
                    appl_type_utility=appl_type_utility,
                    appl_type_nationalphase=appl_type_nationalphase,
                    trans=trans,
                    country=c)

    def detect_data(self, appl_type, country, missing_arr, trans):
        searched = [x for x in trans if x.appl_type == appl_type]
        if len(searched) == 0:
            missing_arr.append({'country': country, 'appl_type': appl_type})
        elif len(searched) > 1:
            for tr in country.available_appl_types.all():
                prev_searched = [x for x in searched if x.prev_appl_type == tr.prev_appl_type]
                if len(prev_searched) > 1:
                    raise Exception('duplicate found with prev_appl_type', appl_type, tr.prev_appl_type)

    def detect_data_test_issue_transforms(self, countries, appl_type_prov, appl_type_pct, appl_type_ep):
        missing_arr = []
        for country in countries:
            trans = IssueTransform.objects.filter(country=country)
            for appl_type in country.available_appl_types.all():
                if appl_type_prov != appl_type and appl_type_pct != appl_type and appl_type_ep != appl_type:
                    self.detect_data(appl_type=appl_type, country=country, missing_arr=missing_arr, trans=trans)

        for missing in missing_arr:
            print('IssueTransform missing ', missing['country'].long_name,
                  ', appl_type = ', missing['appl_type'].application_type)
        return missing_arr

    def detect_data_test_country_oa_num(self, countries, appl_type_prov, appl_type_epvalid):
        missing_arr = []
        for country in countries:
            trans = CountryOANum.objects.filter(country=country)
            for appl_type in country.available_appl_types.all():
                if appl_type_prov != appl_type and appl_type_epvalid != appl_type:
                    self.detect_data(appl_type=appl_type, country=country, missing_arr=missing_arr, trans=trans)

        for missing in missing_arr:
            print('CountryOANum missing ', missing['country'].long_name,
                  ', appl_type = ', missing['appl_type'].application_type)
        return missing_arr

    def detect_data_test_request_examination_transforms(self, countries, appl_type_prov, appl_type_epvalid):
        missing_arr = []
        for country in countries:
            trans = RequestExaminationTransform.objects.filter(country=country)
            for appl_type in country.available_appl_types.all():
                if appl_type_prov != appl_type and appl_type_epvalid != appl_type:
                    self.detect_data(appl_type=appl_type, country=country, missing_arr=missing_arr, trans=trans)

        for missing in missing_arr:
            print('RequestExamTransform missing ', missing['country'].long_name,
                  ', appl_type = ', missing['appl_type'].application_type)
        return missing_arr

    def detect_data_test_oa_transforms(self, countries, appl_type_prov, appl_type_epvalid):
        missing_arr = []
        for country in countries:
            trans = OATransform.objects.filter(country=country)
            for appl_type in country.available_appl_types.all():
                if appl_type_prov != appl_type and appl_type_epvalid != appl_type:
                    self.detect_data(appl_type=appl_type, country=country, missing_arr=missing_arr, trans=trans)

        for missing in missing_arr:
            print('OATransform missing ', missing['country'].long_name,
                  ', appl_type = ', missing['appl_type'].application_type)
        return missing_arr

    def detect_data_test_usoa_transforms(self, appl_type_prov, appl_type_epvalid, appl_type_ep):
        missing_arr = []
        country = Country.objects.get(country='US')
        trans = USOATransform.objects.filter(country=country)
        for appl_type in country.available_appl_types.all():
            if appl_type_prov != appl_type and appl_type_epvalid != appl_type and appl_type_ep != appl_type:
                self.detect_data(appl_type=appl_type, country=country, missing_arr=missing_arr, trans=trans)

        for missing in missing_arr:
            print('USOATransform missing ', missing['country'].long_name,
                  ', appl_type = ', missing['appl_type'].application_type)
        return missing_arr

    def detect_data_test_allowance_transforms(self, countries, appl_type_prov, appl_type_pct):
        missing_arr = []
        for country in countries:
            trans = AllowanceTransform.objects.filter(country=country)
            for appl_type in country.available_appl_types.all():
                if appl_type_prov != appl_type and appl_type_pct != appl_type:
                    self.detect_data(appl_type=appl_type, country=country, missing_arr=missing_arr, trans=trans)

        for missing in missing_arr:
            print('AllowTransform missing ', missing['country'].long_name,
                  ', appl_type = ', missing['appl_type'].application_type)
        return missing_arr

    def detect_data_test_publication_transforms(self, countries, appl_type_prov):
        missing_arr = []
        for country in countries:
            trans = PublicationTransform.objects.filter(country=country)
            for appl_type in country.available_appl_types.all():
                if appl_type_prov != appl_type:
                    self.detect_data(appl_type=appl_type, country=country, missing_arr=missing_arr, trans=trans)

        for missing in missing_arr:
            print('PublTransform missing ', missing['country'].long_name,
                  ', appl_type = ', missing['appl_type'].application_type)
        return missing_arr

    def has_all_prev_appl_types(self, appl_type, appl_type_pct, appl_type_utility,
                                appl_type_ep, appl_type_epvalid, appl_type_nationalphase,
                                appl_type_prov, trans, country):

        selected_trans = []
        for tran in trans:
            if tran.appl_type == appl_type:
                selected_trans.append(tran)

        missing_arr = []
        if appl_type == appl_type_epvalid:
            self.determine_exactly_one_present(selected_trans=selected_trans,
                                               appl_type=appl_type,
                                               prev_appl_type=appl_type_ep,
                                               missing_arr=missing_arr,
                                               country=country)
        elif appl_type == appl_type_nationalphase:
            self.determine_exactly_one_present(selected_trans=selected_trans,
                                               appl_type=appl_type,
                                               prev_appl_type=appl_type_pct,
                                               missing_arr=missing_arr,
                                               country=country)
        elif appl_type == appl_type_prov:
            self.determine_exactly_one_present(selected_trans=selected_trans,
                                               appl_type=appl_type,
                                               prev_appl_type=None,
                                               missing_arr=missing_arr,
                                               country=country)
        elif appl_type == appl_type_pct:
            self.determine_exactly_one_present(selected_trans=selected_trans,
                                               appl_type=appl_type,
                                               prev_appl_type=None,
                                               missing_arr=missing_arr,
                                               country=country)
            self.determine_exactly_one_present(selected_trans=selected_trans,
                                               appl_type=appl_type,
                                               prev_appl_type=appl_type_utility,
                                               missing_arr=missing_arr,
                                               country=country)
            self.determine_exactly_one_present(selected_trans=selected_trans,
                                               appl_type=appl_type,
                                               prev_appl_type=appl_type_ep,
                                               missing_arr=missing_arr,
                                               country=country)
            self.determine_exactly_one_present(selected_trans=selected_trans,
                                               appl_type=appl_type,
                                               prev_appl_type=appl_type_prov,
                                               missing_arr=missing_arr,
                                               country=country)
        else:
            self.determine_exactly_one_present(selected_trans=selected_trans,
                                               appl_type=appl_type,
                                               prev_appl_type=None,
                                               missing_arr=missing_arr,
                                               country=country)
            self.determine_exactly_one_present(selected_trans=selected_trans,
                                               appl_type=appl_type,
                                               prev_appl_type=appl_type_pct,
                                               missing_arr=missing_arr,
                                               country=country)
            self.determine_exactly_one_present(selected_trans=selected_trans,
                                               appl_type=appl_type,
                                               prev_appl_type=appl_type_utility,
                                               missing_arr=missing_arr,
                                               country=country)
            self.determine_exactly_one_present(selected_trans=selected_trans,
                                               appl_type=appl_type,
                                               prev_appl_type=appl_type_ep,
                                               missing_arr=missing_arr,
                                               country=country)
            self.determine_exactly_one_present(selected_trans=selected_trans,
                                               appl_type=appl_type,
                                               prev_appl_type=appl_type_prov,
                                               missing_arr=missing_arr,
                                               country=country)

        for missing in missing_arr:
            if missing['prev_appl_type']:
                prev_appl_type_display = missing['prev_appl_type'].application_type
            else:
                prev_appl_type_display = None
            print('CSTMFilTrans missing ', missing['country'].long_name,
                  ', appl_type = ', missing['appl_type'].application_type,
                  ', prev_appl_type = ', prev_appl_type_display)
        return missing_arr
