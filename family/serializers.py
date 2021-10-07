from rest_framework import serializers
from .models import Family
from rest_framework.fields import CurrentUserDefault


class FamilySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default = serializers.CurrentUserDefault())

    class Meta:
        model = Family
        fields = ('id', 'family_no', 'family_name',
                  'user', 'unique_display_no')
