from typing import Optional
from fastapi import Body, FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from datetime import date
from starlette import status

app = FastAPI()


class Book:
    ID: int
    title: str
    author: str
    description: str
    rating: int
    publish_date: int

    def __init__(self, ID, title, author, description, rating, publish_date):
        self.ID = ID
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date


class BookRequest(BaseModel):
    ID: Optional[int] = Field(description = 'The ID is not needed on create a new book', default = None)
    title: str = Field(min_length = 5)
    author: str = Field(min_length = 3)
    description: str = Field(min_length = 1, max_length = 100)
    rating: int = Field(ge = 0, le = 10)
    publish_date: int = Field(le = date.today().year)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Marouan Boumchahate",
                "description": "A new Description of a book",
                "rating": 5,
                "publish_date": 2024
            }
        }
    }

BOOKS = [
    Book(1, "Clean Code", "Robert C. Martin", "A handbook of agile software craftsmanship, focusing on writing clean, maintainable code.", 9, 1996),
    Book(2, "The Pragmatic Programmer", "Andrew Hunt, David Thomas", "A guide for developers to create flexible, dynamic, and easy-to-maintain code.", 8, 1722),
    Book(3, "Introduction to Algorithms", "Thomas H. Cormen", "Comprehensive guide to algorithms used in computer science and data structures.", 7, 2003),
    Book(4, "Design Patterns", "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides", "A reference for common design patterns in software engineering.", 8, 2020),
    Book(5, "The Mythical Man-Month", "Frederick P. Brooks Jr.", "Essays on software engineering, focusing on project management and scaling.", 7, 1999),
    Book(6, "Refactoring", "Martin Fowler", "Improving the design of existing code to enhance its readability and maintainability.", 9, 2024)
]


@app.get('/books', status_code=status.HTTP_200_OK)
async def readAllBooks():
    return BOOKS


@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt = 0)):
    for book in BOOKS:
        if book.ID == book_id:
            return book
        
    raise HTTPException(status_code=404, detail="Item is not found")


@app.get('/books/published_on/{book_publishedDate}', status_code=status.HTTP_200_OK)
async def read_book_by_publishDate(book_publishedDate: int = Path(ge=1500, lt=2025)):
    books_to_return = []
    for book in BOOKS:
        if book.publish_date == book_publishedDate:
            books_to_return.append(book)

    return books_to_return


@app.get('/books/', status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(le=10, ge=0)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return


# model_dump() same as dict()
@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(findBookID(new_book))

def findBookID(book: Book):
    book.ID = 1 if len(BOOKS) == 0 else BOOKS[-1].ID + 1 
    return book


@app.put('/books/update_book', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    isUpdated = False
    for i in range(len(BOOKS)):
        if BOOKS[i].ID == book.ID:
            isUpdated = True
            BOOKS[i] = book

    if not isUpdated: raise HTTPException(status_code=404, detail='Book Not Found')


@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt = 0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].ID == book_id:
            BOOKS.pop(i)
            return
        
    raise HTTPException(status_code=404, detail='Book Not Found')