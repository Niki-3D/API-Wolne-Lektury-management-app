"""
This module contains functions that interact with the Wolne Lektury API and the book service API.
"""

from typing import Dict, List
import requests
from thefuzz.fuzz import ratio
from config import HOME, TARGET


class BookManager:
    """
    This class manages book-related operations with the Wolne Lektury API and the local book service API.
    """

    @staticmethod
    def fetch_books_from_api(url: str) -> List[Dict[str, str]]:
        """
        Fetch books from the Wolne Lektury API and return them as a list of dictionaries.
        """
        return requests.get(url).json()

    @staticmethod
    def find_book_by_title(title: str) -> Dict[str, str]:
        """
        Get a single book from the API that matches the title.
        """
        books = BookManager.fetch_books_from_api(f"{TARGET}/books")
        highest_similarity = 0
        selected_book = None

        for book in books:
            similarity = ratio(title, book['title'])

            if title == book['title'] or highest_similarity < similarity > 30:
                highest_similarity = similarity
                selected_book = book.copy()

        return selected_book

    @staticmethod
    def submit_book_to_api(book: Dict[str, str]) -> None:
        """
        This function will post a book to the API.
        """
        response = requests.post(url=f"{HOME}/book", json=book)

        if response.status_code != 201:
            print(f"Failed to add book:\n {response.text}")

    @staticmethod
    def add_books_to_db(books: List[Dict[str, str]]) -> None:
        """
        Add a list of books to the database.
        """
        for book in books:
            BookManager.submit_book_to_api(book)

    @staticmethod
    def reformat_books(books: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Reformat books for database insertion.
        """
        return [{"title": book["title"], "author": book["author"], "genre": book["genre"]} for book in books]

    @staticmethod
    def fetch_filtered_books(authors: List[str], genres: str) -> List[Dict[str, str]]:
        """
        Get filtered books from the API.
        """
        books = []

        if authors:
            for author in authors:
                author_books = BookManager.fetch_books_from_api(f"{TARGET}{genres}{author}/books")
                books.extend(BookManager.reformat_books(author_books))
        else:
            books = BookManager.fetch_books_from_api(f"{TARGET}{genres}/books")
            books = BookManager.reformat_books(books)

        return books
