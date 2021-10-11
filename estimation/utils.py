from dateutil.relativedelta import relativedelta
from django.db.models import Q
from application import utils as appl_utils
# take templates and then filter using application details
from characteristics.models import ApplType
from famform.models import OAOptions, AllowOptions


def filter_conditions(templates, application):
    appl_details = application.details
    temp_one = _filter_claims(templates, appl_details)
    temp_two = _filter_pages(temp_one, appl_details)
    temp_three = _filter_drawings(temp_two, appl_details)
    temp_four = _filter_entity_size(temp_three, appl_details)
    temp_five = _filter_indep_claims(temp_four, appl_details)
    temp_six = _filter_annual_prosecution_fee(temp_five, application)
    temp_seven = _filter_prior_appl_pct(temp_six, application)
    temp_eight = _filter_prior_appl_pct_same_country(temp_seven, application)
    temp_nine = _filter_fee_from_prior_appl_filing_date_and_excluding_overlapping_dates(temp_eight, application)
    final_temps = temp_nine
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


def _filter_indep_claims(templates, appl_details):
    # remove templates that exceed conditions
    templates = templates.exclude(
        conditions__condition_indep_claims_min__gte=
        appl_details.num_claims)

    templates = templates.exclude(
        conditions__condition_indep_claims_max__lte=
        appl_details.num_claims)
    return templates


def _filter_pages(templates, appl_details):
    templates = templates.exclude(
        conditions__condition_pages_min__gte=
        appl_details.total_pages)

    templates = templates.exclude(
        conditions__condition_pages_max__lte=
        appl_details.total_pages)
    return templates


def _filter_desc_pages(templates, appl_details):
    templates = templates.exclude(
        conditions__condition_pages_desc_min__gte=
        appl_details.num_pages_description)

    templates = templates.exclude(
        conditions__condition_pages_desc_max__lte=
        appl_details.num_pages_description)

    return templates


def _filter_drawings(templates, appl_details):
    templates = templates.exclude(
        conditions__condition_drawings_min__gte=
        appl_details.num_drawings)

    templates = templates.exclude(
        conditions__condition_drawings_max__lte=
        appl_details.num_drawings)
    return templates


def _filter_entity_size(templates, appl_details):
    templates = templates.filter(
        Q(conditions__condition_entity_size=appl_details.entity_size)
        | Q(conditions__condition_entity_size=None))
    return templates


def _filter_annual_prosecution_fee(templates, application):
    # use applOption to retrieve allowance_option
    appl_option = application.appl_option
    # sum Delta Time between filing and allowance_option
    delta_t = relativedelta(days=0)

    if (AllowOptions.objects.filter(appl=appl_option).exists()):
        allow_option = AllowOptions.objects.get(appl=appl_option)
        delta_t += allow_option.date_diff

    if (OAOptions.objects.filter(appl=appl_option).exists()):
        oa_options = OAOptions.objects.filter(appl=appl_option)
        for oa in oa_options:
            delta_t += oa.date_diff

    templates = templates.exclude(
        Q(conditions__condition_annual_prosecution_fee=True)
        & Q(date_diff__gt=delta_t))
    return templates


def _filter_prior_appl_pct(templates, application):
    prior_appl = application.prior_appl
    prior_pct = False
    if (prior_appl):
        appl_type = appl_utils.convert_class_applType(prior_appl)
        if (appl_type == ApplType.objects.get(application_type='pct')):
            # create us Validation
            prior_pct = True
    templates = templates.filter(
        Q(conditions__prior_pct=prior_pct)
        | Q(conditions__prior_pct=None))
    return templates


def _filter_prior_appl_pct_same_country(templates, application):
    # ISA country not Receiving Office
    prior_appl = application.prior_appl
    prior_pct_same_country = False
    if (prior_appl):
        appl_type = appl_utils.convert_class_applType(prior_appl)
        if (appl_type == ApplType.objects.get(application_type='pct')):
            # create us Validation
            if (prior_appl.isa_country == application.country):
                prior_pct_same_country = True
                # now special conditions apply
    templates = templates.filter(
        Q(conditions__prior_pct_same_country=prior_pct_same_country)
        | Q(conditions__prior_pct_same_country=None))
    return templates


def _filter_fee_from_prior_appl_filing_date_and_excluding_overlapping_dates(templates, application):
    # take in templates
    # calculate date from original date filter out anything less than
    prior_appl = application.prior_appl
    if (prior_appl):
        date_diff = application.date_filing - prior_appl.date_filing
        templates = templates.filter(
            (Q(date_diff__gt=date_diff)
             & Q(conditions__prev_appl_date_excl_intermediary_time=True))
            | (Q(conditions__prev_appl_date_excl_intermediary_time=False)
               | Q(conditions__prev_appl_date_excl_intermediary_time=None))
        )
    return templates
