from django.shortcuts import render
from rest_framework import viewsets
from .models import CustomFilingTransform, PublicationTransform, OATransform,\
 AllowanceTransform, IssueTransform, CountryOANum

from .serializers import CustomFilingTransformSerializer,\
 PublicationTransformSerializer, OATransformSerializer, \
 AllowanceTransformSerializer, IssueTransformSerializer,\
 CountryOANumSerializer 

class CustomFilingTransformViewSet(viewsets.ModelViewSet):
 	serializer_class = CustomFilingTransformSerializer

 	def get_queryset(self):
 		return CustomFilingTransform.objects.all()


class PublicationTransformViewSet(viewsets.ModelViewSet):
 	serializer_class = PublicationTransformSerializer

 	def get_queryset(self):
 		return PublicationTransform.objects.all()

class OATransformViewSet(viewsets.ModelViewSet):
 	serializer_class = OATransformSerializer

 	def get_queryset(self):
 		return OATransform.objects.all()

class AllowanceTransformViewSet(viewsets.ModelViewSet):
 	serializer_class = AllowanceTransformSerializer

 	def get_queryset(self):
 		return AllowanceTransform.objects.all()		

class IssueTransformViewSet(viewsets.ModelViewSet):
 	serializer_class = IssueTransformSerializer

 	def get_queryset(self):
 		return IssueTransform.objects.all()

class CountryOANumViewSet(viewsets.ModelViewSet):
 	serializer_class = CountryOANumSerializer

 	def get_queryset(self):
 		return CountryOANum.objects.all()		