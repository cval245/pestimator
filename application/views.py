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
        family_udn = self.request.query_params.get('familyUDN')
        if family_udn is not None:
            if queryset.filter(user=self.request.user,
                               family__unique_display_no=family_udn).exists():
                queryset = queryset.filter(user=self.request.user,
                                           family__unique_display_no=family_udn)
        return queryset


class ApplDetailViewSet(viewsets.ModelViewSet):
    serializer_class = ApplDetailSerializer

    def get_queryset(self):
        queryset = ApplDetails.objects.filter(baseapplication__user=self.request.user)
        family_udn = self.request.query_params.get('familyUDN')
        if family_udn is not None:
            if queryset.filter(baseapplication__user=self.request.user,
                               baseapplication__family__unique_display_no=family_udn).exists():
                queryset = queryset.filter(baseapplication__user=self.request.user,
                                           baseapplication__family__unique_display_no=family_udn)
        return queryset
