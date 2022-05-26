import json

import stripe
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from rest.views.resource import ResourceView
from shigoto_q.products.api.serializers import (
    CustomerSubscriptionSerializer,
    SessionSerializer,
    SessionDumpSerializer,
)
from shigoto_q.products.services import subscription as subscription_services


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

User = get_user_model()


class CustomerSubscriptionView(ResourceView):
    serializer_load_class = CustomerSubscriptionSerializer
    serializer_dump_class = CustomerSubscriptionSerializer
    owner_check = True

    def execute(self, data):
        subscription_services.create_subscription(
            plan_id=data.get("plan_id"),
            user_id=data.get("user_id"),
        )


@csrf_exempt
def create_checkout(request):
    data = json.loads(request.body)
    try:
        checkout_session = stripe.checkout.Session.create(
            customer=request.user.customer.id,
            success_url=settings.STRIPE_SUCCESS_URL
            + "/?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=settings.STRIPE_CANCEL_URL,
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price": data["priceId"],
                    "quantity": 1,
                }
            ],
        )
        return JsonResponse({"sessionId": checkout_session["id"]})
    except Exception as e:
        return JsonResponse({"error": {"message": str(e)}})


class SessionView(ResourceView):
    serializer_dump_class = SessionDumpSerializer
    serializer_load_class = SessionSerializer
    owner_check = True

    def execute(self, data):
        u = User.objects.get(id=data.get("user_id"))
        checkout_session = stripe.checkout.Session.create(
            customer=u.customer.id,
            success_url=settings.STRIPE_SUCCESS_URL
            + "/?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=settings.STRIPE_CANCEL_URL,
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price": data["price_id"],
                    "quantity": 1,
                }
            ],
        )
        return {"session_id": checkout_session["id"]}
