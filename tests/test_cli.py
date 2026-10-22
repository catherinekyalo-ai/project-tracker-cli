from main import main
from models.project import Project
from models.user import User
from utils import storage


def reload():
    storage.clear_all()
    storage.load()


def test_add_user_persists():
    assert main(["add-user", "--name", "Alex", "--email", "alex@example.com"]) == 0
    reload()
    assert User.find("Alex").email == "alex@example.com"


def test_duplicate_user_fails():
    main(["add-user", "--name", "Alex"])
    assert main(["add-user", "--name", "Alex"]) == 1


def test_add_project_unknown_user_fails():
    assert main(["add-project", "--user", "Ghost", "--title", "X"]) == 1


def test_bad_due_date_fails():
    main(["add-user", "--name", "Alex"])
    assert main(["add-project", "--user", "Alex", "--title", "X", "--due", "2026-13-45"]) == 1


def test_full_workflow():
    assert main(["add-user", "--name", "Alex"]) == 0
    assert main(["add-project", "--user", "Alex", "--title", "CLI Tool"]) == 0
    assert main(["add-task", "--project", "CLI Tool", "--title", "Implement add-task",
                 "--assign", "Alex"]) == 0
    assert main(["complete-task", "--project", "CLI Tool", "--title", "Implement add-task"]) == 0
    reload()
    assert Project.find("CLI Tool").tasks[0].status == "complete"


def test_list_and_search_commands_run():
    main(["add-user", "--name", "Alex"])
    main(["add-project", "--user", "Alex", "--title", "CLI Tool"])
    assert main(["list-users"]) == 0
    assert main(["list-projects", "--user", "Alex"]) == 0
    assert main(["search-projects", "--keyword", "cli"]) == 0
