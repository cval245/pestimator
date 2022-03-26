from django.db.models import F
from rest_framework import viewsets
from application.models import BaseApplication, ApplDetails
from application.serializers import ApplDetailSerializerWithUDN, ApplicationSerializer, ApplDetailSerializer
from user.accesspolicies import AuthenticatedGetAccess


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = (AuthenticatedGetAccess,)

    def get_queryset(self):
        queryset = BaseApplication.objects.filter(user=self.request.user)
        family_udn = self.request.query_params.get('familyUDN')
        if family_udn is not None:
            if queryset.filter(user=self.request.user,
                               family__unique_display_no=family_udn).exists():
                queryset = queryset.filter(user=self.request.user,
                                           family__unique_display_no=family_udn)
        queryset = queryset.annotate(family_udn=F('family__unique_display_no'))
        return queryset


class ApplDetailViewSet(viewsets.ModelViewSet):
    serializer_class = ApplDetailSerializerWithUDN
    permission_classes = (AuthenticatedGetAccess,)

    def get_queryset(self):
        queryset = ApplDetails.objects.filter(baseapplication__user=self.request.user)
        family_udn = self.request.query_params.get('familyUDN')
        if family_udn is not None:
            if queryset.filter(baseapplication__user=self.request.user,
                               baseapplication__family__unique_display_no=family_udn).exists():
                queryset = queryset.filter(baseapplication__user=self.request.user,
                                           baseapplication__family__unique_display_no=family_udn)
        queryset = queryset.annotate(family_udn=F('baseapplication__family__unique_display_no'))
        return queryset
