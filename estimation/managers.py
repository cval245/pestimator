from django.db import models
from django.db.models import Q

from application import utils as applUtils


class EstimateTemplateManager(models.Manager):

    def basic_template_filter(self, country, appl_type, date):
        filtered = self.filter(
            Q(date_disabled__gt=date) | Q(date_disabled=None),
            Q(date_enabled__lte=date),
            country=country,
            appl_type=appl_type,
        )
        filtered = filtered.order_by('detailed_fee_category', '-date_enabled') \
            .distinct('detailed_fee_category')
        return filtered


class USOAEstimateTemplateManager(models.Manager):

    def basic_template_filter(self, country, appl_type, date, oa_final_bool, oa_first_final_bool):
        filtered = self.filter(
            Q(date_disabled__gt=date) | Q(date_disabled=None),
            Q(date_enabled__lte=date),
            country=country,
            appl_type=appl_type,
            oa_final_bool=oa_final_bool,
            oa_first_final_bool=oa_first_final_bool,
        )
        filtered = filtered.order_by('detailed_fee_category', '-date_enabled') \
            .distinct('detailed_fee_category')
        return filtered


class EstimateManager(models.Manager):
    def create_complex_and_simple_est(self, application, est_template, law_firm_est):
        cost = est_template.official_cost
        if est_template.conditions.condition_complex:
            complex_condition = est_template.conditions.condition_complex
            cost = complex_condition.calc_complex_condition(application,
                                                            cost,
                                                            est_template.conditions)
        new_date = application.date_filing + est_template.date_diff
        if est_template.conditions.condition_time_complex:
            time_complex = est_template.conditions.condition_time_complex
            date_diff = est_template.date_diff
            new_date = time_complex.calc_complex_time_condition(application, date_diff,
                                                                est_template.conditions)

        date_of_expiry = applUtils.get_date_of_expiry(application)
        if (date_of_expiry > new_date):
            est = self.create(
                application=application,
                date=new_date,
                official_cost=cost,
                law_firm_est=law_firm_est,
                fee_code=est_template.fee_code,
                description=est_template.description,
            )
            return est
        return None


class PublEstimateManager(models.Manager):

    def create_complex_and_simple_est(self, application, est_template, law_firm_est, publication):
        cost = est_template.official_cost
        if est_template.conditions.condition_complex:
            complex_condition = est_template.conditions.condition_complex
            cost = complex_condition.calc_complex_condition(application,
                                                            cost,
                                                            est_template.conditions)
        new_date = publication.date_publication + est_template.date_diff
        if est_template.conditions.condition_time_complex:
            time_complex = est_template.conditions.condition_time_complex
            date_diff = est_template.date_diff
            new_date = time_complex.calc_complex_time_condition(application, date_diff,
                                                                est_template.conditions)

        date_of_expiry = applUtils.get_date_of_expiry(application)
        if (date_of_expiry > new_date):
            est = self.create(
                application=application,
                date=new_date,
                official_cost=cost,
                publication=publication,
                law_firm_est=law_firm_est,
                fee_code=est_template.fee_code,
                description=est_template.description,
            )
            return est
        return None


class ReqExamEstimateManager(models.Manager):

    def create_complex_and_simple_est(self, application, est_template, law_firm_est, exam_request):
        cost = est_template.official_cost
        if est_template.conditions.condition_complex:
            complex_condition = est_template.conditions.condition_complex
            cost = complex_condition.calc_complex_condition(application,
                                                            cost,
                                                            est_template.conditions)
        new_date = exam_request.date_request_examination + est_template.date_diff
        if est_template.conditions.condition_time_complex:
            time_complex = est_template.conditions.condition_time_complex
            date_diff = est_template.date_diff
            new_date = time_complex.calc_complex_time_condition(application, date_diff,
                                                                est_template.conditions)

        date_of_expiry = applUtils.get_date_of_expiry(application)
        if (date_of_expiry > new_date):
            est = self.create(
                application=application,
                date=new_date,
                official_cost=cost,
                exam_request=exam_request,
                law_firm_est=law_firm_est,
                fee_code=est_template.fee_code,
                description=est_template.description,
            )
            return est
        return None


