"""Scrape the first 20 books from books.toscrape.com."""

from __future__ import annotations

import re
from typing import Any

import requests
from bs4 import BeautifulSoup


URL = "https://books.toscrape.com/"
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def parse_price(price_text: str) -> float:
    match = re.search(r"\d+\.\d+", price_text)
    if not match:
        raise ValueError(f"Could not parse price from: {price_text!r}")
    return float(match.group())


def parse_rating(tag_classes: list[str]) -> int:
    for class_name in tag_classes:
        if class_name in RATING_MAP:
            return RATING_MAP[class_name]
    raise ValueError(f"Could not parse rating from classes: {tag_classes!r}")


def scrape_books() -> list[dict[str, Any]]:
    try:
        response = requests.get(URL, timeout=15)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to fetch {URL}: {exc}") from exc

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.select("article.product_pod")

    if not books:
        raise RuntimeError(
            "Expected book cards were not found on the page. "
            "The scraper expects article.product_pod elements on the main page."
        )

    records: list[dict[str, Any]] = []

    for book in books[:20]:
        title_tag = book.select_one("h3 a")
        price_tag = book.select_one("p.price_color")
        stock_tag = book.select_one("p.instock.availability")
        rating_tag = book.select_one("p.star-rating")

        if not title_tag or not price_tag or not stock_tag or not rating_tag:
            raise RuntimeError(
                "The page structure does not match the scraper's expectations. "
                "One of title, price, stock, or rating fields is missing."
            )

        title = title_tag.get("title") or title_tag.get_text(strip=True)
        price = parse_price(price_tag.get_text(strip=True))
        in_stock = "In stock" in stock_tag.get_text(" ", strip=True)
        rating = parse_rating(rating_tag.get("class", []))

        records.append(
            {
                "title": title,
                "price": price,
                "in_stock": in_stock,
                "rating": rating,
            }
        )

    return records


if __name__ == "__main__":
    books = scrape_books()
    print(f"Scraped {len(books)} books")
    for book in books:
        print(book)