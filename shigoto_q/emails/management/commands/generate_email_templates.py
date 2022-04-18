from __future__ import absolute_import

import logging

import sentry_sdk
from post_office.models import EmailTemplate
from django.core.management.base import BaseCommand
from django.template.loader import get_template

from shigoto_q.emails.constants import EmailTypes

logger = logging.getLogger(__name__)
_LOG_PREFIX = "[GENERATE-EMAIL_TEMPLATES]"


class Command(BaseCommand):
    help = "Command to generate EmailTemplate instances for created templates."
    is_log = False

    @classmethod
    def _log(cls, message):
        if cls.is_log:
            return logger.info(message)
        else:
            return print(message)

    @classmethod
    def _read_template_file(cls, filename: str):
        with open(filename, "r") as f:
            html_string = f.read()
        return html_string

    @classmethod
    def generate_templates(cls):
        for email_template in EmailTypes:
            try:
                template = get_template(email_template.to_html())
                EmailTemplate.objects.create(
                    name=email_template.get_name(),
                    subject=email_template.get_subject(),
                    description=email_template.get_description(),
                    html_content=template.template.source,
                )
            except EmailTemplate.MultipleObjectsReturned:
                cls._log(
                    f"{_LOG_PREFIX} E-mail(name={email_template.name}) already exists, moving on..."
                )
            except Exception as e:
                logger.exception(
                    f"{_LOG_PREFIX} Caught an error while generating email templates."
                )
                sentry_sdk.capture_message(str(e))
            cls._log(
                f"{_LOG_PREFIX} E-mail(name={email_template.name}) has been generated."
            )

    def handle(self, *args, **options):
        self.stdout.write("Generating E-mail templates...")
        self.generate_templates()
