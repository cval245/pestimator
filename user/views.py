from django.shortcuts import render

# Create your views here
from rest_framework.viewsets import ModelViewSet

from user.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return [self.request.user]
