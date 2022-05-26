import typing

from django.contrib.auth import get_user_model
from djstripe import models as stripe_models

from shigoto_q.products import constants as product_constants
from shigoto_q.products import features as products_features
from shigoto_q.users import exceptions as user_exceptions


User = get_user_model()


def subscription_check(func=None, /, *, prerequisites: typing.List):
    def out_wrapper(func):
        def wrapper(*args, **kwargs):
            user = User.objects.get(id=kwargs.get('user_id'))
            user_plan_id = user.customer.active_subscriptions.last().plan.product.id
            limits = products_features.get_limits_by_plan(user_plan_id)
            for prerequisite in prerequisites:
                pre_limit = dict(limits).get(prerequisite)
                field = product_constants.MODEL_LIMIT_FIELDS.get(prerequisite)
                user_field_limit = getattr(user, field)
                if user_field_limit >= pre_limit:
                    raise user_exceptions.UserExceededLimitError(
                        f"Your current plan does not support than {pre_limit} for feature {prerequisite}."
                    )
            res = func(*args, **kwargs)
            return res

        return wrapper

    if func is None:
        return out_wrapper
    return out_wrapper(func)


def _get_plan(product_id: str) -> stripe_models.Product:
    return stripe_models.Product.objects.get(id=product_id)
