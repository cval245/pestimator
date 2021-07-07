from rest_framework import serializers
from .models import BaseApplication, ApplDetails


class ApplicationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default = serializers.CurrentUserDefault())
    # family = FamilySerializer(many=False)
    # law_firm = LawFirmSerializer(many=False)
    # application_type = ApplTypeSerializer(many=False)
    #owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = BaseApplication
        fields = ('id', 'title', 'country', 'user',
                  #'application_type',
                  #'law_firm',
                  #'family',
                  'date_filing')

    # def create(self, validated_data):

    #     family=validated_data['family']
    #     law_firm=validated_data['law_firm']
    #     newAppl=Application.objects.create(
    #         title=validated_data['title'],
    #         appl_no=validated_data['appl_no'],
    #         country=validated_data['country'],
    #         application_type=validated_data['application_type'],
    #         family=family,
    #         law_firm=law_firm,
    #         date_filing=date_filing,
    #     )
    #     newAppl.save()
    #     return newAppl
class ApplDetailSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = ApplDetails
        fields = ('id', 'num_indep_claims', 'num_pages', 'num_claims', 
            'num_drawings', 'entity_size')