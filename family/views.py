import io
import uuid

from djmoney.models.fields import MoneyField
from django.db.models import ExpressionWrapper, F, Q, Sum, Value, DateTimeField
from django.db.models.functions import Cast, Coalesce, Round
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from famform.models import FamEstFormData
from user.accesspolicies import GetOnlyPolicy, StaffOnlyAccess, StaffOnlyPost, AuthenticatedGetAccess
from user.models import User
from . import utils, createXLSX
from .createPDF import generate_pdf_report
from .models import Family
from .serializers import FamilySerializer


# Create your views here.
class FamilyAllViewSet(viewsets.ModelViewSet):
    serializer_class = FamilySerializer
    permission_classes(StaffOnlyAccess)

    def get_queryset(self):
        queryset = Family.objects.all()
        fam_est_form_data_udn = self.request.query_params.get('FamEstFormDataUDN')
        if fam_est_form_data_udn is not None:
            if queryset.filter(user=self.request.user,
                               famestformdata__unique_display_no=fam_est_form_data_udn).exists():
                queryset = queryset.filter(
                    user=self.request.user,
                    famestformdata__unique_display_no=fam_est_form_data_udn)
        return queryset


class FamilyViewSet(viewsets.ModelViewSet):
    serializer_class = FamilySerializer
    permission_classes(StaffOnlyPost)

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
@permission_classes([AuthenticatedGetAccess])
def fam_est_get_tot_costs(request):
    queryset = Family.objects.filter(user=request.user)
    family_udn = request.query_params.get('familyUDN')
    if family_udn is not None:
        if queryset.filter(user=request.user,
                           unique_display_no=family_udn).exists():
            family_id = queryset.get(
                user=request.user,
                unique_display_no=family_udn).id
            famEstTot = utils.get_total_costs(family_id)
            for item in famEstTot:
                item['id'] = uuid.uuid4()
            return Response(famEstTot)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AuthenticatedGetAccess])
def fam_est_all(request):
    famEsts = utils.getFamEstAll(request.user)
    return Response(famEsts)


@api_view(['GET'])
@permission_classes([StaffOnlyAccess])
def fam_est_all_specific_user(request):
    user_id = request.query_params.get('user_id')
    famEsts = utils.getFamEstAll(user_id)
    return Response(famEsts)


# Create your views here.
@api_view(['GET'])
@permission_classes((GetOnlyPolicy,))
def get_open_estimates(request):
    user = User.objects.get(username='guest')
    date = FamEstFormData.objects.filter(user=user).order_by('-date_created').first().date_created  # .date()
    famEsts = Family.objects.filter(user=user,
                                    famestformdata__date_created__day=date.day,
                                    famestformdata__date_created__month=date.month,
                                    famestformdata__date_created__year=date.year) \
        .order_by('-famestformdata__date_created') \
        .annotate(
        famestformdata_udn=F('famestformdata__unique_display_no'),
        country=F('famestformdata__init_appl_country'),
        date_created=Cast('famestformdata__date_created', output_field=DateTimeField()),
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
    ) \
        .values(
        'id', 'official_cost', 'law_firm_cost', 'translation_cost', 'total_cost',
        'famestformdata', 'famestformdata_udn',
        'family_name', 'family_no', 'country')

    country_list = []
    filtered_famEsts = []
    for est in famEsts:
        if est['country'] not in country_list:
            country_list.append(est['country'])
            filtered_famEsts.append(est)
    return Response(filtered_famEsts)


@api_view(['GET'])
@permission_classes([GetOnlyPolicy])
def fam_est_detail_guest(request):
    udn = request.query_params.get('FamEstFormDataUDN')
    user = User.objects.get(username='guest')
    if FamEstFormData.objects.filter(user=user, unique_display_no=udn).exists():
        famEst = FamEstFormData.objects.get(user=user, unique_display_no=udn)
        bob = utils.createFamEstDetails(famEst.family.id)
        return Response(bob)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AuthenticatedGetAccess])
def fam_est_detail(request):
    udn = request.query_params.get('FamEstFormDataUDN')
    if FamEstFormData.objects.filter(user=request.user, unique_display_no=udn).exists():
        famEst = FamEstFormData.objects.get(user=request.user, unique_display_no=udn)
        bob = utils.createFamEstDetails(famEst.family.id)
        return Response(bob)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AuthenticatedGetAccess])
def get_excel_report_fam_est_detail(request):
    udn = request.query_params.get('familyUDN')
    family = Family.objects.get(unique_display_no=udn, user=request.user)
    xls = create_excel_data(family.id)
    return xls


@api_view(['GET'])
@permission_classes([AuthenticatedGetAccess])
def get_pdf_report_fam_est_detail(request):
    udn = request.query_params.get('familyUDN')
    family = Family.objects.get(unique_display_no=udn, user=request.user)
    pdf = create_pdf_report(family.id)
    return pdf


@api_view(['GET'])
@permission_classes([GetOnlyPolicy])
def get_free_pdf_report_fam_est_detail(request, udn):
    user = User.objects.get(username='guest')
    fam_est_form_data = FamEstFormData.objects.get(unique_display_no=udn, user=user)
    country = fam_est_form_data.init_appl_country
    with open('staticfiles/free_estimates/pdf/' + str(country.country) + '.pdf', 'rb') as file:
        response = HttpResponse(file.read(), content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename=PatentEstimate-{country.country}.pdf'
        return response


@api_view(['GET'])
@permission_classes([GetOnlyPolicy])
def get_free_xls_report_fam_est_detail(request, udn):
    user = User.objects.get(username='guest')
    fam_est_form_data = FamEstFormData.objects.get(unique_display_no=udn, user=user)
    country = fam_est_form_data.init_appl_country
    with open('staticfiles/free_estimates/excel/' + str(country.country) + '.xlsx', 'rb') as file:
        response = HttpResponse(file.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        response['Content-Disposition'] = f'attachment; filename=PatentEstimate-{country.country}.xlsx'
        return response


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
