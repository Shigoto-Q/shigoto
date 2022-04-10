from typing import Union


class ColourNotInRangeException(Exception):
    color: Union[str, int]

    def __init__(self, color) -> None:
        self.color = color
        super().__init__()

    def __str__(self) -> str:
        return repr(
            f"{self.color!r} is not in valid range of colors. The valid ranges "
            "of colors are 0 to 16777215 inclusive (INTEGERS) and 0 "
            "to FFFFFF inclusive (HEXADECIMAL)"
        )
