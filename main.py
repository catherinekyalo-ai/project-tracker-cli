import argparse
import logging
import os
import sys

from utils.display import Console, Table

from models.project import Project
from models.user import User
from utils import storage

console = Console()
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "tracker.log")


def get_user(name):
    """Return the named user or raise ValueError."""
    user = User.find(name)
    if user is None:
        raise ValueError(f"User '{name}' not found.")
    return user


def get_project(title):
    """Return the named project or raise ValueError."""
    project = Project.find(title)
    if project is None:
        raise ValueError(f"Project '{title}' not found.")
    return project


def show_projects(projects):
    """Print projects as a table."""
    if not projects:
        console.print("No projects found.")
        return
    table = Table(title="Projects")
    for column in ("ID", "Title", "Owner", "Due", "Contributors", "Done"):
        table.add_column(column)
    for p in projects:
        done = sum(1 for t in p.tasks if t.status == "complete")
        table.add_row(
            str(p.id), p.title, p.owner.name, p.due_date or "-",
            ", ".join(c.name for c in p.contributors), f"{done}/{len(p.tasks)}",
        )
    console.print(table)


def cmd_add_user(args):
    if User.find(args.name):
        raise ValueError(f"User '{args.name}' already exists.")
    user = User(args.name, args.email)
    console.print(f"Added user: {user}")


def cmd_list_users(args):
    if not User.all:
        console.print("No users yet.")
        return
    table = Table(title="Users")
    for column in ("Name", "Email", "Projects owned"):
        table.add_column(column)
    for u in User.all:
        table.add_row(u.name, u.email or "-", str(len(u.projects)))
    console.print(table)


def cmd_add_project(args):
    owner = get_user(args.user)
    if Project.find(args.title):
        raise ValueError(f"Project '{args.title}' already exists.")
    project = Project(args.title, owner, args.description, args.due)
    console.print(f"Added project: {project}")


def cmd_list_projects(args):
    projects = get_user(args.user).projects if args.user else Project.all
    show_projects(projects)


def cmd_search_projects(args):
    show_projects(Project.search(args.keyword))


def cmd_add_contributor(args):
    project = get_project(args.project)
    user = get_user(args.user)
    project.add_contributor(user)
    console.print(f"{user.name} is now a contributor on '{project.title}'.")


def cmd_add_task(args):
    project = get_project(args.project)
    assignee = get_user(args.assign) if args.assign else None
    task = project.add_task(args.title, assignee)
    console.print(f"Added task: {task}")


def cmd_list_tasks(args):
    project = get_project(args.project)
    if not project.tasks:
        console.print("No tasks yet.")
        return
    table = Table(title=f"Tasks for {project.title}")
    for column in ("ID", "Title", "Status", "Assigned to"):
        table.add_column(column)
    for t in project.tasks:
        table.add_row(str(t.id), t.title, t.status, t.assigned_to.name if t.assigned_to else "-")
    console.print(table)


def cmd_complete_task(args):
    project = get_project(args.project)
    task = project.find_task(args.title)
    if task is None:
        raise ValueError(f"Task '{args.title}' not found in '{project.title}'.")
    task.complete()
    console.print(f"Completed: {task}")


def build_parser():
    """Define all CLI subcommands."""
    parser = argparse.ArgumentParser(description="Project tracker CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add-user", help="Create a user")
    p.add_argument("--name", required=True)
    p.add_argument("--email", default="")
    p.set_defaults(func=cmd_add_user)

    p = sub.add_parser("list-users", help="List all users")
    p.set_defaults(func=cmd_list_users)

    p = sub.add_parser("add-project", help="Add a project to a user")
    p.add_argument("--user", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--description", default="")
    p.add_argument("--due", default="", help="YYYY-MM-DD")
    p.set_defaults(func=cmd_add_project)

    p = sub.add_parser("list-projects", help="List projects (optionally for one user)")
    p.add_argument("--user")
    p.set_defaults(func=cmd_list_projects)

    p = sub.add_parser("search-projects", help="Search projects by keyword")
    p.add_argument("--keyword", required=True)
    p.set_defaults(func=cmd_search_projects)

    p = sub.add_parser("add-contributor", help="Add a user as a contributor to a project")
    p.add_argument("--project", required=True)
    p.add_argument("--user", required=True)
    p.set_defaults(func=cmd_add_contributor)

    p = sub.add_parser("add-task", help="Add a task to a project")
    p.add_argument("--project", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--assign", help="Contributor to assign the task to")
    p.set_defaults(func=cmd_add_task)

    p = sub.add_parser("list-tasks", help="List a project's tasks")
    p.add_argument("--project", required=True)
    p.set_defaults(func=cmd_list_tasks)

    p = sub.add_parser("complete-task", help="Mark a task as complete")
    p.add_argument("--project", required=True)
    p.add_argument("--title", required=True)
    p.set_defaults(func=cmd_complete_task)

    return parser


def main(argv=None):
    """Run one command. Returns 0 on success, 1 on a user error."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    args = build_parser().parse_args(argv)
    storage.load()
    try:
        args.func(args)
    except ValueError as error:
        logging.warning("%s failed: %s", args.command, error)
        console.print(f"[red]Error:[/red] {error}")
        return 1
    logging.info("%s succeeded", args.command)
    storage.save()
    return 0


if __name__ == "__main__":
    sys.exit(main())
