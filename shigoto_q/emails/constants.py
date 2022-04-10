import enum

_GENERATED_PREFIX = "generated"
_SOURCE_PREFIX = "src"

_HTML_SUFFIX = ".html"
_SRC_SUFFIX = ".mjml"


class EmailPriority(enum.Enum):
    NOW = "now"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class EmailTypes(enum.Enum):
    USER_SUBSCRIPTION = f"{_GENERATED_PREFIX}/users/subscription"

    def get_description(self):
        return _description_mapping.get(self.value)

    def to_html(self):
        return self.value + _HTML_SUFFIX

    def to_mjml(self):
        return self.value + _SRC_SUFFIX

    def get_name(self):
        return _name_mapping[self.value]

    def get_subject(self):
        return _subject_mapping[self.value]


_description_mapping = {
    EmailTypes.USER_SUBSCRIPTION.value: "E-mail template used for notifying users they have subscribed for our release.",
}
_name_mapping = {
    EmailTypes.USER_SUBSCRIPTION.value: "User subscription e-mail template"
}
_subject_mapping = {EmailTypes.USER_SUBSCRIPTION.value: "Hello there!"}
