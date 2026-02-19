from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.dependencies import get_db
from app.auth import create_access_token
from app.email_utils import create_verification_token, send_verification_email  
from app.email_utils import verify_verification_token 
from app.models import User
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(user: schemas.RegisterModel, db: Session = Depends(get_db)):
    
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    
    db_user = crud.create_user(db, user)

    
    token = create_verification_token(db_user.email)
    send_verification_email(db_user.email, token)

    return {
        "msg": "User created. Please verify your email.",
        "verification_token": token 
    }


@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = crud.authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
  
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/verify")
def verify_email(token: str, db: Session = Depends(get_db)):
    
    email = verify_verification_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    db.commit()

    return {"message": "Email verified successfully!"}

