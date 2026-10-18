# Project Tracker CLI

A command-line tool for managing users, projects, and tasks. Data is saved locally as JSON.

## Setup

    git clone https://github.com/catherinekyalo-ai/project-tracker-cli.git
    cd project-tracker-cli
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Commands

    python3 main.py add-user --name "Alex" --email "alex@example.com"
    python3 main.py list-users
    python3 main.py add-project --user "Alex" --title "CLI Tool" --description "Build a CLI" --due 2026-12-01
    python3 main.py list-projects
    python3 main.py list-projects --user "Alex"
    python3 main.py search-projects --keyword "cli"
    python3 main.py add-contributor --project "CLI Tool" --user "Sam"
    python3 main.py add-task --project "CLI Tool" --title "Implement add-task" --assign "Alex"
    python3 main.py list-tasks --project "CLI Tool"
    python3 main.py complete-task --project "CLI Tool" --title "Implement add-task"

## Features

- Users own many projects (one-to-many); projects have many tasks (one-to-many)
- Projects and contributors are many-to-many; tasks can only be assigned to a project's contributors
- Input validation for names, emails, and due dates (YYYY-MM-DD)
- JSON persistence in `data/tracker.json`, with safe handling of missing or malformed files
- Pretty tables with `rich`; errors are logged to `data/tracker.log`

## Structure

- `main.py`: CLI entry point (argparse)
- `models/`: `Person`, `User`, `Project`, `Task`
- `utils/`: validation and JSON storage
- `tests/`: pytest unit and CLI tests

## Run tests

    pytest -v

## Known issues

- Users, projects, and tasks are identified by name or title, so each must be unique
- No delete or edit commands yet
- Contributors cannot be removed once added
