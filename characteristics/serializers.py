from rest_framework import serializers

from .models import ApplType, Country, EntitySize, Language, EPValidationTranslationRequired, DocFormat, \
    DocFormatCountry, LanguageCountry, TranslationRequiredOptions


class GetLanguageCountrySerializer(serializers.Serializer):
    language = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), required=False)
    id = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), required=False)
    appl_type = serializers.PrimaryKeyRelatedField(
        queryset=ApplType.objects.all(),
        required=False
    )
    default = serializers.BooleanField()


class PostLanguageCountrySerializer(serializers.Serializer):
    language = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), required=False)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), required=False)
    appl_type = serializers.PrimaryKeyRelatedField(
        queryset=ApplType.objects.all(),
        required=False
    )
    default = serializers.BooleanField()


class GetDocFormatCountrySerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), required=False)
    doc_format = serializers.PrimaryKeyRelatedField(queryset=DocFormat.objects.all(), required=False)
    default = serializers.BooleanField()
    appl_type = serializers.PrimaryKeyRelatedField(
        queryset=ApplType.objects.all(),
        required=False
    )


class PostDocFormatCountrySerializer(serializers.Serializer):
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), required=False)
    doc_format = serializers.PrimaryKeyRelatedField(queryset=DocFormat.objects.all(), required=False)
    default = serializers.BooleanField()
    appl_type = serializers.PrimaryKeyRelatedField(
        queryset=ApplType.objects.all(),
        required=False
    )


class ApplTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplType
        fields = ('id', 'application_type', 'long_name', 'country_set', 'internal_bool')


class CountrySerializer(serializers.ModelSerializer):
    available_appl_types = serializers.PrimaryKeyRelatedField(queryset=ApplType.objects.all(), many=True,
                                                              allow_null=True)
    # available_entity_sizes = serializers.PrimaryKeyRelatedField(queryset=EntitySize.objects.all(), many=True,
    #                                                             allow_null=True)
    isa_countries = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), many=True, allow_null=True)
    available_languages = GetLanguageCountrySerializer(source='get_languages', many=True)
    available_doc_formats = GetDocFormatCountrySerializer(source='get_country_formats', many=True)
    ep_validation_translation_required = serializers.PrimaryKeyRelatedField(
        queryset=EPValidationTranslationRequired.objects.all(), read_only=False)

    class Meta:
        model = Country
        fields = ('id', 'country', 'currency_name', 'pct_accept_bool', 'pct_ro_bool',
                  'ep_bool', 'available_languages',
                  'available_appl_types', 'available_doc_formats',
                  'utility_translation_required',
                  'long_name', 'color', 'isa_countries',
                  'ep_validation_translation_required')


class CountryAllSerializer(serializers.ModelSerializer):
    available_appl_types = serializers.PrimaryKeyRelatedField(queryset=ApplType.objects.all(), many=True,
                                                              allow_null=True)
    available_languages = GetLanguageCountrySerializer(source='get_languages', many=True)
    available_doc_formats = GetDocFormatCountrySerializer(source='get_country_formats', many=True)
    isa_countries = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), many=True, allow_null=True)
    ep_validation_translation_required = serializers.PrimaryKeyRelatedField(
        queryset=EPValidationTranslationRequired.objects.all(), read_only=False)

    class Meta:
        model = Country
        fields = ('id', 'country', 'active_bool', 'currency_name', 'pct_accept_bool',
                  'pct_ro_bool',
                  'utility_translation_required',
                  'ep_bool', 'long_name', 'color', 'available_appl_types', 'isa_countries',
                  'available_languages', 'ep_validation_translation_required',
                  'available_doc_formats')


class CountryAllPostSerializer(serializers.ModelSerializer):
    available_appl_types = serializers.PrimaryKeyRelatedField(queryset=ApplType.objects.all(), many=True,
                                                              allow_null=True)
    available_doc_formats = PostDocFormatCountrySerializer(source='get_country_formats', many=True)
    available_languages = PostLanguageCountrySerializer(source='get_languages', many=True)
    isa_countries = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), many=True, allow_null=True)
    ep_validation_translation_required = serializers.PrimaryKeyRelatedField(
        queryset=EPValidationTranslationRequired.objects.all(), read_only=False)

    class Meta:
        model = Country
        fields = ('id', 'country', 'active_bool', 'currency_name', 'pct_accept_bool',
                  'pct_ro_bool',
                  'utility_translation_required',
                  'ep_bool', 'long_name', 'color', 'available_appl_types', 'isa_countries',
                  'available_languages', 'ep_validation_translation_required',
                  'available_doc_formats')

    def update(self, instance, validated_data):
        instance.country = validated_data['country']
        instance.currency_name = validated_data['currency_name']
        instance.pct_accept_bool = validated_data['pct_accept_bool']
        instance.long_name = validated_data['long_name']
        instance.active_bool = validated_data['active_bool']
        instance.ep_bool = validated_data['ep_bool']
        instance.color = validated_data['color']
        isa_countries = []
        for c in validated_data['isa_countries']:
            isa_countries.append(Country.objects.get(id=c))
        instance.isa_countries.set(isa_countries)
        ep_validation_translation_required = EPValidationTranslationRequired(
            id=validated_data['ep_validation_translation_required'])
        instance.ep_validation_translation_required = ep_validation_translation_required
        instance.utility_translation_required = TranslationRequiredOptions(
            id=validated_data['utility_translation_required'])
        instance.available_appl_types.set(validated_data['available_appl_types'])
        available_doc_formats = []
        instance.available_doc_formats.clear()
        for c in validated_data['available_doc_formats']:
            ec = DocFormatCountry.objects.get_or_create(
                country_id=instance.id,
                appl_type_id=c['appl_type'],
                doc_format_id=c['doc_format'],
            )
            dc = ec[0]
            if c['default']:
                dc.default = c['default']
                dc.save()
            available_doc_formats.append(dc)

        available_languages = []
        instance.available_languages.clear()
        for c in validated_data['available_languages']:
            ec = LanguageCountry.objects.get_or_create(
                country_id=instance.id,
                appl_type_id=c['appl_type'],
                language_id=c['language'],
            )
            dc = ec[0]
            if c['default']:
                dc.default = c['default']
                dc.save()
            available_languages.append(dc)
        instance.save()
        return instance


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EntitySize
        fields = ('id', 'entity_size', 'description', 'default_bool', 'country')


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name',)


class EPValidationTranslationRequiredSerializer(serializers.ModelSerializer):
    class Meta:
        model = EPValidationTranslationRequired
        fields = ('id', 'name')


class TranslationRequiredOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationRequiredOptions
        fields = ('id', 'name')


class DocFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocFormat
        fields = ('id', 'name')
