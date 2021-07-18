from rest_framework import viewsets
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.core.mail import send_mail
from user import models

# Create your views here.
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([AllowAny])
def retrieveUsername(request):
    if models.User.objects.get(email=request.data['email']):
        username = models.User.objects.get(email=request.data['email']).username
        send_mail(
            'Retrieve Username',
            'Your username is ' + username,
            'cval.me@patport.cc',
            [request.data['email']]
        )
        return Response()
    return Response()


# Create your views here.
