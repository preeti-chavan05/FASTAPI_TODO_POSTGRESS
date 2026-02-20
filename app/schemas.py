from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Annotated

class RegisterModel(BaseModel):
    email: EmailStr
    password: Annotated[str, 
                        "min_length=6", "max_length=72"
                       ]
    role: str = "User"

class TaskBase(BaseModel):
    name: str
    description: str
    start_date: date
    end_date: date
    priority: str
    status: str
    user_id: int | None = None 

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int

    class Config:
        from_attributes = True 