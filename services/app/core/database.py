import motor.motor_asyncio
from bson.objectid import ObjectId

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# DB details
MONGO_DETAILS = "mongodb://mongodb:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.user_preferences
books_collection = database.get_collection("books_collection")

# helpers

def format_book(book) -> dict:
    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "isbnID": book["isbnID"],
        "notes": book["notes"],
        "tags": book["tags"]
    }

async def add_book(book_data: dict):
    book = await books_collection.insert_one(
        {"_id": ObjectId(), "title": book_data.title, "isbnID": book_data.isbnID, "notes": book_data.notes, "tags": book_data.tags}
    )
    new_book = await books_collection.find_one({"_id": book.inserted_id})
    return format_book(new_book)

async def get_book(book_id: str) -> dict:
    curr_book = await books_collection.find_one({"_id": ObjectId(book_id)})
    return format_book(curr_book)

async def delete_book(book_id: str):
    book_deleted = await books_collection.find_one({"_id": ObjectId(book_id)})
    if book_deleted:
        await books_collection.delete_one({"_id": ObjectId(book_id)})
    return True

async def retrieve_books():
    books = []
    async for curr_book in books_collection.find():
        books.append(format_book(curr_book))
    return books