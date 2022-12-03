from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, utils, oAuth2

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login_user(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = (
        db.query(models.Users).filter(models.Users.email == credentials.username).first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {credentials.email} not found",
        )

    if not utils.decode_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentilas"
        )

    token_body =  {"email": user.email, "id": user.id,  "token_type": "bearer"}
    token = oAuth2.create_access_token(data=token_body)
    return {"access_token": token}