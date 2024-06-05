from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.schema import Author, Genre, Book, Base


class DatabaseConnection:
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
    def __init__(self, connection: DatabaseConnection):
        self.connection = connection

    def rollback_transaction(self) -> None:
        self.connection.session.rollback()

    def find_author_by_name(self, author_name: str) -> Optional[Author]:
        return self.connection.session.query(Author).filter_by(name=author_name).first()

    def find_genre_by_name(self, genre_name: str) -> Optional[Genre]:
        return self.connection.session.query(Genre).filter_by(name=genre_name).first()

    def add_new_author(self, author: Author) -> None:
        try:
            self.connection.session.add(author)
            self.connection.session.commit()
        except Exception as e:
            self.connection.session.rollback()
            print(e)

    def add_new_genre(self, genre: Genre) -> None:
        try:
            self.connection.session.add(genre)
            self.connection.session.commit()
        except Exception as e:
            self.connection.session.rollback()
            print(e)

    def add_new_book(self, title: str, author_id: int, genre_id: int) -> None:
        try:
            new_book = Book(title=title, author_id=author_id, genre_id=genre_id)
            self.connection.session.add(new_book)
            self.connection.session.commit()
        except Exception as e:
            self.connection.session.rollback()
            print(e)

    def get_book_by_title(self, title: str) -> Optional[Book]:
        return self.connection.session.query(Book).filter_by(title=title).first()

    def get_books_by_author_and_genre(self, author_names: List[str], genre_names: List[str]) -> List[dict]:
        query = self.connection.session.query(Book)
        if author_names:
            query = query.join(Author).filter(Author.name.in_(author_names))
        if genre_names:
            query = query.join(Genre).filter(Genre.name.in_(genre_names))

        return query.all()


def provide_connection() -> DatabaseConnection:
    return DatabaseConnection()


def provide_database_handler(connection: DatabaseConnection = provide_connection()) -> DatabaseHandler:
    return DatabaseHandler(connection)
