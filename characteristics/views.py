from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ApplType, Country, EntitySize
from .serializers import ApplTypeSerializer, CountrySerializer, EntitySerializer, \
    CountryAllSerializer


# Create your views here.
class ApplTypeViewSet(viewsets.ModelViewSet):
    serializer_class = ApplTypeSerializer

    def get_queryset(self):
        return ApplType.objects.filter(internal_bool=False)


class ApplTypeAllViewSet(viewsets.ModelViewSet):
    serializer_class = ApplTypeSerializer

    def get_queryset(self):
        return ApplType.objects.all()


class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer

    def get_queryset(self):
        return Country.objects.filter(active_bool=True)


class CountryAllViewSet(viewsets.ModelViewSet):
    serializer_class = CountryAllSerializer

    def get_queryset(self):
        return Country.objects.all()


@api_view(['GET'])
def getEntitySize(request):
    entitySize = EntitySize.objects.all()
    entitySizeSerial = []
    i=0
    for e in entitySize:
        entitySizeSerial.append(EntitySerializer(entitySize[i]).data)
        i+=1
    # return Response(entitySizeSerial)
    #entitySize = list(entitySize)
    #bob = EntitySerializer(entitySize)
    bob = entitySizeSerial
    return Response(bob)

