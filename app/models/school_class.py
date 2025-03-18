from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from enum import Enum


class SchoolClass(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    grade: int = Field(ge=0, le=12)
    letter: str = Field(max_length=1)
