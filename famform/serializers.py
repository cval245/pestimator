from rest_framework import serializers

from application.models import ApplDetails
from application.serializers import ApplDetailSerializer
from characteristics.enums import ApplTypes
from characteristics.models import Country, EntitySize, ApplType, Language, DocFormat
from family.models import Family
from .models import FamEstFormData, PCTCountryCustomization, EPCountryCustomization, \
    ParisCountryCustomization, PCTMethodCustomization, EPMethodCustomization
from .models.CustomApplDetails import CustomApplDetails
from .models.CustomApplOptions import CustomApplOptions


class CustomApplOptionsSerializer(serializers.Serializer):
    request_examination_early_bool = serializers.BooleanField(required=True)
    doc_format = serializers.PrimaryKeyRelatedField(
        required=True,
        allow_null=True,
        queryset=DocFormat.objects.all())


class CustomApplDetailsSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    num_indep_claims = serializers.IntegerField(required=False, allow_null=True)
    num_claims = serializers.IntegerField(required=False, allow_null=True)
    num_claims_multiple_dependent = serializers.IntegerField(required=False, allow_null=True)
    num_drawings = serializers.IntegerField(required=False, allow_null=True)
    num_pages_description = serializers.IntegerField(required=False, allow_null=True)
    num_pages_drawings = serializers.IntegerField(required=False, allow_null=True)
    num_pages_claims = serializers.IntegerField(required=False, allow_null=True)
    entity_size = serializers.PrimaryKeyRelatedField(required=False, allow_null=True,
                                                     queryset=EntitySize.objects.all())
    language = serializers.PrimaryKeyRelatedField(required=False,
                                                  allow_null=True,
                                                  queryset=Language.objects.all())


class PCTMethodCustomizationSerializer(serializers.Serializer):
    custom_appl_details = CustomApplDetailsSerializer(required=False, allow_null=True)
    custom_appl_options = CustomApplOptionsSerializer(required=True)


class EPMethodCustomizationSerializer(serializers.Serializer):
    custom_appl_details = CustomApplDetailsSerializer(required=False, allow_null=True)
    custom_appl_options = CustomApplOptionsSerializer(required=True)


class GetPCTCountryCustomizationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    fam_est_form_data = serializers.PrimaryKeyRelatedField(read_only=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    custom_appl_details = CustomApplDetailsSerializer(required=True, allow_null=False)
    custom_appl_options = CustomApplOptionsSerializer(required=True, allow_null=False)


class PCTCountryCustomizationSerializer(serializers.Serializer):
    fam_est_form_data = serializers.PrimaryKeyRelatedField(read_only=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),
                                                 required=False)
    custom_appl_details = CustomApplDetailsSerializer(required=False, allow_null=True)
    custom_appl_options = CustomApplOptionsSerializer(required=False, allow_null=True)


class GetEPCountryCustomizationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    fam_est_form_data = serializers.PrimaryKeyRelatedField(read_only=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    custom_appl_details = CustomApplDetailsSerializer(required=True, allow_null=False)
    custom_appl_options = CustomApplOptionsSerializer(required=True, allow_null=False)


class EPCountryCustomizationSerializer(serializers.Serializer):
    fam_est_form_data = serializers.PrimaryKeyRelatedField(read_only=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),
                                                 required=False)
    custom_appl_details = CustomApplDetailsSerializer(required=False, allow_null=True)
    custom_appl_options = CustomApplOptionsSerializer(required=False, allow_null=True)


class GetParisCountryCustomizationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    fam_est_form_data = serializers.PrimaryKeyRelatedField(read_only=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    custom_appl_details = CustomApplDetailsSerializer(required=True, allow_null=False)
    custom_appl_options = CustomApplOptionsSerializer(required=True, allow_null=False)


class ParisCountryCustomizationSerializer(serializers.Serializer):
    fam_est_form_data = serializers.PrimaryKeyRelatedField(read_only=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),
                                                 required=False)
    custom_appl_details = CustomApplDetailsSerializer(required=False, allow_null=True)
    custom_appl_options = CustomApplOptionsSerializer(required=False, allow_null=True)


class FamEstFormDataNetSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    family = serializers.PrimaryKeyRelatedField(queryset=Family.objects.all())
    init_appl_filing_date = serializers.DateField()
    init_appl_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    init_appl_type = serializers.PrimaryKeyRelatedField(queryset=ApplType.objects.all())
    init_appl_details = ApplDetailSerializer(required=True)
    init_appl_options = CustomApplOptionsSerializer(required=True)

    pct_method = serializers.BooleanField(default=False, required=False)
    pct_method_customization = PCTMethodCustomizationSerializer(allow_null=True)
    pct_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),
                                                     required=False, allow_null=True)
    isa_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),
                                                     required=False, allow_null=True)
    pct_countries = GetPCTCountryCustomizationSerializer(source='get_pct_countries', many=True, read_only=True)
    ep_method = serializers.BooleanField(default=False, required=False)
    ep_method_customization = EPMethodCustomizationSerializer(allow_null=True)
    ep_countries = GetEPCountryCustomizationSerializer(source='get_ep_countries', many=True, read_only=True)
    paris_countries = GetParisCountryCustomizationSerializer(source='get_paris_countries', many=True, read_only=True)
    unique_display_no = serializers.IntegerField()


class FamEstFormDataNetPostSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    family_name = serializers.CharField(write_only=True)
    family_no = serializers.CharField(default='', max_length=20, write_only=True)
    init_appl_filing_date = serializers.DateField()
    init_appl_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    init_appl_type = serializers.PrimaryKeyRelatedField(queryset=ApplType.objects.all())
    init_appl_details = ApplDetailSerializer(required=True)
    init_appl_options = CustomApplOptionsSerializer(required=True)
    pct_method = serializers.BooleanField(default=False, required=False)
    pct_method_customization = PCTMethodCustomizationSerializer(allow_null=True)
    pct_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),
                                                     required=False, allow_null=True)
    isa_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),
                                                     required=False, allow_null=True)
    pct_countries = PCTCountryCustomizationSerializer(many=True)
    ep_method = serializers.BooleanField(default=False, required=False)
    ep_method_customization = EPMethodCustomizationSerializer(allow_null=True)
    ep_countries = EPCountryCustomizationSerializer(many=True)
    paris_countries = ParisCountryCustomizationSerializer(many=True)
    unique_display_no = serializers.IntegerField()

    def create(self, validated_data):
        fam = Family.objects.create(
            user=validated_data['user'],
            family_name=validated_data['family_name'],
            family_no=validated_data['family_no'],
        )
        fam.save()
        pct_method_customization = self.create_pct_method_customization(validated_data['pct_method_customization'])
        ep_method_customization = self.create_ep_method_customization(validated_data['ep_method_customization'])

        init_appl_details = validated_data['init_appl_details']
        init_appl_details = ApplDetails.objects.create(
            **init_appl_details)
        init_appl_options = validated_data['init_appl_options']
        init_appl_options = CustomApplOptions.objects.create(
            **init_appl_options
        )

        famEstData = FamEstFormData.objects.create(
            family=fam,
            user=validated_data['user'],
            init_appl_filing_date=validated_data['init_appl_filing_date'],
            init_appl_details=init_appl_details,
            init_appl_country=validated_data['init_appl_country'],
            init_appl_type=validated_data['init_appl_type'],
            init_appl_options=init_appl_options,
            pct_method=validated_data['pct_method'],
            pct_method_customization=pct_method_customization,
            pct_country=validated_data['pct_country'],
            isa_country=validated_data['isa_country'],
            ep_method=validated_data['ep_method'],
            ep_method_customization=ep_method_customization,
        )
        famEstData.save()
        validate_entity_size(famEstData.init_appl_country, famEstData.init_appl_details)
        if famEstData.pct_country:
            validate_entity_size(famEstData.pct_country, famEstData.pct_method_customization)

        pct_countries = validated_data.pop('pct_countries')
        for country in pct_countries:
            self.create_pct_country_customization(country, famEstData)
        for country in validated_data.pop('ep_countries'):
            self.create_ep_country_customization(country, famEstData)
        for country in validated_data.pop('paris_countries'):
            self.create_paris_country_customization(country, famEstData)
        # famEstDataCreateOptions
        self.validate_ep_entrypoint(famEstData)
        self.validate_against_double_patenting(famEstData)
        famEstData.generate_family_options()
        return famEstData

    def validate_ep_entrypoint(self, famEstData):
        if famEstData.ep_method:
            ep_country = Country.objects.get(country='EP')
            if famEstData.init_appl_type.get_enum is not ApplTypes.EP \
                    and not ParisCountryCustomization.objects.filter(fam_est_form_data=famEstData,
                                                                     country=ep_country).exists() \
                    and not PCTCountryCustomization.objects.filter(fam_est_form_data=famEstData,
                                                                   country=ep_country).exists():
                raise serializers.ValidationError('entrypoint required for ep application')

    def validate_against_double_patenting(self, famEstData):
        # check if a country is repeated
        if famEstData.init_appl_type.get_enum is not ApplTypes.UTILITY:
            if famEstData.pariscountrycustomization_set.filter(country=famEstData.init_appl_country).exists() \
                    or famEstData.pctcountrycustomization_set.filter(country=famEstData.init_appl_country).exists() \
                    or famEstData.epcountrycustomization_set.filter(country=famEstData.init_appl_country).exists():
                raise serializers.ValidationError(
                    'Multiple Utility applications for the same country, can only accept one --init')

        for c in famEstData.pariscountrycustomization_set.all():
            if famEstData.pctcountrycustomization_set.filter(country=c.country).exists() \
                    or famEstData.epcountrycustomization_set.filter(country=c.country).exists():
                raise serializers.ValidationError(
                    'Multiple Utility applications for the same country, can only accept one--paris')
        for c in famEstData.pctcountrycustomization_set.all():
            if famEstData.pariscountrycustomization_set.filter(country=c.country).exists() \
                    or famEstData.epcountrycustomization_set.filter(country=c.country).exists():
                raise serializers.ValidationError(
                    'Multiple Utility applications for the same country, can only accept one--pct')
        for c in famEstData.epcountrycustomization_set.all():
            if famEstData.pctcountrycustomization_set.filter(country=c.country).exists() \
                    or famEstData.pariscountrycustomization_set.filter(country=c.country).exists():
                raise serializers.ValidationError(
                    'Multiple Utility applications for the same country, can only accept one--ep')

    def create_pct_method_customization(self, pct_method_customization):
        method_customization = create_generic_customization(pct_method_customization)
        return PCTMethodCustomization.objects.create(**method_customization)

    def create_ep_method_customization(self, ep_method_customization):
        method_customization = create_generic_customization(ep_method_customization)
        return EPMethodCustomization.objects.create(**method_customization)

    def create_pct_country_customization(self, country, famEstData):
        country = create_generic_customization(country)
        country['fam_est_form_data'] = famEstData
        validate_entity_size(country['country'], country['custom_appl_details'])
        return PCTCountryCustomization.objects.create(**country)

    def create_ep_country_customization(self, country, famEstData):
        country = create_generic_customization(country)
        country['fam_est_form_data'] = famEstData
        validate_entity_size(country['country'], country['custom_appl_details'])
        return EPCountryCustomization.objects.create(**country)

    def create_paris_country_customization(self, country, famEstData):
        country = create_generic_customization(country)
        country['fam_est_form_data'] = famEstData
        validate_entity_size(country['country'], country['custom_appl_details'])
        return ParisCountryCustomization.objects.create(**country)


def validate_entity_size(country, customApplDetails):
    if len(country.available_entity_sizes.all()) > 0:
        if customApplDetails.entity_size == None:
            raise serializers.ValidationError('entity size is required for country ',
                                              country.country)


def create_generic_customization(method_customization):
    if method_customization is None:
        custom_appl_details = CustomApplDetails.objects.create()
        custom_appl_options = CustomApplOptions.objects.create()
        PCTMethodCustomization.objects.create(
            custom_appl_details=custom_appl_details,
            custom_appl_options=custom_appl_options)
    else:
        if method_customization['custom_appl_details'] is None:
            method_customization['custom_appl_details'] = CustomApplDetails.objects.create()
        else:
            method_customization['custom_appl_details'] = CustomApplDetails.objects.create(
                **method_customization['custom_appl_details'])
        if method_customization['custom_appl_options'] is None:
            method_customization['custom_appl_options'] = CustomApplOptions.objects.create()
        else:
            method_customization['custom_appl_options'] = CustomApplOptions.objects.create(
                **method_customization['custom_appl_options'])
        return method_customization
