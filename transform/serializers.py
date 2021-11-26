from rest_framework import serializers
from .models import CustomFilingTransform, PublicationTransform, OATransform, \
	AllowanceTransform, IssueTransform, CountryOANum, USOATransform, TransComplexTime, RequestExaminationTransform


class TransComplexTimeSerializer(serializers.ModelSerializer):
	class Meta:
		model = TransComplexTime
		fields = ('id', 'name')


class CustomFilingTransformSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomFilingTransform
		fields = ('id', 'date_diff', 'country', 'appl_type', 'prev_appl_type', 'complex_time_conditions')


class PublicationTransformSerializer(serializers.ModelSerializer):
	class Meta:
		model = PublicationTransform
		fields = ('id', 'date_diff', 'country', 'complex_time_conditions')


class RequestExaminationTransformSerializer(serializers.ModelSerializer):
	class Meta:
		model = RequestExaminationTransform
		fields = ('id', 'date_diff', 'country', 'complex_time_conditions')


class OATransformSerializer(serializers.ModelSerializer):
	class Meta:
		model = OATransform
		fields = ('id', 'date_diff', 'country', 'complex_time_conditions')


class USOATransformSerializer(serializers.ModelSerializer):
	class Meta:
		model = USOATransform
		fields = ('id', 'date_diff', 'country', 'final_oa_bool', 'complex_time_conditions')


class AllowanceTransformSerializer(serializers.ModelSerializer):
	class Meta:
		model = AllowanceTransform
		fields = ('id', 'date_diff', 'country', 'complex_time_conditions')

class IssueTransformSerializer(serializers.ModelSerializer):
	class Meta:
		model = IssueTransform
		fields = ('id', 'date_diff', 'country', 'complex_time_conditions')

class CountryOANumSerializer(serializers.ModelSerializer):
	class Meta:
		model = CountryOANum
		fields = ('id', 'country', 'oa_total')
