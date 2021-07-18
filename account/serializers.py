from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = UserProfile
        fields = ('id','company_name', 'address', 'user',
                  'city','state', 'zip_code')

