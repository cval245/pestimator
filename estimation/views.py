from rest_framework import viewsets

from user.accesspolicies import StaffOnlyAccess
from user.permissions import DataPermission
from .models import BaseEstTemplate, FilingEstimateTemplate, LawFirmEstTemplate, PublicationEstTemplate, \
    OAEstimateTemplate, AllowanceEstTemplate, IssueEstTemplate, \
    LineEstimationTemplateConditions, USOAEstimateTemplate, ComplexConditions, ComplexTimeConditions, \
    RequestExamEstTemplate
from characteristics.models import FeeCategory
from .serializers import BaseEstTemplateSerializer, FilingEstimateTemplateSerializer, LawFirmEstTemplateSerializer, \
    PublicationEstTemplateSerializer, OAEstimateTemplateSerializer, \
    AllowanceEstTemplateSerializer, IssueEstTemplateSerializer, \
    ConditionsSerializer, USOAEstimateTemplateSerializer, ComplexConditionsSerializer, ComplexTimeConditionsSerializer, \
    RequestExamEstTemplateSerializer, FeeCategorySerializer


# Create your views here.
class BaseEstTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = BaseEstTemplateSerializer
    permission_classes = [StaffOnlyAccess]

    def get_queryset(self):
        return BaseEstTemplate.objects.all()


class FilingEstimateTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = FilingEstimateTemplateSerializer
    permission_classes = [StaffOnlyAccess]

    def get_queryset(self):
        return FilingEstimateTemplate.objects.all()


class PublicationEstTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = PublicationEstTemplateSerializer
    permission_classes = [StaffOnlyAccess]

    def get_queryset(self):
        return PublicationEstTemplate.objects.all()


class RequestExamEstTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = RequestExamEstTemplateSerializer
    permission_classes = [StaffOnlyAccess]

    def get_queryset(self):
        return RequestExamEstTemplate.objects.all()


class OAEstimateTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = OAEstimateTemplateSerializer
    permission_classes = [StaffOnlyAccess]

    def get_queryset(self):
        return OAEstimateTemplate.objects.all()


class USOAEstimateTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = USOAEstimateTemplateSerializer
    permission_classes = [StaffOnlyAccess]

    def get_queryset(self):
        return USOAEstimateTemplate.objects.all()


class AllowanceEstTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = AllowanceEstTemplateSerializer
    permission_classes = [StaffOnlyAccess]

    def get_queryset(self):
        return AllowanceEstTemplate.objects.all()


class IssueEstTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = IssueEstTemplateSerializer
    permission_classes = [StaffOnlyAccess]

    def get_queryset(self):
        return IssueEstTemplate.objects.all()


class LawFirmEstTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = LawFirmEstTemplateSerializer
    permission_classes = [StaffOnlyAccess]

    def get_queryset(self):
        return LawFirmEstTemplate.objects.all()


class ConditionsViewSet(viewsets.ModelViewSet):
    serializer_class = ConditionsSerializer
    permission_classes = [StaffOnlyAccess]

    def get_queryset(self):
        return LineEstimationTemplateConditions.objects.all()


class ComplexConditionsViewSet(viewsets.ModelViewSet):
    serializer_class = ComplexConditionsSerializer
    permission_classes = [StaffOnlyAccess]

    def get_queryset(self):
        return ComplexConditions.objects.all()


class ComplexTimeConditionsViewSet(viewsets.ModelViewSet):
    serializer_class = ComplexTimeConditionsSerializer
    permission_classes = [StaffOnlyAccess]

    def get_queryset(self):
        return ComplexTimeConditions.objects.all()


class FeeCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = FeeCategorySerializer
    permission_classes = [StaffOnlyAccess]

    def get_queryset(self):
        return FeeCategory.objects.all()
