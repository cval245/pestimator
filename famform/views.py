from django.db.models import F
from rest_framework import status, viewsets
from rest_framework.response import Response
from user.accesspolicies import FamFormPostAccess
from .models import FamEstFormData
from .serializers import FamEstFormDataNetSerializer, FamEstFormDataNetPostSerializer


class FamEstFormDataViewSet(viewsets.ModelViewSet):
    serializer_class = FamEstFormDataNetSerializer
    permission_classes = [FamFormPostAccess]  # separate from normal access policies

    def get_queryset(self):
        udn = self.request.query_params.get('UDN')
        if udn is not None:
            if FamEstFormData.objects.filter(user=self.request.user, unique_display_no=udn).exists():
                return [FamEstFormData.objects.get(user=self.request.user, unique_display_no=udn)]
            else:
                return FamEstFormData.objects.none()
        return FamEstFormData.objects.filter(family__user=self.request.user) \
            .annotate(family_name=F('family__family_name'), family_no=F('family__family_no'))

    def list(self, request, *args, **kwargs):
        udn = self.request.query_params.get('UDN')
        if self.get_queryset() is not None:
            return Response(FamEstFormDataNetSerializer(self.get_queryset(), many=True).data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = FamEstFormDataNetPostSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        new_object = FamEstFormData.objects.filter(id=serializer.data['id']) \
            .annotate(family_name=F('family__family_name'), family_no=F('family__family_no'))[0]
        resp_serializer = FamEstFormDataNetSerializer(new_object)
        return Response(resp_serializer.data)

    def perform_create(self, serializer):
        serializer.save()