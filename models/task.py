class Task:
    """A task that belongs to one project and may be assigned to a user."""

    STATUSES = ("pending", "complete")
    _next_id = 1  # class attribute: ID counter

    def __init__(self, title, project, assigned_to=None, status="pending"):
        self.title = title
        self.status = status
        self.id = Task._next_id
        Task._next_id += 1
        self.project = project
        self.assigned_to = assigned_to

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Task title cannot be empty.")
        self._title = value.strip()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in Task.STATUSES:
            raise ValueError(f"Status must be one of {Task.STATUSES}.")
        self._status = value

    def complete(self):
        """Mark the task as complete."""
        if self.status == "complete":
            raise ValueError("Task is already complete.")
        self.status = "complete"

    @classmethod
    def reset(cls):
        """Reset the ID counter."""
        cls._next_id = 1

    def to_dict(self):
        """Return a JSON-friendly dictionary."""
        return {
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to.name if self.assigned_to else None,
        }

    def __str__(self):
        who = self.assigned_to.name if self.assigned_to else "unassigned"
        return f"#{self.id} {self.title} [{self.status}] ({who})"
