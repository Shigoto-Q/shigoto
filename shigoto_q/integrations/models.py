from django.db import models
from django.contrib.auth import get_user_model

from shigoto_q.integrations.enums import WebhookType
from shigoto_q.integrations.constants import EventMapping, Event


User = get_user_model()


class WebhookIntegration(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=128)
    type = models.PositiveSmallIntegerField(choices=WebhookType.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class WebhookEvent(models.Model):
    name = models.CharField(unique=True, max_length=512)


class WebhookObserver(models.Model):
    name = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    webhook = models.ForeignKey(WebhookIntegration, on_delete=models.CASCADE)
    events = models.ManyToManyField(WebhookEvent)

    def execute(
        self,
        event_type: Event,
        description: str,
    ) -> None:
        client = EventMapping[event_type.name].value()
        client.execute(
            url=self.webhook.url,
            title="Kubernetes deployment",
            description=description,
            color="3970e4",
            embed_url="https://kubernetes.io/",
            footer="This is deployment from shigoto",
        )
