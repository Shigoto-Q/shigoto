from django.db import models


class OperatingSystem(models.IntegerChoices):
    UBUNTU = 0
    DEBIAN = 1
    WINDOWS = 2


class Instance(models.IntegerChoices):
    MICRO = 0


class InstanceState(models.IntegerChoices):
    PENDING = 0
    RUNNING = 1

    @classmethod
    def from_response(cls, state: str):
        return cls(state.upper())


class VolumeAttachmentStatus(models.IntegerChoices):
    ATTACHED = 0


class AvailabilityZone(models.TextChoices):
    EU_CENTRAL_1A = 'eu-central-1a'
    EU_CENTRAL_1B = 'eu-central-1b'
