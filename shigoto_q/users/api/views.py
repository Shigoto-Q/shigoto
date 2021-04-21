from django.contrib.auth import get_user_model
from django.http import Http404
from djstripe.models import Product, Plan
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from .serializers import UserSerializer, ProductSerializer
from django.db.models import Prefetch

User = get_user_model()


class ProductView(APIView):
    permission_classes = []

    def get_objects(self, *args, **kwargs):
        try:
            # TODO sort this by reverse FK (plan)
            return Product.objects.prefetch_related(
                Prefetch("plan_set", queryset=Plan.objects.all().order_by("amount"))
            )
        except Product.DoesNotExist:
            return Http404

    def get(self, request, *args, **kwargs):
        products = self.get_objects()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
