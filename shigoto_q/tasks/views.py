from .api.serializers import CrontabSerializer
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication


class CrontabView(APIView):
    def get_object(self, *args, **kwargs):
        try:
            return CrontabSchedule.objects.all()
        except CrontabSchedule.DoesNotExist:
            return Http404

    def get(self, request, *args, **kwargs):
        crons = self.get_object()
        serializer = CrontabSerializer(crons, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CrontabSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
