import json
import logging
import os

from models.project import Project
from models.user import User

DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "tracker.json"
)


def clear_all():
    """Remove every object and reset ID counters."""
    User.reset()
    Project.reset()


def save(path=None):
    """Write all users, projects, and tasks to a JSON file."""
    path = path or DATA_FILE
    data = {
        "users": [u.to_dict() for u in User.all],
        "projects": [p.to_dict() for p in Project.all],
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as file:
        json.dump(data, file, indent=2)


def load(path=None):
    """Rebuild objects from the JSON file. Missing or bad files start empty."""
    path = path or DATA_FILE
    clear_all()
    try:
        with open(path) as file:
            data = json.load(file)
    except FileNotFoundError:
        return
    except json.JSONDecodeError:
        logging.error("Data file %s is not valid JSON; starting empty.", path)
        return

    try:
        for item in data["users"]:
            User(item["name"], item.get("email", ""))
        for item in data["projects"]:
            project = Project(
                item["title"],
                User.find(item["owner"]),
                item.get("description", ""),
                item.get("due_date", ""),
            )
            for name in item.get("contributors", []):
                project.add_contributor(User.find(name))
            for task in item.get("tasks", []):
                assignee = User.find(task["assigned_to"]) if task.get("assigned_to") else None
                project.add_task(task["title"], assignee, task.get("status", "pending"))
    except (KeyError, ValueError, TypeError, AttributeError) as error:
        logging.error("Data file %s is malformed (%s); starting empty.", path, error)
        clear_all()
