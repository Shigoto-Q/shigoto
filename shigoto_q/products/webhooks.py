import stripe
from djstripe import models as stripe_models
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


endpoint_secret = (
    "whsec_d56e412327d8fcff066ac5203a614affc6953c579a2ba25a852b705907e7819b"
)


@csrf_exempt
def subscription(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        sub_obj = dict(id=session["subscription"])
        customer_obj = dict(id=session["customer"])
        stripe_models.Subscription.sync_from_stripe_data(sub_obj)
        stripe_models.Customer.sync_from_stripe_data(customer_obj)
        if session.payment_status == "paid":
            return HttpResponse(status=200)
        return HttpResponse(status=200)
    elif event["type"] == "checkout.session.async_payment_succeeded":
        session = event["data"]["object"]
        return HttpResponse(status=200)

    elif event["type"] == "checkout.session.async_payment_failed":
        session = event["data"]["object"]
        return HttpResponse(status=400)

    return HttpResponse(status=200)
