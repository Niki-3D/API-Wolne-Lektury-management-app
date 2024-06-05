from flask import Flask, request, jsonify
from model import BookModel
from book_logic import BookLogic
from src.db.db import DatabaseConnection
from src.client.book_management import BookManager

class BookApp:
    def __init__(self, book_logic: BookLogic, db_connection: DatabaseConnection, book_manager: BookManager):
        self.app = Flask(__name__)
        self.book_logic = book_logic
        self.db_connection = db_connection
        self.book_manager = book_manager
        self.register_routes()

    def register_routes(self):
        @self.app.route("/book", methods=["POST"])
        def add_book():
            data = request.get_json()
            book = BookModel(**data)
            status_msg, res = self.book_logic.add_book(book)
            return jsonify(res), 201

        @self.app.route("/book/<string:title>", methods=["GET"])
        def get_book(title):
            status_msg, res = self.book_logic.get_book(title)
            if status_msg == "Found":
                return jsonify(res), 200
            elif status_msg == "Not Found":
                return jsonify(res), 404

        @self.app.route('/books', methods=["GET"])
        def get_books():
            authors = request.args.getlist('author')
            genres = request.args.getlist('genre')
            status_msg, res = self.book_logic.get_books(authors, genres)
            if status_msg == "OK":
                return jsonify(res), 200
            elif status_msg == "Not Found":
                return jsonify(res), 404

        @self.app.route("/fetch_book", methods=["GET"])
        def fetch_book():
            title = request.args.get('title')
            book = self.book_manager.find_book_by_title(title)
            if book:
                self.book_manager.submit_book_to_api(book)
                return jsonify({"msg": "Book added successfully"}), 201
            else:
                return jsonify({"msg": "Book not found"}), 404

        @self.app.route("/fetch_books", methods=["GET"])
        def fetch_books():
            genres = request.args.get('genres', "")
            authors = request.args.getlist('authors')
            books = self.book_manager.fetch_filtered_books(authors, genres)
            if books:
                self.book_manager.add_books_to_db(books)
                return jsonify({"msg": "Books added successfully"}), 201
            else:
                return jsonify({"msg": "Books not found"}), 404

    def run(self):
        self.app.run(debug=True)

if __name__ == "__main__":
    db_connection = DatabaseConnection()
    book_logic = BookLogic(db_connection)
    book_manager = BookManager()
    book_app = BookApp(book_logic, db_connection, book_manager)
    book_app.run()
