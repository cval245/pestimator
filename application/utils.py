from dateutil.relativedelta import relativedelta

from characteristics.models import ApplType


def convert_class_applType(appl):
    if hasattr(appl, 'baseutilityapplication'):
        baseAppl = appl.baseutilityapplication
        if hasattr(baseAppl, 'epapplication'):
            return ApplType.objects.get(application_type='ep')
        else:
            return ApplType.objects.get(application_type='utility')
    elif hasattr(appl, 'pctapplication'):
        return ApplType.objects.get(application_type='pct')
    elif hasattr(appl, 'provapplication'):
        return ApplType.objects.get(application_type='prov')
    elif hasattr(appl, 'usutilityapplication'):
        return ApplType.objects.get(application_type='utility')
    elif hasattr(appl, 'epvalidationapplication'):
        return ApplType.objects.get(application_type='epvalidation')


def get_date_of_expiry(application):
    appl = application
    date_of_origin = application.date_filing
    while (appl != None):
        if (convert_class_applType(appl) != ApplType.objects.get(application_type='prov')):
            date_of_origin = appl.date_filing
            # get the date
        else:
            break
        appl = appl.prior_appl
    date_of_expiry = date_of_origin + relativedelta(years=20)
    return date_of_expiry
