import logging

from django.db import connection, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from shigoto_q.users.models import User

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
@transaction.atomic()
def create_trigger_for_new_user(sender, instance, created, **kwargs):
    query = (
        "CREATE TRIGGER result_notify_event_{id} "
        "AFTER INSERT OR UPDATE OR DELETE on tasks_taskresult FOR EACH ROW "
        "EXECUTE PROCEDURE notify_event({id});"
    )
    with connection.cursor() as curr:
        if created:
            curr.execute(query.format(id=instance.id))
            logger.info(f"Created tasks_taskresult trigger for User(id={instance.id}")
