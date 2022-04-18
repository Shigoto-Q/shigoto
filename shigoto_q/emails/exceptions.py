class BaseEmailException(Exception):
    pass


class EmailRecipientDoesNotExist(BaseEmailException):
    pass


class UserEmailNotFound(BaseEmailException):
    pass
