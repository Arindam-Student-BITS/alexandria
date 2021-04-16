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
        "tags": book["tags"],
        "publisher": book["publisher"] # Added key 'publisher' - Arindam
    }

async def add_book(book_data: dict):
    book = await books_collection.insert_one(
        {"_id": ObjectId(), "title": book_data.title, "isbnID": book_data.isbnID, "notes": book_data.notes, "tags": book_data.tags,"publisher": book_data.publisher}
    # Added key 'publisher' - Arindam
    )
    new_book = await books_collection.find_one({"_id": book.inserted_id})
    return format_book(new_book)

# Added by ArchanaTBits
async def update_book_by_id(book_id:str, book_data: dict) -> dict:
    curr_book = await books_collection.find_one({"_id": ObjectId(book_id)})
    if curr_book is not None:
        logger.info("Book Exists")
        update_criteria = { "_id": ObjectId(book_id) }
        newvalues = {"$set": { "title": book_data.title if (book_data.title is not None and len(book_data.title) > 0) else curr_book.title ,
                             "isbnID": book_data.isbnID if (book_data.isbnID is not None  and len(book_data.isbnID) > 0) else curr_book.isbnID,
                             "notes": book_data.notes if (book_data.notes is not None  and len(book_data.notes) > 0) else curr_book.notes,
                              "tags": book_data.tags  if (book_data.tags is not None  and len(book_data.tags) > 0) else curr_book.tags} }
    book_updated = await books_collection.update_one(update_criteria, newvalues)
    return book_updated.acknowledged# returns true: if updated successfully



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
