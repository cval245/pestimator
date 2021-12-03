from django.db import models

from characteristics.enums import TranslationRequirements, ApplTypes


class TranslationImplementedPseudoEnumManager(models.Manager):

    def get_name_from_enum(self, enum):
        if enum is TranslationRequirements.FULL_TRANSLATION:
            return self.get(name='full translation')
        elif enum is TranslationRequirements.NO_TRANSLATION:
            return self.get(name='no translation')


class ApplTypesEnumManager(models.Manager):

    def get_name_from_enum(self, enum):
        if enum is ApplTypes.UTILITY:
            return self.get(application_type='utility')
        elif enum is ApplTypes.PCT_NATIONAL_PHASE:
            return self.get(application_type='nationalphase')
        elif enum is ApplTypes.EP_VALIDATION:
            return self.get(application_type='epvalidation')
        elif enum is ApplTypes.PCT:
            return self.get(application_type='pct')
        elif enum is ApplTypes.EP:
            return self.get(application_type='ep')
        elif enum is ApplTypes.PROV:
            return self.get(application_type='prov')
        else:
            # default to utility
            return self.get(application_type='utility')
