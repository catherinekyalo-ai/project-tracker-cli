from utils.validation import is_valid_email


class Person:
    """Base class for anyone with a name and an optional email."""

    def __init__(self, name, email=""):
        self.name = name
        self.email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Name must be a non-empty string
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        # Email is optional, but must look valid if given
        value = (value or "").strip()
        if value and not is_valid_email(value):
            raise ValueError("Invalid email address.")
        self._email = value
