# To-Do API

A small FastAPI application implementing a To-Do list with CRUD endpoints,
backed by SQLite via SQLAlchemy.

## Features

- `POST /todos` — create a to-do item (optionally with an ISO `due_date`, e.g. `2026-01-15`)
- `GET /todos` — list to-do items (supports `skip`/`limit` pagination and a `due_before` date filter)
- `GET /todos/{todo_id}` — fetch a single to-do item
- `PATCH /todos/{todo_id}` — partially update a to-do item
- `DELETE /todos/{todo_id}` — delete a to-do item
- `GET /health` — health check

### `due_date` field

Each to-do has an optional `due_date` (ISO `YYYY-MM-DD`). Use `GET /todos?due_before=<date>`
to list only items whose `due_date` is earlier than the given date. Items without a
`due_date` are excluded from `due_before` results.

## Requirements

- Python 3.11+

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Interactive docs are
served at `http://127.0.0.1:8000/docs`.

Data is stored in a local SQLite file `todos.db` (created automatically on
first run). Override the location via the `DATABASE_URL` environment
variable, e.g.:

```bash
DATABASE_URL=sqlite:///./data/todos.db uvicorn app.main:app
```

## Running the tests

```bash
pytest
```

Tests run against isolated, temporary SQLite databases and do not touch the
development database file.

## Example usage

```bash
# Create a todo
curl -X POST http://127.0.0.1:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk", "description": "2 liters"}'

# List todos
curl http://127.0.0.1:8000/todos

# List todos due before a given date
curl "http://127.0.0.1:8000/todos?due_before=2026-06-01"

# Mark a todo as completed
curl -X PATCH http://127.0.0.1:8000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete a todo
curl -X DELETE http://127.0.0.1:8000/todos/1
```

## Project layout

```
app/
  main.py       # FastAPI app and route handlers
  database.py   # SQLAlchemy engine/session setup
  models.py     # ORM models
  schemas.py    # Pydantic request/response schemas
  crud.py       # Database access functions
tests/
  conftest.py   # Test fixtures (isolated SQLite DB per test)
  test_todos.py # CRUD endpoint tests
```
