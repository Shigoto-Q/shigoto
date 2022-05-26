class BaseUserException(Exception):
    pass


class UserExceededLimitError(BaseUserException):
    pass
