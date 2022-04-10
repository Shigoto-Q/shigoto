from django.contrib.auth import get_user_model
from django.conf import settings
from post_office import mail

from shigoto_q.emails.constants import EmailTypes, EmailPriority
from shigoto_q.emails.exceptions import UserEmailNotFound


User = get_user_model()


def send_email(
    template_name: EmailTypes,
    priority: EmailPriority = EmailPriority.HIGH,
    user_id: int = None,
    context: dict = None,
    override_email=None,
):
    _default_context = {}
    to_email = _get_email(user_id, override_email)
    _update_default_context(_default_context, to_email)
    context = {**context, **_default_context}

    mail.send(
        [to_email],
        settings.DEFAULT_INFO_EMAIL,
        template=template_name.get_name(),
        context=context,
        priority=priority.value,
    )


def _get_email(user_id=None, override_email=None):
    if user_id:
        try:
            return User.objects.get(id=user_id).email
        except User.DoesNotExist:
            raise UserEmailNotFound(f"User(id={user_id}) not found.")
    if override_email:
        return override_email


def _update_default_context(context, to_email):
    context.update(
        dict(
            to_email=to_email,
        )
    )
