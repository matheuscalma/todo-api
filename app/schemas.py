"""Pydantic schemas for request/response validation."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    completed: bool = False
    due_date: date | None = None


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    """All fields optional to support partial updates via PATCH."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    completed: bool | None = None
    due_date: date | None = None


class TodoRead(TodoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
