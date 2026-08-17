"""CRUD endpoint tests for the To-Do API."""


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_todo(client):
    response = client.post(
        "/todos", json={"title": "Buy milk", "description": "2 liters"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["description"] == "2 liters"
    assert data["completed"] is False
    assert data["due_date"] is None
    assert "id" in data
    assert "created_at" in data


def test_create_todo_with_due_date(client):
    response = client.post(
        "/todos", json={"title": "Pay rent", "due_date": "2026-01-15"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["due_date"] == "2026-01-15"


def test_create_todo_rejects_invalid_due_date(client):
    response = client.post(
        "/todos", json={"title": "Bad date", "due_date": "not-a-date"}
    )
    assert response.status_code == 422


def test_create_todo_requires_title(client):
    response = client.post("/todos", json={"description": "no title"})
    assert response.status_code == 422


def test_list_todos_empty(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_list_todos_returns_created_items(client):
    client.post("/todos", json={"title": "First"})
    client.post("/todos", json={"title": "Second"})

    response = client.get("/todos")
    assert response.status_code == 200
    titles = [todo["title"] for todo in response.json()]
    assert titles == ["First", "Second"]


def test_list_todos_filter_due_before(client):
    client.post("/todos", json={"title": "Overdue", "due_date": "2026-01-01"})
    client.post("/todos", json={"title": "Due soon", "due_date": "2026-06-01"})
    client.post("/todos", json={"title": "No due date"})

    response = client.get("/todos", params={"due_before": "2026-03-01"})
    assert response.status_code == 200
    titles = [todo["title"] for todo in response.json()]
    assert titles == ["Overdue"]


def test_list_todos_filter_due_before_excludes_items_without_due_date(client):
    client.post("/todos", json={"title": "No due date"})

    response = client.get("/todos", params={"due_before": "2099-01-01"})
    assert response.status_code == 200
    assert response.json() == []


def test_list_todos_filter_due_before_invalid_date(client):
    response = client.get("/todos", params={"due_before": "not-a-date"})
    assert response.status_code == 422


def test_get_todo_by_id(client):
    created = client.post("/todos", json={"title": "Read a book"}).json()

    response = client.get(f"/todos/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Read a book"


def test_get_todo_not_found(client):
    response = client.get("/todos/9999")
    assert response.status_code == 404


def test_update_todo_partial(client):
    created = client.post("/todos", json={"title": "Old title"}).json()

    response = client.patch(f"/todos/{created['id']}", json={"completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    assert data["title"] == "Old title"


def test_update_todo_due_date(client):
    created = client.post("/todos", json={"title": "Old title"}).json()

    response = client.patch(
        f"/todos/{created['id']}", json={"due_date": "2026-12-25"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["due_date"] == "2026-12-25"
    assert data["title"] == "Old title"


def test_update_todo_not_found(client):
    response = client.patch("/todos/9999", json={"title": "Nope"})
    assert response.status_code == 404


def test_delete_todo(client):
    created = client.post("/todos", json={"title": "Delete me"}).json()

    response = client.delete(f"/todos/{created['id']}")
    assert response.status_code == 204

    response = client.get(f"/todos/{created['id']}")
    assert response.status_code == 404


def test_delete_todo_not_found(client):
    response = client.delete("/todos/9999")
    assert response.status_code == 404
