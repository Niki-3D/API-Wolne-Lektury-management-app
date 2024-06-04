from flask import Flask, request, jsonify
from model import BookModel, FiltersModel
from book_logic import BookLogic
from src.db.db import DatabaseConnection
from src.client.book_management import BookManager

app = Flask(__name__)
db = DatabaseConnection()
book_logic = BookLogic(db)

@app.route("/book", methods=["POST"])
def add_book():
    data = request.get_json()
    book = BookModel(**data)
    status_msg, res = book_logic.add_book(book)
    return jsonify(res), 201

@app.route("/book/<string:title>", methods=["GET"])
def get_book(title):
    status_msg, res = book_logic.get_book(title)
    if status_msg == "Found":
        return jsonify(res), 200
    elif status_msg == "Not Found":
        return jsonify(res), 404

@app.route('/books', methods=["GET"])
def get_books():
    authors = request.args.getlist('author')
    genres = request.args.getlist('genre')
    status_msg, res = book_logic.get_books(authors, genres)
    if status_msg == "OK":
        return jsonify(res), 200
    elif status_msg == "Not Found":
        return jsonify(res), 404

@app.route("/fetch_book", methods=["GET"])
def fetch_book():
    title = request.args.get('title')
    book = BookManager.find_book_by_title(title)
    if book:
        BookManager.submit_book_to_api(book)
        return jsonify({"msg": "Book added successfully"}), 201
    else:
        return jsonify({"msg": "Book not found"}), 404

@app.route("/fetch_books", methods=["GET"])
def fetch_books():
    genres = request.args.get('genres', "")
    authors = request.args.getlist('authors')
    books = BookManager.fetch_filtered_books(authors, genres)
    if books:
        BookManager.add_books_to_db(books)
        return jsonify({"msg": "Books added successfully"}), 201
    else:
        return jsonify({"msg": "Books not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
