"""FastAPI To-Do API with SQLite storage."""

from datetime import date

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="To-Do API", version="1.0.0")


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


@app.post(
    "/todos",
    response_model=schemas.TodoRead,
    status_code=status.HTTP_201_CREATED,
    tags=["todos"],
)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)


@app.get("/todos", response_model=list[schemas.TodoRead], tags=["todos"])
def list_todos(
    skip: int = 0,
    limit: int = 100,
    due_before: date | None = None,
    priority: schemas.Priority | None = None,
    db: Session = Depends(get_db),
):
    """List todos, optionally filtered by ``due_before`` and/or ``priority``.

    Todos without a due_date are excluded when ``due_before`` is set.
    """
    return crud.get_todos(db, skip=skip, limit=limit, due_before=due_before, priority=priority)


@app.get("/todos/{todo_id}", response_model=schemas.TodoRead, tags=["todos"])
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return db_todo


@app.patch("/todos/{todo_id}", response_model=schemas.TodoRead, tags=["todos"])
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id, todo)
    if db_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return db_todo


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["todos"])
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_todo(db, todo_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