class AllowanceEstimateManager(models.Manager):

    def create_complex_and_simple_est(self, application, est_template, law_firm_est, allowance):
        cost = est_template.official_cost
        if est_template.conditions.condition_complex:
            complex_condition = est_template.conditions.condition_complex
            cost = complex_condition.calc_complex_condition(application,
                                                            cost,
                                                            est_template.conditions)
        new_date = allowance.date_allowance + est_template.date_diff
        if est_template.conditions.condition_time_complex:
            time_complex = est_template.conditions.condition_time_complex
            date_diff = est_template.date_diff
            new_date = time_complex.calc_complex_time_condition(application, date_diff,
                                                                est_template.conditions)

        date_of_expiry = applUtils.get_date_of_expiry(application)
        if (date_of_expiry > new_date):
            est = self.create(
                application=application,
                date=new_date,
                official_cost=cost,
                allowance=allowance,
                law_firm_est=law_firm_est,
                fee_code=est_template.fee_code,
                description=est_template.description,
            )
            return est
        return None


class IssueEstimateManager(models.Manager):

    def create_complex_and_simple_est(self, application, est_template, law_firm_est, issuance):
        cost = est_template.official_cost
        if est_template.conditions.condition_complex:
            complex_condition = est_template.conditions.condition_complex
            cost = complex_condition.calc_complex_condition(application,
                                                            cost,
                                                            est_template.conditions)
        new_date = issuance.date_issuance + est_template.date_diff
        if est_template.conditions.condition_time_complex:
            time_complex = est_template.conditions.condition_time_complex
            date_diff = est_template.date_diff
            new_date = time_complex.calc_complex_time_condition(application, date_diff,
                                                                est_template.conditions)

        date_of_expiry = applUtils.get_date_of_expiry(application)
        if (date_of_expiry > new_date):
            est = self.create(
                application=application,
                date=new_date,
                official_cost=cost,
                issue=issuance,
                law_firm_est=law_firm_est,
                fee_code=est_template.fee_code,
                description=est_template.description,
            )

            return est
        return None


class OAEstimateManager(models.Manager):

    def create_complex_and_simple_est(self, application, est_template, law_firm_est, office_action):
        cost = est_template.official_cost
        if est_template.conditions.condition_complex:
            complex_condition = est_template.conditions.condition_complex
            cost = complex_condition.calc_complex_condition(application,
                                                            cost,
                                                            est_template.conditions)
        new_date = office_action.date_office_action + est_template.date_diff
        if est_template.conditions.condition_time_complex:
            time_complex = est_template.conditions.condition_time_complex
            date_diff = est_template.date_diff
            new_date = time_complex.calc_complex_time_condition(application, date_diff,
                                                                est_template.conditions)

        date_of_expiry = applUtils.get_date_of_expiry(application)
        if (date_of_expiry > new_date):
            est = self.create(
                application=application,
                date=new_date,
                official_cost=cost,
                office_action=office_action,
                law_firm_est=law_firm_est,
                fee_code=est_template.fee_code,
                description=est_template.description,
            )
            return est
        return None


class USOAEstimateManager(models.Manager):

    def create_complex_and_simple_est(self, application, est_template, law_firm_est, office_action):
        cost = est_template.official_cost
        if est_template.conditions.condition_complex:
            complex_condition = est_template.conditions.condition_complex
            cost = complex_condition.calc_complex_condition(application,
                                                            cost,
                                                            est_template.conditions)
        new_date = office_action.date_office_action + est_template.date_diff
        if est_template.conditions.condition_time_complex:
            time_complex = est_template.conditions.condition_time_complex
            date_diff = est_template.date_diff
            new_date = time_complex.calc_complex_time_condition(application, date_diff,
                                                                est_template.conditions)

        date_of_expiry = applUtils.get_date_of_expiry(application)
        if date_of_expiry > new_date:
            est = self.create(
                application=application,
                date=new_date,
                official_cost=cost,
                office_action=office_action,
                law_firm_est=law_firm_est,
                fee_code=est_template.fee_code,
                description=est_template.description,
            )
            return est
        return None
