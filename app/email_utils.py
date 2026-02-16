import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException

SECRET_KEY = "your_secret_key"  
ALGORITHM = "HS256"
EMAIL_TOKEN_EXPIRE_MINUTES = 30

def create_verification_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=EMAIL_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def send_verification_email(email: str, token: str):
    
    verification_link = f"http://localhost:8000/auth/verify?token={token}"
    print(f"Send this verification link to {email}: {verification_link}")
