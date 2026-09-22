"""SQLite database layer for storing books."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class BookDatabase:
    def __init__(self, db_path: str = "books.db") -> None:
        self.db_path = Path(db_path)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _row_to_book(self, row: sqlite3.Row) -> dict[str, Any]:
        return {
            "id": row["id"],
            "title": row["title"],
            "price": row["price"],
            "in_stock": bool(row["in_stock"]),
            "rating": row["rating"],
        }

    def create_table(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    price REAL NOT NULL,
                    in_stock BOOLEAN NOT NULL,
                    rating INTEGER NOT NULL
                )
                """
            )
            connection.commit()

    def add_book(self, title: str, price: float, in_stock: bool, rating: int) -> int:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO books (title, price, in_stock, rating)
                VALUES (?, ?, ?, ?)
                """,
                (title, price, in_stock, rating),
            )
            connection.commit()
            return int(cursor.lastrowid)

    def get_books(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            cursor = connection.execute(
                "SELECT id, title, price, in_stock, rating FROM books ORDER BY id"
            )
            rows = cursor.fetchall()
            return [self._row_to_book(row) for row in rows]

    def get_book(self, book_id: int) -> dict[str, Any] | None:
        with self._connect() as connection:
            cursor = connection.execute(
                "SELECT id, title, price, in_stock, rating FROM books WHERE id = ?",
                (book_id,),
            )
            row = cursor.fetchone()
            return self._row_to_book(row) if row else None

    def update_book(
        self,
        book_id: int,
        title: str,
        price: float,
        in_stock: bool,
        rating: int,
    ) -> bool:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE books
                SET title = ?, price = ?, in_stock = ?, rating = ?
                WHERE id = ?
                """,
                (title, price, in_stock, rating, book_id),
            )
            connection.commit()
            return cursor.rowcount > 0

    def delete_book(self, book_id: int) -> bool:
        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM books WHERE id = ?",
                (book_id,),
            )
            connection.commit()
            return cursor.rowcount > 0