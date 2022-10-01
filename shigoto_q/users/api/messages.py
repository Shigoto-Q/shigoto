import typing
from dataclasses import dataclass


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    two_factor_auth_enabled: typing.Optional[bool]
    is_first_login: typing.Optional[bool]
    company: typing.Optional[str]
    country: typing.Optional[str]

    @classmethod
    def from_dict(cls, user):
        return cls(
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            two_factor_auth_enabled=user["two_factor_enabled"],
            is_first_login=user["is_first_login"],
            company=None,
            country=None,
        )

    @classmethod
    def from_model(cls, user):
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            two_factor_auth_enabled=None,
            is_first_login=None,
            company=user.company,
            country=user.country,
        )
