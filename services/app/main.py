__author__ = 'archanda'
__date__ = '31-Mar-2021'
__copyright__ = "Copyright 2021"
__credits__ = ["archanda"]
__license__ = "All rights reserved"
__maintainer__ = "archanda"
__email__ = "2020mt93064@wilp.bits-pilani.ac.in"
__status__ = "dev"

from fastapi import FastAPI, Body
from fastapi import Response, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# local
from api.routes import urls
from services import book_details_module

from core.database import (
    add_book,
    get_book,
    delete_book,
    retrieve_books
)
from models.schemas.book import (
    BookSchema
)


app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# saving the book data to mongodb..
@app.post(urls.save_book_url)
async def save_book(book_data: BookSchema = Body(...)):
    new_entry = await add_book(book_data)
    return {"new book": new_entry}

# Getting book by id from mongodb...
@app.get(urls.get_book_by_id_url)
async def get_book_by_id(book_id: str):
    #print(book_id)
    book_found = await get_book(book_id)
    if book_found:
        return {"book": book_found}

# Deleting book data
@app.delete(urls.delete_book_by_id_url)
async def delete_book_by_id(book_id: str):
    book_deleted = await delete_book(book_id)
    if book_deleted:
        return {"id": book_id, "message": "Deletion successful"}

# Getting list of books from mongodb...
@app.get(urls.get_all_books_url)
async def get_book_list():
    books = await retrieve_books()
    return {"books": books, "totalBooks": len(books)}


# Fetching book by ISBN...
@app.get(urls.get_book_details_by_isbn)
async def get_books_by_isbn(isbn):
    logger.info("Fetching Book details for the ISBN {}".format(isbn))
    item = book_details_module.get_books_by_filter('isbn', isbn)
    if item:
        return item
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"isbn": isbn,
            "message": "book not found for given ISBN"}

# Fetching book by Author name...
@app.get(urls.get_book_details_by_author)
async def get_books_by_author(author_name):
    logger.info("Fetching Book details for the Author Name: \"{}\"".format(author_name))
    item = book_details_module.get_books_by_filter('inauthor', author_name)
    if item:
        return item
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"author": author_name,
            "message": "Either invalid author name or book not found for given Author Name"}

# Fetching book by Author name...
@app.get(urls.get_book_details_by_genre)
async def get_books_by_genre(genre):
    logger.info("Fetching Book details for the genre: \"{}\"".format(genre))
    item = book_details_module.get_books_by_filter('subject', genre)
    if item:
        return item
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"genre": genre,
            "message": "Either invalid genre or book not found for given genre"}
