from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import NewUser, UsersResponse, updateUser
from app.utils import hash_password, decode_password

router = APIRouter(prefix="/user", tags=["user"])


@router.get("", status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):

    all_users = db.query(models.Users).all()
    return {"users": all_users}


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: NewUser, db: Session = Depends(get_db)):

    # new_user = models.Users(
    # 	first_name=user.first_name,
    # 	last_name=user.last_name,
    # 	email=user.email,
    # 	password=user.password,
    # )

    #hash password
    hash = hash_password(user.password)
    user.password = hash
    
    # better way to do this is to use **user.dict()
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=UsersResponse, status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )

    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id)

    if user.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )

    user.delete(synchronize_session=False)
    db.commit()
    return {"detail": f"User with id {id} deleted"}


@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_user(id: int, new_user: updateUser, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id)

    if user.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )

    user.update(new_user.dict(), synchronize_session=False)
    db.commit()
    return {"detail": f"User with id {id} updated"}