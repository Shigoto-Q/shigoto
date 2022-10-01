from django.db import models
from django.contrib.auth import get_user_model

from common.db import fields as common_fields
from shigoto_q.horizon.enums import OperatingSystem, Instance, InstanceState, VolumeAttachmentStatus, AvailabilityZone


User = get_user_model()


class Database(models.Model):
    engine = common_fields.EncryptedCharField(max_length=512)
    host = common_fields.EncryptedCharField(max_length=512, null=True)
    port = common_fields.EncryptedPositiveSmallIntegerField(null=True)
    name = common_fields.EncryptedCharField(max_length=512, null=True)
    username = common_fields.EncryptedCharField(max_length=512, null=True)
    password = models.CharField(max_length=512, null=True)


class VirtualMachine(models.Model):
    instance_id = models.CharField(max_length=512, primary_key=True, unique=True)
    name = models.CharField(max_length=512)
    description = models.CharField(max_length=512)
    image_id = models.CharField(max_length=512, null=True)
    type = models.PositiveIntegerField(choices=Instance.choices)
    state = models.PositiveSmallIntegerField(choices=InstanceState.choices)

    launch_time = models.DateTimeField()

    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    volume = models.ForeignKey('Volume', on_delete=models.PROTECT)
    network = models.ForeignKey('Network', on_delete=models.PROTECT)
    key = models.ForeignKey('key', on_delete=models.PROTECT, null=True)


class Volume(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=512)
    device_name = models.CharField(max_length=512)
    attachment_status = models.PositiveSmallIntegerField(choices=VolumeAttachmentStatus.choices)
    attachment_time = models.DateTimeField()
    encrypted = models.BooleanField(default=False)
    size = models.PositiveSmallIntegerField()

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.PROTECT)


class Network(models.Model):
    interface_id = models.CharField(primary_key=True, unique=True, max_length=512)
    description = models.CharField(max_length=512)

    availability_zone = models.CharField(choices=AvailabilityZone.choices, max_length=512)

    public_ipv4_dns = models.CharField(max_length=512, null=True)
    public_ipv4_address = models.CharField(max_length=512, null=True)

    private_ipv4_dns = common_fields.EncryptedCharField(max_length=512, null=True)
    private_ipv4_address = common_fields.EncryptedCharField(max_length=512, null=True)

    public_ipv6_address = models.CharField(max_length=512, null=True)

    vpc_id = common_fields.EncryptedCharField(max_length=512)
    subnet_id = common_fields.EncryptedCharField(max_length=512)

    owner = models.ForeignKey(User, on_delete=models.PROTECT)


class Key(models.Model):
    pair_id = common_fields.EncryptedCharField(max_length=512, unique=True, primary_key=True)
    name = common_fields.EncryptedCharField(max_length=512)
    fingerprint = common_fields.EncryptedTextField()

    owner = models.OneToOneField(User, on_delete=models.PROTECT)

