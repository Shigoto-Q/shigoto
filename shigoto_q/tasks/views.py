from django_celery_beat.models import (
    CrontabSchedule,
    IntervalSchedule,
    ClockedSchedule,
    SolarSchedule,
)
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .api.serializers import (
    CrontabSerializer,
    IntervalSerializer,
    ClockedSerializer,
    SolarSerializer,
)
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


class IntervalView(APIView):
    """
    Lists all intervalss for the user
    Creates an interval for the user
    """

    def get_object(self, user, *args, **kwargs):
        try:
            return user.interval.all()
        except IntervalSchedule.DoesNotExist:
            return Http404

    def get(self, request, *args, **kwargs):
        interval = self.get_object(request.user)
        serializer = IntervalSerializer(interval, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = IntervalSerializer(data=request.data)
        if serializer.is_valid():
            model_obj = serializer.save()
            request.user.interval.add(model_obj)
            request.user.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class ClockedView(APIView):
    """
    Lists all clock schedules for the user
    Creates a clock for the user
    """

    def get_object(self, user, *args, **kwargs):
        try:
            return user.clocked.all()
        except ClockedSchedule.DoesNotExist:
            return Http404

    def get(self, request, *args, **kwargs):
        clock = self.get_object(request.user)
        serializer = ClockedSerializer(clock, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ClockedSerializer(data=request.data)
        if serializer.is_valid():
            model_obj = serializer.save()
            request.user.clocked.add(model_obj)
            request.user.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class SolarView(APIView):
    """
    Lists all solar schedules for the user
    Creates a solar schedule for the user
    """

    def get_object(self, user, *args, **kwargs):
        try:
            return user.solar.all()
        except SolarSchedule.DoesNotExist:
            return Http404

    def get(self, request, *args, **kwargs):
        solar = self.get_object(request.user)
        serializer = SolarSerializer(solar, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = SolarSerializer(data=request.data)
        if serializer.is_valid():
            model_obj = serializer.save()
            request.user.solar.add(model_obj)
            request.user.save()
            return Response(serializer.data)
        return Response(serializer.errors)
