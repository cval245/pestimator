from django.db.models import Q
# take templates and then filter using application details

def filter_conditions(templates, appl_details):
    temp_one = _filter_claims(templates, appl_details)
    temp_two = _filter_pages(temp_one, appl_details)
    temp_three = _filter_drawings(temp_two, appl_details)
    temp_four = _filter_entity_size(temp_three, appl_details)
    final_temps = temp_four
    return final_temps

def _filter_claims(templates, appl_details):
    # remove templates that exceed conditions
    templates = templates.exclude(
        conditions__condition_claims_min__gte=
    appl_details.num_claims)

    templates = templates.exclude(
        conditions__condition_claims_max__lte=
        appl_details.num_claims)
    return templates

def _filter_pages(templates, appl_details):
    templates = templates.exclude(
        conditions__condition_pages_min__gte=
    appl_details.num_pages)

    templates = templates.exclude(
        conditions__condition_pages_max__lte=
        appl_details.num_pages)
    return templates

def _filter_drawings(templates, appl_details):
    templates = templates.exclude(
        conditions__condition_drawings_min__gte=
        appl_details.num_pages)

    templates = templates.exclude(
        conditions__condition_drawings_max__lte=
        appl_details.num_pages)
    return templates

def _filter_entity_size(templates, appl_details):
    templates = templates.filter(
        Q(conditions__condition_entity_size=appl_details.entity_size)
        | Q(conditions__condition_entity_size=None))
    return templates
