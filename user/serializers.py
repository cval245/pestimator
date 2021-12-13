from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'is_staff', 'is_active')


class UserAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'is_staff', 'is_active', 'date_joined',
                  'is_superuser', 'last_login', 'admin_data', 'terms_agreed')
