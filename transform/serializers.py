from rest_framework import serializers
from .models import CustomFilingTransform, PublicationTransform, OATransform,\
 AllowanceTransform, IssueTransform, CountryOANum

class CustomFilingTransformSerializer(serializers.ModelSerializer):
 	class Meta:
 		model = CustomFilingTransform
 		fields = ('id', 'date_diff', 'country')


class PublicationTransformSerializer(serializers.ModelSerializer):
 	class Meta:
 		model = PublicationTransform
 		fields = ('id', 'date_diff', 'country')

class OATransformSerializer(serializers.ModelSerializer):
 	class Meta:
 		model = OATransform
 		fields = ('id', 'date_diff', 'country')

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
		fields = ('id', 'date_diff', 'country', 'oa_total')
