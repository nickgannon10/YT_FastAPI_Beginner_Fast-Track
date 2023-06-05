import logging

from fastapi import APIRouter, FastAPI, HTTPException, Response, status
from fastapi_sqlalchemy import DBSessionMiddleware, db

from .. import models, schema, utils

router = APIRouter()

@router.get("/users/{id}", response_model=schema.UserOut)
def get_users(id: int):
    logging.debug('Starting to get users.')
    try:
        users = db.session.query(models.User).filter(models.User.id == id).first()
        logging.debug('Successfully got users.')
        return users
    except Exception as e:
        logging.error('An error occurred while getting users: %s', str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/users/", response_model=schema.UserOut,  status_code=status.HTTP_201_CREATED) # response_model=SchemaUser
def create_user(user: schema.User):
    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    db_user = models.User(**user.dict())
    db.session.add(db_user)
    db.session.commit()
    db.session.refresh(db_user)
    return db_user