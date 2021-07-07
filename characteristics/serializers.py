from rest_framework import serializers
from .models import ApplType, Country, EntitySize


class ApplTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplType
        fields = ('id', 'application_type')


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'


class EntitySerializer(serializers.ModelSerializer):

    class Meta:
        model = EntitySize
        fields = ('id', 'entity_size')
