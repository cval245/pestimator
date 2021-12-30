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
		fields = ('id', 'date_diff', 'country', 'appl_type', 'prev_appl_type', 'trans_complex_time_condition')


class PublicationTransformSerializer(serializers.ModelSerializer):
	class Meta:
		model = PublicationTransform
		fields = ('id', 'date_diff', 'country', 'appl_type', 'trans_complex_time_condition')


class RequestExaminationTransformSerializer(serializers.ModelSerializer):
	class Meta:
		model = RequestExaminationTransform
		fields = ('id', 'date_diff', 'country', 'appl_type', 'trans_complex_time_condition')


class OATransformSerializer(serializers.ModelSerializer):
	class Meta:
		model = OATransform
		fields = ('id', 'date_diff', 'country', 'appl_type', 'trans_complex_time_condition')


class USOATransformSerializer(serializers.ModelSerializer):
	class Meta:
		model = USOATransform
		fields = ('id', 'date_diff', 'country', 'appl_type', 'final_oa_bool', 'trans_complex_time_condition')


class AllowanceTransformSerializer(serializers.ModelSerializer):
	class Meta:
		model = AllowanceTransform
		fields = ('id', 'date_diff', 'country', 'appl_type', 'trans_complex_time_condition')

class IssueTransformSerializer(serializers.ModelSerializer):
	class Meta:
		model = IssueTransform
		fields = ('id', 'date_diff', 'country', 'appl_type', 'trans_complex_time_condition')

class CountryOANumSerializer(serializers.ModelSerializer):
	class Meta:
		model = CountryOANum
		fields = ('id', 'country', 'oa_total', 'appl_type')
