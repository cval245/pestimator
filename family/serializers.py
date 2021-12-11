from rest_framework import serializers

from famform.models import FamEstFormData
from .models import Family
from rest_framework.fields import CurrentUserDefault


class FamilySerializer(serializers.ModelSerializer):
    fam_est_form_data_udn = serializers.IntegerField(
        source='get_fam_est_form_data_udn',
        read_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Family
        fields = ('id', 'family_no', 'family_name', 'famestformdata',
                  'user', 'unique_display_no', 'fam_est_form_data_udn')
