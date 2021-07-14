from rest_framework import serializers
from .models import BaseEstTemplate, FilingEstimateTemplate, LawFirmEstTemplate, PublicationEstTemplate,\
	OAEstimateTemplate, AllowanceEstTemplate, IssueEstTemplate


class BaseEstTemplateSerializer(serializers.ModelSerializer):
	class Meta:
		model = BaseEstTemplate
		fields = ('id', 'official_cost', 'date_diff', 'country', 
			'appl_type', 'conditions', 'law_firm_template')

class FilingEstimateTemplateSerializer(serializers.ModelSerializer):
	class Meta:
		model = FilingEstimateTemplate
		fields = ('id', 'official_cost', 'date_diff', 'country', 
			'appl_type', 'conditions', 'law_firm_template')

class PublicationEstTemplateSerializer(serializers.ModelSerializer):
	class Meta:
		model = PublicationEstTemplate
		fields = ('id', 'official_cost', 'date_diff', 'country', 
			'appl_type', 'conditions', 'law_firm_template')


class OAEstimateTemplateSerializer(serializers.ModelSerializer):
	class Meta:
		model = OAEstimateTemplate
		fields = ('id', 'official_cost', 'date_diff', 'country', 
			'appl_type', 'conditions', 'law_firm_template')


class AllowanceEstTemplateSerializer(serializers.ModelSerializer):
	class Meta:
		model = AllowanceEstTemplate
		fields = ('id', 'official_cost', 'date_diff', 'country', 
			'appl_type', 'conditions', 'law_firm_template')

class IssueEstTemplateSerializer(serializers.ModelSerializer):
	class Meta:
		model = IssueEstTemplate
		fields = ('id', 'official_cost', 'date_diff', 'country', 
			'appl_type', 'conditions', 'law_firm_template')

class LawFirmEstTemplateSerializer(serializers.ModelSerializer):
	class Meta:
		model = LawFirmEstTemplate
		fields = ('id', 'law_firm_cost', 'date_diff')
    
