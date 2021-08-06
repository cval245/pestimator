from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from application.models import BaseApplication, ApplDetails
from application.serializers import ApplicationSerializer, ApplDetailSerializer
from family.models import Family


# Create your views here.
class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        queryset = BaseApplication.objects.filter(user=self.request.user)
        family=self.request.query_params.get('family')
        if family is not None:
            if queryset.filter(family=family).exists():
                queryset = queryset.filter(family=family)
        return queryset


    @action(detail=False,url_path='filter/family=(?P<family_id>\d+)')
    def filter(self, request, family_id):
        family=Family.objects.get(id=family_id)
        applications=BaseApplication.objects.filter(family=family)
        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)

class ApplDetailViewSet(viewsets.ModelViewSet):
    serializer_class = ApplDetailSerializer

    def get_queryset(self):
        queryset = ApplDetails.objects.filter(baseapplication__user=self.request.user)
