import logging

from fastapi import APIRouter, FastAPI, HTTPException, Response, status
from fastapi_sqlalchemy import db

from .. import models, schema

router = APIRouter()

@router.get("/posts/", response_model=list[schema.Post])
def get_posts():
    logging.debug('Starting to get posts.')
    try:
        posts = db.session.query(models.Post).all()
        logging.debug('Successfully got posts.')
        return posts
    except Exception as e:
        logging.error('An error occurred while getting posts: %s', str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/posts/{id}")
def get_products(id: int):
    logging.debug('Starting to get products.')
    try:
        posts = db.session.query(models.Post).filter(models.Post.id == id).first()
        logging.debug('Successfully got products.')
        return posts
    except Exception as e:
        logging.error('An error occurred while getting products: %s', str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("/posts/", response_model=schema.Post, status_code=status.HTTP_201_CREATED)
def add_post(post: schema.Post):
    logging.debug('Starting to add a post: %s', post.dict())
    try:
        db_post = models.Post(**post.dict())
        db.session.add(db_post)
        db.session.commit()
        logging.debug('Successfully added a post.')
        return db_post
    except Exception as e:
        logging.error('An error occurred while adding a post: %s', str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = db.session.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    post.delete()
    db.session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}", response_model=schema.Post)
def update_post(id: int, post: schema.Post):
    db_post = db.session.query(models.Post).filter(models.Post.id == id).first()

    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    db_post.title = post.title
    db_post.content = post.content
    db_post.published = post.published

    db.session.commit()
    return db_post