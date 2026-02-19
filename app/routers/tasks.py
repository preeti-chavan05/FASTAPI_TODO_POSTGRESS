from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.models import User, Task 
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

@router.delete("/{task_id}")
def delete_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if current_user.role != "Admin" and task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this task")
    
    db.delete(task)
    db.commit()
    return {"msg": "Task deleted successfully"}

@router.post("/unsubscribe")
def unsubscribe(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.is_subscribed = False
    db.commit()
    db.refresh(current_user)   

    return {
        "msg": "You have unsubscribed from email notifications.",
        "is_subscribed": current_user.is_subscribed
    }
