from django.db import models
from django.contrib.auth import get_user_model

from common.db import fields as common_fields


User = get_user_model()


class Database(models.Model):
    engine = common_fields.EncryptedCharField(max_length=512)
    host = common_fields.EncryptedCharField(max_length=512, null=True)
    port = common_fields.EncryptedPositiveSmallIntegerField(null=True)
    name = common_fields.EncryptedCharField(max_length=512, null=True)
    username = common_fields.EncryptedCharField(max_length=512, null=True)
    password = models.CharField(max_length=512, null=True)
