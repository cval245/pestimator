from datetime import date

from django.conf import settings
from django.db import models
from django.db.models import Max, Sum

from application.models import ApplDetails
from characteristics.enums import ApplTypes
from characteristics.models import ApplType, Country, EntitySize

from famform.models.PCTCountryCustomization import PCTCountryCustomization
from famform.models.AllowOptions import AllowOptions
from famform.models.EPCountryCustomization import EPCountryCustomization
from famform.models.FamOptions import FamOptions
from famform.models.OAOptions import OAOptions
from famform.models.ParisCountryCustomization import ParisCountryCustomization
from famform.models.CustomApplOptions import CustomApplOptions
from famform.models.EPMethodCustomization import EPMethodCustomization
from famform.models.PCTMethodCustomization import PCTMethodCustomization
from family.models import Family


class FamEstFormData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    family = models.OneToOneField(Family, on_delete=models.CASCADE)
    unique_display_no = models.IntegerField()
    init_appl_filing_date = models.DateField(default=date(2020, 1, 1))
    init_appl_country = models.ForeignKey(Country,
                                          on_delete=models.CASCADE,
                                          related_name='init_country')
    init_appl_type = models.ForeignKey(ApplType, on_delete=models.CASCADE)
    init_appl_details = models.OneToOneField(ApplDetails, on_delete=models.CASCADE, null=False)
    init_appl_options = models.OneToOneField(CustomApplOptions, on_delete=models.CASCADE, null=False)

    date_created = models.DateTimeField(auto_now_add=True)
    pct_method = models.BooleanField(default=False)
    pct_method_customization = models.OneToOneField(PCTMethodCustomization,
                                                    on_delete=models.CASCADE)
    pct_country = models.ForeignKey(Country,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    related_name='pct_country')
    isa_country = models.ForeignKey(Country,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    related_name='isa_country')

    isa_entity_size = models.ForeignKey(EntitySize,
                                        on_delete=models.CASCADE,
                                        null=True)

    pct_countries = models.ManyToManyField(Country,
                                           through='PCTCountryCustomization',
                                           through_fields=('fam_est_form_data', 'country'),
                                           related_name='pct_countries')  # pct appl countries

    ep_method = models.BooleanField(default=False)
    ep_method_customization = models.OneToOneField(EPMethodCustomization,
                                                   on_delete=models.CASCADE)
    ep_countries = models.ManyToManyField(Country,
                                          through='EPCountryCustomization',
                                          through_fields=('fam_est_form_data', 'country'),
                                          related_name='ep_countries')  # utility appl countries

    paris_countries = models.ManyToManyField(Country,
                                             through='ParisCountryCustomization',
                                             through_fields=('fam_est_form_data', 'country'),
                                             related_name='paris_countries')  # utility appl countries

    def get_paris_countries(self):
        return ParisCountryCustomization.objects.filter(fam_est_form_data=self)

    def get_pct_countries(self):
        return PCTCountryCustomization.objects.filter(fam_est_form_data=self)

    def get_ep_countries(self):
        return EPCountryCustomization.objects.filter(fam_est_form_data=self)

    # generate route
    def save(self, *args, **kwargs):
        if self.pk is None:
            # get all pervious families by user
            max_udn = FamEstFormData.objects.filter(user=self.user).aggregate(max_udn=Max('unique_display_no'))
            if max_udn['max_udn'] is not None:
                self.unique_display_no = max_udn['max_udn'] + 1
            else:
                self.unique_display_no = 1
        return super(FamEstFormData, self).save(*args, **kwargs)

    def generate_family_options(self):
        famOptions = FamOptions.objects.create(family=self.family)
        # !important the ep application must be added in either first appl
        # or paris appls or pct appls
        # todo handle multiple instead of just first optionally add for user
        # language = self.init_appl_country.available_languages.get(default=True, appl_type=self.init_appl_type)

        applDetails = self.init_appl_details

        init_appl_option = self.parse_first_appl_stage(famOptions, applDetails)
        if self.init_appl_type.get_enum() is not ApplTypes.PCT and self.pct_method is True:
            self.parse_international_stage(famOptions=famOptions,
                                           applDetails=applDetails,
                                           prevApplOption=init_appl_option,
                                           firstApplBool=False,
                                           prevDate=init_appl_option.date_filing,
                                           prevApplType=self.init_appl_type)

        self.parse_paris_stage(famOptions=famOptions, applDetails=applDetails,
                               prevApplOption=init_appl_option)
        self.family.create_appls(famOptions)

    def parse_first_appl_stage(self, famOptions, applDetails):
        # take in first appl
        # if ep, then commence
        # parse_ep_stage()
        if self.init_appl_type.get_enum() is ApplTypes.PCT:
            first_appl_option = self.parse_international_stage(famOptions=famOptions,
                                                               applDetails=applDetails,
                                                               prevApplOption=None,
                                                               prevDate=self.init_appl_filing_date,
                                                               prevApplType=self.init_appl_type,
                                                               firstApplBool=True)

        elif self.init_appl_type.get_enum() is ApplTypes.EP:
            first_appl_option = self.parse_ep_stage(famOptions=famOptions,
                                                    applDetails=applDetails,
                                                    prevApplOption=None,
                                                    firstApplBool=True,
                                                    prev_date=self.init_appl_filing_date,
                                                    prev_appl_type=self.init_appl_type,
                                                    )

        else:
            first_appl_option = famOptions.generate_appl(details=applDetails,
                                                         custom_details=None,  # by defn same as first
                                                         custom_options=self.init_appl_options,
                                                         country=self.init_appl_country,
                                                         appl_type=self.init_appl_type,
                                                         prev_appl_type=None,
                                                         prev_date=self.init_appl_filing_date,
                                                         first_appl_bool=True,
                                                         prev_appl_option=None)
        return first_appl_option

    def parse_international_stage(self, famOptions, applDetails,
                                  prevApplOption, prevDate, prevApplType, firstApplBool):
        if self.pct_method is True:
            # take in pct_countries
            # check if ep stage is also checked
            # check if first appl was ep
            # if yes and then no, create ep option
            # if ep first was checked then get nothing
            pct_valid_type = ApplType.objects.get_name_from_enum(ApplTypes.PCT)
            custom_details = None
            custom_options = None
            if self.pct_method_customization is not None:
                custom_details = self.pct_method_customization.custom_appl_details
                custom_options = self.pct_method_customization.custom_appl_options
            pct_appl_option = famOptions.generate_pct_appl(details=applDetails,
                                                           custom_details=custom_details,
                                                           custom_options=custom_options,
                                                           country=self.pct_country,
                                                           isa_country=self.isa_country,
                                                           isa_entity_size=self.isa_entity_size,
                                                           prev_appl_type=prevApplType,
                                                           prev_date=prevDate,
                                                           first_appl_bool=firstApplBool,
                                                           prev_appl_option=prevApplOption)

            utility_type = ApplType.objects.get_name_from_enum(ApplTypes.UTILITY)
            for pct_country_customization in self.pct_countries.through.objects.filter(fam_est_form_data_id=self.id):
                if (pct_country_customization.country == Country.objects.get(country='EP')
                        and self.ep_method is True
                        and self.init_appl_type.get_enum() is not ApplTypes.EP):
                    self.parse_ep_stage(famOptions=famOptions,
                                        applDetails=applDetails,
                                        prevApplOption=pct_appl_option,
                                        firstApplBool=False,
                                        prev_date=pct_appl_option.date_filing,
                                        prev_appl_type=pct_valid_type)
                else:
                    custom_details = pct_country_customization.custom_appl_details
                    custom_options = pct_country_customization.custom_appl_options
                    famOptions.generate_appl(details=applDetails,
                                             custom_details=custom_details,
                                             country=pct_country_customization.country,
                                             appl_type=utility_type,
                                             prev_appl_type=pct_valid_type,
                                             prev_date=pct_appl_option.date_filing,
                                             first_appl_bool=False,
                                             prev_appl_option=pct_appl_option,
                                             custom_options=custom_options)
            return pct_appl_option
        return prevApplOption

    def parse_ep_stage(self, famOptions, applDetails, prevApplOption, firstApplBool, prev_date, prev_appl_type):
        # take in ep_countries
        # check if pct countries apply
        if self.ep_method is True:
            ep_type = ApplType.objects.get_name_from_enum(ApplTypes.EP)
            ep_country = Country.objects.get(country='EP')
            custom_details = None
            custom_options = None
            if self.ep_method_customization is not None:
                custom_details = self.ep_method_customization.custom_appl_details
                custom_options = self.ep_method_customization.custom_appl_options
            ep_appl_option = famOptions.generate_appl(details=applDetails,
                                                      custom_details=custom_details,
                                                      custom_options=custom_options,
                                                      country=ep_country,
                                                      appl_type=ep_type,
                                                      prev_appl_type=prev_appl_type,
                                                      prev_date=prev_date,
                                                      first_appl_bool=firstApplBool,
                                                      prev_appl_option=prevApplOption)
            self.parse_ep_validation_stage(famOptions=famOptions,
                                           applDetails=applDetails,
                                           prevApplOption=ep_appl_option)
            return ep_appl_option

    def parse_ep_validation_stage(self, famOptions, applDetails, prevApplOption):

        ep_valid_type = ApplType.objects.get_name_from_enum(ApplTypes.EP_VALIDATION)
        oa_diff = OAOptions.objects.filter(appl=prevApplOption).aggregate(date_diff=Sum('date_diff'))['date_diff']
        allow_diff = AllowOptions.objects.get(appl=prevApplOption).date_diff
        ep_prev_date = prevApplOption.date_filing + oa_diff + allow_diff
        for ep_country_customization in self.ep_countries.through.objects.filter(fam_est_form_data_id=self.id):
            custom_details = ep_country_customization.custom_appl_details
            custom_options = ep_country_customization.custom_appl_options
            famOptions.generate_appl(details=applDetails,
                                     custom_details=custom_details,
                                     custom_options=custom_options,
                                     country=ep_country_customization.country,
                                     appl_type=ep_valid_type,
                                     prev_appl_type=prevApplOption.appl_type,
                                     prev_date=ep_prev_date,
                                     first_appl_bool=False,
                                     prev_appl_option=prevApplOption)
        return prevApplOption

    def parse_paris_stage(self, famOptions, applDetails, prevApplOption):
        # take in paris_countries
        utility_appl = ApplType.objects.get_name_from_enum(ApplTypes.UTILITY)
        for paris_country_customization in self.paris_countries.through.objects.filter(fam_est_form_data_id=self.id):
            custom_details = paris_country_customization.custom_appl_details
            custom_options = paris_country_customization.custom_appl_options
            if (paris_country_customization.country == Country.objects.get(country='EP')
                    and self.ep_method is True):
                self.parse_ep_stage(famOptions=famOptions,
                                    applDetails=applDetails,
                                    prevApplOption=prevApplOption,
                                    firstApplBool=False,
                                    prev_date=prevApplOption.date_filing,
                                    prev_appl_type=prevApplOption.appl_type,
                                    )
            else:
                famOptions.generate_appl(details=applDetails,
                                         custom_details=custom_details,
                                         custom_options=custom_options,
                                         country=paris_country_customization.country,
                                         appl_type=utility_appl,
                                         prev_appl_type=prevApplOption.appl_type,
                                         prev_date=prevApplOption.date_filing,
                                         first_appl_bool=False,
                                         prev_appl_option=prevApplOption)
        return prevApplOption
