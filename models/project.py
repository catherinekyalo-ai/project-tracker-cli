from models.task import Task
from utils.validation import is_valid_date


class Project:
    """A project with one owner, many tasks, and many contributors."""

    all = []       # class attribute: every project created
    _next_id = 1   # class attribute: ID counter

    def __init__(self, title, owner, description="", due_date=""):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.id = Project._next_id
        Project._next_id += 1
        self.owner = owner
        self.tasks = []
        self.contributors = []
        owner.projects.append(self)      # one-to-many: User -> Projects
        self.add_contributor(owner)      # owner is always a contributor
        Project.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Project title cannot be empty.")
        self._title = value.strip()

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        # Due date is optional, but must be YYYY-MM-DD if given
        value = (value or "").strip()
        if value and not is_valid_date(value):
            raise ValueError("Due date must be a real date in YYYY-MM-DD format.")
        self._due_date = value

    def add_contributor(self, user):
        """Link a user and this project on both sides (many-to-many)."""
        if user not in self.contributors:
            self.contributors.append(user)
            user.contributions.append(self)

    def find_task(self, title):
        """Return the task with this title (case-insensitive), or None."""
        for task in self.tasks:
            if task.title.lower() == title.strip().lower():
                return task
        return None

    def add_task(self, title, assigned_to=None, status="pending"):
        """Add a task. The assignee must be a contributor on this project."""
        if assigned_to is not None and assigned_to not in self.contributors:
            raise ValueError(f"{assigned_to.name} is not a contributor on '{self.title}'.")
        if self.find_task(title):
            raise ValueError(f"Task '{title}' already exists in '{self.title}'.")
        task = Task(title, self, assigned_to, status)
        self.tasks.append(task)
        return task

    @classmethod
    def find(cls, title):
        """Return the project with this title (case-insensitive), or None."""
        for project in cls.all:
            if project.title.lower() == title.strip().lower():
                return project
        return None

    @classmethod
    def search(cls, keyword):
        """Return projects whose title or description contains the keyword."""
        keyword = keyword.lower()
        return [
            p for p in cls.all
            if keyword in p.title.lower() or keyword in p.description.lower()
        ]

    @classmethod
    def reset(cls):
        """Forget all projects and tasks, and reset ID counters."""
        cls.all.clear()
        cls._next_id = 1
        Task.reset()

    def to_dict(self):
        """Return a JSON-friendly dictionary."""
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "owner": self.owner.name,
            "contributors": [u.name for u in self.contributors],
            "tasks": [t.to_dict() for t in self.tasks],
        }

    def __str__(self):
        return f"#{self.id} {self.title} (owner: {self.owner.name}, due: {self.due_date or 'n/a'})"
