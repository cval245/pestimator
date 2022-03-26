from rest_framework import serializers

from lawfirm.models import LawFirm


class LawFirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawFirm
        fields = ('id', 'name', 'country', 'long_description',
                  'website', 'email', 'phone', 'slug', 'image_location')
