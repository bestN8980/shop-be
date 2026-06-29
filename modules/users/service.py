from modules.users.repository import get_user_by_email, create_user, update_user, delete_user
from sqlalchemy.orm import Session
from modules.users.schema import UserResponse, Token, ChangePassword, UserUpdate
from fastapi import HTTPException
from core.security import hash_password, verify_password, create_access_token
from modules.users.model import User, UserRole

def register_user(db:Session, user)->UserResponse:
    existing_user = get_user_by_email(db, user.email)

    if existing_user is not None:
        raise HTTPException(
    status_code=400,
    detail="Email already exists"
)
    hashed_password = hash_password(user.password)
    new_user = create_user(db=db, user=user, hashed_password=hashed_password )

    return UserResponse.model_validate(new_user)

def login_user(db: Session, user)->Token:
    found_user = get_user_by_email(db, user.email)
    if found_user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    

    if not verify_password(user.password, found_user.hashed_password):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    payload = {
         "sub": str(found_user.id),
         "email": found_user.email,
        "role": found_user.role,
    }
    token = create_access_token(payload)
    return Token(access_token=token, token_type="bearer")

def change_password(password: ChangePassword, db: Session, current_user ):
    if not verify_password(password.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    updated_password = hash_password(password.new_password)
    current_user.hashed_password = updated_password

    db.commit()
    db.refresh(current_user)

    return {
        "message":"Password changed successfully"
    }

def update_profile(db: Session, current_user, user: UserUpdate ):
    if current_user.email != user.email:
        existing_user = get_user_by_email(db, user.email)

        if existing_user is not None:
            raise HTTPException(status_code=400, detail="Invalid email")
    updated_user = update_user(db, current_user.id, user)
    return updated_user

def delete_user_service(db, user_id: int):
    user = delete_user(db, user_id)

    if not user:
        return {"message": "User not found"}

    return {"message": "User deleted successfully"}

def create_admin_service(db: Session):
    email = "admin@gmail.com"
    password = "admin123"

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Admin already exists")

    admin = User(
        username="admin",
        email=email,
        hashed_password=hash_password(password),
        full_name="System Admin",
        phone="0000000000",
        role=UserRole.ADMIN
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return admin