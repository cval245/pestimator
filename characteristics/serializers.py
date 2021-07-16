from rest_framework import serializers
from .models import ApplType, Country, EntitySize


class ApplTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplType
        fields = ('id', 'application_type')


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('id', 'country', 'currency_name')

class CountryAllSerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('id', 'country', 'active_bool', 'currency_name')


class EntitySerializer(serializers.ModelSerializer):

    class Meta:
        model = EntitySize
        fields = ('id', 'entity_size')
