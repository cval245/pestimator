from rest_framework import serializers

from characteristics.models import Country, EntitySize, ApplType
from .models import FamEstFormData
from .models import Family


class FamEstFormDataNetSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    family_name = serializers.CharField(write_only=False)
    family_no = serializers.CharField(default='', max_length=20, write_only=False)
    countries = serializers.PrimaryKeyRelatedField(many=True, queryset=Country.objects.all())
    init_appl_filing_date = serializers.DateField()
    init_appl_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    init_appl_type = serializers.PrimaryKeyRelatedField(queryset=ApplType.objects.all())
    init_appl_claims = serializers.IntegerField()
    init_appl_drawings = serializers.IntegerField()
    init_appl_pages_desc = serializers.IntegerField()
    init_appl_pages_claims = serializers.IntegerField()
    init_appl_pages_drawings = serializers.IntegerField()
    init_appl_indep_claims = serializers.IntegerField()
    method = serializers.BooleanField(default=False, required=False)
    meth_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),
                                                      required=False, allow_null=True)
    ep_method = serializers.BooleanField(default=False, required=False)
    entity_size = serializers.PrimaryKeyRelatedField(queryset=EntitySize.objects.all())

    unique_display_no = serializers.IntegerField()


class FamEstFormDataNetPostSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    family_name = serializers.CharField(write_only=True)
    family_no = serializers.CharField(default='', max_length=20, write_only=True)
    countries = serializers.PrimaryKeyRelatedField(many=True, queryset=Country.objects.all())
    init_appl_filing_date = serializers.DateField()
    init_appl_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    init_appl_type = serializers.PrimaryKeyRelatedField(queryset=ApplType.objects.all())
    init_appl_claims = serializers.IntegerField()
    init_appl_drawings = serializers.IntegerField()
    init_appl_pages_desc = serializers.IntegerField()
    init_appl_pages_claims = serializers.IntegerField()
    init_appl_pages_drawings = serializers.IntegerField()
    init_appl_indep_claims = serializers.IntegerField()
    method = serializers.BooleanField(default=False, required=False)
    meth_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(),
                                                      required=False, allow_null=True)
    ep_method = serializers.BooleanField(default=False, required=False)
    entity_size = serializers.PrimaryKeyRelatedField(queryset=EntitySize.objects.all())
    unique_display_no = serializers.IntegerField()

    def create(self, validated_data):
        fam = Family.objects.create(
            user=validated_data['user'],
            family_name=validated_data['family_name'],
            family_no=validated_data['family_no'],
        )
        fam.save()

        famEstData = FamEstFormData.objects.create(
            family=fam,
            user=validated_data['user'],
            init_appl_filing_date=validated_data['init_appl_filing_date'],
            init_appl_drawings=validated_data['init_appl_drawings'],
            init_appl_pages_desc=validated_data['init_appl_pages_desc'],
            init_appl_pages_claims=validated_data['init_appl_pages_claims'],
            init_appl_pages_drawings=validated_data['init_appl_pages_drawings'],
            init_appl_claims=validated_data['init_appl_claims'],
            init_appl_country=validated_data['init_appl_country'],
            init_appl_type=validated_data['init_appl_type'],
            init_appl_indep_claims=validated_data['init_appl_indep_claims'],
            entity_size=validated_data['entity_size'],
            method=validated_data['method'],
            meth_country=validated_data['meth_country'],
            ep_method=validated_data['ep_method'],
        )
        famEstData.save()
        famEstData.countries.set(validated_data['countries'])
        # famEstDataCreateOptions
        famEstData.generate_family_options()
        return famEstData

