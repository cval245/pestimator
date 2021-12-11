from django.db.models import F, ExpressionWrapper, Sum, Q, Value
from django.db.models.functions import Coalesce, Round
from djmoney.models.fields import MoneyField
from estimation.models import BaseEst

import uuid

from family.models import Family


def getFamEstAll(user):
    famEsts = Family.objects.filter(user=user).values('id', 'famestformdata', 'famestformdata__date_created') \
        .order_by('-famestformdata__date_created').annotate(
        official_cost=ExpressionWrapper(
            Coalesce(Sum(Round('baseapplication__baseest__official_cost'),
                         filter=Q(baseapplication__baseest__translation_bool=False)), Value(0)),
            output_field=MoneyField()),
        law_firm_cost=ExpressionWrapper(
            Coalesce(Sum(Round('baseapplication__baseest__law_firm_est__law_firm_cost')), Value(0)),
            output_field=MoneyField()),
        translation_cost=ExpressionWrapper(
            Coalesce(Sum(Round('baseapplication__baseest__official_cost'),
                         filter=Q(baseapplication__baseest__translation_bool=True)), Value(0)),
            output_field=MoneyField()),
        total_cost=F('official_cost') + F('law_firm_cost') + F('translation_cost'),
    )
    return famEsts


def createFamEstDetails(id):
    bob = BaseEst.objects.filter(application__family=id).order_by('date__year', 'application__country')

    bill = bob.values(country=F('application__country'),
                      country_long_name=F('application__country__long_name'),
                      currency=F('official_cost_currency'),
                      year=F('date__year')) \
        .annotate(
        official_cost_sum=ExpressionWrapper(
            Coalesce(Sum(Round('official_cost'), filter=Q(translation_bool=False)), Value(0)),
            output_field=MoneyField()),
        law_firm_cost_sum=ExpressionWrapper(
            Coalesce(Sum(Round('law_firm_est__law_firm_cost')), Value(0)),
            output_field=MoneyField()),
        translation_cost_sum=ExpressionWrapper(
            Coalesce(Sum(Round('official_cost'), filter=Q(translation_bool=True)), Value(0)),
            output_field=MoneyField()),
        total_cost_sum=F('official_cost_sum') + F('law_firm_cost_sum') + F('translation_cost_sum'),
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
            Coalesce(Sum(Round('official_cost'), filter=Q(translation_bool=False)), Value(0)),
            output_field=MoneyField()),
        law_firm_cost_sum=ExpressionWrapper(
            Coalesce(Sum(Round('law_firm_est__law_firm_cost')), Value(0)),
            output_field=MoneyField()),
        translation_cost_sum=ExpressionWrapper(
            Coalesce(Sum(Round('official_cost'), filter=Q(translation_bool=True)), Value(0)),
            output_field=MoneyField()),
        total_cost_sum=F('official_cost_sum') + F('law_firm_cost_sum') + F('translation_cost_sum'))
    return bob


def get_totals_per_year(id):
    bob = BaseEst.objects.filter(application__family=id).order_by('date__year') \
        .values(year=F('date__year')) \
        .annotate(
        official_cost_sum=ExpressionWrapper(
            Coalesce(Sum(Round('official_cost'), filter=Q(translation_bool=False)), Value(0)),
            output_field=MoneyField()),
        law_firm_cost_sum=ExpressionWrapper(
            Coalesce(Sum(Round('law_firm_est__law_firm_cost')), Value(0)),
            output_field=MoneyField()),
        translation_cost_sum=ExpressionWrapper(
            Coalesce(Sum(Round('official_cost'), filter=Q(translation_bool=True)), Value(0)),
            output_field=MoneyField()),
        total_cost_sum=F('official_cost_sum') + F('law_firm_cost_sum') + F('translation_cost_sum'))
    return bob


def get_total_costs(id):
    bob = BaseEst.objects.filter(application__family=id).order_by('application__family') \
        .values(year=F('application__family')) \
        .annotate(
        official_cost_sum=ExpressionWrapper(
            Coalesce(Sum(Round('official_cost'), filter=Q(translation_bool=False)), Value(0)),
            output_field=MoneyField()),
        law_firm_cost_sum=ExpressionWrapper(
            Coalesce(Sum(Round('law_firm_est__law_firm_cost')), Value(0)),
            output_field=MoneyField()),
        translation_cost_sum=ExpressionWrapper(
            Coalesce(Sum(Round('official_cost'), filter=Q(translation_bool=True)), Value(0)),
            output_field=MoneyField()),
        total_cost_sum=F('official_cost_sum') + F('law_firm_cost_sum') + F('translation_cost_sum'))
    return bob
