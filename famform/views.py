from django.db.models import F
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from user.permissions import PostFamFormPermission
from .models import FamEstFormData
from .serializers import FamEstFormDataNetSerializer, FamEstFormDataNetPostSerializer


# Create your views here.

class FamEstFormDataViewSet(viewsets.ViewSet):
    serializer_class = FamEstFormDataNetSerializer
    permission_classes = [PostFamFormPermission]

    def get_queryset(self):
        udn = self.request.query_params.get('UDN')

        if udn is not None:
            if FamEstFormData.objects.filter(user=self.request.user, family__unique_display_no=udn).exists():
                return [FamEstFormData.objects.get(user=self.request.user, family__unique_display_no=udn)]
        return FamEstFormData.objects.filter(family__user=self.request.user) \
            .annotate(family_name=F('family__family_name'), family_no=F('family__family_no'))

    def list(self, request):
        return Response(FamEstFormDataNetSerializer(self.get_queryset(), many=True).data)

    def create(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = FamEstFormDataNetPostSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # return Response(serializer.data)
        new_object = FamEstFormData.objects.filter(id=serializer.data['id']) \
            .annotate(family_name=F('family__family_name'), family_no=F('family__family_no'))[0]
        resp_serializer = FamEstFormDataNetSerializer(new_object)
        # serializer.data.id
        return Response(resp_serializer.data)

    def perform_create(self, serializer):
        serializer.save()
