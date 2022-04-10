from django.conf import settings
from djstripe.models import Product
from rest_framework import permissions

from shigoto_q.products import constants as product_constants


class PersonalPlanPermission(permissions.BasePermission):
    message = "Your current plan does not support this feature."

    def has_permission(self, request, view):
        product = Product.objects.get(id=settings.PERSONAL_PLAN)
        return request.user.customer.is_subscribed_to(product=product)


class ProfessionalPlanPermission(permissions.BasePermission):
    message = "Your current plan does not support this feature."

    def has_permission(self, request, view):
        product = Product.objects.get(id=settings.PROFESSIONAL_PLAN)
        return request.user.customer.is_subscribed_to(product=product)


class BusinessPlanPermission(permissions.BasePermission):
    message = "Your current plan does not support this feature."

    def has_permission(self, request, view):
        product = Product.objects.get(id=settings.BUSINESS_PLAN)
        return request.user.customer.is_subscribed_to(product=product)
