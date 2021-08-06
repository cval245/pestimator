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
