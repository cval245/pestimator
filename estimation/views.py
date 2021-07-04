from django.shortcuts import render
from rest_framework import viewsets

from .models import BaseEstTemplate, FilingEstimateTemplate, PublicationEstTemplate,\
	OAEstimateTemplate, AllowanceEstTemplate, IssueEstTemplate

from .serializers import BaseEstTemplateSerializer, FilingEstimateTemplateSerializer, \
	PublicationEstTemplateSerializer, OAEstimateTemplateSerializer,\
	 AllowanceEstTemplateSerializer, IssueEstTemplateSerializer


# Create your views here.
class BaseEstTemplateViewSet(viewsets.ModelViewSet):
	serializer_class = BaseEstTemplateSerializer

	def get_queryset(self):
		return BaseEstTemplate.objects.all()

class FilingEstimateTemplateViewSet(viewsets.ModelViewSet):
	serializer_class = FilingEstimateTemplateSerializer

	def get_queryset(self):
		return FilingEstimateTemplate.objects.all()

class PublicationEstTemplateViewSet(viewsets.ModelViewSet):

	def get_queryset(self):
		return PublicationEstTemplate.objects.all()

class OAEstimateTemplateViewSet(viewsets.ModelViewSet):

	def get_queryset(self):
		return OAEstimateTemplate.objects.all()

class AllowanceEstTemplateViewSet(viewsets.ModelViewSet):

	def get_queryset(self):
		return AllowanceEstTemplate.objects.all()

class IssueEstTemplateViewSet(viewsets.ModelViewSet):

	def get_queryset(self):
		return IssueEstTemplate.objects.all()

