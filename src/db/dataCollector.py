import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.schema import Author, Genre, Base


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


def fetch_data_from_api(url: str):
    """
    Fetch data from the given API URL and return the JSON response.
    """
    response = requests.get(url).json()
    return response


def collect_authors():
    """
    Collect author names from the API.
    """
    authors_data = fetch_data_from_api("https://wolnelektury.pl/api/authors/")
    return [author["name"] for author in authors_data]


def collect_genres():
    """
    Collect genre names from the API.
    """
    genres_data = fetch_data_from_api("https://wolnelektury.pl/api/kinds/")
    return [genre["name"] for genre in genres_data]


def insert_authors(authors, session):
    """
    Insert authors into the database.
    """
    for author_name in authors:
        existing_author = session.query(Author).filter_by(name=author_name).first()
        if existing_author is None:
            author = Author(name=author_name)
            session.add(author)
    session.commit()


def insert_genres(genres, session):
    """
    Insert genres into the database.
    """
    for genre_name in genres:
        existing_genre = session.query(Genre).filter_by(name=genre_name).first()
        if existing_genre is None:
            genre = Genre(name=genre_name)
            session.add(genre)
    session.commit()


def display_all_authors(session):
    """
    Display all authors from the database.
    """
    authors = session.query(Author).all()
    for author in authors:
        print(author.name)


def display_all_genres(session):
    """
    Display all genres from the database.
    """
    genres = session.query(Genre).all()
    for genre in genres:
        print(genre.name)


def main():
    """
    Main function to execute the script.
    """
    connection = DatabaseConnection()

    # Fetch and insert authors
    authors = collect_authors()
    insert_authors(authors, connection.session)
    display_all_authors(connection.session)

    # Fetch and insert genres
    genres = collect_genres()
    insert_genres(genres, connection.session)
    display_all_genres(connection.session)


if __name__ == "__main__":
    main()
