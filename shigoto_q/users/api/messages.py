from dataclasses import dataclass


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    two_factor_auth_enabled: bool
    is_first_login: bool

    @classmethod
    def from_dict(cls, user):
        return cls(
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            two_factor_auth_enabled=user["two_factor_enabled"],
            is_first_login=user["is_first_login"],
        )
