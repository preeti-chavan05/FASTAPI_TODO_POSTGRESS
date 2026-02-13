from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_db, get_current_user


router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.create_task(db, task, user.id)

@router.get("", response_model=list[schemas.TaskOut])
def get_tasks(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.get_tasks(db, user.id)

@router.get("/filter", response_model=list[schemas.TaskOut])
def filter_tasks(priority: str = None, status: str = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.filter_tasks(db, user.id, priority, status)

@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    updated = crud.update_task(db, task_id, task, user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    deleted = crud.delete_task(db, task_id, user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
