from dateutil.relativedelta import relativedelta
from django.db.models import Q
from application import utils as appl_utils
# take templates and then filter using application details
from characteristics.models import ApplType
from famform.models import OAOptions, AllowOptions, IssueOptions


def filter_conditions(templates, application):
    appl_details = application.details

    # filter claims
    temp = _filter_claims(templates, appl_details)
    temp = _filter_indep_claims(temp, appl_details)
    temp = _filter_claims_multiple_dependent(temp, appl_details)

    # filter pages
    temp = _filter_total_pages(temp, appl_details)
    temp = _filter_desc_pages(temp, appl_details)
    temp = _filter_claims_pages(temp, appl_details)
    temp = _filter_drawings_pages(temp, appl_details)

    temp = _filter_drawings(temp, appl_details)
    temp = _filter_entity_size(temp, appl_details)
    temp = _filter_annual_prosecution_fee(temp, application)
    temp = _filter_annual_prosecution_fee_until_grant(temp, application)
    temp = _filter_renewal_fee_from_filing_after_grant(temp, application)
    temp = _filter_prior_appl_pct(temp, application)
    temp = _filter_prior_appl_pct_same_country(temp, application)
    temp = _filter_fee_from_prior_appl_filing_date_and_excluding_overlapping_dates(temp, application)
    temp = _filter_fee_if_first_appl(temp, application)

    temp = _filter_fee_doc_format(temp, application)
    final_temps = temp
    return final_temps


def _filter_fee_doc_format(templates, application):
    custom_options = application.appl_option.custom_appl_options
    templates = templates.filter(
        Q(conditions__doc_format=custom_options.doc_format) | Q(conditions__doc_format=None)
    )
    return templates


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
        appl_details.num_indep_claims)

    templates = templates.exclude(
        conditions__condition_indep_claims_max__lte=
        appl_details.num_indep_claims)
    return templates


def _filter_claims_multiple_dependent(templates, appl_details):
    # remove templates that exceed conditions
    templates = templates.exclude(
        conditions__condition_claims_multiple_dependent_min__gte=
        appl_details.num_claims_multiple_dependent)

    templates = templates.exclude(
        conditions__condition_claims_multiple_dependent_max__lte=
        appl_details.num_claims_multiple_dependent)
    return templates


def _filter_total_pages(templates, appl_details):
    templates = templates.exclude(
        conditions__condition_pages_total_min__gte=
        appl_details.total_pages)

    templates = templates.exclude(
        conditions__condition_pages_total_max__lte=
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


def _filter_claims_pages(templates, appl_details):
    templates = templates.exclude(
        conditions__condition_pages_claims_min__gte=
        appl_details.num_pages_claims)

    templates = templates.exclude(
        conditions__condition_pages_claims_max__lte=
        appl_details.num_pages_claims)

    return templates


def _filter_drawings_pages(templates, appl_details):
    templates = templates.exclude(
        conditions__condition_pages_drawings_min__gte=
        appl_details.num_pages_drawings)

    templates = templates.exclude(
        conditions__condition_pages_drawings_max__lte=
        appl_details.num_pages_drawings)

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


def _filter_annual_prosecution_fee_until_grant(templates, application):
    # use applOption to retrieve allowance_option
    appl_option = application.appl_option
    # sum Delta Time between filing and allowance_option
    delta_t = relativedelta(days=0)

    if (IssueOptions.objects.filter(appl=appl_option).exists()):
        issue_option = IssueOptions.objects.get(appl=appl_option)
        delta_t += issue_option.date_diff

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


def _filter_renewal_fee_from_filing_after_grant(templates, application):
    # remove all that are less than the issue date
    # use applOption to retrieve allowance_option
    appl_option = application.appl_option
    # sum Delta Time between filing and allowance_option
    delta_t = relativedelta(days=0)

    if (IssueOptions.objects.filter(appl=appl_option).exists()):
        issue_option = IssueOptions.objects.get(appl=appl_option)
        delta_t += issue_option.date_diff

    if (AllowOptions.objects.filter(appl=appl_option).exists()):
        allow_option = AllowOptions.objects.get(appl=appl_option)
        delta_t += allow_option.date_diff

    if (OAOptions.objects.filter(appl=appl_option).exists()):
        oa_options = OAOptions.objects.filter(appl=appl_option)
        for oa in oa_options:
            delta_t += oa.date_diff

    templates = templates.exclude(
        Q(conditions__condition_annual_prosecution_fee=True)
        & Q(date_diff__lt=delta_t))
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
            from application.models import PCTApplication
            prior_pct_appl = PCTApplication.objects.get(baseapplication_ptr=prior_appl)
            if (prior_pct_appl.isa_country == application.country):
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


def _filter_fee_if_first_appl(templates, application):
    # if application.prior_appl:
    if application.prior_appl:
        templates = templates.exclude(conditions__prior_appl_exists=False)
    else:
        templates = templates.exclude(conditions__prior_appl_exists=True)
    return templates
