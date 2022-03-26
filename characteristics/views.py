from djmoney.settings import CURRENCY_CHOICES
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from user.accesspolicies import AllGetStaffOnlyPost, GetOnlyPolicy, StaffOnlyPost, AuthenticatedGetAccess
from .models import ApplType, Country, EntitySize, Language, EPValidationTranslationRequired, DocFormat, \
    DocFormatCountry, TranslationRequiredOptions
from .serializers import ApplTypeSerializer, CountrySerializer, EntitySerializer, \
    CountryAllSerializer, LanguageSerializer, EPValidationTranslationRequiredSerializer, DocFormatSerializer, \
    PostDocFormatCountrySerializer, CountryAllPostSerializer, TranslationRequiredOptionsSerializer


# Create your views here.
class ApplTypeViewSet(viewsets.ModelViewSet):
    serializer_class = ApplTypeSerializer
    # access_policy = StaffOnlyAccess
    permission_classes = (StaffOnlyPost,)

    def get_queryset(self):
        # from django.conf import settings.djmoney
        return ApplType.objects.filter(internal_bool=False)

    # class Meta:
    #     permission_classes = [DataPermission]


class ApplTypeAllViewSet(viewsets.ModelViewSet):
    serializer_class = ApplTypeSerializer
    permission_classes = (StaffOnlyPost,)

    def get_queryset(self):
        return ApplType.objects.all()


class EPValidationTranslationRequiredViewSet(viewsets.ModelViewSet):
    serializer_class = EPValidationTranslationRequiredSerializer
    permission_classes = (StaffOnlyPost,)

    def get_queryset(self):
        return EPValidationTranslationRequired.objects.all()


class TranslationRequiredOptionsViewSet(viewsets.ModelViewSet):
    serializer_class = TranslationRequiredOptionsSerializer
    permission_classes = (StaffOnlyPost,)

    def get_queryset(self):
        return TranslationRequiredOptions.objects.all()


class CountryViewSet(viewsets.ModelViewSet):
    permission_classes = (AllGetStaffOnlyPost,)
    serializer_class = CountrySerializer

    def get_queryset(self):
        return Country.objects.filter(active_bool=True)


class CountryAllViewSet(viewsets.ModelViewSet):
    permission_classes = (AllGetStaffOnlyPost,)
    serializer_class = CountryAllSerializer

    def get_queryset(self):
        return Country.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        s = CountryAllPostSerializer()
        country = s.update(instance=instance, validated_data=request.data)
        resp = CountryAllSerializer(country)
        return Response(resp.data)


class LanguageViewSet(viewsets.ModelViewSet):
    permission_classes = (StaffOnlyPost,)
    serializer_class = LanguageSerializer

    def get_queryset(self):
        return Language.objects.all()


class DocFormatViewSet(viewsets.ModelViewSet):
    permission_classes = (StaffOnlyPost,)
    serializer_class = DocFormatSerializer

    def get_queryset(self):
        return DocFormat.objects.all()


class DocFormatCountryViewSet(viewsets.ModelViewSet):
    permission_classes = (StaffOnlyPost,)
    serializer_class = PostDocFormatCountrySerializer

    def get_queryset(self):
        return DocFormatCountry.objects.all()


@api_view(['GET'])
@permission_classes([AuthenticatedGetAccess])
def getEntitySize(request):
    entitySize = EntitySize.objects.all()
    entitySizeSerial = []
    i = 0
    for e in entitySize:
        entitySizeSerial.append(EntitySerializer(entitySize[i]).data)
        i += 1
    bob = entitySizeSerial
    return Response(bob)


@api_view(['GET'])
@permission_classes([AuthenticatedGetAccess])
def getCurrencyView(request):
    # Important, the ID is meaningless and subject to change
    # convert list of tuples to serialized version
    currencies = []
    for i, c in enumerate(CURRENCY_CHOICES):
        currency = {'id': i + 1, 'currency_name': c[0], 'currency_full_name': c[1]}
        currencies.append(currency)
    return Response(currencies)
