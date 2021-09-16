from django.db import models


class AdminConfig(models.Model):
    environment = models.CharField(max_length=120, default='production')
    repository = models.CharField(max_length=120, default='backend')
    base_url = models.CharField(max_length=56, default="http://shigoto.live")
    notes = models.CharField(max_length=256, default='')
