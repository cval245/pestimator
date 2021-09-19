from rest_framework import serializers

from .models import BaseApplication, ApplDetails


class ApplicationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    # family = FamilySerializer(many=False)
    # law_firm = LawFirmSerializer(many=False)
    # application_type = ApplTypeSerializer(many=False)
    # owner = serializers.ReadOnlyField(source='owner.username')
    appl_type = serializers.SerializerMethodField()

    class Meta:
        model = BaseApplication
        fields = ('id', 'title', 'country', 'user',
                  'appl_type',
                  'date_filing')

    def get_appl_type(self, obj):
        return obj.get_appl_type().id


class ApplDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplDetails
        fields = ('id', 'num_indep_claims', 'num_pages_description', 'num_claims',
                  'num_pages_drawings', 'num_pages_claims', 'entity_size')
