"""API client that exports book data and creates a plot."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests


API_URL = "http://127.0.0.1:8000/books"
BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "exported_books.csv"
PLOT_FILE = BASE_DIR / "price_vs_rating.png"


def fetch_books() -> list[dict]:
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to fetch books from API: {exc}") from exc


def main() -> None:
    books = fetch_books()

    if not books:
        raise RuntimeError("No books were returned by the API.")

    dataframe = pd.DataFrame(books)
    print(dataframe)

    dataframe.to_csv(CSV_FILE, index=False)

    plt.figure(figsize=(8, 5))
    plt.scatter(dataframe["price"], dataframe["rating"])
    plt.title("Book Price vs Rating")
    plt.xlabel("Price")
    plt.ylabel("Rating")
    plt.tight_layout()
    plt.savefig(PLOT_FILE)
    plt.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(exc)
        sys.exit(1)