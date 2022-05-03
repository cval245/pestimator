from rest_framework import serializers

from .models import BaseEstTemplate, FilingEstimateTemplate, LawFirmEstTemplate, LineEstimationTemplateConditions, \
    PublicationEstTemplate, \
    OAEstimateTemplate, AllowanceEstTemplate, IssueEstTemplate, USOAEstimateTemplate, ComplexConditions, \
    ComplexTimeConditions, RequestExamEstTemplate
from characteristics.models import ApplType, DetailedFeeCategory, FeeCategory


class BaseEstTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseEstTemplate
        fields = ('id', 'official_cost', 'official_cost_currency', 'date_diff', 'country',
                  'detailed_fee_category',
                  'fee_category',
                  'date_enabled', 'date_disabled',
                  'appl_type', 'conditions', 'law_firm_template',
                  'description', 'fee_code')


class FilingEstimateTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilingEstimateTemplate
        fields = ('id', 'official_cost', 'official_cost_currency', 'date_diff', 'country',
                  'detailed_fee_category',
                  'date_enabled', 'date_disabled',
                  'fee_category', 'description', 'fee_code',
                  'appl_type', 'conditions', 'law_firm_template')


class PublicationEstTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationEstTemplate
        fields = ('id', 'official_cost', 'official_cost_currency', 'date_diff', 'country',
                  'detailed_fee_category',
                  'fee_category',
                  'date_enabled', 'date_disabled',
                  'description', 'fee_code',
                  'appl_type', 'conditions', 'law_firm_template')


class RequestExamEstTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestExamEstTemplate
        fields = ('id', 'official_cost', 'official_cost_currency', 'date_diff', 'country',
                  'detailed_fee_category',
                  'fee_category',
                  'date_enabled', 'date_disabled',
                  'description', 'fee_code',
                  'appl_type', 'conditions', 'law_firm_template')


class OAEstimateTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OAEstimateTemplate
        fields = ('id', 'official_cost', 'official_cost_currency', 'date_diff', 'country',
                  'detailed_fee_category',
                  'date_enabled', 'date_disabled',
                  'fee_category', 'description', 'fee_code',
                  'appl_type', 'conditions', 'law_firm_template')


class USOAEstimateTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = USOAEstimateTemplate
        fields = ('id', 'official_cost', 'official_cost_currency', 'date_diff', 'country', 'oa_final_bool',
                  'detailed_fee_category',
                  'fee_category',
                  'date_enabled', 'date_disabled',
                  'oa_first_final_bool',
                  'description', 'fee_code',
                  'appl_type', 'conditions', 'law_firm_template')


class AllowanceEstTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllowanceEstTemplate
        fields = ('id', 'official_cost', 'official_cost_currency', 'date_diff', 'country',
                  'detailed_fee_category',
                  'date_enabled', 'date_disabled',
                  'fee_category',
                  'description', 'fee_code',
                  'appl_type', 'conditions', 'law_firm_template')


class IssueEstTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueEstTemplate
        fields = ('id', 'official_cost', 'official_cost_currency', 'date_diff', 'country',
                  'detailed_fee_category',
                  'date_enabled', 'date_disabled',
                  'fee_category',
                  'description', 'fee_code',
                  'appl_type', 'conditions', 'law_firm_template')


class LawFirmEstTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawFirmEstTemplate
        fields = ('id', 'law_firm_cost', 'law_firm_cost_currency', 'date_diff')


class ConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineEstimationTemplateConditions
        fields = ('id',
                  'condition_annual_prosecution_fee',
                  'condition_annual_prosecution_fee_until_grant',
                  'condition_renewal_fee_from_filing_of_prior_after_grant',
                  'condition_renewal_fee_from_filing_after_grant',
                  'condition_claims_min', 'condition_claims_max',
                  'condition_claims_multiple_dependent_min', 'condition_claims_multiple_dependent_max',
                  'condition_indep_claims_min', 'condition_indep_claims_max',
                  'condition_pages_total_min', 'condition_pages_total_max',
                  'condition_pages_desc_min', 'condition_pages_desc_max',
                  'condition_pages_claims_min', 'condition_pages_claims_max',
                  'condition_pages_drawings_min', 'condition_pages_drawings_max',
                  'condition_drawings_min', 'condition_drawings_max',
                  'condition_entity_size',
                  'condition_time_complex', 'condition_complex',
                  'prior_pct_same_country', 'prior_pct',
                  'prior_appl_exists',
                  'isa_country_fee_only',
                  'prev_appl_date_excl_intermediary_time', 'doc_format',
                  'language')


class ComplexConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplexConditions
        fields = ('id', 'name')


class ComplexTimeConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplexTimeConditions
        fields = ('id', 'name')


class FeeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeCategory
        fields = ('id', 'name')


class DetailedFeeCategorySerializer(serializers.ModelSerializer):
    appl_types = serializers.PrimaryKeyRelatedField(many=True, queryset=ApplType.objects.all())

    class Meta:
        model = DetailedFeeCategory
        fields = ('id', 'name', 'country', 'appl_types')
