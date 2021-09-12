from django.db import models


class EstimateManager(models.Manager):
    def create_complex_and_simple_est(self, application, est_template, law_firm_est):
        cost = est_template.official_cost
        if est_template.conditions.condition_complex:
            complex_condition = est_template.conditions.condition_complex
            cost = complex_condition.calc_complex_condition(application.details,
                                                            cost,
                                                            est_template.conditions)
        new_date = application.date_filing + est_template.date_diff
        if est_template.conditions.condition_time_complex:
            time_complex = est_template.conditions.condition_time_complex
            date_diff = est_template.date_diff
            new_date = time_complex.calc_complex_time_condition(application, date_diff,
                                                                est_template.conditions)

        est = self.create(
            application=application,
            date=new_date,
            official_cost=cost,
            law_firm_est=law_firm_est,
        )
        return est


class PublEstimateManager(models.Manager):

    def create_complex_and_simple_est(self, application, est_template, law_firm_est, publication):
        cost = est_template.official_cost
        if est_template.conditions.condition_complex:
            complex_condition = est_template.conditions.condition_complex
            cost = complex_condition.calc_complex_condition(application.details,
                                                            cost,
                                                            est_template.conditions)
        new_date = publication.date_publication + est_template.date_diff
        if est_template.conditions.condition_time_complex:
            time_complex = est_template.conditions.condition_time_complex
            date_diff = est_template.date_diff
            new_date = time_complex.calc_complex_time_condition(application, date_diff,
                                                                est_template.conditions)

        est = self.create(
            application=application,
            date=new_date,
            official_cost=cost,
            publication=publication,
            law_firm_est=law_firm_est,
        )
        return est
    # def create_complex_and_simple_est(self, application, appl_details,
    #                                   template_conditions,
    #                                   date, official_cost, law_firm_est, publication):
    #     cost = official_cost
    #     if template_conditions.condition_complex:
    #         complex_condition = template_conditions.condition_complex
    #         cost = complex_condition.calc_complex_condition(appl_details,
    #                                                         official_cost,
    #                                                         template_conditions)
    #
    #     est = self.create(
    #         application=application,
    #         date=date,
    #         official_cost=cost,
    #         publication=publication,
    #         law_firm_est=law_firm_est,
    #     )
    #     return est


class AllowanceEstimateManager(models.Manager):

    def create_complex_and_simple_est(self, application, est_template, law_firm_est, allowance):
        cost = est_template.official_cost
        if est_template.conditions.condition_complex:
            complex_condition = est_template.conditions.condition_complex
            cost = complex_condition.calc_complex_condition(application.details,
                                                            cost,
                                                            est_template.conditions)
        new_date = allowance.date_allowance + est_template.date_diff
        if est_template.conditions.condition_time_complex:
            time_complex = est_template.conditions.condition_time_complex
            date_diff = est_template.date_diff
            new_date = time_complex.calc_complex_time_condition(application, date_diff,
                                                                est_template.conditions)

        est = self.create(
            application=application,
            date=new_date,
            official_cost=cost,
            allowance=allowance,
            law_firm_est=law_firm_est,
        )
        return est

    # def create_complex_and_simple_est(self, application, appl_details,
    #                                   template_conditions,
    #                                   date, official_cost, law_firm_est, allowance):
    #     cost = official_cost
    #     if template_conditions.condition_complex:
    #         complex_condition = template_conditions.condition_complex
    #         cost = complex_condition.calc_complex_condition(appl_details,
    #                                                         official_cost,
    #                                                         template_conditions)
    #
    #     est = self.create(
    #         application=application,
    #         date=date,
    #         official_cost=cost,
    #         allowance=allowance,
    #         law_firm_est=law_firm_est,
    #     )
    #     return est


