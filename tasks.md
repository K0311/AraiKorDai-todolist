# Project: Python CLI To-Do List Application

## Context & Architecture
We are building a command-line interface (CLI) application for managing to-do lists. The application acts as a REPL (Read-Eval-Print Loop) or interactive shell.
* **Language:** Python 3.10+
* **Data Storage:** Local JSON files (`users.json` for auth, `todos.json` for items).
* **Structure:** Separation of concerns between `AuthManager` (User logic), `TodoManager` (Business logic), and `App` (CLI presentation).

## Data Models

**1. User Schema**
Stored in `users.json`:
`{"username": "...", "password": "..."}`

**2. Todo Schema**
Stored in `todos.json`. Note that `id` must be unique (UUID).
    {
      "id": "uuid-string",
      "title": "String",
      "details": "String",
      "priority": "HIGH | MID | LOW",
      "status": "PENDING | COMPLETED",
      "owner": "username_string",
      "created_at": "ISO-8601 String",
      "updated_at": "ISO-8601 String"
    }

---

## Development Tasks

- [ ] **1. Project Initialization & Data Models**
    - Create `main.py` as the entry point.
    - Create a `models.py` file.
    - Define a `TodoItem` class (using dataclasses or Pydantic) containing the fields defined in the Todo Schema above.
    - Create Python `Enum` classes for Priority (HIGH, MID, LOW) and Status (PENDING, COMPLETED) to ensure consistency.

- [ ] **2. CLI Interface - Basic Interaction**
    - Implement a main application loop.
    - Create a "Pre-Login" menu: Options for [1] Login, [2] Sign Up, [3] Exit.
