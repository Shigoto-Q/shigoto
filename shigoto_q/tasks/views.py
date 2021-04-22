from django_celery_beat.models import CrontabSchedule
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .api.serializers import CrontabSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class CrontabView(APIView):
    """
    Lists all crontabs for the user
    Creates a crontab for the user
    """

    def get_object(self, user, *args, **kwargs):
        try:
            return user.crontab.all()
        except CrontabSchedule.DoesNotExist:
            return Http404

    def get(self, request, *args, **kwargs):
        crons = self.get_object(request.user)
        serializer = CrontabSerializer(crons, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CrontabSerializer(data=request.data)
        if serializer.is_valid():
            model_obj = serializer.save()
            request.user.crontab.add(model_obj)
            request.user.save()
            return Response(serializer.data)
        return Response(serializer.errors)
