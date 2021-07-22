from rest_framework import serializers
from .models import CustomFilingTransform, PublicationTransform, OATransform,\
 AllowanceTransform, IssueTransform, CountryOANum, USOATransform

class CustomFilingTransformSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomFilingTransform
		fields = ('id', 'date_diff', 'country', 'appl_type', 'prev_appl_type')


class PublicationTransformSerializer(serializers.ModelSerializer):
	class Meta:
		model = PublicationTransform
		fields = ('id', 'date_diff', 'country')

class OATransformSerializer(serializers.ModelSerializer):
	class Meta:
		model = OATransform
		fields = ('id', 'date_diff', 'country')


class USOATransformSerializer(serializers.ModelSerializer):
	class Meta:
		model = USOATransform
		fields = ('id', 'date_diff', 'country', 'final_oa_bool')


class AllowanceTransformSerializer(serializers.ModelSerializer):
	class Meta:
		model = AllowanceTransform
		fields = ('id', 'date_diff', 'country')

class IssueTransformSerializer(serializers.ModelSerializer):
	class Meta:
		model = IssueTransform
		fields = ('id', 'date_diff', 'country')

class CountryOANumSerializer(serializers.ModelSerializer):
	class Meta:
		model = CountryOANum
		fields = ('id', 'country', 'oa_total')
