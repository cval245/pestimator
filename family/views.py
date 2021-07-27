from django.db.models import Sum, F, Value, ExpressionWrapper
from django.db.models.functions import Coalesce
from djmoney.models.fields import MoneyField
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from estimation.models import BaseEst
from famform.models import FamEstFormData
from .models import Family
from .serializers import FamilySerializer


# Create your views here.

class FamilyViewSet(viewsets.ModelViewSet):
    serializer_class = FamilySerializer

    def get_queryset(self):
        queryset = Family.objects.filter(user=self.request.user)
        fam_est_form_data = self.request.query_params.get('FamEstFormData')
        if fam_est_form_data is not None:
            if queryset.filter(famestformdata=fam_est_form_data).exists():
                queryset = queryset.filter(famestformdata=fam_est_form_data)
        return queryset


@api_view(['GET'])
def fam_est_all(request):
    families = Family.objects.filter(user=request.user)
    print('families = ', families)

    s = families.values('id', 'famestformdata').annotate(
        official_cost=ExpressionWrapper(
            Coalesce(Sum('baseapplication__baseest__official_cost'), Value(0)),
            output_field=MoneyField()),
        law_firm_cost=ExpressionWrapper(
            Coalesce(Sum('baseapplication__baseest__law_firm_est__law_firm_cost'),
                     Value(0)),
            output_field=MoneyField()))
    s = s.annotate(total_cost=F('official_cost') + F('law_firm_cost'))
    return Response(s)


@api_view(['GET'])
def fam_est(request, id):
    famEst = FamEstFormData.objects.get(id=id)
    famEstDetails = createFamEstDetails(famEst.family.id)
    return Response({'FamEstDetail': famEstDetails})


@api_view(['GET'])
def fam_est_detail(request):
    id = request.query_params.get('FamEstFormData')
    if FamEstFormData.objects.filter(id=id).exists():
        famEst = FamEstFormData.objects.get(id=id)
        bob = createFamEstDetails(famEst.family.id)
        return Response(bob)
    return Response(status=status.HTTP_404_NOT_FOUND)


def createFamEstDetails(id):
    bob = BaseEst.objects.filter(application__family=id)

    bill = bob.values('id', country=F('application__country'),
                      currency=F('official_cost_currency'),
                      year=F('date__year')) \
        .annotate(
        official_cost_sum=ExpressionWrapper(
            Coalesce(Sum('official_cost'), Value(0)), output_field=MoneyField()),
        law_firm_cost_sum=ExpressionWrapper(
            Coalesce(Sum('law_firm_est__law_firm_cost'), Value(0)),
            output_field=MoneyField()),
        # total_cost_sum=Sum('total_cost'),
        total_cost_sum=F('official_cost_sum') + F('law_firm_cost_sum'),
    )

    return bill
