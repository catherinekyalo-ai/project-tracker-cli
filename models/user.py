from models.person import Person


class User(Person):
    """A team member. One user owns many projects (one-to-many)."""

    all = []  # class attribute: every user created

    def __init__(self, name, email=""):
        super().__init__(name, email)
        self.projects = []       # projects this user owns
        self.contributions = []  # projects this user contributes to (many-to-many)
        User.all.append(self)

    @classmethod
    def find(cls, name):
        """Return the user with this name (case-insensitive), or None."""
        for user in cls.all:
            if user.name.lower() == name.lower():
                return user
        return None

    @classmethod
    def reset(cls):
        """Forget all users (used when loading data and in tests)."""
        cls.all.clear()

    def to_dict(self):
        """Return a JSON-friendly dictionary."""
        return {"name": self.name, "email": self.email}

    def __str__(self):
        return f"{self.name} ({self.email or 'no email'}) - {len(self.projects)} project(s)"

    def __repr__(self):
        return f"User(name={self.name!r})"
