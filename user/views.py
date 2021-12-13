from django.shortcuts import render

# Create your views here
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from account.models import UserProfile
from user.accesspolicies import StaffOnlyAccess
from user.models import User
from user.serializers import UserSerializer, UserAllSerializer
from rest_framework.response import Response


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return [self.request.user]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # create UserProfile object
        print('ser.data', serializer.data)
        UserProfile.objects.create(user_id=serializer.data.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserAllViewSet(ModelViewSet):
    serializer_class = UserAllSerializer
    permission_classes = (StaffOnlyAccess,)

    def get_queryset(self):
        return User.objects.all()
