"""Database access layer for To-Do items."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate


def create_todo(db: Session, todo: TodoCreate) -> Todo:
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todo(db: Session, todo_id: int) -> Todo | None:
    return db.get(Todo, todo_id)


def get_todos(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    due_before: date | None = None,
) -> list[Todo]:
    stmt = select(Todo)
    if due_before is not None:
        stmt = stmt.where(Todo.due_date.is_not(None), Todo.due_date < due_before)
    stmt = stmt.order_by(Todo.id).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def update_todo(db: Session, todo_id: int, todo: TodoUpdate) -> Todo | None:
    db_todo = get_todo(db, todo_id)
    if db_todo is None:
        return None

    updates = todo.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(db_todo, field, value)

    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int) -> bool:
    db_todo = get_todo(db, todo_id)
    if db_todo is None:
        return False

    db.delete(db_todo)
    db.commit()
    return True
