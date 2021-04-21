import json

import stripe
import djstripe
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from djstripe.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


@csrf_exempt
def create_customer_sub(request):
    """
    Create a Stripe Customer and Subscription object and map them onto the User object
    Expects the inbound POST data to look something like this:
    {
        'email': 'cory@saaspegasus.com',
        'payment_method': 'pm_1GGgzaIXTEadrB0y0tthO3UH',
        'plan_id': 'plan_GqvXkzAvxlF0wR',
    }
    """
    body = json.loads(request.body)
    email = body.get("email")
    payment_method = body.get("payment_method")
    plan_id = body.get("plan_id")
    payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
    djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)
    customer = stripe.Customer.create(
        payment_method=payment_method,
        email=email,
        invoice_settings={"default_payment_method": payment_method},
    )
    djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)
    subscription = stripe.Subscription.create(
        customer=customer.id,
        items=[
            {"plan": plan_id},
        ],
        expand=["latest_invoice.payment_intent"],
    )
    djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(
        subscription
    )

    request.user.customer = djstripe_customer
    request.user.subscription = djstripe_subscription
    request.user.save()

    data = {"customer": customer, "subscription": subscription}
    return JsonResponse(data=data)


@csrf_exempt
def create_checkout(request):
    data = json.loads(request.body)
    try:
        checkout_session = stripe.checkout.Session.create(
            success_url="https://example.com/success.html?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://example.com/canceled.html",
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price": data["priceId"],
                    "quantity": 1,
                }
            ],
        )
        print(checkout_session)
        return JsonResponse({"sessionId": checkout_session["id"]})
    except Exception as e:
        return JsonResponse({"error": {"message": str(e)}})


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, stripe.api_key)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Save an order in your database, marked as 'awaiting payment'
        create_order(session)

        # Check if the order is already paid (e.g., from a card payment)
        #
        # A delayed notification payment will have an `unpaid` status, as
        # you're still waiting for funds to be transferred from the customer's
        # account.
        if session.payment_status == "paid":
            fulfill_order(session)
    elif event["type"] == "checkout.session.async_payment_succeeded":
        session = event["data"]["object"]

        # Fulfill the purchase
        fulfill_order(session)

    elif event["type"] == "checkout.session.async_payment_failed":
        session = event["data"]["object"]

        # Send an email to the customer asking them to retry their order
        email_customer_about_failed_payment(session)


def fulfill_order(session):
    # TODO: fill me in
    print("Fulfilling order")


def create_order(session):
    # TODO: fill me in
    print("Creating order")


def email_customer_about_failed_payment(session):
    # TODO: fill me in
    print("Emailing customer")
