from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {
        "ID": 1,
        "title": "A Brief History of Time",
        "author": "Stephen Hawking",
        "category": "Physics"
    },
    {
        "ID": 2,
        "title": "The Selfish Gene",
        "author": "Richard Dawkins",
        "category": "Biology"
    },
    {
        "ID": 3,
        "title": "The Origin of Species",
        "author": "Charles Darwin",
        "category": "Evolutionary Biology"
    },
    {
        "ID": 4,
        "title": "The Double Helix",
        "author": "Stephen Hawking",
        "category": "Genetics"
    },
    {
        "ID": 5,
        "title": "The Elegant Universe",
        "author": "Brian Greene",
        "category": "Theoretical Physics"
    },
    {
        "ID": 6,
        "title": "World is small",
        "author": "Stephen Hawking",
        "category": "Physics"
    },
]


@app.get("/books")
def read_all_books():
    return BOOKS



# @app.get("/books/mybook")
# async def read_all_books():
#     return {'book_title' : 'My Favorite Book!'}



@app.get("/books/{book_title}")
def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book



@app.get('/books/')
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return



@app.get('/books/{book_author}/')
async def read_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if  book.get('author').casefold() == book_author.casefold()\
        and\
            book.get('category').casefold() == category.casefold():
            
            books_to_return.append(book)

    return books_to_return


@app.get('/books/{author}/books')
async def all_author_books(author: str):
    books = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books.append(book)

    return books




@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)



@app.put('/books/update_book')
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('ID') == updated_book.get('ID'):
            BOOKS[i] = updated_book
            break


@app.delete('/books/delete_book/{book_ID}')
async def delete_book(book_ID: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('ID') == book_ID:
            BOOKS.pop(i)
            break

        