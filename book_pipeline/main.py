"""FastAPI app for the book pipeline database."""

from __future__ import annotations

import traceback
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from book_pipeline.database import BookDatabase


app = FastAPI(title="Book Pipeline API")
DB_PATH = Path(__file__).resolve().parent / "books.db"
db = BookDatabase(str(DB_PATH))


class BookCreate(BaseModel):
    title: str
    price: float
    in_stock: bool
    rating: int


class BookUpdate(BaseModel):
    title: str
    price: float
    in_stock: bool
    rating: int


class BookResponse(BaseModel):
    id: int
    title: str
    price: float
    in_stock: bool
    rating: int


def validate_book_data(price: float, rating: int) -> None:
    if price < 0:
        raise HTTPException(status_code=400, detail="Price cannot be negative")
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")


def handle_unexpected_error(exc: Exception) -> HTTPException:
    print(f"Unexpected database error: {exc}")
    traceback.print_exc()
    return HTTPException(status_code=500, detail="Internal server error")


@app.on_event("startup")
def startup() -> None:
    db.create_table()


@app.get("/books", response_model=list[BookResponse])
def get_books() -> list[dict]:
    try:
        return db.get_books()
    except Exception as exc:
        raise handle_unexpected_error(exc)


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int) -> dict:
    try:
        book = db.get_book(book_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return book
    except HTTPException:
        raise
    except Exception as exc:
        raise handle_unexpected_error(exc)


@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate) -> dict:
    validate_book_data(book.price, book.rating)

    try:
        book_id = db.add_book(book.title, book.price, book.in_stock, book.rating)
        created_book = db.get_book(book_id)
        if created_book is None:
            raise HTTPException(status_code=500, detail="Internal server error")
        return created_book
    except HTTPException:
        raise
    except Exception as exc:
        raise handle_unexpected_error(exc)


@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookUpdate) -> dict:
    validate_book_data(book.price, book.rating)

    try:
        updated = db.update_book(book_id, book.title, book.price, book.in_stock, book.rating)
        if not updated:
            raise HTTPException(status_code=404, detail="Book not found")

        updated_book = db.get_book(book_id)
        if updated_book is None:
            raise HTTPException(status_code=500, detail="Internal server error")
        return updated_book
    except HTTPException:
        raise
    except Exception as exc:
        raise handle_unexpected_error(exc)


@app.delete("/books/{book_id}")
def delete_book(book_id: int) -> dict:
    try:
        deleted = db.delete_book(book_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"detail": "Book deleted successfully"}
    except HTTPException:
        raise
    except Exception as exc:
        raise handle_unexpected_error(exc)