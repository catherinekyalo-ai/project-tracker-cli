import pytest

from models.project import Project
from models.user import User
from utils import storage


def test_invalid_email_rejected():
    with pytest.raises(ValueError):
        User("Alex", "not-an-email")


def test_empty_name_rejected():
    with pytest.raises(ValueError):
        User("   ")


def test_user_owns_many_projects():
    alex = User("Alex")
    Project("One", alex)
    Project("Two", alex)
    assert [p.title for p in alex.projects] == ["One", "Two"]


def test_bad_due_date_rejected():
    with pytest.raises(ValueError):
        Project("One", User("Alex"), due_date="2026-13-45")


def test_contributors_are_many_to_many():
    alex, sam = User("Alex"), User("Sam")
    one, two = Project("One", alex), Project("Two", alex)
    one.add_contributor(sam)
    two.add_contributor(sam)
    assert sam in one.contributors and sam in two.contributors
    assert one in sam.contributions and two in sam.contributions


def test_task_assignee_must_be_contributor():
    alex, sam = User("Alex"), User("Sam")
    project = Project("One", alex)
    with pytest.raises(ValueError):
        project.add_task("Write code", sam)
    project.add_contributor(sam)
    assert project.add_task("Write code", sam).assigned_to is sam


def test_duplicate_task_rejected():
    project = Project("One", User("Alex"))
    project.add_task("Write code")
    with pytest.raises(ValueError):
        project.add_task("write code")


def test_complete_task_twice_fails():
    task = Project("One", User("Alex")).add_task("Write code")
    task.complete()
    assert task.status == "complete"
    with pytest.raises(ValueError):
        task.complete()


def test_search_matches_title_and_description():
    alex = User("Alex")
    Project("CLI Tool", alex, "command line")
    Project("Website", alex, "landing page")
    assert [p.title for p in Project.search("cli")] == ["CLI Tool"]
    assert [p.title for p in Project.search("landing")] == ["Website"]


def test_save_and_load_round_trip():
    alex = User("Alex", "alex@example.com")
    project = Project("One", alex, "desc", "2026-11-01")
    project.add_task("Write code", alex).complete()
    storage.save()
    storage.clear_all()
    storage.load()
    loaded = Project.find("One")
    assert loaded.owner.email == "alex@example.com"
    assert loaded.tasks[0].status == "complete"
    assert loaded.tasks[0].assigned_to.name == "Alex"


def test_missing_file_starts_empty():
    storage.load()
    assert User.all == [] and Project.all == []


def test_malformed_file_starts_empty():
    with open(storage.DATA_FILE, "w") as file:
        file.write("{ not json")
    storage.load()
    assert User.all == []
