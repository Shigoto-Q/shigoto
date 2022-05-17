from shigoto_q.integrations.models import WebhookEvent, WebhookObserver


def get_observer_for_event(user_id: int, event: str):
    event = WebhookEvent.objects.get(name=event)
    return (
        WebhookObserver.objects.filter(user_id=user_id)
        .filter(events__in=[event])
        .distinct()
        .first()
    )
