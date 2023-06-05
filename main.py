import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, status
from fastapi_sqlalchemy import DBSessionMiddleware, db

from models import Post
from models import Post as ModelPost
from models import User
from models import User as ModelUser
from schema import Post as SchemaPost
from schema import UserCreate as SchemaUser
from schema import UserOut as SchemaUserOut
from utils import hash

from .routers import posts, user

load_dotenv(".env")
app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

app.include_router(posts.router)
app.include_router(user.router)

@app.get("/")
async def root():
    logging.debug('Accessing root endpoint.')
    return {"message": "Hello World"}

# @app.get("/posts/", response_model=list[SchemaPost])
# def get_posts():
#     logging.debug('Starting to get posts.')
#     try:
#         posts = db.session.query(Post).all()
#         logging.debug('Successfully got posts.')
#         return posts
#     except Exception as e:
#         logging.error('An error occurred while getting posts: %s', str(e))
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
# @app.get("/posts/{id}")
# def get_products(id: int):
#     logging.debug('Starting to get products.')
#     try:
#         posts = db.session.query(Post).filter(Post.id == id).first()
#         logging.debug('Successfully got products.')
#         return posts
#     except Exception as e:
#         logging.error('An error occurred while getting products: %s', str(e))
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
# @app.get("/users/{id}", response_model=SchemaUserOut)
# def get_users(id: int):
#     logging.debug('Starting to get users.')
#     try:
#         users = db.session.query(User).filter(User.id == id).first()
#         logging.debug('Successfully got users.')
#         return users
#     except Exception as e:
#         logging.error('An error occurred while getting users: %s', str(e))
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# @app.post("/posts/", response_model=SchemaPost, status_code=status.HTTP_201_CREATED)
# def add_post(post: SchemaPost):
#     logging.debug('Starting to add a post: %s', post.dict())
#     try:
#         db_post = ModelPost(**post.dict())
#         db.session.add(db_post)
#         db.session.commit()
#         logging.debug('Successfully added a post.')
#         return db_post
#     except Exception as e:
#         logging.error('An error occurred while adding a post: %s', str(e))
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     post = db.session.query(Post).filter(Post.id == id)

#     if post.first() is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
#     post.delete()
#     db.session.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# # Need To Create PUT
# @app.put("/posts/{id}", response_model=SchemaPost)
# def update_post(id: int, post: SchemaPost):
#     db_post = db.session.query(Post).filter(Post.id == id).first()

#     if db_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

#     db_post.title = post.title
#     db_post.content = post.content
#     db_post.published = post.published

#     db.session.commit()
#     return db_post


# ## Ther is no product PUT and DELETE yet

# @app.post("/users/", response_model=SchemaUserOut,  status_code=status.HTTP_201_CREATED) # response_model=SchemaUser
# def create_user(user: SchemaUser):
#     # hash the password
#     hashed_password = hash(user.password)
#     user.password = hashed_password
#     db_user = ModelUser(**user.dict())
#     db.session.add(db_user)
#     db.session.commit()
#     db.session.refresh(db_user)
#     return db_user

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
