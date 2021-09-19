from django.shortcuts import render
from rest_framework import viewsets

from user.permissions import DataPermission
from .models import CustomFilingTransform, PublicationTransform, OATransform, \
    AllowanceTransform, IssueTransform, CountryOANum, USOATransform

from .serializers import CustomFilingTransformSerializer, \
    PublicationTransformSerializer, OATransformSerializer, \
    AllowanceTransformSerializer, IssueTransformSerializer, \
    CountryOANumSerializer, USOATransformSerializer


class CustomFilingTransformViewSet(viewsets.ModelViewSet):
    serializer_class = CustomFilingTransformSerializer
    permission_classes = [DataPermission]

    def get_queryset(self):
        return CustomFilingTransform.objects.all()


class PublicationTransformViewSet(viewsets.ModelViewSet):
    serializer_class = PublicationTransformSerializer
    permission_classes = [DataPermission]

    def get_queryset(self):
        return PublicationTransform.objects.all()


class OATransformViewSet(viewsets.ModelViewSet):
    serializer_class = OATransformSerializer
    permission_classes = [DataPermission]

    def get_queryset(self):
        return OATransform.objects.all()


class AllowanceTransformViewSet(viewsets.ModelViewSet):
    serializer_class = AllowanceTransformSerializer
    permission_classes = [DataPermission]

    def get_queryset(self):
        return AllowanceTransform.objects.all()


class IssueTransformViewSet(viewsets.ModelViewSet):
    serializer_class = IssueTransformSerializer
    permission_classes = [DataPermission]

    def get_queryset(self):
        return IssueTransform.objects.all()


class CountryOANumViewSet(viewsets.ModelViewSet):
    serializer_class = CountryOANumSerializer
    permission_classes = [DataPermission]

    def get_queryset(self):
        return CountryOANum.objects.all()


class USOATransformViewSet(viewsets.ModelViewSet):
    serializer_class = USOATransformSerializer
    permission_classes = [DataPermission]

    def get_queryset(self):
        return USOATransform.objects.all()

