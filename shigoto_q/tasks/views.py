import json
import re

from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.http import JsonResponse
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from kombu.utils.json import loads
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from config.celery_app import app

from .api.serializers import (
    ClockedSerializer,
    CrontabSerializer,
    IntervalSerializer,
    SolarSerializer,
    TaskGetSerializer,
    TaskPostSerializer,
    TaskResultSerializer,
)
from .models import TaskResult

User = get_user_model()


class TestView(APIView):
    def get_object(self):
        qs = TaskResult.objects.filter(user=self.request.user).aggregate(
            success=Count("pk", filter=Q(status="SUCCESS")),
            failure=Count("pk", filter=Q(status="FAILURE")),
            pending=Count("pk", filter=Q(status="PENDING")),
        )
        return qs

    def get(self, request):
        obj = self.get_object()
        return Response(obj)


class TaskResultView(APIView):
    def get_object(self, task_id):
        try:
            return TaskResult.objects.filter(user=self.request.user, task_id=task_id)
        except TaskResult.DoesNotExist:
            return Http404

    def get(self, request, task_id, *args, **kwargs):
        task_result = self.get_object(task_id)
        serializer = TaskResultSerializer(task_result, many=True)
        return Response(serializer.data)


def run_task(request, task_id):
    """
    get:
        Runs a task with the given task id
    """
    app.loader.import_default_modules()
    tasks = PeriodicTask.objects.filter(id=task_id)
    celery_task = [(app.tasks.get(task.task), loads(task.kwargs)) for task in tasks]
    if any(task is None for task in tasks):
        for task in tasks:
            if task is None:
                break
        not_found_name = tasks[0].name
        return JsonResponse({"message": f"No valid task for {not_found_name}"})
    task_ids = [task.apply_async(kwargs=kwargs) for task, kwargs in celery_task]
    return JsonResponse({"message": "success"})


class TaskView(ListCreateAPIView):
    """
    get:
        Returns a list for user created tasks.

    post:
        Creates a new task
    """

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TaskGetSerializer
        elif self.request.method == "POST":
            return TaskPostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

    def get_queryset(self):
        return self.request.user.task.all()


class CrontabView(APIView):
    """
    get:
        Lists all crontabs for the user
    post:
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
    get:
        Lists all intervals for the user
    post:
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
    get:
        Lists all clock schedules for the user
    post:
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
    get:
        Lists all solar schedules for the user
    post:
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
