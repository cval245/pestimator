from characteristics.models import ApplType
def convert_class_applType(appl):
    print('appl is', (appl))
    if hasattr(appl, 'baseutilityapplication'):
        return ApplType.objects.get(application_type='utility')
    elif hasattr(appl, 'pctapplication'):
        return ApplType.objects.get(application_type='pct')
    elif hasattr(appl, 'provapplication'):
        return ApplType.objects.get(application_type='prov')
    elif hasattr(appl, 'usutilityapplication'):
        return ApplType.objects.get(application_type='utility')
