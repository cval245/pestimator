from django.core.management.base import BaseCommand

from characteristics.models import ApplType, Country, DetailedFeeCategory, EntitySize
from estimation.models import AllowanceEstTemplate, FilingEstimateTemplate, IssueEstTemplate, OAEstimateTemplate, \
    PublicationEstTemplate, \
    RequestExamEstTemplate, USOAEstimateTemplate


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
    total_list = []
    country_us = 0

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

        self.country_us = Country.objects.get(country='US')
        self.entity_size_us_micro = EntitySize.objects.get(country=self.country_us, entity_size='micro')
        self.entity_size_us_small = EntitySize.objects.get(country=self.country_us, entity_size='small')
        self.entity_size_us_default = EntitySize.objects.get(country=self.country_us, entity_size='default')

        self.test_all()
        self.stdout.write(self.style.SUCCESS('Successfully ran run_estimation_data_test'))

    def test_all(self):

        # countries = Country.objects.filter(active_bool=True)
        countries = Country.objects.all()
        for country in countries:
            temp_list = []
            templates = list(FilingEstimateTemplate.objects.filter(country=country).select_related())
            templates += list(PublicationEstTemplate.objects.filter(country=country).select_related())
            templates += list(RequestExamEstTemplate.objects.filter(country=country).select_related())
            if country == self.country_us:
                templates += list(USOAEstimateTemplate.objects.filter(country=country).select_related())
            else:
                templates += list(OAEstimateTemplate.objects.filter(country=country).select_related())
            templates += list(AllowanceEstTemplate.objects.filter(country=country).select_related())
            templates += list(IssueEstTemplate.objects.filter(country=country).select_related())

            temp_list = self.test_templates(country=country, templates=templates, temp_list=temp_list)

            country_obj = {'country': country}
            country_obj['country_total'] = temp_list
            self.total_list.append(country_obj)

        for item in self.total_list:
            if len(item['country_total']) > 1:
                print('\n==================================================================')
                print('country ', item['country'].long_name)
                for x in item['country_total']:
                    print(x['name'])

    def test_templates(self, country, templates, temp_list):
        country_template_list = []
        entity_sizes = EntitySize.objects.filter(country=country)
        entity_sizes = list(entity_sizes)
        for applType in country.available_appl_types.all():
            det_cats = DetailedFeeCategory.objects.filter(country=country, appl_types=applType)
            det_cats_absent = DetailedFeeCategory.objects.filter(country=country).exclude(appl_types=applType)
            templates_appltype_filtered = [x for x in templates if x.appl_type == applType]
            for temp in templates_appltype_filtered:
                if temp.detailed_fee_category in det_cats_absent:
                    name = 'Wrong Category ==> ' + applType.application_type + ' ==> ' + temp.detailed_fee_category.name
                    country_template_list.append({'name': name, 'detailed_fee_category': temp.detailed_fee_category})

            if len(entity_sizes) > 0:
                for category in det_cats:
                    for entity_size in entity_sizes:
                        temp_filtered = [x for x in templates_appltype_filtered if x.detailed_fee_category == category]
                        self.fundamental_entity_size_test(templates=temp_filtered,
                                                          detailed_fee_category=category,
                                                          appl_type=applType,
                                                          country_total_list=country_template_list,
                                                          entity_size=entity_size)
            else:
                for category in det_cats:
                    temp_filtered = [x for x in templates_appltype_filtered if x.detailed_fee_category == category]
                    self.fundamental_test(templates=temp_filtered,
                                          detailed_fee_category=category,
                                          appl_type=applType,
                                          country_total_list=country_template_list,
                                          temp_list=temp_list)
        return country_template_list

    def fundamental_test(self, templates, appl_type, detailed_fee_category, country_total_list, temp_list):
        len_temp = len(templates)
        if len_temp < 1:
            name = 'missing  ==> ' + appl_type.application_type + ' ==> ' + detailed_fee_category.name
            country_total_list.append({'name': name, 'detailed_fee_category': detailed_fee_category})
        elif len_temp > 1:
            name = 'Too Many  ==> ' + appl_type.application_type + ' ==> ' + detailed_fee_category.name + ' count ' + str(
                len_temp)
            country_total_list.append({'name': name, 'detailed_fee_category': detailed_fee_category})

    def fundamental_entity_size_test(self, templates, appl_type, detailed_fee_category, country_total_list,
                                     entity_size):
        temp_filtered = [x for x in templates if x.conditions.condition_entity_size_id is None]
        len_fil = len(temp_filtered)
        len_total = len(templates)
        if len_fil == 1 and len_total == 1:
            return
        temp_filtered = [x for x in templates if x.conditions.condition_entity_size_id == entity_size.id]
        len_micro = len(temp_filtered)
        if len_micro < 1:
            name = 'missing ' + entity_size.entity_size + ' entity size ==> ' + appl_type.application_type + ' ==> ' + detailed_fee_category.name
            country_total_list.append({'name': name, 'detailed_fee_category': detailed_fee_category})
        elif len_micro > 1:
            name = 'Too Many' + entity_size.entity_size + ' entity size ==> ' + appl_type.application_type + ' ==> ' + detailed_fee_category.name + ' count ' + str(
                len_micro)
            country_total_list.append({'name': name, 'detailed_fee_category': detailed_fee_category})

        # temp_filtered = [x for x in templates if x.conditions.condition_entity_size == self.entity_size_us_small]
        # len_small = len(temp_filtered)
        # if len_small < 1:
        #     name = 'missing small entity size ==> ' + appl_type.application_type + ' ==> ' + detailed_fee_category.name
        #     country_total_list.append({'name': name, 'detailed_fee_category': detailed_fee_category})
        # elif len_small > 1:
        #     name = 'Too Many small entity size ==> ' + appl_type.application_type + ' ==> ' + detailed_fee_category.name + ' count ' + str(
        #         len_micro)
        #     country_total_list.append({'name': name, 'detailed_fee_category': detailed_fee_category})
        #
        # temp_filtered = [x for x in templates if x.conditions.condition_entity_size == self.entity_size_us_default]
        # len_default = len(temp_filtered)
        # if len_default < 1:
        #     name = 'missing default entity size ==> ' + appl_type.application_type + ' ==> ' + detailed_fee_category.name
        #     country_total_list.append({'name': name, 'detailed_fee_category': detailed_fee_category})
        # elif len_default > 1:
        #     name = 'Too Many default entity size ==> ' + appl_type.application_type + ' ==> ' + detailed_fee_category.name + ' count ' + str(
        #         len_default)
        #     country_total_list.append({'name': name, 'detailed_fee_category': detailed_fee_category})
