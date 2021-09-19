from rest_framework import serializers

from .models import BaseEstTemplate, FilingEstimateTemplate, LawFirmEstTemplate, LineEstimationTemplateConditions, \
	PublicationEstTemplate, \
	OAEstimateTemplate, AllowanceEstTemplate, IssueEstTemplate, USOAEstimateTemplate, ComplexConditions, \
	ComplexTimeConditions


class BaseEstTemplateSerializer(serializers.ModelSerializer):
	class Meta:
		model = BaseEstTemplate
		fields = ('id', 'official_cost', 'date_diff', 'country',
				  'appl_type', 'conditions', 'law_firm_template',
				  'description', 'fee_code'
				  )


class FilingEstimateTemplateSerializer(serializers.ModelSerializer):
	class Meta:
		model = FilingEstimateTemplate
		fields = ('id', 'official_cost', 'date_diff', 'country',
				  'description', 'fee_code',
				  'appl_type', 'conditions', 'law_firm_template')


class PublicationEstTemplateSerializer(serializers.ModelSerializer):
	class Meta:
		model = PublicationEstTemplate
		fields = ('id', 'official_cost', 'date_diff', 'country',
				  'description', 'fee_code',
				  'appl_type', 'conditions', 'law_firm_template')


class OAEstimateTemplateSerializer(serializers.ModelSerializer):
	class Meta:
		model = OAEstimateTemplate
		fields = ('id', 'official_cost', 'date_diff', 'country',
				  'description', 'fee_code',
				  'appl_type', 'conditions', 'law_firm_template')


class USOAEstimateTemplateSerializer(serializers.ModelSerializer):
	class Meta:
		model = USOAEstimateTemplate
		fields = ('id', 'official_cost', 'date_diff', 'country', 'oa_final_bool',
				  'oa_first_final_bool',
				  'description', 'fee_code',
				  'appl_type', 'conditions', 'law_firm_template')


class AllowanceEstTemplateSerializer(serializers.ModelSerializer):
	class Meta:
		model = AllowanceEstTemplate
		fields = ('id', 'official_cost', 'date_diff', 'country',
				  'description', 'fee_code',
				  'appl_type', 'conditions', 'law_firm_template')


class IssueEstTemplateSerializer(serializers.ModelSerializer):
	class Meta:
		model = IssueEstTemplate
		fields = ('id', 'official_cost', 'date_diff', 'country',
				  'description', 'fee_code',
				  'appl_type', 'conditions', 'law_firm_template')


class LawFirmEstTemplateSerializer(serializers.ModelSerializer):
	class Meta:
		model = LawFirmEstTemplate
		fields = ('id', 'law_firm_cost', 'date_diff')


class ConditionsSerializer(serializers.ModelSerializer):
	class Meta:
		model = LineEstimationTemplateConditions
		fields = ('id',
                  'condition_annual_prosecution_fee',
                  'condition_claims_min', 'condition_claims_max',
                  'condition_indep_claims_min', 'condition_indep_claims_max',
                  'condition_pages_min', 'condition_pages_max',
                  'condition_pages_desc_min', 'condition_pages_desc_max',
                  'condition_drawings_min', 'condition_drawings_max',
                  'condition_entity_size',
                  'condition_time_complex', 'condition_complex',
                  'prior_pct_same_country', 'prior_pct',
                  'prev_appl_date_excl_intermediary_time')


class ComplexConditionsSerializer(serializers.ModelSerializer):
	class Meta:
		model = ComplexConditions
		fields = ('id', 'name')


class ComplexTimeConditionsSerializer(serializers.ModelSerializer):
	class Meta:
		model = ComplexTimeConditions
		fields = ('id', 'name')
