from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ApplType, Country, EntitySize
from .serializers import ApplTypeSerializer, CountrySerializer, EntitySerializer, \
    CountryAllSerializer


# Create your views here.
class ApplTypeViewSet(viewsets.ModelViewSet):
    queryset = ApplType.objects.all()
    serializer_class = ApplTypeSerializer


class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer

    def get_queryset(self):
        return Country.objects.filter(active_bool=True).exclude(country='EP')


class CountryAllViewSet(viewsets.ModelViewSet):
    serializer_class = CountryAllSerializer

    def get_queryset(self):
        return Country.objects.all()


@api_view(['GET'])
def getEntitySize(request):
    entitySize = EntitySize.objects.all()
    print(entitySize)
    entitySizeSerial = []
    i=0
    for e in entitySize:
        entitySizeSerial.append(EntitySerializer(entitySize[i]).data)
        print(entitySizeSerial)
        i+=1
    print(entitySizeSerial)
    # return Response(entitySizeSerial)
    #entitySize = list(entitySize)
    #bob = EntitySerializer(entitySize)
    bob = entitySizeSerial
    return Response(bob)

