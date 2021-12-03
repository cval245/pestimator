from dateutil.relativedelta import relativedelta

from characteristics.enums import ApplTypes
from characteristics.models import ApplType


def convert_class_applType(appl):
    if hasattr(appl, 'baseutilityapplication'):
        baseAppl = appl.baseutilityapplication
        if hasattr(baseAppl, 'epapplication'):
            return ApplType.objects.get_name_from_enum(ApplTypes.EP)
        else:
            return ApplType.objects.get_name_from_enum(ApplTypes.UTILITY)
    elif hasattr(appl, 'pctapplication'):
        return ApplType.objects.get_name_from_enum(ApplTypes.PCT)
    elif hasattr(appl, 'provapplication'):
        return ApplType.objects.get_name_from_enum(ApplTypes.PROV)
    elif hasattr(appl, 'usutilityapplication'):
        return ApplType.objects.get_name_from_enum(ApplTypes.UTILITY)
    elif hasattr(appl, 'epvalidationapplication'):
        return ApplType.objects.get_name_from_enum(ApplTypes.EP_VALIDATION)


def get_date_of_expiry(application):
    appl = application
    date_of_origin = application.date_filing
    while appl is not None:
        if convert_class_applType(appl) != ApplType.objects.get_name_from_enum(ApplTypes.PROV):
            date_of_origin = appl.date_filing
            # get the date
        else:
            break
        appl = appl.prior_appl
    date_of_expiry = date_of_origin + relativedelta(years=20)
    return date_of_expiry
