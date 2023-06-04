# from fastapi import FastAPI, Response, status, 
# from fastapi.params import Body
# from pydantic import BaseModel
# from typing import Optional
# from random import randint
import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi_sqlalchemy import DBSessionMiddleware, db

from models import Author
from models import Author as ModelAuthor
from models import Book
from models import Book as ModelBook
from models import Post
from models import Post as ModelPost
from models import Product
from models import Product as ModelProduct
from schema import Author as SchemaAuthor
from schema import Book as SchemaBook
from schema import Post as SchemaPost
from schema import Product as SchemaProduct

load_dotenv(".env")
app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

@app.get("/")
async def root():
    logging.debug('Accessing root endpoint.')
    return {"message": "Hello World"}

@app.get("/books/")
def get_books():
    logging.debug('Starting to get books.')
    try:
        books = db.session.query(Book).all()
        logging.debug('Successfully got books.')
        return books
    except Exception as e:
        logging.error('An error occurred while getting books: %s', str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/posts/")
def get_posts():
    logging.debug('Starting to get posts.')
    try:
        posts = db.session.query(Post).all()
        logging.debug('Successfully got posts.')
        return posts
    except Exception as e:
        logging.error('An error occurred while getting posts: %s', str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/query/")
    

@app.get("/products/")
def get_products():
    logging.debug('Starting to get products.')
    try:
        products = db.session.query(Product).all()
        logging.debug('Successfully got products.')
        return products
    except Exception as e:
        logging.error('An error occurred while getting products: %s', str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/add-book/", response_model=SchemaBook)
def add_book(book: SchemaBook):
    db_book = ModelBook(title=book.title, rating=book.rating, author_id=book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book


@app.post("/add-author/", response_model=SchemaAuthor)
def add_author(author: SchemaAuthor):
    db_author = ModelAuthor(name=author.name, age=author.age)
    db.session.add(db_author)
    db.session.commit()
    return db_author

@app.post("/add-posts/", response_model=SchemaPost, status_code=status.HTTP_201_CREATED)
def add_post(post: SchemaPost):
    logging.debug('Starting to add a post: %s', post.dict())
    try:
        db_post = ModelPost(**post.dict())
        db.session.add(db_post)
        db.session.commit()
        logging.debug('Successfully added a post.')
        return db_post
    except Exception as e:
        logging.error('An error occurred while adding a post: %s', str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/add-product/", response_model=SchemaProduct, status_code=status.HTTP_201_CREATED)
def add_product(product: SchemaProduct):
    logging.debug('Starting to add a product: %s', product.dict())
    try:
        db_product = ModelProduct(**product.dict())
        db.session.add(db_product)
        db.session.commit()
        logging.debug('Successfully added a product.')
        return db_product
    except Exception as e:
        logging.error('An error occurred while adding a product: %s', str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Need To Create DELETE AND PUT




# @app.post("/user/", response_model=SchemaUser)
# def create_user(user: SchemaUser):
#     db_user = ModelUser(
#         first_name=user.first_name, last_name=user.last_name, age=user.age
#     )
#     db.session.add(db_user)
#     db.session.commit()
#     return db_user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
