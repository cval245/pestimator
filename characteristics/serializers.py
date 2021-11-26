from rest_framework import serializers

from .models import ApplType, Country, EntitySize, Languages, EPValidationTranslationRequired, DocFormat


class ApplTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplType
        fields = ('id', 'application_type', 'long_name', 'country_set')


class CountrySerializer(serializers.ModelSerializer):
    available_appl_types = serializers.PrimaryKeyRelatedField(queryset=ApplType.objects.all(), many=True,
                                                              allow_null=True)
    available_entity_sizes = serializers.PrimaryKeyRelatedField(queryset=EntitySize.objects.all(), many=True,
                                                                allow_null=True)
    available_doc_formats = serializers.PrimaryKeyRelatedField(queryset=DocFormat.objects.all(), many=True,
                                                               allow_null=True)
    isa_countries = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), many=True, allow_null=True)

    class Meta:
        model = Country
        fields = ('id', 'country', 'currency_name', 'pct_accept_bool', 'pct_ro_bool', 'ep_bool',
                  'available_appl_types', 'available_doc_formats',
                  'long_name', 'color', 'isa_countries', 'languages_set', 'ep_validation_translation_required',
                  'entity_size_available', 'available_entity_sizes')


class CountryAllSerializer(serializers.ModelSerializer):
    available_appl_types = serializers.PrimaryKeyRelatedField(queryset=ApplType.objects.all(), many=True,
                                                              allow_null=True)
    available_entity_sizes = serializers.PrimaryKeyRelatedField(queryset=EntitySize.objects.all(), many=True,
                                                                allow_null=True)
    available_doc_formats = serializers.PrimaryKeyRelatedField(queryset=DocFormat.objects.all(), many=True,
                                                               allow_null=True)
    isa_countries = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), many=True, allow_null=True)
    ep_validation_translation_required = serializers.PrimaryKeyRelatedField(
        queryset=EPValidationTranslationRequired.objects.all(), read_only=False)

    class Meta:
        model = Country
        fields = ('id', 'country', 'active_bool', 'currency_name', 'pct_accept_bool', 'pct_ro_bool',
                  'ep_bool', 'long_name', 'color', 'available_appl_types', 'isa_countries',
                  'languages_set', 'ep_validation_translation_required', 'entity_size_available',
                  'available_entity_sizes', 'available_doc_formats')


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EntitySize
        fields = ('id', 'entity_size', 'description')


class LanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = ('id', 'name', 'country')


class EPValidationTranslationRequiredSerializer(serializers.ModelSerializer):
    class Meta:
        model = EPValidationTranslationRequired
        fields = ('id', 'name', 'applicable_bool')


class DocFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocFormat
        fields = ('id', 'name')
