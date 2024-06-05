from typing import Dict, List
import requests
from config import HOME, TARGET

class BookManager:
    @staticmethod
    def fetch_books_from_api(url: str) -> List[Dict[str, str]]:
        return requests.get(url).json()

    @staticmethod
    def find_book_by_title(title: str) -> Dict[str, str]:
        books = BookManager.fetch_books_from_api(f"{TARGET}/books")
        for book in books:
            if title.lower() == book['title'].lower():
                return book.copy()
        return None

    @staticmethod
    def submit_book_to_api(book: Dict[str, str]) -> None:
        response = requests.post(url=f"{HOME}/book", json=book)
        if response.status_code != 201:
            print(f"Failed to add book:\n {response.text}")

    @staticmethod
    def add_books_to_db(books: List[Dict[str, str]]) -> None:
        for book in books:
            BookManager.submit_book_to_api(book)

    @staticmethod
    def reformat_books(books: List[Dict[str, str]]) -> List[Dict[str, str]]:
        return [{"title": book["title"], "author": book["author"], "genre": book["genre"]} for book in books]

    @staticmethod
    def fetch_filtered_books(authors: List[str], genres: str) -> List[Dict[str, str]]:
        books = []
        if authors:
            for author in authors:
                author_books = BookManager.fetch_books_from_api(f"{TARGET}{genres}{author}/books")
                books.extend(BookManager.reformat_books(author_books))
        else:
            books = BookManager.fetch_books_from_api(f"{TARGET}{genres}/books")
            books = BookManager.reformat_books(books)
        return books
