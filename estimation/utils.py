from dateutil.relativedelta import relativedelta
from django.db.models import Q
from application import utils as appl_utils
# take templates and then filter using application details
from characteristics.enums import ApplTypes


def filter_conditions(templates, application, isa_filter=False):
    appl_details = application.details
    particulars = application.appl_option.particulars

    # filter claims
    temp = _filter_claims(templates, appl_details)
    temp = _filter_indep_claims(temp, appl_details)
    temp = _filter_claims_multiple_dependent(temp, appl_details)

    # filter pages
    temp = _filter_total_pages(temp, appl_details)
    temp = _filter_desc_pages(temp, appl_details)
    temp = _filter_claims_pages(temp, appl_details)
    temp = _filter_drawings_pages(temp, appl_details)

    temp = _filter_entity_size(temp, application, isa_filter)
    temp = _filter_drawings(temp, appl_details)
    temp = _filter_annual_prosecution_fee(temp, application)
    temp = _filter_annual_prosecution_fee_until_grant(temp, application)
    temp = _filter_renewal_fee_from_filing_after_grant(temp, application)
    temp = _filter_renewal_fee_from_filing_of_prior_after_grant(temp, application)
    temp = _filter_prior_appl_pct(temp, application)
    temp = _filter_prior_appl_pct_isa_same_country(temp, application)
    temp = _filter_fee_from_prior_appl_filing_date_and_excluding_overlapping_dates(temp, application)
    temp = _filter_fee_if_first_appl(temp, application)

    temp = _filter_languages(temp, appl_details)
    temp = _filter_fee_doc_format(temp, particulars)
    temp = _filter_fee_select_avail_currency_if_local_or_default(temp, application)
    final_temps = temp
    return final_temps


def _filter_fee_select_avail_currency_if_local_or_default(templates, application):
    if hasattr(application, 'pctapplication'):
        preferred_currency = application.country.currency_name
        templates_preferred = templates.filter(
            Q(conditions__isa_country_fee_only=False) |
            Q(conditions__isa_country_fee_only=True, official_cost_currency=preferred_currency)
        )
        if templates_preferred.exists():
            templates = templates_preferred
        else:
            normal_currency = application.isa_country.currency_name
            templates = templates.filter(
                Q(conditions__isa_country_fee_only=False) |
                Q(conditions__isa_country_fee_only=True, official_cost_currency=normal_currency)
            )
    else:
        templates = templates.filter(conditions__isa_country_fee_only=False)
    return templates


def _filter_fee_doc_format(templates, particulars):
    templates = templates.filter(
        Q(conditions__doc_format=particulars.doc_format) | Q(conditions__doc_format=None)
    )
    return templates


def _filter_languages(templates, appl_details):
    templates = templates.filter(
        Q(conditions__language=appl_details.language) | Q(conditions__language=None)
    )
    return templates


def _filter_claims(templates, appl_details):
    # remove templates that exceed conditions
    templates = templates.exclude(
        conditions__condition_claims_min__gt=
        appl_details.num_claims)

    templates = templates.exclude(
        conditions__condition_claims_max__lt=
        appl_details.num_claims)
    return templates


def _filter_indep_claims(templates, appl_details):
    # remove templates that exceed conditions
    templates = templates.exclude(
        conditions__condition_indep_claims_min__gt=
        appl_details.num_indep_claims)

    templates = templates.exclude(
        conditions__condition_indep_claims_max__lt=
        appl_details.num_indep_claims)
    return templates


def _filter_claims_multiple_dependent(templates, appl_details):
    # remove templates that exceed conditions
    templates = templates.exclude(
        conditions__condition_claims_multiple_dependent_min__gt=
        appl_details.num_claims_multiple_dependent)

    templates = templates.exclude(
        conditions__condition_claims_multiple_dependent_max__lt=
        appl_details.num_claims_multiple_dependent)
    return templates


def _filter_total_pages(templates, appl_details):
    templates = templates.exclude(
        conditions__condition_pages_total_min__gt=
        appl_details.total_pages)

    templates = templates.exclude(
        conditions__condition_pages_total_max__lt=
        appl_details.total_pages)
    return templates


def _filter_desc_pages(templates, appl_details):
    templates = templates.exclude(
        conditions__condition_pages_desc_min__gt=
        appl_details.num_pages_description)

    templates = templates.exclude(
        conditions__condition_pages_desc_max__lt=
        appl_details.num_pages_description)

    return templates


def _filter_claims_pages(templates, appl_details):
    templates = templates.exclude(
        conditions__condition_pages_claims_min__gt=
        appl_details.num_pages_claims)

    templates = templates.exclude(
        conditions__condition_pages_claims_max__lt=
        appl_details.num_pages_claims)

    return templates


