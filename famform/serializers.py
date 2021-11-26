from rest_framework import serializers

from application.models import ApplDetails
from application.serializers import ApplDetailSerializer
from characteristics.models import Country, EntitySize, ApplType, Languages, DocFormat
from family.models import Family
from .models import FamEstFormData, PCTCountryCustomization, EPCountryCustomization, \
    ParisCountryCustomization, PCTMethodCustomization, EPMethodCustomization
from .models.CustomApplDetails import CustomApplDetails
from .models.CustomApplOptions import CustomApplOptions


class CustomApplOptionsSerializer(serializers.Serializer):
    request_examination_early_bool = serializers.BooleanField(required=False)
    doc_format = serializers.PrimaryKeyRelatedField(
        required=False,
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
                                                  queryset=Languages.objects.all())


class PCTMethodCustomizationSerializer(serializers.Serializer):
    custom_appl_details = CustomApplDetailsSerializer(required=False, allow_null=True)
    custom_appl_options = CustomApplOptionsSerializer(required=True)


class EPMethodCustomizationSerializer(serializers.Serializer):
    custom_appl_details = CustomApplDetailsSerializer(required=False, allow_null=True)
    custom_appl_options = CustomApplOptionsSerializer(required=True)


class GetPCTCountryCustomizationSerializer(serializers.Serializer):
    fam_est_form_data = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),
                                            required=False)
    country = id
    custom_appl_details = CustomApplDetailsSerializer(required=False, allow_null=True)
    custom_appl_options = CustomApplOptionsSerializer(required=False, allow_null=True)


class PCTCountryCustomizationSerializer(serializers.Serializer):
    fam_est_form_data = serializers.PrimaryKeyRelatedField(read_only=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),
                                                 required=False)
    custom_appl_details = CustomApplDetailsSerializer(required=False, allow_null=True)
    custom_appl_options = CustomApplOptionsSerializer(required=False, allow_null=True)


class GetEPCountryCustomizationSerializer(serializers.Serializer):
    fam_est_form_data = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),
                                            required=False)
    country = id
    custom_appl_details = CustomApplDetailsSerializer(required=False, allow_null=True)
    custom_appl_options = CustomApplOptionsSerializer(required=False, allow_null=True)

    class Meta:
        model = EPCountryCustomization
        # fields=('country', 'custom_appl_details')


class EPCountryCustomizationSerializer(serializers.Serializer):
    fam_est_form_data = serializers.PrimaryKeyRelatedField(read_only=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),
                                                 required=False)
    custom_appl_details = CustomApplDetailsSerializer(required=False, allow_null=True)
    custom_appl_options = CustomApplOptionsSerializer(required=False, allow_null=True)


class GetParisCountryCustomizationSerializer(serializers.Serializer):
    fam_est_form_data = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),
                                            required=False)
    country = id
    custom_appl_details = CustomApplDetailsSerializer(required=False, allow_null=True)
    custom_appl_options = CustomApplOptionsSerializer(required=False, allow_null=True)


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
    pct_countries = GetPCTCountryCustomizationSerializer(many=True)
    ep_method = serializers.BooleanField(default=False, required=False)
    ep_method_customization = EPMethodCustomizationSerializer(allow_null=True)
    ep_countries = GetEPCountryCustomizationSerializer(many=True)
    paris_countries = GetParisCountryCustomizationSerializer(many=True)
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
        pct_method_customization = validated_data['pct_method_customization']
        if pct_method_customization is not None:
            if pct_method_customization['custom_appl_details'] is not None:
                pct_method_customization['custom_appl_details'] = CustomApplDetails.objects.create(
                    **pct_method_customization['custom_appl_details'])
                pct_method_customization['custom_appl_options'] = CustomApplOptions.objects.create(
                    **pct_method_customization['custom_appl_options'])

            pct_method_customization = PCTMethodCustomization.objects.create(**pct_method_customization)
        ep_method_customization = validated_data['ep_method_customization']
        print('ep', ep_method_customization)
        if ep_method_customization is not None:
            if ep_method_customization['custom_appl_details'] is not None:
                ep_method_customization['custom_appl_details'] = CustomApplDetails.objects.create(
                    **ep_method_customization['custom_appl_details'])
                ep_method_customization['custom_appl_options'] = CustomApplOptions.objects.create(
                    **ep_method_customization['custom_appl_options'])
            ep_method_customization = EPMethodCustomization.objects.create(**ep_method_customization)
            print('eee', ep_method_customization.__dict__)

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
        # validate_entity_size(famEstData.ep_country, famEstData.ep_method_customization)

        pct_countries = validated_data.pop('pct_countries')
        for country in pct_countries:
            country['fam_est_form_data'] = famEstData
            if country['custom_appl_details'] is not None:
                country['custom_appl_details'] = CustomApplDetails.objects.create(**country['custom_appl_details'])
                country['custom_appl_options'] = CustomApplOptions.objects.create(**country['custom_appl_options'])
                validate_entity_size(country['country'], country['custom_appl_details'])
            PCTCountryCustomization.objects.create(**country)
        for country in validated_data.pop('ep_countries'):
            country['fam_est_form_data'] = famEstData
            if country['custom_appl_details'] is not None:
                country['custom_appl_details'] = CustomApplDetails.objects.create(**country['custom_appl_details'])
                country['custom_appl_options'] = CustomApplOptions.objects.create(**country['custom_appl_options'])
                validate_entity_size(country['country'], country['custom_appl_details'])
            EPCountryCustomization.objects.create(**country)
        for country in validated_data.pop('paris_countries'):
            country['fam_est_form_data'] = famEstData
            if country['custom_appl_details'] is not None:
                country['custom_appl_details'] = CustomApplDetails.objects.create(**country['custom_appl_details'])
                country['custom_appl_options'] = CustomApplOptions.objects.create(**country['custom_appl_options'])
                validate_entity_size(country['country'], country['custom_appl_details'])
            ParisCountryCustomization.objects.create(**country)

        # famEstDataCreateOptions
        self.validate_ep_entrypoint(famEstData)
        self.validate_against_double_patenting(famEstData)
        famEstData.generate_family_options()
        return famEstData

    def validate_ep_entrypoint(self, famEstData):
        if famEstData.ep_method:
            ep_country = Country.objects.get(country='EP')
            if famEstData.init_appl_type != ApplType.objects.get(application_type='ep') \
                    and not ParisCountryCustomization.objects.filter(fam_est_form_data=famEstData,
                                                                     country=ep_country).exists() \
                    and not PCTCountryCustomization.objects.filter(fam_est_form_data=famEstData,
                                                                   country=ep_country).exists():
                raise serializers.ValidationError('entrypoint required for ep application')

    def validate_against_double_patenting(self, famEstData):
        # check if a country is repeated
        # famEstData.pariscountrycustomization_set.filter(country=famEstData.init_appl_country)
        if famEstData.init_appl_type == ApplType.objects.get(application_type='utility'):
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


def validate_entity_size(country, customApplDetails):
    if country.entity_size_available == True:
        if customApplDetails.entity_size == None:
            raise serializers.ValidationError('entity size is required for country ',
                                              country.country)
