from rest_framework import viewsets

from .models import BaseEstTemplate, FilingEstimateTemplate, LawFirmEstTemplate, PublicationEstTemplate, \
	OAEstimateTemplate, AllowanceEstTemplate, IssueEstTemplate, \
	LineEstimationTemplateConditions, USOAEstimateTemplate
from .serializers import BaseEstTemplateSerializer, FilingEstimateTemplateSerializer, LawFirmEstTemplateSerializer, \
	PublicationEstTemplateSerializer, OAEstimateTemplateSerializer, \
	AllowanceEstTemplateSerializer, IssueEstTemplateSerializer, \
	ConditionsSerializer, USOAEstimateTemplateSerializer


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
	serializer_class = PublicationEstTemplateSerializer

	def get_queryset(self):
		return PublicationEstTemplate.objects.all()


class OAEstimateTemplateViewSet(viewsets.ModelViewSet):
	serializer_class = OAEstimateTemplateSerializer

	def get_queryset(self):
		return OAEstimateTemplate.objects.all()


class USOAEstimateTemplateViewSet(viewsets.ModelViewSet):
	serializer_class = USOAEstimateTemplateSerializer

	def get_queryset(self):
		return USOAEstimateTemplate.objects.all()


class AllowanceEstTemplateViewSet(viewsets.ModelViewSet):
	serializer_class = AllowanceEstTemplateSerializer

	def get_queryset(self):
		return AllowanceEstTemplate.objects.all()


class IssueEstTemplateViewSet(viewsets.ModelViewSet):
	serializer_class = IssueEstTemplateSerializer

	def get_queryset(self):
		return IssueEstTemplate.objects.all()

class LawFirmEstTemplateViewSet(viewsets.ModelViewSet):
	serializer_class = LawFirmEstTemplateSerializer 

	def get_queryset(self):
		return LawFirmEstTemplate.objects.all()

class ConditionsViewSet(viewsets.ModelViewSet):
	serializer_class = ConditionsSerializer

	def get_queryset(self):
		return LineEstimationTemplateConditions.objects.all()
	