from django.db.models import IntegerChoices


class WebhookType(IntegerChoices):
    DISCORD = 0
    SLACK = 1


class WebhookEvent(IntegerChoices):
    pass
