import itertools
import cryptography.fernet

import django.db
import django.db.models
from django.core import validators
from django.utils.functional import cached_property

from common.db.utils import encrypt_str, decrypt_str


class EncryptedMixin(object):
    def to_python(self, value):
        if value is None:
            return value

        if isinstance(value, (bytes, str)):
            if isinstance(value, bytes):
                value = value.decode("utf-8")
            try:
                value = decrypt_str(value)
            except cryptography.fernet.InvalidToken:
                pass

        return super(EncryptedMixin, self).to_python(value)

    def from_db_value(self, value, *args, **kwargs):
        return self.to_python(value)

    def get_db_prep_save(self, value, connection):
        value = super(EncryptedMixin, self).get_db_prep_save(value, connection)

        if value is None:
            return value
        # decode the encrypted value to a unicode string, else this breaks in pgsql
        return (encrypt_str(str(value))).decode("utf-8")

    def get_internal_type(self):
        return "TextField"

    def deconstruct(self):
        name, path, args, kwargs = super(EncryptedMixin, self).deconstruct()

        if "max_length" in kwargs:
            del kwargs["max_length"]

        return name, path, args, kwargs


class EncryptedNumberMixin(EncryptedMixin):
    max_length = 20

    @cached_property
    def validators(self):
        # These validators can't be added at field initialization time since
        # they're based on values retrieved from `connection`.
        range_validators = []
        internal_type = self.__class__.__name__[9:]
        min_value, max_value = django.db.connection.ops.integer_field_range(
            internal_type
        )
        if min_value is not None:
            range_validators.append(validators.MinValueValidator(min_value))
        if max_value is not None:
            range_validators.append(validators.MaxValueValidator(max_value))
        return list(
            itertools.chain(self.default_validators, self._validators, range_validators)
        )
