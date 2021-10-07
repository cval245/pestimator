
from django.db.models import Sum, F, Value, ExpressionWrapper, Q
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
        fam_est_form_data_udn = self.request.query_params.get('FamEstFormDataUDN')
        if fam_est_form_data_udn is not None:
            if queryset.filter(user=self.request.user,
                               famestformdata__unique_display_no=fam_est_form_data_udn).exists():
                queryset = queryset.filter(
                    user=self.request.user,
                    famestformdata__unique_display_no=fam_est_form_data_udn)
        return queryset


@api_view(['GET'])
def fam_est_all(request):
    families = Family.objects.filter(user=request.user)

    s = families.values('id', 'famestformdata').annotate(
        official_cost=ExpressionWrapper(
            Coalesce(Sum('baseapplication__baseest__official_cost'), Value(0)),
            output_field=MoneyField()),
        law_firm_cost=ExpressionWrapper(
            Coalesce(Sum('baseapplication__baseest__law_firm_est__law_firm_cost'),
                     Value(0)),
            output_field=MoneyField()),
        date_created=F('famestformdata__date_created'))
    s = s.annotate(total_cost=F('official_cost') + F('law_firm_cost'))
    return Response(s)


@api_view(['GET'])
def fam_est(request, udn):
    # famEst = FamEstFormData.objects.get(id=id)
    famEst = FamEstFormData.objects.get(unique_display_no=udn, user=request.user)
    famEstDetails = createFamEstDetails(famEst.family.id)
    return Response({'FamEstDetail': famEstDetails})


@api_view(['GET'])
def fam_est_detail(request):
    udn = request.query_params.get('FamEstFormDataUDN')
    if FamEstFormData.objects.filter(user=request.user, unique_display_no=udn).exists():
        famEst = FamEstFormData.objects.get(user=request.user, unique_display_no=udn)
        bob = createFamEstDetails(famEst.family.id)
        # jane = bob.aggregate(Sum('law_firm_cost_sum'))
        # law fees canceld out
        return Response(bob)
    return Response(status=status.HTTP_404_NOT_FOUND)


def createFamEstDetails(id):
    bob = BaseEst.objects.filter(application__family=id)

    bill = bob.values('id', country=F('application__country'),
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
    )

    return bill
