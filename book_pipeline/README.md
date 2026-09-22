# End-to-End Book Data Pipeline & Analytics System

Simple Python capstone project that:
- scrapes the first 20 books from `books.toscrape.com`
- stores the data in SQLite
- exposes the data through a FastAPI REST API
- fetches the API data into Pandas
- exports a CSV file
- creates a scatter plot of price vs rating

## Project Structure

- `scraper.py` - scrapes the books from the website
- `database.py` - SQLite CRUD layer
- `main.py` - FastAPI app
- `client.py` - API client, CSV export, and plot generation
- `books.db` - SQLite database file created by the API
- `exported_books.csv` - exported book data
- `price_vs_rating.png` - scatter plot output
- `requirements.txt` - pinned dependencies
- `README.md` - project guide

## Requirements

- Python 3.10.11
- Windows
- Existing virtual environment in the project folder

## Install Dependencies

Activate the existing virtual environment:

```powershell
venv\Scripts\activate
```

Install packages:

```powershell
pip install -r book_pipeline\requirements.txt
```

## Run the Project

### 1. Scrape the books

```powershell
python book_pipeline\scraper.py
```

Expected result:
- prints `Scraped 20 books`
- prints 20 book dictionaries

### 2. Start the API

```powershell
uvicorn book_pipeline.main:app --reload
```

Expected result:
- FastAPI starts on `http://127.0.0.1:8000`

### 3. Seed the database

Run the scraper and POST the 20 books into the API using the client or a small script.

The API stores records in `book_pipeline\books.db`.

### 4. Run the client

```powershell
python book_pipeline\client.py
```

Expected result:
- prints a Pandas DataFrame
- creates `book_pipeline\exported_books.csv`
- creates `book_pipeline\price_vs_rating.png`

## End-to-End Test

1. Run `scraper.py` and confirm 20 records are returned.
2. Start the FastAPI server from `main.py`.
3. Seed the database with the scraped book records.
4. Open `GET /books` in the browser or with `requests` and confirm books are returned.
5. Run `client.py`.
6. Confirm the CSV and plot are created in `book_pipeline/`.

## API Endpoints

- `GET /books` - return all books
- `GET /books/{id}` - return one book
- `POST /books` - create a book
- `PUT /books/{id}` - update a book
- `DELETE /books/{id}` - delete a book

## Notes

- The scraper only uses the main page of `books.toscrape.com`.
- No SQLAlchemy is used.
- The database layer uses the built-in `sqlite3` module.
- All important fields stay consistent across scraper, database, API, and client.