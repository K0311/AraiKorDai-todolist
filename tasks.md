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

- [x] **1. Project Initialization & Data Models**
    - Create `main.py` as the entry point.
    - Create a `models.py` file.
    - Define a `TodoItem` class (using dataclasses or Pydantic) containing the fields defined in the Todo Schema above.
    - Create Python `Enum` classes for Priority (HIGH, MID, LOW) and Status (PENDING, COMPLETED) to ensure consistency.

- [x] **2. CLI Interface - Basic Interaction**
    - Implement a main application loop.
    - Create a "Pre-Login" menu: Options for [1] Login, [2] Sign Up, [3] Exit.
  
- [x] **3. Create & Edit To-Do List Items**
    - Implement a CLI menu option to **create a new to-do item**.
    - Prompt the user to input required fields:
        - Title
        - Description (optional)
        - Priority (HIGH / MID / LOW)
        - Due date (optional)
    - Automatically assign default values:
        - Status = PENDING
        - Created timestamp
    - Validate user input (e.g., valid priority, non-empty title).
    - Store created to-do items in an in-memory list or data structure.
    - Implement an **edit to-do item** feature:
        - Display existing to-do items with unique IDs or indexes.
        - Allow the user to select an item to edit.
        - Enable updating one or more fields (title, description, priority, status, due date).
    - Persist changes to the selected to-do item.

- [x] **4. View All To-Do List Items**
    - Implement a CLI menu option to **view all to-do items**.
    - Retrieve all stored to-do items from the in-memory data structure.
    - Display each to-do item in a clear, readable format, including:
        - ID or index
        - Title
        - Priority
        - Status
        - Due date (if available)
    - Handle the case where no to-do items exist by displaying an appropriate message.
    - Ensure the list is ordered logically (e.g., by creation time or due date).
    - Format output for readability in the CLI (spacing, separators, numbering).

- [x] **5. View To-Do List Item Details**
    - Implement a CLI menu option to **view detailed information of a specific to-do item**.
    - Display a list of existing to-do items with their IDs or indexes for selection.
    - Allow the user to select a to-do item by ID or index.
    - Display the selected to-do item’s details, including:
        - Title
        - Details (description)
        - Priority (HIGH / MID / LOW)
        - Status (COMPLETED / PENDING)
        - Owner
        - Created date
        - Updated date
    - Handle invalid selections gracefully (e.g., item not found).
    - Ensure dates are formatted consistently and clearly for CLI output.

- [x] **6. Mark a To-Do List Item as Completed**
    - Implement a CLI menu option to **mark a to-do item as completed**.
    - Display a list of existing to-do items with their IDs or indexes.
    - Allow the user to select a to-do item by ID or index.
    - Update the selected to-do item’s status to:
        - Status = COMPLETED
    - Automatically update the item’s updated date timestamp.
    - Prevent re-completing an already completed item and display an appropriate message.
    - Confirm the successful status update to the user.
    - Handle invalid selections gracefully (e.g., item not found).
