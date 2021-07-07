from django.shortcuts import render
from djmoney.models.fields import MoneyField
from django.db.models import Sum, F, Case, Value, When
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Family
from .serializers import FamilySerializer
from estimation.models import BaseEst
from famform.models import FamEstFormData

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
    # families = Family.objects.select_all_fam_ests(user=request.user)
    families = Family.objects.filter(user=request.user)
    # families = Family.objects.filter(user=request.user).select_all_fam_ests()
    print('families = ', families)
    # families.
    # s = families.values('id', 'famestformdata').annotate(
    #         official_cost=Sum('base')            
    #     )
    print('sdfsdfsdf', BaseEst.objects.all())    
    print(BaseEst.objects.values('law_firm_est'))
    print('val',  families.values('baseapplication__baseest__law_firm_est'))
    s = families.values('id', 'famestformdata').annotate(
        official_cost=Sum('baseapplication__baseest__official_cost'),
        law_firm_cost=Sum('baseapplication__baseest__law_firm_est__law_firm_cost'))
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
        print('famEst = ', famEst)
        bob = createFamEstDetails(famEst.family.id)
        print('bob', bob)
        return Response(bob)
    return Response(status=status.HTTP_404_NOT_FOUND) 

def createFamEstDetails(id):
    print('sdfsdf', BaseEst.objects.all().values_list('law_firm_est'))
    bob = BaseEst.objects.annotate(
        total_cost=Case(
            When(law_firm_est=None, 
                then=F('official_cost')),
            When(law_firm_est=None, 
                then=(F('law_firm_est__law_firm_cost')+ F('official_cost')))
            
            )
            
        ).filter(application__family=id)

    bill = bob.values('id', country=F('application__country'), 
        year=F('date__year'))\
              .annotate(official_cost_sum=Sum('official_cost'),
                        law_firm_cost_sum=Sum('law_firm_est__law_firm_cost'),
                        total_cost_sum=Sum('total_cost'),
              )

    return bill