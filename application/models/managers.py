from django.db import models

# class ApplManager(PolymorphicManager):
from famform.models import PCTApplOptions


class ApplManager(models.Manager):

    def create_full(self, options, user, family_id):
        return self.create_correct_appl(options, user, family_id)

    def generate_appl(self, options, user, family_id):
        applDetails = options.details
        applDetails.pk = None
        applDetails.save()
        prev_appl = None
        if (options.prev_appl_options):
            prev_appl = options.prev_appl_options.baseapplication

        appl = self.create(user=user, title=options.title,
                           date_filing=options.date_filing,
                           family_id=family_id,
                           country=options.country,
                           details=applDetails,
                           appl_option=options,
                           prior_appl=prev_appl)
        appl.generate_dates(options)
        return appl

    def generate_pct_appl(self, options, user, family_id):
        applDetails = options.details
        applDetails.pk = None
        applDetails.save()
        prev_appl = None
        if (options.prev_appl_options):
            prev_appl = options.prev_appl_options.baseapplication

        appl = self.create(user=user,
                           title=options.title,
                           date_filing=options.date_filing,
                           family_id=family_id,
                           country=options.country,
                           isa_country=options.isa_country,
                           details=applDetails,
                           appl_option=options,
                           prior_appl=prev_appl)
        appl.generate_dates(options)
        return appl

    def create_correct_appl(self, options, user, family_id):

        if (options.appl_type.application_type == 'prov'):
            # create prov
            from application.models import ProvApplication
            return ProvApplication.objects.generate_appl(options=options, user=user, family_id=family_id)
        elif (options.appl_type.application_type == 'pct'):
            # create pct
            from application.models import PCTApplication
            pct_options = PCTApplOptions.objects.get(apploptions_ptr_id=options.id)
            return PCTApplication.objects.generate_pct_appl(options=pct_options, user=user, family_id=family_id)
        elif (options.appl_type.application_type == 'utility'):
            # create utility
            if options.country.country == 'US':
                # US Utility Application
                from application.models import USUtilityApplication
                return USUtilityApplication.objects.generate_appl(options=options, user=user, family_id=family_id)
            else:
                # Generic Utility Application
                from application.models import BaseUtilityApplication
                return BaseUtilityApplication.objects.generate_appl(options=options, user=user, family_id=family_id)
        elif (options.appl_type.application_type == 'ep'):
            from application.models import EPApplication
            return EPApplication.objects.generate_appl(options=options, user=user, family_id=family_id)
        elif (options.appl_type.application_type == 'epvalidation'):
            from application.models.epValidationApplication import EPValidationApplication
            return EPValidationApplication.objects.generate_appl(options=options, user=user, family_id=family_id)
