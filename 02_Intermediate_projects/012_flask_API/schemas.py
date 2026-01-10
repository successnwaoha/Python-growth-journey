from pydantic import BaseModel, constr, Field
from typing import Optional


class UserCreateSchema(BaseModel):
    username: constr(min_length=3, max_length=80)
    email: constr(min_length=5, max_length=120)
    password: constr(min_length=6)


class UserLoginSchema(BaseModel):
    username: constr(min_length=3, max_length=80)
    password: constr(min_length=6)


class TodoCreateSchema(BaseModel):
    title: constr(min_length=1, max_length=200)
    description: Optional[str] = None
    completed: bool = False


class TodoUpdateSchema(BaseModel):
    title: Optional[constr(min_length=1, max_length=200)] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
