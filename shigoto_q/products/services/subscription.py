import stripe
from djstripe import models as stripe_models
from django.contrib.auth import get_user_model


User = get_user_model()


def create_subscription(plan_id, user_id):
    user = User.objects.get(id=user_id)

    payment_method_obj = stripe.PaymentMethod.retrieve('card')
    stripe_models.PaymentMethod.sync_from_stripe_data(payment_method_obj)

    user.customer.add_payment_method(payment_method='card')
    subscription = stripe.Subscription.create(
        customer=user.customer.id,
        items=[
            {"plan": plan_id},
        ],
        expand=["latest_invoice.payment_intent"],
    )
    return stripe_models.Subscription.sync_from_stripe_data(
        subscription
    )
