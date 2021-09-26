from __future__ import absolute_import

from django.contrib.auth import get_user_model
from django.http import Http404
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from config.celery_app import app
from shigoto_q.tasks.api.serializers import (
    ClockedSerializer,
    CrontabSerializer,
    IntervalSerializer,
    SolarSerializer,
    TaskGetSerializer,
    TaskPostSerializer,
    TaskResultSerializer,
    TaskUpdateSerializer,
)
from shigoto_q.tasks.models import TaskResult, UserTask
from shigoto_q.tasks.services import tasks as task_services

User = get_user_model()


class RunTaskView(APIView):
    """
    An APIView to run the given task
    get:
        runs the task
    """

    def get_object(self, task_id: int):
        return task_services.run_task(app, task_id)
        # try:
        #    return task_services.run_task(app, task_id)
        # except Exception:
        #    return None

    def get(self, request, task_id: int, *args, **kwargs):
        result = self.get_object(task_id)
        if result:
            return Response(result)
        return Response(status=404)


class TaskResultView(APIView):
    """
    View to return task results
    """

    def get_object(self, task_id: int):
        try:
            return TaskResult.objects.filter(user=self.request.user, task_id=task_id)
        except TaskResult.DoesNotExist:
            return Http404

    def get(self, request, task_id: int, *args, **kwargs):
        task_result = self.get_object(task_id)
        serializer = TaskResultSerializer(task_result, many=True)
        return Response(serializer.data)


class TaskUpdateView(UpdateAPIView):
    serializer_class = TaskUpdateSerializer

    def get_object(self, task_id: int):
        try:
            return UserTask.objects.get(pk=task_id)
        except UserTask.DoesNotExist:
            raise Http404

    def update(self, request, task_id, *args, **kwargs):
        instance = self.get_object(task_id)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class TaskDeleteView(APIView):
    """
    View to delete the given task id
    delete:
        deletes the task
    """

    def get_object(self, task_id: int):
        try:
            return PeriodicTask.objects.filter(id=task_id)
        except PeriodicTask.DoesNotExist:
            raise Http404

    def delete(self, request, task_id: int, format=None):
        task = self.get_object(task_id)
        task.delete()
        return Response(data=task_id, status=204)


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
