from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import hash_password, verify_password


def create_user(db: Session, user: schemas.RegisterModel):
    hashed_pwd = hash_password(user.password)
    db_user = models.User(
        email=user.email,
        password=hashed_pwd,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def authenticate_user(db: Session, email: str, password: str):
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return None 

    if not verify_password(password, user.password):
        return None  

    return user  


def create_task(db: Session, task: schemas.TaskCreate, current_user):
    if current_user.role == "Admin" and task.user_id:
        db_task = models.Task(
            **task.model_dump(exclude={"user_id"}),
            user_id=task.user_id,
            assigned_by_admin=True
        )
    else:
        db_task = models.Task(
            **task.model_dump(exclude={"user_id"}),
            user_id=current_user.id
        )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, current_user):
    if current_user.role == "Admin":
        return db.query(models.Task).all()
    return db.query(models.Task).filter(models.Task.user_id == current_user.id).all()


def update_task(db: Session, task_id: int, new_task, current_user):
    if current_user.role == "Admin":
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    else:
        db_task = db.query(models.Task).filter(
            models.Task.id == task_id,
            models.Task.user_id == current_user.id
        ).first()

    if db_task:
        for key, value in new_task.model_dump(exclude={"user_id"}).items():
            setattr(db_task, key, value)

        db.commit()
        db.refresh(db_task)

    return db_task


def delete_task(db: Session, task_id: int, current_user):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        return None

    if current_user.role == "Admin":
        db.delete(task)
        db.commit()
        return task

    if task.assigned_by_admin:
        return None

    if task.user_id == current_user.id:
        db.delete(task)
        db.commit()
        return task

    return None