def _filter_drawings_pages(templates, appl_details):
    templates = templates.exclude(
        conditions__condition_pages_drawings_min__gt=
        appl_details.num_pages_drawings)

    templates = templates.exclude(
        conditions__condition_pages_drawings_max__lt=
        appl_details.num_pages_drawings)

    return templates


def _filter_drawings(templates, appl_details):
    templates = templates.exclude(
        conditions__condition_drawings_min__gt=
        appl_details.num_drawings)

    templates = templates.exclude(
        conditions__condition_drawings_max__lt=
        appl_details.num_drawings)
    return templates


def _filter_entity_size(templates, application, isa_filter):
    # ISA only applies for PCTApplication
    entity_size = application.details.entity_size
    if isa_filter:
        entity_size = application.isa_entity_size
    templates = templates.filter(
        Q(conditions__condition_entity_size=entity_size)
        | Q(conditions__condition_entity_size=None))
    return templates


def _filter_annual_prosecution_fee(templates, application):
    # sum Delta Time between filing and allowance_option
    delta_t = relativedelta(days=0)
    if hasattr(application, 'allowance'):
        date_allowance = application.allowance.date_allowance
        delta_t = date_allowance - application.date_filing

    templates = templates.exclude(
        Q(conditions__condition_annual_prosecution_fee=True)
        & Q(date_diff__gt=delta_t))
    return templates


def _filter_annual_prosecution_fee_until_grant(templates, application):
    # use applOption to retrieve allowance_option
    # sum Delta Time between filing and allowance_option
    delta_t = relativedelta(days=0)
    if hasattr(application, 'issue'):
        delta_t = application.issue.date_issuance - application.date_filing
    bob = templates.filter(Q(conditions__condition_annual_prosecution_fee_until_grant=True))
    bill = bob.filter(date_diff__gt=delta_t)
    templates = templates.exclude(
        Q(conditions__condition_annual_prosecution_fee_until_grant=True)
        & Q(date_diff__gt=delta_t))
    return templates


def _filter_renewal_fee_from_filing_of_prior_after_grant(templates, application):
    # remove all that are less than the issue date
    # sum Delta Time between filing and issuance_date

    delta_t = relativedelta(days=0)
    if hasattr(application, 'issue'):
        if application.prior_appl:
            delta_t = application.issue.date_issuance - application.prior_appl.date_filing
        else:
            delta_t = application.issue.date_issuance - application.date_filing

    templates = templates.exclude(
        Q(conditions__condition_renewal_fee_from_filing_of_prior_after_grant=True)
        & Q(date_diff__lt=delta_t))
    return templates


def _filter_renewal_fee_from_filing_after_grant(templates, application):
    # remove all that are less than the issue date
    # sum Delta Time between filing and issuance_date

    delta_t = relativedelta(days=0)
    if hasattr(application, 'issue'):
        delta_t = application.issue.date_issuance - application.date_filing

    templates = templates.exclude(
        Q(conditions__condition_renewal_fee_from_filing_after_grant=True)
        & Q(date_diff__lt=delta_t))
    return templates


def _filter_prior_appl_pct(templates, application):
    prior_appl = application.prior_appl
    prior_pct = False
    if prior_appl:
        appl_type = appl_utils.convert_class_applType(prior_appl)
        if appl_type.get_enum() is ApplTypes.PCT:
            # create us Validation
            prior_pct = True
    templates = templates.filter(
        Q(conditions__prior_pct=prior_pct)
        | Q(conditions__prior_pct=None))
    return templates


def _filter_prior_appl_pct_isa_same_country(templates, application):
    # ISA country not Receiving Office
    prior_appl = application.prior_appl
    prior_pct_same_country = False
    if prior_appl:
        appl_type = appl_utils.convert_class_applType(prior_appl)
        if appl_type.get_enum() is ApplTypes.PCT:
            # create us Validation
            from application.models import PCTApplication
            prior_pct_appl = PCTApplication.objects.get(baseapplication_ptr=prior_appl)
            if prior_pct_appl.isa_country == application.country:
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
    if prior_appl:
        date_diff = application.date_filing - prior_appl.date_filing
        templates = templates.filter(
            (Q(date_diff__gt=date_diff)
             & Q(conditions__prev_appl_date_excl_intermediary_time=True))
            | (Q(conditions__prev_appl_date_excl_intermediary_time=False)
               )
        )
    return templates


def _filter_fee_if_first_appl(templates, application):
    # if application.prior_appl:
    if application.prior_appl:
        templates = templates.exclude(conditions__prior_appl_exists=False)
    else:
        templates = templates.exclude(conditions__prior_appl_exists=True)
    return templates
