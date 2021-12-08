import io
import xlsxwriter
from django.db.models import Sum, F, Value, ExpressionWrapper
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from djmoney.models.fields import MoneyField
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from famform.models import FamEstFormData
from . import utils, createXLSX
from .createPDF import generate_pdf_report
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
    famEsts = utils.getFamEstAll(request.user)
    return Response(famEsts)


@api_view(['GET'])
def fam_est(request, udn):
    # famEst = FamEstFormData.objects.get(id=id)
    famEst = FamEstFormData.objects.get(unique_display_no=udn, user=request.user)
    famEstDetails = utils.createFamEstDetails(famEst.family.id)
    return Response({'FamEstDetail': famEstDetails})


@api_view(['GET'])
def fam_est_detail(request):
    udn = request.query_params.get('FamEstFormDataUDN')
    if FamEstFormData.objects.filter(user=request.user, unique_display_no=udn).exists():
        famEst = FamEstFormData.objects.get(user=request.user, unique_display_no=udn)
        bob = utils.createFamEstDetails(famEst.family.id)
        # jane = bob.aggregate(Sum('law_firm_cost_sum'))
        # law fees canceld out
        return Response(bob)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_excel_report_fam_est_detail(request):
    udn = request.query_params.get('familyUDN')
    family = Family.objects.get(unique_display_no=udn, user=request.user)
    xls = create_excel_data(family.id)
    return xls


@api_view(['GET'])
def get_pdf_report_fam_est_detail(request):
    udn = request.query_params.get('familyUDN')
    family = Family.objects.get(unique_display_no=udn, user=request.user)
    pdf = create_pdf_report(family.id)
    return pdf


def create_excel_data(id):
    output = io.BytesIO()

    createXLSX.create_workbook(output, id)
    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
    family = Family.objects.get(id=id)
    filename = family.family_no + '-' + family.family_name
    response['Content-Disposition'] = f'attachment; filename=PatentEstimate-{filename}.xlsx'

    output.close()
    return response


def create_pdf_report(id):
    output = generate_pdf_report(id)
    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/pdf"
                            )
    family = Family.objects.get(id=id)
    filename = family.family_no + '-' + family.family_name
    response['Content-Disposition'] = f'attachment; filename=PatentEstimate-{filename}.pdf'

    output.close()
    return response
