from rest_framework import serializers
from lawfirm.models import LawFirm, LawFirmFees


class LawFirmSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField()
    image_location = serializers.ImageField(read_only=True, use_url=True)

    class Meta:
        model = LawFirm
        fields = ('id', 'name', 'country', 'long_description', 'lawfirm_submit_data_permissions',
                  'website', 'email', 'phone', 'slug', 'image_location')


class LawFirmPostSerializer(serializers.ModelSerializer):
    image_location = serializers.ImageField(read_only=True, use_url=True)

    class Meta:
        model = LawFirm
        fields = ('id', 'name', 'country', 'long_description', 'lawfirm_submit_data_permissions',
                  'website', 'email', 'phone', 'image_location')


class LawFirmFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawFirmFees
        fields = ('id', 'lawfirm', 'feetype', 'fee_amount', 'fee_amount_currency')
