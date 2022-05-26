import typing
from dataclasses import dataclass

from django.conf import settings

from shigoto_q.products import features


@dataclass
class ProductMetadata(object):
    stripe_id: str
    name: str
    features: typing.Dict[str]
    description: str = ''
    is_default: bool = False


PERSONAL = ProductMetadata(
    stripe_id=settings.PERSONAL_PLAN,
    name='Personal',
    description='For personal use.',
    is_default=False,
    features=dict(features.PERSONAL_PLAN_LIMITS)
)


PROFESSIONAL = ProductMetadata(
    stripe_id=settings.PROFESSIONAL_PLAN,
    name='Personal',
    description='For professional needs',
    is_default=False,
    features=dict(features.PROFESSIONAL_PLAN_LIMITS)
)

BUSINESS = ProductMetadata(
    stripe_id=settings.BUSINESS_PLAN,
    name='Personal',
    description='For business needs',
    is_default=False,
    features=dict(features.BUSINESS_PLAN_LIMITS)
)
