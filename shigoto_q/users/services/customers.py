import stripe
from django.conf import settings
from django.db import transaction

from djstripe import models as stripe_models


stripe.api_key = settings.STRIPE_API_KEY


@transaction.atomic()
def create_customer(name: str, email: str, payment_method: str = None) -> stripe_models.Customer:
    customer = stripe.Customer.create(
        name=name,
        email=email,
        payment_method=payment_method,
        invoice_settings={
            'default_payment_method': payment_method,
        },
    )
    c = stripe_models.Customer.sync_from_stripe_data(customer)
    return c
