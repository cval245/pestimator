from rest_framework import serializers

from lawfirm.models import LawFirm


class LawFirmSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField()
    image_location = serializers.ImageField(read_only=True, use_url=True)

    class Meta:
        model = LawFirm
        fields = ('id', 'name', 'country', 'long_description',
                  'website', 'email', 'phone', 'slug', 'image_location')


class LawFirmPostSerializer(serializers.ModelSerializer):
    image_location = serializers.ImageField(read_only=True, use_url=True)
    class Meta:
        model = LawFirm
        fields = ('id', 'name', 'country', 'long_description',
                  'website', 'email', 'phone', 'image_location')
