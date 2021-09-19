from django.db.models import F
from rest_framework import viewsets
from rest_framework.response import Response

from user.permissions import PostFamFormPermission
from .models import FamEstFormData
from .serializers import FamEstFormDataNetSerializer, FamEstFormDataNetPostSerializer


# Create your views here.

class FamEstFormDataViewSet(viewsets.ViewSet):
    serializer_class = FamEstFormDataNetSerializer
    permission_classes = [PostFamFormPermission]

    def get_queryset(self):
        return FamEstFormData.objects.filter(family__user=self.request.user) \
            .annotate(family_name=F('family__family_name'), family_no=F('family__family_no'))

    def list(self, request):
        return Response(FamEstFormDataNetSerializer(self.get_queryset(), many=True).data)

    def create(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = FamEstFormDataNetPostSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()
