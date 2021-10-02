from django.http import JsonResponse
from rest_framework import viewsets

from user.models import User
from .models import UserProfile, PurchaseOrder, LineItem, ProductPrice
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.core.mail import send_mail
from user import models
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_PRIVATE_KEY


# Create your views here.
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # add one free estimate
        request.data['estimates_remaining'] = 1

        return super().create(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([AllowAny])
def retrieveUsername(request):
    if models.User.objects.get(email=request.data['email']):
        username = models.User.objects.get(email=request.data['email']).username
        send_mail(
            'Retrieve Username',
            'Your username is ' + username,
            settings.DEFAULT_FROM_EMAIL,
            [request.data['email']]
        )
        return Response()
    return Response()


@api_view(['POST'])
@permission_classes([AllowAny])
def webhook_stripe_add_estimate(request):
    event = None
    payload = request.data
    try:
        # event = simplejson.loads(payload)
        event = payload
    except:
        return JsonResponse(data={'success': False})

    if event and event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        # session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
        session = request
        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)
    elif event['type'] == 'payment_method.attached':
        payment_method = event['data']['object']  # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)

    elif event['type'] == 'checkout.session.completed':
        # user = request.user
        user = User.objects.get(id=1)
        po = PurchaseOrder.objects.create(user=user,
                                          session_id=event['data']['object']['id'],
                                          paid=True,
                                          total_amount=event['data']['object']['amount_total'] / 100.00
                                          # Stripe stores dollars in cents
                                          )
        # po = PurchaseOrder.objects.get(session_id=event['data']['object']['id'])
        # po.paid = True
        # po.total_amount = event['data']['amount_total'] / 100.00 #Stripe stores dollars in cents
        line_items = stripe.checkout.Session.list_line_items(
            event['data']['object']['id'],
            limit=10)
        for item in line_items['data']:
            LineItem.objects.create(purchase_order=po,
                                    quantity_purchased=item['quantity'],
                                    product_id=item['price']['product'],
                                    line_item_id=item['id']
                                    )
            userProfile = UserProfile.objects.get(user=user)
            userProfile.estimates_remaining = userProfile.estimates_remaining + item['quantity']
            userProfile.save()


    return JsonResponse(data={'success': True})


# stripe views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    try:
        price_item = ProductPrice.objects.get(price_description="estimate-normal-price")
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price_item.price_id,
                    'adjustable_quantity': {
                        'enabled': True,
                        'minimum': 1,
                        'maximum': 10,
                    },
                    'quantity': request.data['quantity'],
                },
            ],
            payment_method_types=[
                'card',
            ],
            mode='payment',
            success_url=settings.DOMAIN_FULL + '/account/checkout/success',
            cancel_url=settings.DOMAIN_FULL + '/account/checkout/cancel',
        )
    except Exception as e:
        return Response(str(e))

    return Response({'id': checkout_session.id}, status=200)
