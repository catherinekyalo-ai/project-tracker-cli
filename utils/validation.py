import re
from datetime import datetime

EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


def is_valid_email(email):
    """Return True if the email looks like name@domain.tld."""
    return bool(EMAIL_PATTERN.match(email))


def is_valid_date(date_text):
    """Return True if date_text is a real date in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False
