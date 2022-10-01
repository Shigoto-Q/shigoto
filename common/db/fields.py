import django.db
import django.db.models
from django.conf import settings
from django.utils import timezone

from common.db.utils import encrypt_str
from common.db.mixins import EncryptedMixin, EncryptedNumberMixin


class EncryptedCharField(EncryptedMixin, django.db.models.CharField):
    pass


class EncryptedTextField(EncryptedMixin, django.db.models.TextField):
    pass


class EncryptedDateField(EncryptedMixin, django.db.models.DateField):
    pass


class EncryptedDateTimeField(EncryptedMixin, django.db.models.DateTimeField):
    # credit to Oleg Pesok...
    def to_python(self, value):
        value = super(EncryptedDateTimeField, self).to_python(value)

        if value is not None and settings.USE_TZ and timezone.is_naive(value):
            default_timezone = timezone.get_default_timezone()
            value = timezone.make_aware(value, default_timezone)

        return value


class EncryptedEmailField(EncryptedMixin, django.db.models.EmailField):
    pass


class EncryptedBooleanField(EncryptedMixin, django.db.models.BooleanField):

    def get_db_prep_save(self, value, connection):
        if value is None:
            return value
        if value is True:
            value = '1'
        elif value is False:
            value = '0'
        # decode the encrypted value to a unicode string, else this breaks in pgsql
        return encrypt_str(str(value)).decode('utf-8')


class EncryptedIntegerField(EncryptedNumberMixin, django.db.models.IntegerField):
    description = "An IntegerField that is encrypted before " \
                  "inserting into a database using the python cryptography " \
                  "library"
    pass


class EncryptedPositiveIntegerField(EncryptedNumberMixin, django.db.models.PositiveIntegerField):
    pass


class EncryptedSmallIntegerField(EncryptedNumberMixin, django.db.models.SmallIntegerField):
    pass


class EncryptedPositiveSmallIntegerField(
        EncryptedNumberMixin, django.db.models.PositiveSmallIntegerField
):
    pass


class EncryptedBigIntegerField(EncryptedNumberMixin, django.db.models.BigIntegerField):
    pass
