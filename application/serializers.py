from rest_framework import serializers

from .models import BaseApplication, ApplDetails


class ApplicationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    appl_type = serializers.SerializerMethodField()
    family_udn = serializers.IntegerField()

    class Meta:
        model = BaseApplication
        fields = ('id', 'title', 'country', 'user',
                  'appl_type', 'family_udn',
                  'date_filing')

    def get_appl_type(self, obj):
        return obj.get_appl_type().id


class ApplDetailSerializerWithUDN(serializers.ModelSerializer):
    family_udn = serializers.IntegerField()

    class Meta:
        model = ApplDetails
        fields = ('id', 'num_indep_claims', 'num_drawings', 'num_pages_description',
                  'num_claims', 'num_claims_multiple_dependent',
                  'num_pages_drawings', 'num_pages_claims', 'entity_size', 'language',
                  'family_udn'
                  )


class ApplDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplDetails
        fields = ('id', 'num_indep_claims', 'num_drawings', 'num_pages_description',
                  'num_claims', 'num_claims_multiple_dependent',
                  'num_pages_drawings', 'num_pages_claims', 'entity_size', 'language',
                  )
