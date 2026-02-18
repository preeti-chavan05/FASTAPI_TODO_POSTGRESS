from fastapi import FastAPI
from app.models import User, Task
from app.crud import create_task, get_tasks
from app.database import engine, Base
from app.routers import auth, tasks


Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Todo with PostgreSQL")

app.include_router(auth.router)
app.include_router(tasks.router)