from os import getenv
from typing import List, Optional

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from src.db.schema import Author, Genre, Book, Base


class DatabaseConnection:
    """
    Singleton class to create a connection to the database.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        
        connection_string = "your_connection_string_here"  # Replace with your actual connection string
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        self.__initialized = True


class DatabaseHandler:
    """
    Class for interacting with the database.
    """

    def __init__(self, connection: DatabaseConnection):
        self.connection = connection

    def rollback_transaction(self) -> None:
        """
        Roll back the current session.
        """
        self.connection.session.rollback()

    def find_author_by_name(self, author_name: str) -> Optional[Author]:
        """
        Find an author by name. If exists, return the author.
        """
        return self.connection.session.query(Author).filter_by(name=author_name).first()

    def find_genre_by_name(self, genre_name: str) -> Optional[Genre]:
        """
        Find a genre by name. If exists, return the genre.
        """
        return self.connection.session.query(Genre).filter_by(name=genre_name).first()

    def add_new_author(self, author: Author) -> None:
        """
        Add a new author to the database.
        """
        try:
            self.connection.session.add(author)
            self.connection.session.commit()
        except Exception as e:
            self.connection.session.rollback()
            print(e)

    def add_new_genre(self, genre: Genre) -> None:
        """
        Add a new genre to the database.
        """
        try:
            self.connection.session.add(genre)
            self.connection.session.commit()
        except Exception as e:
            self.connection.session.rollback()
            print(e)

    def add_new_book(self, title: str, author_id: int, genre_id: int) -> None:
        """
        Add a new book to the database.
        """
        try:
            new_book = Book(title=title, author_id=author_id, genre_id=genre_id)
            self.connection.session.add(new_book)
            self.connection.session.commit()
        except Exception as e:
            self.connection.session.rollback()
            print(e)

    def get_book_by_title(self, title: str) -> Optional[Book]:
        """
        Retrieve a book by its title.
        """
        return self.connection.session.query(Book).filter_by(title=title).first()

    def get_books_by_author_and_genre(self, author_names: List[str], genre_names: List[str]) -> List[dict]:
        """
        Retrieve books based on provided author and genre names.
        """
        query = self.connection.session.query(Book)
        if author_names:
            query = query.join(Author).filter(Author.name.in_(author_names))
        if genre_names:
            query = query.join(Genre).filter(Genre.name.in_(genre_names))

        return query.all()


def provide_connection() -> DatabaseConnection:
    """
    Provide a connection to the database.
    """
    return DatabaseConnection()


def provide_database_handler(connection: DatabaseConnection = provide_connection()) -> DatabaseHandler:
    """
    Provide a database handler object.
    """
    return DatabaseHandler(connection)