class IssueEstimateManager(models.Manager):

    def create_complex_and_simple_est(self, application, est_template, law_firm_est, issuance):
        cost = est_template.official_cost
        if est_template.conditions.condition_complex:
            complex_condition = est_template.conditions.condition_complex
            cost = complex_condition.calc_complex_condition(application.details,
                                                            cost,
                                                            est_template.conditions)
        new_date = issuance.date_issuance + est_template.date_diff
        if est_template.conditions.condition_time_complex:
            time_complex = est_template.conditions.condition_time_complex
            date_diff = est_template.date_diff
            new_date = time_complex.calc_complex_time_condition(application, date_diff,
                                                                est_template.conditions)

        est = self.create(
            application=application,
            date=new_date,
            official_cost=cost,
            issue=issuance,
            law_firm_est=law_firm_est,
        )
        return est

    # def create_complex_and_simple_est(self, application, appl_details,
    #                                   template_conditions,
    #                                   date, official_cost, law_firm_est, issuance):
    #     cost = official_cost
    #     if template_conditions.condition_complex:
    #         complex_condition = template_conditions.condition_complex
    #         cost = complex_condition.calc_complex_condition(appl_details,
    #                                                         official_cost,
    #                                                         template_conditions)
    #
    #     est = self.create(
    #         application=application,
    #         date=date,
    #         official_cost=cost,
    #         issue=issuance,
    #         law_firm_est=law_firm_est,
    #     )
    #     return est


class OAEstimateManager(models.Manager):

    def create_complex_and_simple_est(self, application, est_template, law_firm_est, office_action):
        cost = est_template.official_cost
        if est_template.conditions.condition_complex:
            complex_condition = est_template.conditions.condition_complex
            cost = complex_condition.calc_complex_condition(application.details,
                                                            cost,
                                                            est_template.conditions)
        new_date = office_action.date_office_action + est_template.date_diff
        if est_template.conditions.condition_time_complex:
            time_complex = est_template.conditions.condition_time_complex
            date_diff = est_template.date_diff
            new_date = time_complex.calc_complex_time_condition(application, date_diff,
                                                                est_template.conditions)

        est = self.create(
            application=application,
            date=new_date,
            official_cost=cost,
            office_action=office_action,
            law_firm_est=law_firm_est,
        )
        return est
    # def create_complex_and_simple_est(self, application, appl_details,
    #                                   template_conditions,
    #                                   date, official_cost, law_firm_est, office_action):
    #     cost = official_cost
    #     if template_conditions.condition_complex:
    #         complex_condition = template_conditions.condition_complex
    #         cost = complex_condition.calc_complex_condition(appl_details,
    #                                                         official_cost,
    #                                                         template_conditions)
    #
    #     est = self.create(
    #         application=application,
    #         date=date,
    #         official_cost=cost,
    #         office_action=office_action,
    #         law_firm_est=law_firm_est,
    #     )
    #     return est


class USOAEstimateManager(models.Manager):

    def create_complex_and_simple_est(self, application, est_template, law_firm_est, office_action):
        cost = est_template.official_cost
        if est_template.conditions.condition_complex:
            complex_condition = est_template.conditions.condition_complex
            cost = complex_condition.calc_complex_condition(application.details,
                                                            cost,
                                                            est_template.conditions)
        new_date = office_action.date_office_action + est_template.date_diff
        if est_template.conditions.condition_time_complex:
            time_complex = est_template.conditions.condition_time_complex
            date_diff = est_template.date_diff
            new_date = time_complex.calc_complex_time_condition(application, date_diff,
                                                                est_template.conditions)

        est = self.create(
            application=application,
            date=new_date,
            official_cost=cost,
            office_action=office_action,
            law_firm_est=law_firm_est,
        )
        return est

    # def create_complex_and_simple_est(self, application, appl_details,
    #                                   template_conditions,
    #                                   date, official_cost, law_firm_est, office_action):
    #     cost = official_cost
    #     if template_conditions.condition_complex:
    #         complex_condition = template_conditions.condition_complex
    #         cost = complex_condition.calc_complex_condition(appl_details,
    #                                                         official_cost,
    #                                                         template_conditions)
    #
    #     est = self.create(
    #         application=application,
    #         date=date,
    #         official_cost=cost,
    #         office_action=office_action,
    #         law_firm_est=law_firm_est,
    #     )
    #     return est
