from rest_framework import serializers
from .models import UserProfile


class UserProfileAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'company_name', 'address', 'user',
                  'city', 'state', 'zip_code', 'estimates_remaining')


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = UserProfile
        fields = ('id', 'company_name', 'address', 'user',
                  'city', 'state', 'zip_code', 'estimates_remaining')
        read_only_fields = ['estimates_remaining']
