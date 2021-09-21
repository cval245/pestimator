from django.shortcuts import redirect
from rest_framework import viewsets
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.core.mail import send_mail
from user import models
import stripe

stripe.api_key = 'pk_live_51H7SvaEsr85VxCzRM4aq4caJU7F5pUWWKFN8zqi2TbHbcPov8vfWAxPosuDlEFJ6NqMuOpujh6gZ2dLcuxK5hLvP00aQdz1FZQ'


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


# stripe views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    print('create checkout session')
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # price of product
                    'price': '50.00',
                    'quantity': 1,
                },
            ],
            payment_method_types=[
                'card',
            ],
            mode='payment',
            # TODO replace with environment variables prod and not prod
            success_url='localhost:4200?success=true',
            cancel_url='localhost:4200?cancel=true',
        )
    except Exception as e:
        print('exception occured')
        print('str', str(e))
        return Response(str(e))
        # return str(e)
    return Response(checkout_session.url, code=303)
    # return redirect(checkout_session.url, code=303)
