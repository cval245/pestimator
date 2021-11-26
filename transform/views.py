from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from characteristics.models import ApplType, Country
from user.accesspolicies import StaffOnlyAccess
from user.permissions import DataPermission
from .models import CustomFilingTransform, PublicationTransform, OATransform, \
    AllowanceTransform, IssueTransform, CountryOANum, USOATransform, TransComplexTime

from .serializers import CustomFilingTransformSerializer, \
    PublicationTransformSerializer, OATransformSerializer, \
    AllowanceTransformSerializer, IssueTransformSerializer, \
    CountryOANumSerializer, USOATransformSerializer, TransComplexTimeSerializer, RequestExaminationTransformSerializer


class TransComplexTimeViewSet(viewsets.ModelViewSet):
    serializer_class = TransComplexTimeSerializer
    permission_classes = (StaffOnlyAccess,)

    def get_queryset(self):
        return TransComplexTime.objects.all()


class CustomFilingTransformViewSet(viewsets.ModelViewSet):
    serializer_class = CustomFilingTransformSerializer
    permission_classes = (StaffOnlyAccess,)

    def get_queryset(self):
        return CustomFilingTransform.objects.all()


class PublicationTransformViewSet(viewsets.ModelViewSet):
    serializer_class = PublicationTransformSerializer
    permission_classes = (StaffOnlyAccess,)

    def get_queryset(self):
        return PublicationTransform.objects.all()


class RequestExaminationTransformViewSet(viewsets.ModelViewSet):
    serializer_class = RequestExaminationTransformSerializer
    permission_classes = (StaffOnlyAccess,)

    def get_queryset(self):
        return PublicationTransform.objects.all()


class OATransformViewSet(viewsets.ModelViewSet):
    serializer_class = OATransformSerializer
    permission_classes = (StaffOnlyAccess,)

    def get_queryset(self):
        return OATransform.objects.all()


class AllowanceTransformViewSet(viewsets.ModelViewSet):
    serializer_class = AllowanceTransformSerializer
    permission_classes = (StaffOnlyAccess,)

    def get_queryset(self):
        return AllowanceTransform.objects.all()


class IssueTransformViewSet(viewsets.ModelViewSet):
    serializer_class = IssueTransformSerializer
    permission_classes = (StaffOnlyAccess,)

    def get_queryset(self):
        return IssueTransform.objects.all()


class CountryOANumViewSet(viewsets.ModelViewSet):
    serializer_class = CountryOANumSerializer
    permission_classes = (StaffOnlyAccess,)

    def get_queryset(self):
        return CountryOANum.objects.all()


class USOATransformViewSet(viewsets.ModelViewSet):
    serializer_class = USOATransformSerializer
    permission_classes = (StaffOnlyAccess,)

    def get_queryset(self):
        return USOATransform.objects.all()


@api_view(['GET'])
def get_needed(request):
    # take country
    # retrieve and succeed
    countries = Country.objects.all()
    countries_list = []
    for c in countries:
        countries_list.append({'country': c.id, 'required_transforms': requiredFilingTransforms(c)})
    return Response(countries_list)


def requiredFilingTransforms(country):
    missingPairs = []
    cstmFilTrans = CustomFilingTransform.objects.filter(country=country)
    ep_appl_type = ApplType.objects.get(application_type='ep')
    epvalid_appl_type = ApplType.objects.get(application_type='epvalidation')
    pct_appl_type = ApplType.objects.get(application_type='pct')
    natphase_appl_type = ApplType.objects.get(application_type='nationalphase')
    prov_appl_type = ApplType.objects.get(application_type='prov')
    utility_appl_type = ApplType.objects.get(application_type='utility')

    available_appl_types = country.available_appl_types.all()

    for a in available_appl_types:
        transApplTypes = list(filter(lambda x: x.appl_type == a, cstmFilTrans))
        if a == prov_appl_type:
            checkThenAddApplType(a, None, transApplTypes, missingPairs)
            pass
        if a == pct_appl_type:
            checkThenAddApplType(a, None, transApplTypes, missingPairs)
            checkThenAddApplType(a, utility_appl_type, transApplTypes, missingPairs)
            checkThenAddApplType(a, ep_appl_type, transApplTypes, missingPairs)
        if a == natphase_appl_type:
            checkThenAddApplType(a, pct_appl_type, transApplTypes, missingPairs)
        if a == utility_appl_type:
            checkThenAddApplType(a, None, transApplTypes, missingPairs)
            checkThenAddApplType(a, prov_appl_type, transApplTypes, missingPairs)
            checkThenAddApplType(a, ep_appl_type, transApplTypes, missingPairs)
            checkThenAddApplType(a, utility_appl_type, transApplTypes, missingPairs)
            checkThenAddApplType(a, pct_appl_type, transApplTypes, missingPairs)
        if a == ep_appl_type:
            checkThenAddApplType(a, None, transApplTypes, missingPairs)
            checkThenAddApplType(a, prov_appl_type, transApplTypes, missingPairs)
            checkThenAddApplType(a, utility_appl_type, transApplTypes, missingPairs)
            checkThenAddApplType(a, pct_appl_type, transApplTypes, missingPairs)
        if a == epvalid_appl_type:
            checkThenAddApplType(a, ep_appl_type, transApplTypes, missingPairs)
    return missingPairs


def checkThenAddApplType(appl_type, prev_appl_type, transApplTypes, missingPairs):
    if len(list(filter(lambda x: x.prev_appl_type == prev_appl_type, transApplTypes))) == 0:
        if prev_appl_type:
            missingPairs.append({'prev_appl_type': prev_appl_type.id, 'appl_type': appl_type.id})
        else:
            missingPairs.append({'prev_appl_type': prev_appl_type, 'appl_type': appl_type.id})

# for item in appl_types
