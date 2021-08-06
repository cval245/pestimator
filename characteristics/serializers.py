from rest_framework import serializers

from .models import ApplType, Country, EntitySize


class ApplTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplType
        fields = ('id', 'application_type', 'long_name')


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('id', 'country', 'currency_name', 'pct_analysis_bool', 'ep_bool',
                  'long_name', 'color')

class CountryAllSerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('id', 'country', 'active_bool', 'currency_name', 'pct_analysis_bool',
                  'ep_bool', 'long_name', 'color')


class EntitySerializer(serializers.ModelSerializer):

    class Meta:
        model = EntitySize
        fields = ('id', 'entity_size')
