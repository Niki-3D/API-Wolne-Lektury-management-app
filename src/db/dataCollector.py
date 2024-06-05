import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.schema import Author, Genre, Base


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

        connection_string = "your_connection_string_here"  
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        self.__initialized = True


def fetch_data_from_api(url: str):
    response = requests.get(url).json()
    return response


def collect_authors():
    authors_data = fetch_data_from_api("https://wolnelektury.pl/api/authors/")
    return [author["name"] for author in authors_data]


def collect_genres():
    genres_data = fetch_data_from_api("https://wolnelektury.pl/api/kinds/")
    return [genre["name"] for genre in genres_data]


def insert_authors(authors, session):
    for author_name in authors:
        existing_author = session.query(Author).filter_by(name=author_name).first()
        if existing_author is None:
            author = Author(name=author_name)
            session.add(author)
    session.commit()


def insert_genres(genres, session):
    for genre_name in genres:
        existing_genre = session.query(Genre).filter_by(name=genre_name).first()
        if existing_genre is None:
            genre = Genre(name=genre_name)
            session.add(genre)
    session.commit()


def display_all_authors(session):
    authors = session.query(Author).all()
    for author in authors:
        print(author.name)


def display_all_genres(session):
    genres = session.query(Genre).all()
    for genre in genres:
        print(genre.name)


def main():
    connection = DatabaseConnection()

    authors = collect_authors()
    insert_authors(authors, connection.session)
    display_all_authors(connection.session)

    genres = collect_genres()
    insert_genres(genres, connection.session)
    display_all_genres(connection.session)


if __name__ == "__main__":
    main()
