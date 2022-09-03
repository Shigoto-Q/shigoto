from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class FeatureFlag(models.Model):
    definition = models.CharField(max_length=512)
    description = models.TextField(max_length=1024)
    enabled = models.BooleanField(default=False)
    users = models.ManyToManyField(User)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
