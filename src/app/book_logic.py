from typing import List, Tuple
from model import BookModel
from src.db.db import Author, Kind
from src.db.db import DatabaseHandler as Database

class BookLogic:
    def __init__(self, db: Database):
        self.db = db

    def create_author(self, author_name: str) -> Author:
        author = self.db.is_author(author_name)
        if not author:
            author = Author(name=author_name)
            self.db.add_author(author)
        return author

    def create_genre(self, genre_name: str) -> Kind:
        genre = self.db.is_kind(genre_name)
        if not genre:
            genre = Kind(name=genre_name)
            self.db.add_kind(genre)
        return genre

    def add_book(self, book: BookModel) -> Tuple[str, dict]:
        author = self.create_author(book.author)
        genre = self.create_genre(book.genre)
        self.db.add_book(book.title, author.id, genre.id)
        return "Created", {"msg": "Book created successfully"}

    def get_book(self, title: str) -> Tuple[str, dict]:
        book = self.db.get_book(title)
        if book:
            return "Found", book.get_dict()
        else:
            return "Not Found", {"msg": "Book not found"}

    def get_books(self, authors: List[str], genres: List[str]) -> Tuple[str, dict]:
        books = self.db.get_books(authors, genres)
        if books:
            return "OK", books
        else:
            return "Not Found", {"msg": "No books found"}
