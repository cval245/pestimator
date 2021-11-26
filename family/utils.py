from django.db.models import F, ExpressionWrapper, Sum, Q, Value
from django.db.models.functions import Coalesce
from djmoney.models.fields import MoneyField
from estimation.models import BaseEst

import uuid


def createFamEstDetails(id):
    bob = BaseEst.objects.filter(application__family=id).order_by('date__year', 'application__country')

    bill = bob.values(country=F('application__country'),
                      country_long_name=F('application__country__long_name'),
                      currency=F('official_cost_currency'),
                      year=F('date__year')) \
        .annotate(
        official_cost_sum=ExpressionWrapper(
            Coalesce(Sum('official_cost', filter=Q(translation_bool=False)), Value(0)), output_field=MoneyField()),
        law_firm_cost_sum=ExpressionWrapper(
            Coalesce(Sum('law_firm_est__law_firm_cost'), Value(0)),
            output_field=MoneyField()),
        translation_cost_sum=ExpressionWrapper(
            Coalesce(Sum('official_cost', filter=Q(translation_bool=True)), Value(0)), output_field=MoneyField()),
        total_cost_sum=F('official_cost_sum') + F('law_firm_cost_sum') + F('translation_cost_sum'),
        # id=uuid.uuid4()
    )

    for item in bill:
        item['id'] = uuid.uuid4()
    return bill


# , country_long_name=F('application__country__long_name')) \
def get_totals_per_country(id):
    bob = BaseEst.objects.filter(application__family=id).order_by('application__country') \
        .values(country=F('application__country'), country_long_name=F('application__country__long_name')) \
        .annotate(
        official_cost_sum=ExpressionWrapper(
            Coalesce(Sum('official_cost', filter=Q(translation_bool=False)), Value(0)), output_field=MoneyField()),
        law_firm_cost_sum=ExpressionWrapper(
            Coalesce(Sum('law_firm_est__law_firm_cost'), Value(0)),
            output_field=MoneyField()),
        translation_cost_sum=ExpressionWrapper(
            Coalesce(Sum('official_cost', filter=Q(translation_bool=True)), Value(0)), output_field=MoneyField()),
        total_cost_sum=F('official_cost_sum') + F('law_firm_cost_sum') + F('translation_cost_sum'))
    # x = BaseEst.objects.filter(application__family=id).order_by('application__country')\
    #     .distinct('application__country').values('application__country')
    return bob


def get_totals_per_year(id):
    bob = BaseEst.objects.filter(application__family=id).order_by('date__year') \
        .values(year=F('date__year')) \
        .annotate(
        official_cost_sum=ExpressionWrapper(
            Coalesce(Sum('official_cost', filter=Q(translation_bool=False)), Value(0)), output_field=MoneyField()),
        law_firm_cost_sum=ExpressionWrapper(
            Coalesce(Sum('law_firm_est__law_firm_cost'), Value(0)),
            output_field=MoneyField()),
        translation_cost_sum=ExpressionWrapper(
            Coalesce(Sum('official_cost', filter=Q(translation_bool=True)), Value(0)), output_field=MoneyField()),
        total_cost_sum=F('official_cost_sum') + F('law_firm_cost_sum') + F('translation_cost_sum'))
    return bob


def get_total_costs(id):
    bob = BaseEst.objects.filter(application__family=id).order_by('application__family') \
        .values(year=F('application__family')) \
        .annotate(
        official_cost_sum=ExpressionWrapper(
            Coalesce(Sum('official_cost', filter=Q(translation_bool=False)), Value(0)), output_field=MoneyField()),
        law_firm_cost_sum=ExpressionWrapper(
            Coalesce(Sum('law_firm_est__law_firm_cost'), Value(0)),
            output_field=MoneyField()),
        translation_cost_sum=ExpressionWrapper(
            Coalesce(Sum('official_cost', filter=Q(translation_bool=True)), Value(0)), output_field=MoneyField()),
        total_cost_sum=F('official_cost_sum') + F('law_firm_cost_sum') + F('translation_cost_sum'))
    return bob
